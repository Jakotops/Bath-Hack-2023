import folium
import os, sys, re, Backend
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QHeaderView,  QMessageBox, QCalendarWidget, QLabel, QPushButton, QButtonGroup, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


UI_FILE_PATH = "UI Files" #Directory in which the UI files are stored

session_id = None

LOGIN_INDEX = 0
REGISTER_INDEX = 1
MAIN_INDEX = 2
BUS_STOP_INDEX = 3 # temporarily set to 2 for testing purposes

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
        # load the UI file
        super(RegisterPage, self).__init__()
        loadUi(os.path.join(UI_FILE_PATH, "RegisterPage.ui"), self)
        self.setWindowTitle("Register")
        
        # set placeholder text
        self.Name.setPlaceholderText("Name")
        self.Username.setPlaceholderText("Username")
        self.Password.setPlaceholderText("Password")
        self.RepeatPassword.setPlaceholderText("Confirm Password")
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.RepeatPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        
        self.Login_Button.clicked.connect(self.go_to_login)
        self.Register_Button.clicked.connect(self.attempt_register)
    
    """Checks if the string is all alpha characters"""
    def string_all_alpha(self, string):
        return string.isalpha()
    
    """Checks if the user input is valid"""
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
    
    """Attempts to register the user"""
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
      
    """Checks if the passwords match and are at least 6 characters long"""
    def check_passwords_match(self, message, password, repeat_password):
        if password != repeat_password:
            message += RegisterPage.BULLET_POINT +  "Passwords do not match\n"

        elif len(password) < 6:
            message += RegisterPage.BULLET_POINT +  "Password is too short, must be at least 6 characters long\n"
            
        return message
    
    
    """Clears the fields"""
    def clear_fields(self):
        self.Name.clear()
        self.Username.clear()
        self.Password.clear()
        self.RepeatPassword.clear()  
    
class MainPage(QDialog):
    def __init__(self):
        # load the UI file
        super(MainPage, self).__init__()
        loadUi(os.path.join(UI_FILE_PATH, "MainPage.ui"), self)
        self.setWindowTitle("Main Page")
        
        self.logout_button.clicked.connect(self.logout)
        self.get_more_info.clicked.connect(self.go_to_bus_stop)
        self.U1.clicked.connect(self.show_U1_route)
        self.U2.clicked.connect(self.show_U2_route)
        
        self.webview = self.findChild(QWebEngineView, 'webview')
        
        self.webview.wheelEvent = lambda event: None
        
        m = folium.Map(location=[51.380001, -2.360000], zoom_start=13)
        html = m._repr_html_()
        html = f"""
        <html>
            <head>
                <style>
                    #map-container {{
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        height: 100%;
                    }}
                </style>
            </head>
            <body>
                <div id="map-container">{html}</div>
            </body>
        </html>
        """
        
        self.webview.setHtml(html)
     
        
    def show_U1_route(self):
        print("Showing U1 route")
        
    
    def show_U2_route(self):    
        print("Showing U2 route")
        
    def go_to_bus_stop(self):
        widget.setCurrentIndex(BUS_STOP_INDEX)
        
    def logout(self):
        global session_id
        session_id = None
        widget.setCurrentIndex(LOGIN_INDEX)
        
class LoginPage(QDialog):
    def __init__(self):
        # load the UI file
        super(LoginPage, self).__init__()
        loadUi(os.path.join(UI_FILE_PATH, "LoginPage.ui"), self)
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
            widget.setCurrentIndex(MAIN_INDEX)
        else:
            warning_messagebox("Invalid username or password")

     
class BusStopPage(QDialog):
    def __init__(self):
        # load the UI file
        super(BusStopPage, self).__init__()
        loadUi(os.path.join(UI_FILE_PATH, "BusStopPage.ui"), self)
        self.setWindowTitle("Bus Stop")
        
        # Set up table
        self.table = self.findChild(QTableWidget, "Table")
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Our Predicted Arrival Time", "Timetabled Arrival Time"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        font = QtGui.QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        self.Back_Button.clicked.connect(self.go_back)
        
    def go_back(self):
        widget.setCurrentIndex(MAIN_INDEX)

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)

# adds the widgets to the stack
widget = QtWidgets.QStackedWidget()
widget.addWidget(LoginPage())
widget.addWidget(RegisterPage())
widget.addWidget(MainPage())
widget.addWidget(BusStopPage())


widget.setFixedSize(1280, 720)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass