from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QFormLayout, QPushButton, QCheckBox, QMessageBox
from Views.AddConfessionDialog.AddConfessionDialogViewModel import AddConfessionViewModel
from Core.Manager.DatabaseManager import DatabaseManager
from Core.Manager.UserManager import UserManager
class AddConfessionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("İtiraf Ekle")
        self.setStyleSheet("background-color: #2C2C2C;")
        self.setFixedSize(300, 250)

        layout = QFormLayout(self)

        # İtiraf metni girişi
        self.confession_input = QLineEdit(self)
        self.confession_input.setPlaceholderText("İtirafınızı buraya yazın...")

        # İtirafın açık mı olduğunu seçmek için checkbox
        self.is_open_checkbox = QCheckBox("Açık itiraf mı?", self)

        # Gönder butonu
        submit_button = QPushButton("Gönder", self)
        submit_button.clicked.connect(self.submit_confession)

        layout.addRow(QLabel("Yeni İtiraf"), self.confession_input)
        layout.addRow(self.is_open_checkbox)  # Checkbox
        layout.addRow(submit_button)

    def submit_confession(self):
        confession_text = self.confession_input.text()
        is_open = self.is_open_checkbox.isChecked()

        # ViewModel'i oluşturuyoruz
        view_model = AddConfessionViewModel()  # Bağımlılıkları burada yaratıyoruz
        view_model.success_signal.connect(self.on_success)
        view_model.error_signal.connect(self.on_error)

        # İtirafı ViewModel üzerinden gönderiyoruz
        view_model.submit_confession(confession_text, is_open)

    def on_success(self, message: str):
        QMessageBox.information(self, "Başarılı", message)
        self.accept()  # Dialogu kapat

    def on_error(self, message: str):
        QMessageBox.warning(self, "Hata", message)