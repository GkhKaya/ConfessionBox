# UpdateConfessionDialogViewModel.py
from PyQt5.QtCore import QObject, pyqtSignal
from Core.Manager.DatabaseManager import DatabaseManager
from bson import ObjectId

class UpdateConfessionViewModel(QObject):
    success_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()

    def update_confession(self, confession_id: str, confession_text: str, is_open: bool):
        if not confession_text:
            self.error_signal.emit("İtiraf metni boş olamaz.")
            return

        try:
            # Update the confession
            result = self.db_manager.update_one(
                "confessions",
                {"_id": ObjectId(confession_id)},
                {
                    "text": confession_text,
                    "is_open": is_open
                }
            )

            if result["success"]:
                self.success_signal.emit("İtiraf başarıyla güncellendi.")
            else:
                self.error_signal.emit(result.get("error", "İtiraf güncellenirken bir hata oluştu."))
        except Exception as e:
            self.error_signal.emit(f"Bir hata oluştu: {str(e)}")