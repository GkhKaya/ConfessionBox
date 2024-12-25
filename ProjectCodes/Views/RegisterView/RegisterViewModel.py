from Core.Manager.UserManager import UserManager
from utils.enum.ProjectError import DatabaseError
from utils.enum.ProjectError import ValidateError

class RegisterViewModel:
    """
    The RegisterViewModel class handles user registration logic, including
    input validation and interaction with the UserManager for database operations.
    """
     
    def __init__(self):
        self.user_manager = UserManager()

    def register_user(self, username: str, password: str, email: str = None, gender: str = None):
        if not username or not password:
            return {"success": False, "error": ValidateError.EMPTY_FIELD.value}

        if len(password) < 6:
            return {"success": False, "error": ValidateError.LEAST_EIGHT_CHATACTER.value}

        if not any(char.isdigit() for char in password):
            return {"success": False, "error": ValidateError.MUST_CONTAIN_NUMBER.value}

        if not any(char.islower() for char in password):
            return {"success": False, "error": ValidateError.MUST_CONTAIN_LOWERCASE.value}

        if not any(char.isupper() for char in password):
            return {"success": False, "error": ValidateError.MUST_CONTAIN_UPPERCASE.value}

        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?' for char in password):
            return {"success": False, "error": ValidateError.MUST_CONTAIN_SPECIAL_CHAR.value}

        try:
            result = self.user_manager.register_user(username=username, password=password, email=email, gender=gender)

            # Geri dönen değeri yazdır
            print(f"Register işlemi sonucu: {result}")

            return result
        except Exception as e:
            print(f"Register sırasında hata oluştu: {e}")
            return {"success": False, "error": "Registration failed. Please try again later."}