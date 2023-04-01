import os, sys, re
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QCalendarWidget, QLabel, QPushButton, QButtonGroup

UI_FILE_PATH = "UI Files" #Directory in which the UI files are stored


LOGIN_INDEX = 0
REGISTER_INDEX = 1

"""Displays warning messagebox to the scren
    @param title title of window
    @param string_message string to display
"""
def infomation_messagebox(title, string_message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(string_message)
    msg.setWindowTitle(title)    
    msg.exec_()
    
"""Displays warning messagebox to the scren
    @param string_message string to display
"""
def warning_messagebox(string_message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(string_message)
    msg.setWindowTitle("Error")    
    msg.exec_()
    
class RegisterPage(QDialog):
    def __init__(self):
        super(RegisterPage, self).__init__()
        loadUi(f"{UI_FILE_PATH}\RegisterPage.ui", self)
        self.setWindowTitle("Register")
        self.setFixedSize(self.size())
        self.Login_Button.clicked.connect(self.go_to_login)
        
    def go_to_login(self):
        widget.setCurrentIndex(LOGIN_INDEX)
        
    def attempt_register(self):
        print("Register Attempted")
        
class LoginPage(QDialog):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi(f"{UI_FILE_PATH}\LoginPage.ui", self)
        self.setWindowTitle("Login")
        self.setFixedSize(self.size())
        
        self.Login_Button.clicked.connect(self.attempt_login)
        self.Register_Button.clicked.connect(self.go_to_register)
    
    def go_to_register(self):
        widget.setCurrentIndex(REGISTER_INDEX)
        
    def attempt_login(self):
        print("Login Attempted")


        
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()
widget.addWidget(LoginPage())
widget.addWidget(RegisterPage())


widget.setFixedSize(1280, 720)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass