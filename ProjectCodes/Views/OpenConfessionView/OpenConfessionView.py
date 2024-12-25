from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtCore import Qt
from Views.OpenConfessionView.OpenConfessionViewModel import OpenConfessionViewModel
from utils.widgets.ConfessionCard import CardWidget

class OpenConfessionView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view_model = OpenConfessionViewModel()  
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget) 
        try:
            card_widgets = self.view_model.get_confessions()
            if card_widgets:  
                for card_widget in card_widgets:
                    content_layout.addWidget(card_widget)
            else:
                no_data_label = QLabel("Henüz bir itiraf yok.")
                no_data_label.setAlignment(Qt.AlignCenter)
                content_layout.addWidget(no_data_label)
        except Exception as e:
            error_label = QLabel(f"Hata oluştu: {e}")
            error_label.setAlignment(Qt.AlignCenter)
            content_layout.addWidget(error_label)

        scroll_area.setWidget(content_widget)  
        layout.addWidget(scroll_area) 

        
        self.setLayout(layout)
        self.setWindowTitle("Confessions") 
        self.setGeometry(100, 100, 600, 400)  