import os, sys, re
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QCalendarWidget, QLabel, QPushButton, QButtonGroup

UI_FILE_PATH = "UI Files" #Directory in which the UI files are stored

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

        
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)

widget = QtWidgets.QStackedWidget()
widget.addWidget(RegisterPage())

widget.setFixedSize(1280, 720)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass