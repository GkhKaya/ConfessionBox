import pymongo
from Model.UserModel import UserModel
from utils.enum.ProjectError import DatabaseError
import bcrypt

class UserManager:
    """
    UserManager handles operations related to user management, 
    such as user registration, login, and interactions with the user database.
    """

    def __init__(self, db_url="mongodb://localhost:27017/", db_name="user_database"):
        """
        Initializes the UserManager and establishes a connection to the MongoDB database.

        Args:
            db_url (str): The MongoDB connection URL. Defaults to 'mongodb://localhost:27017/'.
            db_name (str): The name of the database to use. Defaults to 'user_database'.

        Raises:
            Exception: If the database connection fails.
        """
        try:
            self.client = pymongo.MongoClient(db_url)
            self.db = self.client[db_name]
            self.users_collection = self.db["users"]
            self.logged_in_user = None  # Giriş yapan kullanıcıyı takip etmek için
        except Exception:
            raise Exception(str(DatabaseError.CONNECTION_FAILED))

    def register_user(self, username, password, email=None, full_name=None, gender=None):
        """
        Registers a new user by adding their details to the database.

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
            email (str, optional): The email address of the user. Defaults to None.
            full_name (str, optional): The full name of the user. Defaults to None.
            gender (str, optional): The gender of the user. Defaults to None.

        Returns:
            dict: A dictionary containing the success status and a message or error.
                Example:
                    {"success": True, "message": "User registered successfully."}
                    {"success": False, "error": "User already exists."}
        """
        try:
            # Check if the username already exists in the database
            if self.users_collection.find_one({"username": username}):
                return {"success": False, "error": str(DatabaseError.USER_ALREADY_EXISTS)}
            
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create a new user instance and save it to the database
            user = UserModel(
                username=username, 
                password=hashed_password, 
                email=email, 
                full_name=full_name, 
                gender=gender
            )
            self.users_collection.insert_one(user.to_dict())
            return {"success": True, "message": "User registered successfully."}
        except Exception:
            return {"success": False, "error": str(DatabaseError.INSERT_FAILED)}

    def login_user(self, username, password):
        """
        Authenticates a user by verifying their credentials.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            dict: A dictionary containing the success status and a message or error.
                Example:
                    {"success": True, "message": "Login is completed!"}
                    {"success": False, "error": "User not found."}
                    {"success": False, "error": "Incorrect password."}
        """
        try:
            # Check if the user exists in the database
            user = self.users_collection.find_one({"username": username})
            if not user:
                return {"success": False, "error": str(DatabaseError.USER_NOT_FOUND)}

            # Verify the password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                self.logged_in_user = user  # Giriş yapan kullanıcıyı sakla
                return {"success": True, "message": "Login is completed!"}
            else:
                return {"success": False, "error": str(DatabaseError.INCORRECT_PASSWORD)}
        except Exception:
            return {"success": False, "error": str(DatabaseError.QUERY_FAILED)}

    def current_user(self):
        """
        Returns the currently logged-in user.

        Returns:
            dict: A dictionary containing the success status and user information or an error.
                Example:
                    {"success": True, "user": {...}}
                    {"success": False, "error": "No user is currently logged in."}
        """
        if self.logged_in_user:
            # Return logged-in user details
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
        """
        Logs out the currently logged-in user.

        Returns:
            dict: A dictionary indicating the logout status.
                Example:
                    {"success": True, "message": "User logged out successfully."}
        """
        if self.logged_in_user:
            self.logged_in_user = None
            return {"success": True, "message": "User logged out successfully."}
        else:
            return {"success": False, "error": "No user is currently logged in."}