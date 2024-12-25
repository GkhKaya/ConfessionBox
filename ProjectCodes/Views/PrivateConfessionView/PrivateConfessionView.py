from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import Qt
from utils.widgets.ConfessionCard import LoremIpsumCard
from Views.PrivateConfessionView.PrivateConfessionViewModel import PrivateConfessionViewModel

class PrivateConfessionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(15)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_widget.setStyleSheet("background: transparent;")
        
        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)
        
        self.setStyleSheet("background-color: #F5F5F5;")
        self.setMinimumSize(600, 400)

    def init_ui(self):
        self.clear_cards()
        view_model = PrivateConfessionViewModel()
        confessions = view_model.get_private_confessions()
        
        for confession in confessions:
            card = LoremIpsumCard(
                text=confession.get('text', 'No text available'),
                date=confession.get('created_at', 'No date provided')
            )
            self.content_layout.addWidget(card)
        self.content_layout.addStretch()

    def clear_cards(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def showEvent(self, event):
        self.init_ui()
        super().showEvent(event)