import pymongo
from Model.UserModel import UserModel
from utils.enum.ProjectError import DatabaseError
import bcrypt

class UserManager:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="user_database"):
        try:
            self.client = pymongo.MongoClient(db_url)
            self.db = self.client[db_name]
            self.users_collection = self.db["users"]
        except Exception:
            raise Exception(str(DatabaseError.CONNECTION_FAILED))
    
    def register_user(self, username, password, email=None, full_name=None):
        try:
            # Kullanıcı adı kontrolü
            if self.users_collection.find_one({"username": username}):
                return {"success": False, "error": str(DatabaseError.USER_ALREADY_EXISTS)}

            # UserModel'i oluştur ve MongoDB'ye ekle
            user = UserModel(username=username, password=password, email=email, full_name=full_name)
            self.users_collection.insert_one(user.to_dict())
            return {"success": True, "message": "User registered successfully."}
        except Exception:
            return {"success": False, "error": str(DatabaseError.INSERT_FAILED)}
    
    def login_user(self, username, password):
        try:
            # Kullanıcı adı kontrolü
            user = self.users_collection.find_one({"username": username})
            if not user:
                return {"success": False, "error": str(DatabaseError.USER_NOT_FOUND)}

            # Şifre doğrulaması
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                return {"success": True, "message": "Login is complated!"}
            else:
                return {"success": False, "error": str(DatabaseError.INCORRECT_PASSWORD)}
        except Exception:
            return {"success": False, "error": str(DatabaseError.QUERY_FAILED)}