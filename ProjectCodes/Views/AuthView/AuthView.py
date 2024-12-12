from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel,QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Views.LoginView.LoginView import LoginView  
from Views.RegisterView.RegisterView import RegisterView  
from Views.Widget.ButtonWithText import ButtonWithText

class AuthView(QWidget):
    def __init__(self):
        super().__init__()
        self.button_style = """
            QPushButton {
                background-color: #FF8C00;
                color: black;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
        """
        self.init_ui()

    def init_ui(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        self.setStyleSheet("background-color: #0B192C;")  

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Başlık
        title_label = QLabel("İtiraf Kutusu")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #F8F8F8;")  
        title_label.setAlignment(Qt.AlignCenter)

        # Butonlar
        login_button = ButtonWithText(text="Giriş Yap", style=self.button_style, function=self.show_login_view)
        register_button = ButtonWithText(text="Kayıt Ol", style=self.button_style, function=self.show_register_view)

        button_layout = QVBoxLayout()
        button_layout.addWidget(login_button)
        button_layout.addWidget(register_button)
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignCenter)

        # Öğeleri ana düzene ekleme
        layout.addWidget(title_label)
        layout.addSpacing(50)  
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def show_login_view(self):
        self.login_view = LoginView()
        self.login_view.show()
        self.close()

    def show_register_view(self):
        self.register_view = RegisterView()
        self.register_view.show()
        self.close()