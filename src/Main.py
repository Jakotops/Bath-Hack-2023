import Route
import folium
import jinja2
from jinja2 import Template
import os, sys, re, Backend
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QHeaderView,  QMessageBox, QCalendarWidget, QLabel, QPushButton, QButtonGroup, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from folium.map import Marker


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
    send_signal = QtCore.pyqtSignal(str)
    
    def __init__(self):
        # load the UI file
        super(MainPage, self).__init__()
        loadUi(os.path.join(UI_FILE_PATH, "MainPage.ui"), self)
        self.setWindowTitle("Main Page")
        
        self.Entry.setPlaceholderText("Enter Bus Stop coordinates")
        
        self.logout_button.clicked.connect(self.logout)
        self.get_more_info.clicked.connect(self.go_to_bus_stop)
        self.U1.clicked.connect(self.show_U1_route)
        self.U2.clicked.connect(self.show_U2_route)
        self.show_all.clicked.connect(self.show_all_routes)
        

        self.webview = self.findChild(QWebEngineView, 'webview')
        
        self.webview.wheelEvent = lambda event: None
        
        self.m = folium.Map(location=[51.380001, -2.360000], zoom_start=13)
        
        self.load_map()
        
        
     
    def load_map(self):
        html = self.m._repr_html_()
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
        
    def clear_map(self):
        self.m = None
        self.m = folium.Map(location=[51.380001, -2.360000], zoom_start=13)
        self.load_map()
        
    def genertate_route(self, route_id, line_color, stop_color):
        bus_stops = Route.findBusStopCoordinates(route_id)
        for bus_stop in bus_stops:
            print(list(bus_stop))
            marker = folium.Marker(list(bus_stop), popup= f'<p id="latlon">{bus_stop[0]}, {bus_stop[1]}</p>',  color=stop_color, icon=folium.Icon(icon="bus-simple", prefix='fa'))
            marker.add_to(self.m)
    
            
        bus_route = Route.findRouteCoordinatesList(route_id)
        print(bus_route)
        folium.PolyLine(bus_route, color=line_color, weight=2.5, opacity=1).add_to(self.m)
        self.load_map()
        
    def show_U1_route(self):
        self.clear_map()
        self.genertate_route(0, "#921c76", "purple")
        print("Showing U1 route")
        
    #Route 8 is the U2 route
    def show_U2_route(self):  
        self.clear_map()  
        self.genertate_route(8, "#05326e", "blue")
        print("Showing U2 route")
    
    def show_all_routes(self):
        self.clear_map()
        self.genertate_route(0, "#921c76", "purple")
        self.genertate_route(8, "#05326e", "blue")
        print("Showing all routes")
        
        
    def check_string_as_coordinates(self, input):
        pattern = "^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?)([,]\s*|\s+)[-+]?([1-9]?\d(\.\d+)?|1[0-7]\d(\.\d+)?|180(\.0+)?)$"
        if re.match(pattern, input):
            return True
        else:
            return False
                
    
    def go_to_bus_stop(self):
        coords = self.Entry.text().strip()
        if coords == "":
            warning_messagebox("Please enter a bus stop")
            return
        if not self.check_string_as_coordinates(coords):
            warning_messagebox("Please enter valid coordinates") 
            return
        print("Valid coordinates")
        widget.setCurrentIndex(BUS_STOP_INDEX) 
        self.send_signal.emit(coords)
        
        
        
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
    
    def recieve_data(self, coords):
        self.Title.setText(f"Here are our predictions for the stop at {coords}")
        
    def go_back(self):
        widget.setCurrentIndex(MAIN_INDEX)

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)

# adds the widgets to the stack
widget = QtWidgets.QStackedWidget()

main_page = MainPage()

bus_stop_page = BusStopPage()

widget.addWidget(LoginPage())
widget.addWidget(RegisterPage())
widget.addWidget(main_page)
widget.addWidget(bus_stop_page)

main_page.send_signal.connect(bus_stop_page.recieve_data)

widget.setFixedSize(1280, 720)
widget.show()

try:
    sys.exit(app.exec_())
except:
    pass