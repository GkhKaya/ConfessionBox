import pymongo
from Model.UserModel import UserModel
from utils.enum.ProjectError import DatabaseError
import bcrypt
import json
from PyQt5.QtCore import QSettings

class UserManager:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="confessiondb"):
        try:
            self.client = pymongo.MongoClient(db_url)
            self.db = self.client[db_name]
            self.users_collection = self.db["users"]
            self.logged_in_user = None
            self.settings = QSettings("YourCompany", "YourApp")  # Bellek yönetimi için QSettings kullanıyoruz
        except Exception:
            raise Exception(str(DatabaseError.CONNECTION_FAILED))

    def register_user(self, username, password, email=None, full_name=None, gender=None):
        try:
            if self.users_collection.find_one({"username": username}):
                return {"success": False, "error": str(DatabaseError.USER_ALREADY_EXISTS)}
            
            # Create UserModel instance - password hashing is handled in the model
            user = UserModel(
                username=username, 
                password=password,  # Pass the plain password, UserModel will hash it
                email=email, 
                full_name=full_name, 
                gender=gender
            )
            
            # Insert the user document
            self.users_collection.insert_one(user.to_dict())
            return {"success": True, "message": "User registered successfully."}

        except pymongo.errors.ServerSelectionTimeoutError as timeout_error:
            print(f"Database connection error: {timeout_error}")
            return {"success": False, "error": "Unable to connect to the database. Please check the database server."}

        except pymongo.errors.OperationFailure as operation_error:
            print(f"Database operation failed: {operation_error}")
            return {"success": False, "error": "An error occurred during the database operation. Please try again later."}

        except Exception as e:
            print(f"Unexpected error during registration: {e}")
            return {"success": False, "error": f"Unexpected error: {e}"}

    def login_user(self, username, password):
        try:
            user = self.users_collection.find_one({"username": username})
            if not user:
                return {"success": False, "error": str(DatabaseError.USER_NOT_FOUND)}

            # Convert password to bytes if it's a string
            if isinstance(password, str):
                password = password.encode('utf-8')

            if bcrypt.checkpw(password, user['password']):
                self.logged_in_user = user
                self.save_user_to_memory(user)  # Kullanıcıyı bellek ile kaydediyoruz
                return {"success": True, "message": "Login is completed!"}
            else:
                return {"success": False, "error": str(DatabaseError.INCORRECT_PASSWORD)}
        except Exception:
            return {"success": False, "error": str(DatabaseError.QUERY_FAILED)}

    def save_user_to_memory(self, user):
        # Kullanıcı bilgilerini JSON formatında saklıyoruz
        user_data = {
            "user_id": str(user["_id"]),
            "username": user["username"],
            "email": user.get("email"),
            "full_name": user.get("full_name"),
            "gender": user.get("gender")
        }
        # Kullanıcıyı belleğe kaydediyoruz
        self.settings.setValue("user", json.dumps(user_data))

    def get_user_from_memory(self):
        # Kullanıcı bilgilerini bellekten alıyoruz
        user_data = self.settings.value("user")
        if user_data:
            return json.loads(user_data)
        return None

    def current_user(self):
        # Bellekten kullanıcı bilgilerini alıyoruz
        user = self.get_user_from_memory()
        if user:
            return {
                "success": True,
                "user_id": user["user_id"],
                "username": user["username"],
                "email": user["email"],
                "full_name": user["full_name"],
                "gender": user["gender"],
            }
        else:
            return {"success": False, "error": "No user is currently logged in."}

    def logout_user(self):
        if self.logged_in_user:
            self.logged_in_user = None
            self.settings.remove("user")  # Bellekten kullanıcı bilgisini siliyoruz
            return {"success": True, "message": "User logged out successfully."}
        else:
            return {"success": False, "error": "No user is currently logged in."}