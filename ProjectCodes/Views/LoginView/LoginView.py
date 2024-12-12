from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from Views.Widget.ButtonWithText import ButtonWithText

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Pencere başlığı ve boyutu
        self.setWindowTitle("Giriş Yap")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        self.setStyleSheet("background-color: #0B192C;")  # Arka plan rengi

        # Ana dikey düzen
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Geri butonu
        back_button_layout = QHBoxLayout()
        back_button = QPushButton("")
        back_button.setFlat(True)  # Butonun arka planını kaldır
        back_button.setIcon(QIcon("assets/chevron.left.png"))  # İkon ekle
        back_button.setIconSize(QSize(16, 16))  # İkon boyutunu butonla eşleştir
        back_button.clicked.connect(self.go_back)
        back_button_layout.addWidget(back_button)
        back_button_layout.setAlignment(Qt.AlignLeft)

        # Başlık
        title_label = QLabel("Giriş Yap")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #F8F8F8;")  # Yazı rengi
        title_label.setAlignment(Qt.AlignCenter)

        # E-Posta ve Şifre alanları
        email_label = QLabel("E-Posta")
        password_label = QLabel("Şifre")

        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Şifreyi gizle

        # Buton oluşturma ve stil atama
        login_button = ButtonWithText(
            text="Giriş Yap",
            style="""
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
            """,
            function=self.login_procress
        )

        # Öğeleri ana düzene ekleme
        layout.addLayout(back_button_layout)  # Geri butonu ekle
        layout.addWidget(title_label)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def go_back(self):
        from Views.AuthView.AuthView import AuthView
        self.auth_view = AuthView()
        self.auth_view.show()
        self.close()

    def login_procress(self):
        
        pass