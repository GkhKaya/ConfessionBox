import pymongo
from Model.UserModel import UserModel
from utils.enum.ProjectError import DatabaseError
import bcrypt

class UserManager:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="confessiondb"):
        try:
            self.client = pymongo.MongoClient(db_url)
            self.db = self.client[db_name]
            self.users_collection = self.db["users"]
            self.logged_in_user = None
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
                return {"success": True, "message": "Login is completed!"}
            else:
                return {"success": False, "error": str(DatabaseError.INCORRECT_PASSWORD)}
        except Exception:
            return {"success": False, "error": str(DatabaseError.QUERY_FAILED)}

    def current_user(self):
        if self.logged_in_user:
            return {
                "success": True,
                "user": {
                    "username": self.logged_in_user["username"],
                    "email": self.logged_in_user.get("email"),
                    "full_name": self.logged_in_user.get("full_name"),
                    "gender": self.logged_in_user.get("gender"),
                }
            }
        else:
            return {"success": False, "error": "No user is currently logged in."}

    def logout_user(self):
        if self.logged_in_user:
            self.logged_in_user = None
            return {"success": True, "message": "User logged out successfully."}
        else:
            return {"success": False, "error": "No user is currently logged in."}