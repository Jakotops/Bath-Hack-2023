import os, sys, re, Backend
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QCalendarWidget, QLabel, QPushButton, QButtonGroup

UI_FILE_PATH = "UI Files" #Directory in which the UI files are stored

session_id = None

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
    BULLET_POINT = "• "
    
    
    def __init__(self):
        super(RegisterPage, self).__init__()
        loadUi(f"{UI_FILE_PATH}\RegisterPage.ui", self)
        self.setWindowTitle("Register")
        
        self.Name.setPlaceholderText("Name")
        self.Username.setPlaceholderText("Username")
        self.Password.setPlaceholderText("Password")
        self.RepeatPassword.setPlaceholderText("Confirm Password")
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.RepeatPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.Login_Button.clicked.connect(self.go_to_login)
        self.Register_Button.clicked.connect(self.attempt_register)
       
    def string_all_alpha(self, string):
        return string.isalpha()
    
    def check_user_input(self, message, field, input):
        if len(input) < 3:
            message += f"{RegisterPage.BULLET_POINT}{field} is too short, must be at least 3 characters long\n"
        elif len(input) > 15:
            message += f"{RegisterPage.BULLET_POINT}{field} is too long, must be at most 15 characters long\n"
        elif not self.string_all_alpha(input):
            message += f"{RegisterPage.BULLET_POINT}{field} must only contain letters\n"
        return message
      
    def go_to_login(self):
        widget.setCurrentIndex(LOGIN_INDEX)
        
    def attempt_register(self):
        name = self.Name.text()
        username = self.Username.text()
        password = self.Password.text()
        repeat_password = self.RepeatPassword.text()
        
        message = ""
        
        message = self.check_user_input(message, "Name", name)
        message = self.check_user_input(message, "Username", username)
        message = self.check_passwords_match(message, password, repeat_password)

        if message != "":
            return warning_messagebox(message)
        else: 
            result = Backend.User().add_user(name, username, password)
            print(f"Successful register: {result}")
            infomation_messagebox("Success", "Account created successfully")
            widget.setCurrentIndex(LOGIN_INDEX)
            self.clear_fields()  
      
    def clear_fields(self):
        self.Name.clear()
        self.Username.clear()
        self.Password.clear()
        self.RepeatPassword.clear()  
          
    def check_passwords_match(self, message, password, repeat_password):
        if password != repeat_password:
            message += RegisterPage.BULLET_POINT +  "Passwords do not match\n"

        elif len(password) < 6:
            message += RegisterPage.BULLET_POINT +  "Password is too short, must be at least 6 characters long\n"
            
        return message

        
class LoginPage(QDialog):
    def __init__(self):
        super(LoginPage, self).__init__()
        loadUi(f"{UI_FILE_PATH}\LoginPage.ui", self)
        self.setWindowTitle("Login")
        
        self.Username.setPlaceholderText("Username")
        self.Password.setPlaceholderText("Password")
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.Login_Button.clicked.connect(self.attempt_login)
        self.Register_Button.clicked.connect(self.go_to_register)
    
    def go_to_register(self):
        widget.setCurrentIndex(REGISTER_INDEX)
        
    def attempt_login(self):
        username = self.Username.text()
        password = self.Password.text()
        
        print(f"Sucessful login: {Backend.User().validate_user(username, password)}")
        
        if Backend.User().validate_user(username, password): 
            self.Username.clear()
            self.Password.clear()
            
            global session_id
            session_id = Backend.User().set_session_id(password)
            
            print("Logged in successfully")
        else:
            warning_messagebox("Invalid username or password")
        

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