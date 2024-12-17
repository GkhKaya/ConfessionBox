from datetime import datetime
import bcrypt


class UserModel:
    def __init__(self, username: str, password: str, email: str = None, full_name: str = None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.password = self.hash_password(password)
        self.created_at = datetime.utcnow()

    @staticmethod
    def hash_password(password):
        """Şifreyi hashle."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def to_dict(self):
        """MongoDB'ye eklenirken kullanılacak sözlük formatı."""
        return {
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "created_at": self.created_at
        }