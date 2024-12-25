from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, 
    QHBoxLayout, QApplication, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from Views.RegisterView.RegisterViewModel import RegisterViewModel
from Views.Widget.ButtonWithText import ButtonWithText


class RegisterView(QWidget):
    """
    A PyQt5 widget for the user registration view.

    Provides input fields for username, password, and gender, along with a registration button.
    """

    def __init__(self):
        """
        Initializes the RegisterView widget.
        """
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        Sets up the user interface for the registration view, including layout, styles, and event handling.
        """
        # Configure the main window size and background color
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        self.setStyleSheet("background-color: #0B192C;")  # Set a dark background color

        # Create the main layout for the view
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Back button layout and setup
        back_button_layout = QHBoxLayout()
        back_button = QPushButton("")
        back_button.setFlat(True)  # Make the button appear flat
        back_button.setIcon(QIcon("assets/chevron.left.png"))  # Set the icon for the back button
        back_button.setIconSize(QSize(16, 16))  # Set the icon size
        back_button.clicked.connect(self.go_back)  # Connect the back button to its handler
        back_button_layout.addWidget(back_button)
        back_button_layout.setAlignment(Qt.AlignLeft)

        # Title label for the registration view
        title_label = QLabel("Register")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #F8F8F8;")  # White text color
        title_label.setAlignment(Qt.AlignCenter)

        # Labels for input fields
        username_label = QLabel("Username")
        password_label = QLabel("Password")
        gender_label = QLabel("Gender")

        # Input fields for user data
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # Mask the password input

        # Gender selection dropdown
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Prefer not to say", "Male", "Female", "Other"])

        # Registration button with custom styling
        register_button = ButtonWithText(
            text="Register",
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

        # Add widgets to the main layout
        layout.addLayout(back_button_layout)  # Add the back button
        layout.addWidget(title_label)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(gender_label)
        layout.addWidget(self.gender_combo)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def go_back(self):
        """
        Navigates back to the authentication view when the back button is clicked.
        """
        from Views.AuthView.AuthView import AuthView  # Import the authentication view
        self.auth_view = AuthView()  # Create an instance of the authentication view
        self.auth_view.show()
        self.close()

    def register_procress(self):
        """
        Handles the registration process when the register button is clicked.
        
        Gathers input values from the form, validates them, and attempts to register the user
        via the RegisterViewModel. Displays success or error messages based on the result.
        """
        # Get input values
        username = self.username_input.text()
        password = self.password_input.text()
        gender = self.gender_combo.currentText()

        # Call the view model for registration
        view_model = RegisterViewModel()
        result = view_model.register_user(username=username, password=password, gender=gender)

        # Display success or error message
        if result["success"]:
            QMessageBox.information(self, "Success", result["message"])
            self.go_back()
        else:
            # Konsola hata yazdır
            print(f"Hata detayı: {result['error']}")
            QMessageBox.warning(self, "Error", result["error"])
