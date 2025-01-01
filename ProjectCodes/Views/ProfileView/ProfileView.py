from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QScrollArea, QLabel, QHBoxLayout, QDialog,QApplication
from PyQt5.QtCore import Qt
from Views.ProfileView.ProfileViewModel import ProfileViewModel
from utils.widgets.ConfessionCard import LoremIpsumCard
from Views.UpdateConfessionDialog.UpdateConfessionDialog import UpdateConfessionDialog
from Views.AuthView.AuthView import AuthView  # AuthView sınıfını ekliyoruz

class ProfileView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model = ProfileViewModel()
        self.parent = parent  # Parent view bilgisi
        self.setup_ui()
        self.load_user_data()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Profile Section
        profile_widget = QWidget()
        profile_layout = QVBoxLayout(profile_widget)
        
        # Profile Form
        form_layout = QFormLayout()
        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.full_name_edit = QLineEdit()

        form_layout.addRow("Username:", self.username_edit)
        form_layout.addRow("Email:", self.email_edit)
        form_layout.addRow("Full Name:", self.full_name_edit)

        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)

        profile_layout.addLayout(form_layout)
        profile_layout.addWidget(save_button)

        # Logout Button
        logout_button = QPushButton("Çıkış Yap")
        logout_button.setStyleSheet("background-color: orange; color: white; font-weight: bold;")
        logout_button.clicked.connect(self.logout_user)
        profile_layout.addWidget(logout_button)

        main_layout.addWidget(profile_widget)

        # Confessions Title
        title_layout = QHBoxLayout()
        title_label = QLabel("İtiraflarım")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: orange; background: transparent;")
        title_layout.addWidget(title_label)
        main_layout.addLayout(title_layout)

        # Scroll Area for Confessions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        # Content Widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(15)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_widget.setStyleSheet("background: transparent;")

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

        # Set minimum size and styles
        self.setMinimumSize(600, 400)
        self.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #DDD;
                border-radius: 4px;
                background-color: transparent; 
                color: white; 
            }
            QPushButton {
                background-color: black;
                color: white;
                padding: 8px 16px;
                border: 1px solid orange;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: orange;
            }
            QLabel {
                color: white; 
            }
            QScrollBar:vertical {
                background: #2C2C2C;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #404040;
                border-radius: 5px;
            }
        """)

    def load_user_data(self):
        user_data = self.view_model.get_user_data()
        if user_data["success"]:
            self.username_edit.setText(user_data["data"]["username"])
            self.email_edit.setText(user_data["data"]["email"] or "")
            self.full_name_edit.setText(user_data["data"]["full_name"] or "")
            self.init_confessions()

    def clear_cards(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def init_confessions(self):
        self.clear_cards()
        result = self.view_model.get_user_confessions()
        
        if result["success"]:
            confessions = result["confessions"]
            if not confessions:
                no_confessions_label = QLabel("Henüz itiraf bulunmamaktadır")
                no_confessions_label.setStyleSheet("color: #888; padding: 20px; font-size: 16px;")
                self.content_layout.addWidget(no_confessions_label)
            else:
                for confession in confessions:
                    card = LoremIpsumCard(
                        text=confession.get('text', 'No text available'),
                        date=str(confession.get('created_at', 'No date provided')),
                        author=None
                    )
                    card.mousePressEvent = lambda e, c=confession: self.show_update_dialog(c)
                    card.setCursor(Qt.PointingHandCursor)
                    self.content_layout.addWidget(card)
                
                self.content_layout.addStretch()
        else:
            error_label = QLabel("İtiraflar yüklenirken bir hata oluştu")
            error_label.setStyleSheet("color: red; padding: 20px; font-size: 16px;")
            self.content_layout.addWidget(error_label)

    def show_update_dialog(self, confession):
        dialog = UpdateConfessionDialog(
            confession_id=str(confession['_id']),
            confession_text=confession.get('text', ''),
            is_open=confession.get('is_open', False)
        )
        if dialog.exec_() == QDialog.Accepted:
            self.load_user_data()

    def save_changes(self):
        update_data = {
            "username": self.username_edit.text(),
            "email": self.email_edit.text(),
            "full_name": self.full_name_edit.text()
        }
        
        result = self.view_model.update_user_data(update_data)
        
        if result["success"]:
            QMessageBox.information(self, "Başarılı", "Profil başarıyla güncellendi!")
            self.load_user_data()
        else:
            QMessageBox.critical(self, "Hata", result["error"])

    def logout_user(self):
        result = self.view_model.logout_user()
        if result["success"]:
            QApplication.quit()  # Uygulamayı kapat
        else:
            QMessageBox.critical(self, "Hata", result["error"])