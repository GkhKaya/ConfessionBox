from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from Views.AuthView import AuthView  # AuthView'u doğrudan buraya import et
from Views.Widget.ButtonWithText import ButtonWithText

class RegisterView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Pencere başlığı ve boyutu
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(100, 100, 400, 300)
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
        title_label = QLabel("Kayıt Ol")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #F8F8F8;")  # Yazı rengi
        title_label.setAlignment(Qt.AlignCenter)

        # E-Posta, Şifre ve Cinsiyet alanları
        email_label = QLabel("E-Posta")
        password_label = QLabel("Şifre")
        gender_label = QLabel("Cinsiyet")

        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Şifreyi gizle

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Belirtmek istemiyorum", "Erkek", "Kadın", "Diğer"])

        # Düğme stil ayarları
        register_button = ButtonWithText(
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
            function=self.register_procress
        )

        # Öğeleri ana düzene ekleme
        layout.addLayout(back_button_layout)  # Geri butonu ekle
        layout.addWidget(title_label)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(gender_label)
        layout.addWidget(self.gender_combo)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def go_back(self):
        self.auth_view = AuthView()  # AuthView nesnesi oluşturuluyor ve gösteriliyor
        self.auth_view.show()
        self.close()
    def register_procress(self):
        
        pass

