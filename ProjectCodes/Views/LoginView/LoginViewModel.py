from Core.UserManager.UserManager import UserManager
from utils.enum.ProjectError import DatabaseError
from utils.enum.ProjectError import ValidateError

class LoginViewModel:
    """
    The LoginViewModel class handles user login logic, including
    input validation and interaction with the UserManager for database operations.
    """

    def __init__(self):
        self.user_manager = UserManager()

    def login_user(self, username: str, password: str):
    # Validate if username or password fields are empty
        if not username or not password:
            return {"success": False, "error": ValidateError.EMPTY_FIELD.value}
        
        
    
        try:
        # Call the user manager to perform the login operation
            result = self.user_manager.login_user(username=username, password=password)
            return result
        except Exception as e:
        # Handle any unexpected exceptions and return an error
            return {"success": False, "error": str(e)}