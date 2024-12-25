from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from Views.ProfileView.ProfileViewModel import ProfileViewModel

class ProfileView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model = ProfileViewModel()
        self.setup_ui()
        self.load_user_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.username_edit = QLineEdit()
        self.email_edit = QLineEdit()
        self.full_name_edit = QLineEdit()

        form_layout.addRow("Username:", self.username_edit)
        form_layout.addRow("Email:", self.email_edit)
        form_layout.addRow("Full Name:", self.full_name_edit)

        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)

        layout.addLayout(form_layout)
        layout.addWidget(save_button)
        
        # Stil güncellemesi
        self.setStyleSheet("""
            QWidget {
                background-color: #000000; /* Genel arka plan siyah */
            }
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
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: orange;
            }
            QLabel {
                color: white; 
            }
        """)

    def load_user_data(self):
        user_data = self.view_model.get_user_data()
        if user_data["success"]:
            self.username_edit.setText(user_data["data"]["username"])
            self.email_edit.setText(user_data["data"]["email"] or "")
            self.full_name_edit.setText(user_data["data"]["full_name"] or "")

    def save_changes(self):
        update_data = {
            "username": self.username_edit.text(),
            "email": self.email_edit.text(),
            "full_name": self.full_name_edit.text()
        }
        
        result = self.view_model.update_user_data(update_data)
        
        if result["success"]:
            QMessageBox.information(self, "Success", "Profile updated successfully!")
        else:
            QMessageBox.critical(self, "Error", result["error"])