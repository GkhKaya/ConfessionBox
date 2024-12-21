from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QApplication,QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from Views.Widget.ButtonWithText import ButtonWithText
from Views.LoginView.LoginViewModel import LoginViewModel

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
        username_label = QLabel("Username")
        password_label = QLabel("Password")

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Şifreyi gizle

        # Buton oluşturma ve stil atama
        login_button = ButtonWithText(
            text="Login",
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
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
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
        username = self.username_input.text()
        password = self.password_input.text()

        # LoginViewModel sınıfından bir örnek oluştur
        viewModel = LoginViewModel()

        # Metodu örnek üzerinden çağır
        result = viewModel.login_user(username=username, password=password)

        if result["success"]:
            QMessageBox.information(self, "Success", result["message"])

            # HomeView'i aç
            from Views.HomeView.HomeView import HomeView
            self.home_view = HomeView()
            self.home_view.show()

            # LoginView'i kapat
            self.close()
        else:
            QMessageBox.warning(self, "Error", result["error"])