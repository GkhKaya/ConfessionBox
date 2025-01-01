from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime
from Model.ConfessionModel import ConfessionModel
from Core.Manager.DatabaseManager import DatabaseManager
from Core.Manager.UserManager import UserManager
from bson import ObjectId

class AddConfessionViewModel(QObject):
    success_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.db_manager = DatabaseManager()

    def submit_confession(self, confession_text: str, is_open: bool):
        # Get current user information
        current_user = self.user_manager.current_user()

        if not current_user["success"]:
            self.error_signal.emit("Kullanıcı bilgisi alınamadı.")
            return
        
        user_id = current_user["user_id"]
        category_id = None

        if not confession_text:
            self.error_signal.emit("İtiraf metni boş olamaz.")
            return

        # Create ConfessionModel
        confession = ConfessionModel(
            user_id=user_id,
            category_id=category_id,
            text=confession_text,
            is_open=is_open,
            created_at=datetime.now()  
        )

        # Add confession to database
        result = self.db_manager.insert_one("confessions", confession.to_dict())

        if result["success"]:
            try:
                # Get the last inserted confession's ID
                last_confession = self.db_manager.find_one(
                    "confessions",
                    {"user_id": user_id}
                )
                
                if last_confession and "_id" in last_confession:
                    confession_id = str(last_confession["_id"])
                    
                    # Update user's hobbies_id list
                    user_query = {"_id": ObjectId(user_id)}
                    update_data = {"$push": {"hobbies_id": confession_id}}
                    
                    # Use update_one without $set since we're using $push operator
                    collection = self.db_manager.db["users"]
                    update_result = collection.update_one(user_query, update_data)

                    if update_result.modified_count > 0:
                        self.success_signal.emit("İtiraf başarıyla eklendi ve kullanıcı bilgileri güncellendi.")
                    else:
                        self.error_signal.emit("İtiraf eklendi fakat kullanıcı bilgileri güncellenemedi.")
                else:
                    self.error_signal.emit("İtiraf ID'si alınamadı.")
            except Exception as e:
                self.error_signal.emit(f"İtiraf eklendi fakat bir hata oluştu: {str(e)}")
        else:
            self.error_signal.emit("İtiraf eklenirken bir hata oluştu.")