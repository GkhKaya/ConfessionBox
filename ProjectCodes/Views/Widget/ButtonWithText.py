from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class ButtonWithText(QWidget):
    def __init__(self, text, style, function):
        super().__init__()
        self.init_ui(text, style, function)

    def init_ui(self, text, style, function):
        layout = QVBoxLayout()
        button = QPushButton(text)
        button.setFlat(True)  # Butonun arka planını kaldır
        button.setStyleSheet(style)
        button.clicked.connect(function)
        layout.addWidget(button)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)