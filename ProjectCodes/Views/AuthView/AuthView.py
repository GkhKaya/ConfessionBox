from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class AuthView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("İtiraf Kutusu")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #0B192C;")  

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Başlık
        title_label = QLabel("İtiraf Kutusu")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #F8F8F8;")  
        title_label.setAlignment(Qt.AlignCenter)

    
        login_button = QPushButton("Giriş Yap")
        register_button = QPushButton("Kayıt Ol")

        
        button_style = """
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
        login_button.setStyleSheet(button_style)
        register_button.setStyleSheet(button_style)

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