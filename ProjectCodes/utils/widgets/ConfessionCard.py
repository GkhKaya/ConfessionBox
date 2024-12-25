import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont
from datetime import datetime

class LoremIpsumCard(QWidget):
    def __init__(self, text: str, date: str):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        try:
            formatted_date = datetime.fromisoformat(date).strftime('%d.%m.%Y %H:%M')
        except ValueError:
            formatted_date = date
            
        self.init_ui(text, formatted_date)
        
    def init_ui(self, text: str, date: str):
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)
        
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setFont(QFont("Segoe UI", 13))
        text_label.setStyleSheet("color: #2C3E50;")
        
        date_label = QLabel(date)
        date_label.setAlignment(Qt.AlignRight)
        date_label.setFont(QFont("Segoe UI", 11))
        date_label.setStyleSheet("color: #7F8C8D;")
        
        layout.addWidget(text_label)
        layout.addWidget(date_label)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            LoremIpsumCard {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
            LoremIpsumCard:hover {
                border: 1px solid #BDBDBD;
                background-color: #FAFAFA;
            }
        """)
        
    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return QSize(0, 120)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    card = LoremIpsumCard("Test confession text", "2024-01-01")
    card.show()
    sys.exit(app.exec_())
