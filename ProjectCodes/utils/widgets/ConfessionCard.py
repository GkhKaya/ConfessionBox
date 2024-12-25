from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import os


class CardWidget(QWidget):
    def __init__(self, text: str, date: str, author: str = None, parent=None):
        super().__init__(parent)
        self.text = text
        self.author = author
        self.date = date
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #D3D3D3; border-radius: 10px;")
        self.setFixedSize(500, 200)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        text_label = QLabel(self.text, self)
        text_label.setWordWrap(True)
        text_label.setStyleSheet("color: #0B192C;")
        text_label.setFont(QFont("Arial", 12))
        text_label.setAlignment(Qt.AlignTop)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 10, 0, 0)

        if self.author:
            author_layout = QHBoxLayout()

            icon_path = os.path.join("assets", "person.fill.png")
            icon_label = QLabel(self)
            icon_label.setFixedSize(20, 20)
            icon_label.setPixmap(
                QPixmap(icon_path).scaled(
                    20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )

            author_label = QLabel(self.author, self)
            author_label.setStyleSheet("color: #0B192C;")
            author_label.setFont(QFont("Arial", 10))
            author_layout.addWidget(icon_label)
            author_layout.addWidget(author_label)
            bottom_layout.addLayout(author_layout)

        bottom_layout.addStretch()

        date_label = QLabel(self.date, self)
        date_label.setStyleSheet("color: #0B192C;")
        date_label.setFont(QFont("Arial", 10))
        bottom_layout.addWidget(date_label)

        main_layout.addWidget(text_label)
        main_layout.addLayout(bottom_layout)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    text = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s."
    author = "Gokhan Kaya"
    date = "12.12.2022"

    card = CardWidget(text, date, author)
    card.show()

    sys.exit(app.exec_())