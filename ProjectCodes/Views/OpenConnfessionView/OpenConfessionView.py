import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class OpenConfessionView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("İtiraflar")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("background-color: #0B192C; color: white;")

        # Main Layout
        main_layout = QHBoxLayout(self)

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenConfessionView()
    window.show()
    sys.exit(app.exec_())