from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget, QDialog, QLineEdit, QLabel, QFormLayout
from PyQt5.QtCore import Qt
from Views.AddConfessionDialog.AddConfessionDialog import AddConfessionDialog
from Views.PrivateConfessionView.PrivateConfessionView import PrivateConfessionView

class CloseConfessionsView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #3C3C3C;")
        # Add content to the Close Confessions view here

class OpenConfessionsView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #3C3C3C;")
        # Add content to the Close Confessions view here


class ProfileView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #4C4C4C;")
        # Add content to the Profile view here

class OpenConfessionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Itiraf Ekle")
        self.setStyleSheet("background-color: #2C2C2C;")
        self.setFixedSize(300, 200)

        layout = QFormLayout(self)

        self.confession_input = QLineEdit(self)
        self.confession_input.setPlaceholderText("İtirafınızı buraya yazın...")

        submit_button = QPushButton("Gönder", self)
        submit_button.clicked.connect(self.submit_confession)

        layout.addRow(QLabel("Yeni Itiraf"), self.confession_input)
        layout.addRow(submit_button)

    def submit_confession(self):
        confession = self.confession_input.text()
        if confession:
            print(f"Yeni itiraf: {confession}")
            self.accept()  # Dialogu kapat

class HomeView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        self.setStyleSheet("background-color: #0B192C;")

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        left_panel = QWidget(self)
        left_panel.setFixedWidth(screen_geometry.width() // 5)
        left_panel.setStyleSheet("background-color: #4d4d4d;")

        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignTop)

        self.buttons = []
        button_texts = ["Open Confessions", "Close Confessions", "Profile", "Itiraf Ekle"]

        for text in button_texts:
            button = QPushButton(text, left_panel)
            button.setStyleSheet(self.default_button_style())
            button.clicked.connect(self.on_button_clicked)
            left_layout.addWidget(button)
            self.buttons.append(button)

        self.buttons[0].setStyleSheet(self.active_button_style())

        # Stacked Widget for content views
        self.stacked_widget = QStackedWidget(self)
        self.confessions_view = OpenConfessionsView()
        self.close_confessions_view = PrivateConfessionView()
        self.profile_view = ProfileView()

        self.stacked_widget.addWidget(self.confessions_view)  # Initial view
        self.stacked_widget.addWidget(self.close_confessions_view)
        self.stacked_widget.addWidget(self.profile_view)

        main_layout.addWidget(left_panel)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def on_button_clicked(self):
        clicked_button = self.sender()
        button_index = self.buttons.index(clicked_button)

        # If the "Itiraf Ekle" button is clicked, open the confession dialog
        if button_index == 3:  # "Itiraf Ekle"
            self.open_confession_dialog()
        else:
            # Change the content shown in stacked widget based on the button index
            if button_index == 0:
                self.stacked_widget.setCurrentWidget(self.confessions_view)
            elif button_index == 1:
                self.stacked_widget.setCurrentWidget(self.close_confessions_view)
            elif button_index == 2:
                self.stacked_widget.setCurrentWidget(self.profile_view)

            # Update button styles
            for button in self.buttons:
                if button == clicked_button:
                    button.setStyleSheet(self.active_button_style())
                else:
                    button.setStyleSheet(self.default_button_style())

    def open_confession_dialog(self):
        dialog = AddConfessionDialog()
        dialog.exec_()

    @staticmethod
    def default_button_style():
        return """
            QPushButton {
                background: none;
                color: white;
                font-size: 16px;
                border: none;
                text-align: center;
                padding: 10px 20px;
            }
        """

    @staticmethod
    def active_button_style():
        return """
            QPushButton {
                background: none;
                color: orange;
                font-size: 24px;
                border: none;
                text-align: center;
                padding: 10px 20px;
            }
        """

# PyQt5 uygulamasını çalıştır
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = HomeView()
    window.show()
    sys.exit(app.exec_())