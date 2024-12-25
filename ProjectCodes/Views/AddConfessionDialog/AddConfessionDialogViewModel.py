from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime
from Model.ConfessionModel import ConfessionModel
from Core.Manager.DatabaseManager import DatabaseManager
from Core.Manager.UserManager import UserManager

class AddConfessionViewModel(QObject):
    success_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()  # UserManager'ı burada başlatıyoruz
        self.db_manager = DatabaseManager()  # DatabaseManager'ı burada başlatıyoruz

    def submit_confession(self, confession_text: str, is_open: bool):
        # Mevcut kullanıcı bilgilerini alalım
        current_user = self.user_manager.current_user()

        if not current_user["success"]:
            self.error_signal.emit("Kullanıcı bilgisi alınamadı.")
            return
        
        user_id = current_user["user_id"]
        category_id = None  # Şu an için null olarak alıyoruz

        if not confession_text:
            self.error_signal.emit("İtiraf metni boş olamaz.")
            return

        # ConfessionModel oluşturuluyor
        confession = ConfessionModel(
            user_id=user_id,
            category_id=category_id,
            text=confession_text,
            is_open=is_open,
            created_at=datetime.now()  
        )

        # Veritabanına itiraf ekleniyor
        result = self.db_manager.insert_one("confessions", confession.to_dict())

        if result["success"]:
            self.success_signal.emit("İtiraf başarıyla eklendi.")
        else:
            self.error_signal.emit("İtiraf eklenirken bir hata oluştu.")