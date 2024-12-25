from datetime import datetime
from typing import Optional

class ConfessionModel:
    """
    Represents a confession model for storing and processing confession data.

    Attributes:
        user_id (str): The unique identifier of the user who made the confession.
        category_id (str): The unique identifier of the category the confession belongs to.
        text (str): The content of the confession.
        is_open (bool): A flag indicating whether the confession is open or private.
        created_at (datetime): The timestamp when the confession was created.
        author_name (str): The name of the user who made the confession.
    """

    def __init__(self, user_id: str, category_id: str, text: str, is_open: bool, created_at: datetime, author_name: Optional[str] = "Unknown"):
        """
        Initializes the ConfessionModel with the provided attributes.

        Args:
            user_id (str): The unique identifier of the user who made the confession.
            category_id (str): The unique identifier of the category the confession belongs to.
            text (str): The content of the confession.
            is_open (bool): A flag indicating whether the confession is open or private.
            created_at (datetime): The timestamp when the confession was created.
            author_name (str): The name of the user who made the confession.
        """
        self.user_id = user_id
        self.category_id = category_id
        self.text = text
        self.is_open = is_open
        self.created_at = created_at
        self.author_name = author_name

    @staticmethod
    def from_dict(doc: dict):
        """
        Converts a dictionary (typically from MongoDB) into a ConfessionModel instance.

        Args:
            doc (dict): The dictionary representation of a confession document from the database.

        Returns:
            ConfessionModel: A ConfessionModel instance.
        """
        user_id = str(doc.get("user_id"))
        category_id = str(doc.get("category_id"))
        text = doc.get("text")
        is_open = doc.get("is_open", False)
        
        created_at = doc.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        elif isinstance(created_at, dict) and "$date" in created_at:
            created_at = created_at["$date"]
            created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # `author_name`'i ekliyoruz
        author_name = doc.get('author_name', 'Unknown')
        
        return ConfessionModel(user_id, category_id, text, is_open, created_at, author_name)

    def to_dict(self):
        """
        Converts the ConfessionModel instance into a dictionary for database storage.

        Returns:
            dict: A dictionary representation of the confession model.
        """
        return {
            "user_id": self.user_id,
            "category_id": self.category_id,
            "text": self.text,
            "is_open": self.is_open,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "author_name": self.author_name
        }