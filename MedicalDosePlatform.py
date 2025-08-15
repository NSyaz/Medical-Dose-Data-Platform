import sys
import time
import mysql.connector as con

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

WINDOW_SIZE = 0

class ShowTable(QWidget):
    def __init__(self):
        super(ShowTable,self).__init__()
        loadUi("UI/ViewTable.ui",self)
        self.table.horizontalHeader()
        self.show()

class LoginApp(QWidget):
    def __init__(self):
        super(LoginApp,self).__init__()
        loadUi("UI/LogMasuk.ui",self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.b2.clicked.connect(self.login)
        self.b3.clicked.connect(self.show_reg)

        self.show()

    def login(self):
        username = self.tb1.text()
        password = self.tb2.text()
        db = con.connect(host="localhost", user = "root", password="", db="kkm_login")
        cursor = db.cursor()
        cursor.execute("select * from pengguna where pengguna_id='"+ username +"' and katalaluan = '"+ password +"'")
        result = cursor.fetchone()
        self.tb1.setText("")
        self.tb2.setText("")
        if result:
            QMessageBox.information(self, "Login Output","Log in successfully.")
        else:
            QMessageBox.information(self, "Login Output", "Invalid username or password")

    def show_reg(self):
        self.close()
        self.reg = RegApp()
        self.reg.show()

class RegApp(QWidget):
    def __init__(self):
        super(RegApp,self).__init__()
        loadUi("UI/Daftar.ui",self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #self.b4.clicked.connect(self.reg)
        self.registerButton.clicked.connect(self.mainApp)
        #self.stackedWidget.setCurrentWidget(self.CTadult_page0)

    def reg(self):
        username = self.tb3.text()
        password = self.tb4.text()
        password_confirmation = self.tb5.text()
        full_name = self.tb6.text()
        email = self.tb7.text()
        hospital = self.tb8.text()
        department = self.tb9.text()

        db = con.connect(host="localhost", user="root", password="", db="kkm_login")
        cursor = db.cursor()
        cursor.execute("select * from pengguna where pengguna_id='" + username + "' and katalaluan = '" + password + "'")
        result = cursor.fetchone()

        if result:
            QMessageBox.information(self, "Login Form", "The user already registered.")
        else:
            cursor.execute("insert into pengguna values('"+ username +"', '"+ password +"','"+ password_confirmation +"', '"+ full_name +"','"+ hospital +"','"+ department +"','"+ email +"')")
            db.commit()
            QMessageBox.information(self, "Login Form", "The user successfully registered.")

    def mainApp(self):
        self.close()
        self.mainWin = FormApp()
        self.mainWin.show()

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("UI/Splash screen.ui", self)
        self.centre()

        self.counter = 0
        self.n = 101

        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(40)

    def centre(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def progress(self):
        self.pBar.setValue(self.counter)
        self.label.setStyleSheet("color:rgb(255,255,255);background-color:rgba(0,0,0,0);font: 57 13pt 'Futura'")
        self.pBar.setTextVisible(False)

        if self.counter == int(self.n * 0.4):
            self.label.setText('In progress....')
        elif self.counter == int(self.n * 0.8):
            self.label.setText('Starting....')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            self.login = LoginApp()
            self.login.show()

        self.counter += 1

class FormApp(QMainWindow):
    def __init__(self,parent = None):
        super(FormApp,self).__init__(parent)
        loadUi("UI/Form_Window.ui",self)
        self.centre()

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.closeButton.setIcon(QtGui.QIcon(u"icons/cil-x.png"))
        self.maximizeButton.setIcon(QtGui.QIcon(u"icons/cil-window-maximize.png"))
        self.minimizeButton.setIcon(QtGui.QIcon(u"icons/cil-window-minimize.png"))

        #self.stackedWidgets.setCurrentWidget(self.CTadult_page0)
        self.stackedWidgets.setCurrentIndex(0)

        self.closeButton.clicked.connect(self.closeWindow)
        self.maximizeButton.clicked.connect(self.maximizedWindow)
        self.minimizeButton.clicked.connect(self.minimizedWindow)
        self.CTButton.clicked.connect(self.slideLeftMenu)

        self.CT_AdultButton.clicked.connect(self.CT_page0)
        self.CT_PaediatricButton.clicked.connect(self.CT_page2)
        self.xRayButton.clicked.connect(self.Xray_page4)
        self.MammButton.clicked.connect(self.Mammo_page6)

        self.viewButton.clicked.connect(self.slideLeftMenuBottom)
        self.show_CTadult_button.clicked.connect(self.showCTpage1)
        self.show_CTpaed_button.clicked.connect(self.showCTpage3)
        self.show_Mammo_button.clicked.connect(self.showMammopage5)
        self.show_XRay_button.clicked.connect(self.showXRaypage7)

        self.editButton_page0.clicked.connect(lambda :self.stackedWidgets.setCurrentIndex(1))
        self.editButton_page2.clicked.connect(lambda :self.stackedWidgets.setCurrentIndex(3))
        self.editButton_page4.clicked.connect(lambda :self.stackedWidgets.setCurrentIndex(5))
        self.editButton_page6.clicked.connect(lambda :self.stackedWidgets.setCurrentIndex(7))

        self.oldPos = self.pos()

    def centre(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeWindow(self):
        QApplication.quit()

    def maximizedWindow(self):
        global WINDOW_SIZE
        window_status = WINDOW_SIZE

        if window_status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()
            self.maximizeButton.setIcon(QtGui.QIcon(u"icons/cil-window-restore.png"))

        else:
            WINDOW_SIZE = 0
            self.showNormal()
            self.maximizeButton.setIcon(QtGui.QIcon(u"icons/cil-window-maximize.png"))

    def minimizedWindow(self):
        self.showMinimized()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def slideLeftMenu(self):
        width = self.left_menu_top_btns.width()

        if width == 130:
            newWidth = 235
        else:
            newWidth = 130

        self.animation = QPropertyAnimation(self.left_menu_top_btns, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def CT_page0(self):
        self.stackedWidgets.setCurrentIndex(0)

        width = self.left_menu_top_btns.width()
        if width == 235:
            newWidth = 130
        else:
            newWidth = 235

        self.animation = QPropertyAnimation(self.left_menu_top_btns, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def CT_page2(self):
        self.stackedWidgets.setCurrentIndex(2)

        width = self.left_menu_top_btns.width()
        if width == 235:
            newWidth = 130
        else:
            newWidth = 235

        self.animation = QPropertyAnimation(self.left_menu_top_btns, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def Xray_page4(self):
        self.stackedWidgets.setCurrentIndex(4)

        width = self.left_menu_top_btns.width()
        if width == 235:
            newWidth = 130
        else:
            newWidth = 130

        self.animation = QPropertyAnimation(self.left_menu_top_btns, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def Mammo_page6(self):
        self.stackedWidgets.setCurrentWidget(self.Mamm_page6)
        #self.stackedWidgets.setCurrentIndex(3)

        width = self.left_menu_top_btns.width()
        if width == 235:
            newWidth = 130
        else:
            newWidth = 130

        self.animation = QPropertyAnimation(self.left_menu_top_btns, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def slideLeftMenuBottom(self):
        width = self.left_menu_bottom_btns.width()

        if width == 130:
            newWidth = 240
        else:
            newWidth = 130

        self.animation = QPropertyAnimation(self.left_menu_bottom_btns, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def showCTpage1(self):
        width = self.left_menu_bottom_btns.width()

        if width == 240:
            newWidth = 130
        else:
            newWidth = 240

        self.animation = QPropertyAnimation(self.left_menu_bottom_btns, b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

        self.tableCT1 = ShowTable()
        self.tableCT1.setWindowTitle("Computed Tomography-Adult")
        self.tableCT1.table.setColumnCount(5)
        self.tableCT1.table.setHorizontalHeaderLabels(['ID','Name','Age','Sex','Address'])

        self.tableCT1.show()


    def showCTpage3(self):
        width = self.left_menu_bottom_btns.width()

        if width == 240:
            newWidth = 130
        else:
            newWidth = 240

        self.animation = QPropertyAnimation(self.left_menu_bottom_btns,b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

        self.tableCT3 = ShowTable()
        self.tableCT3.setWindowTitle("Computed Tomography-Paediatric")
        self.tableCT3.table.setColumnCount(5)
        self.tableCT3.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Sex', 'Address'])
        self.tableCT3.show()

    def showMammopage5(self):
        width = self.left_menu_bottom_btns.width()

        if width == 240:
            newWidth = 130
        else:
            newWidth = 240

        self.animation = QPropertyAnimation(self.left_menu_bottom_btns,b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

        self.tableMammo = ShowTable()
        self.tableMammo.setWindowTitle("Mammography")
        self.tableMammo.table.setColumnCount(5)
        self.tableMammo.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Sex', 'Address'])
        self.tableMammo.show()

    def showXRaypage7(self):
        width = self.left_menu_bottom_btns.width()

        if width == 240:
            newWidth = 130
        else:
            newWidth = 240

        self.animation = QPropertyAnimation(self.left_menu_bottom_btns,b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

        self.tableXRay = ShowTable()
        self.tableXRay.setWindowTitle("X-Ray")
        self.tableXRay.table.setColumnCount(5)
        self.tableXRay.table.setHorizontalHeaderLabels(['ID', 'Name', 'Age', 'Sex', 'Address'])
        self.tableXRay.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SplashScreen()
    window.show()
    app.exec_()







