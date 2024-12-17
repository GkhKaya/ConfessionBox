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

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        sidebar.setContentsMargins(20, 20, 20, 20)
        sidebar.setAlignment(Qt.AlignTop)

        sidebar_buttons = ["Açık İtiraflar", "Kapalı İtiraflar", "Profil"]
        for button_text in sidebar_buttons:
            button = QPushButton(button_text)
            button.setStyleSheet("""
                QPushButton {
                    color: orange;
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """)
            sidebar.addWidget(button)

        # Logout Button
        logout_button = QPushButton("Çıkış Yap")
        logout_button.setStyleSheet("color: #007BFF; background-color: transparent; border: none; font-size: 14px;")
        sidebar.addStretch()
        sidebar.addWidget(logout_button)

        # Content Area
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("İtiraflar")
        header.setStyleSheet("font-size: 28px; font-weight: bold; color: white;")
        header.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(header)

        # Confession Items
        for _ in range(3):  # 3 kart ekliyoruz
            confession_widget = self.create_confession_widget(
                "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
                "Gokhan Kaya",
                "12.12.2022",
            )
            content_layout.addWidget(confession_widget)

        content_layout.addStretch()

        # Add layouts to main layout
        main_layout.addLayout(sidebar, 1)  # Yan menü
        main_layout.addLayout(content_layout, 3)  # İçerik alanı

    def create_confession_widget(self, text, user, date):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #1E293B;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        widget_layout = QVBoxLayout(widget)

        # Text
        text_label = QLabel(text)
        text_label.setStyleSheet("color: white; font-size: 14px;")
        text_label.setWordWrap(True)
        widget_layout.addWidget(text_label)

        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 10, 0, 0)

        # User
        user_label = QLabel(f"👤 {user}")
        user_label.setStyleSheet("color: #94A3B8; font-size: 12px;")
        footer_layout.addWidget(user_label)

        footer_layout.addStretch()

        # Date
        date_label = QLabel(f"⏰ {date}")
        date_label.setStyleSheet("color: #94A3B8; font-size: 12px;")
        footer_layout.addWidget(date_label)

        widget_layout.addLayout(footer_layout)
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OpenConfessionView()
    window.show()
    sys.exit(app.exec_())