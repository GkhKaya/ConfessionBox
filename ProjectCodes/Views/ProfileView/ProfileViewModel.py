from bson import ObjectId
from Core.Manager.DatabaseManager import DatabaseManager
from Core.Manager.UserManager import UserManager


class ProfileViewModel:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.user_manager = UserManager()
        self.validator = ProfileValidator()

    def get_user_data(self):
        current_user = self.user_manager.current_user()
        if not current_user["success"]:
            return {"success": False, "error": "User not found"}
        return {"success": True, "data": current_user}

    def get_user_confessions(self):
        # Get current user data
        current_user = self.user_manager.current_user()
        if not current_user["success"]:
            return {"success": False, "error": "User not found"}

        try:
            # Get user document with hobbies_id list
            user = self.db_manager.find_one(
                "users",
                {"_id": ObjectId(current_user["user_id"])}
            )

            if not user or 'hobbies_id' not in user:
                return {"success": True, "confessions": []}

            # Convert confession IDs to ObjectId
            confession_ids = [ObjectId(conf_id) for conf_id in user['hobbies_id']]
            
            # Fetch all confessions
            confessions = self.db_manager.find_all(
                "confessions",
                {"_id": {"$in": confession_ids}}
            )

            # Sort confessions by created_at in descending order
            sorted_confessions = sorted(
                confessions,
                key=lambda x: x.get('created_at', ''),
                reverse=True
            )

            return {"success": True, "confessions": sorted_confessions}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_user_data(self, update_data):
        # Existing update_user_data code remains the same
        validation_result = self.validator.validate_update_data(update_data)
        if not validation_result["success"]:
            return validation_result

        current_user = self.user_manager.current_user()
        if not current_user["success"]:
            return {"success": False, "error": "User not found"}

        try:
            result = self.db_manager.update_one(
                "users",
                {"_id": ObjectId(current_user["user_id"])},
                update_data
            )
            
            if result["success"]:
                user = self.db_manager.find_one("users", {"_id": ObjectId(current_user["user_id"])})
                self.user_manager.save_user_to_memory(user)
                
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
        

    def logout_user(self):
        try:
            # UserManager sınıfındaki logout_user fonksiyonunu çağırıyoruz
            logout_result = self.user_manager.logout_user()
            if logout_result["success"]:
                return {"success": True, "message": "User logged out successfully."}
            return {"success": False, "error": logout_result["error"]}
        except Exception as e:
            return {"success": False, "error": f"An error occurred during logout: {e}"}
        

import re

class ProfileValidator:
    def validate_update_data(self, data):
        if not data["username"]:
            return {"success": False, "error": "Username cannot be empty"}

        if data["email"] and not self._is_valid_email(data["email"]):
            return {"success": False, "error": "Invalid email format"}

        return {"success": True}

    def _is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None