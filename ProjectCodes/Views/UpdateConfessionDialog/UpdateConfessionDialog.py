# UpdateConfessionDialog.py
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFormLayout, QPushButton, QCheckBox, QMessageBox
from Views.UpdateConfessionDialog.UpdateConfessionDialogViewModel import UpdateConfessionViewModel

class UpdateConfessionDialog(QDialog):
    def __init__(self, confession_id, confession_text, is_open):
        super().__init__()
        self.confession_id = confession_id
        self.original_text = confession_text
        self.original_is_open = is_open
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("İtiraf Düzenle")
        self.setStyleSheet("""
            QDialog {
                background-color: #2C2C2C;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #DDD;
                border-radius: 4px;
                background-color: #3C3C3C;
                color: white;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                padding: 8px 16px;
                border: 1px solid orange;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: orange;
            }
            QCheckBox {
                color: white;
            }
        """)
        self.setFixedSize(300, 250)

        layout = QFormLayout(self)

        # İtiraf metni girişi
        self.confession_input = QLineEdit(self)
        self.confession_input.setText(self.original_text)
        self.confession_input.setPlaceholderText("İtirafınızı düzenleyin...")

        # İtirafın açık mı olduğunu seçmek için checkbox
        self.is_open_checkbox = QCheckBox("Açık itiraf mı?", self)
        self.is_open_checkbox.setChecked(self.original_is_open)

        # Güncelle butonu
        update_button = QPushButton("Güncelle", self)
        update_button.clicked.connect(self.update_confession)

        # İptal butonu
        cancel_button = QPushButton("İptal", self)
        cancel_button.clicked.connect(self.reject)

        layout.addRow(QLabel("İtiraf Metni:"), self.confession_input)
        layout.addRow(self.is_open_checkbox)
        layout.addRow(update_button)
        layout.addRow(cancel_button)

    def update_confession(self):
        confession_text = self.confession_input.text()
        is_open = self.is_open_checkbox.isChecked()

        # Check if anything changed
        if confession_text == self.original_text and is_open == self.original_is_open:
            QMessageBox.information(self, "Bilgi", "Herhangi bir değişiklik yapılmadı.")
            self.accept()
            return

        view_model = UpdateConfessionViewModel()
        view_model.success_signal.connect(self.on_success)
        view_model.error_signal.connect(self.on_error)

        view_model.update_confession(self.confession_id, confession_text, is_open)

    def on_success(self, message: str):
        QMessageBox.information(self, "Başarılı", message)
        self.accept()

    def on_error(self, message: str):
        QMessageBox.warning(self, "Hata", message)


