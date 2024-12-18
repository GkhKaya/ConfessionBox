from datetime import datetime
import bcrypt


class UserModel:
    """
    Represents a user model for storing user data and performing password hashing.

    Attributes:
        username (str): The username of the user.
        email (str): The email address of the user. Optional.
        full_name (str): The full name of the user. Optional.
        password (str): The hashed password of the user.
        gender (str): The gender of the user. Optional.
        created_at (datetime): The timestamp when the user was created.
    """
    def __init__(self, username: str, password: str, email: str = None, full_name: str = None, gender: str = None):

        """
        Initializes the UserModel with the provided attributes and hashes the password.

        Args:
            username (str): The username of the user.
            password (str): The plaintext password of the user to be hashed.
            email (str, optional): The email address of the user. Defaults to None.
            full_name (str, optional): The full name of the user. Defaults to None.
            gender (str, optional): The gender of the user. Defaults to None.
        """
         
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password = self.hash_password(password)
        self.gender = gender  
        self.created_at = datetime.utcnow()

    @staticmethod
    def hash_password(password):
        """
        Hashes a plaintext password using bcrypt.

        Args:
            password (str): The plaintext password to hash.

        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def to_dict(self):
        """
        Converts the UserModel instance into a dictionary for database storage.

        Returns:
            dict: A dictionary representation of the user model.
                  Example:
                  {
                      "username": "johndoe",
                      "email": "johndoe@example.com",
                      "full_name": "John Doe",
                      "password": "<hashed_password>",
                      "gender": "Male",
                      "created_at": "<timestamp>"
                  }
        """
        
        return {
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "gender": self.gender,  
            "created_at": self.created_at
        }