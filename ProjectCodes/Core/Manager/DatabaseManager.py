import pymongo
from typing import Dict, Any, List, Optional
from utils.enum.ProjectError import DatabaseError


class DatabaseManager:
    """
    DatabaseManager handles CRUD operations for MongoDB collections.
    """

    def __init__(self, db_url="mongodb://localhost:27017/", db_name="confessiondb"):
        """
        Initializes the DatabaseManager and establishes a connection to the MongoDB database.

        Args:
            db_url (str): The MongoDB connection URL. Defaults to 'mongodb://localhost:27017/'.
            db_name (str): The name of the database to use. Defaults to 'default_database'.

        Raises:
            Exception: If the database connection fails.
        """
        try:
            self.client = pymongo.MongoClient(db_url)
            self.db = self.client[db_name]
        except Exception:
            raise Exception(str(DatabaseError.CONNECTION_FAILED))

    def insert_one(self, collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inserts a single document into the specified collection.

        Args:
            collection_name (str): The name of the collection.
            data (Dict[str, Any]): The data to insert.

        Returns:
            dict: A dictionary containing the success status and a message or error.
        """
        try:
            collection = self.db[collection_name]
            collection.insert_one(data)
            return {"success": True, "message": "Document inserted successfully."}
        except Exception:
            return {"success": False, "error": str(DatabaseError.INSERT_FAILED)}

    def find_one(self, collection_name: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Finds a single document in the specified collection that matches the query.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to filter documents.

        Returns:
            Optional[Dict[str, Any]]: The found document, or None if no match.
        """
        try:
            collection = self.db[collection_name]
            return collection.find_one(query)
        except Exception:
            return None

    def find_all(self, collection_name: str, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """
        Finds all documents in the specified collection that match the query.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any], optional): The query to filter documents. Defaults to {}.

        Returns:
            List[Dict[str, Any]]: A list of matching documents.
        """
        try:
            collection = self.db[collection_name]
            return list(collection.find(query))
        except Exception:
            return []

    def update_one(self, collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates a single document in the specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to filter the document.
            update_data (Dict[str, Any]): The data to update.

        Returns:
            dict: A dictionary containing the success status and a message or error.
        """
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {"$set": update_data})
            if result.modified_count > 0:
                return {"success": True, "message": "Document updated successfully."}
            else:
                return {"success": False, "error": "No document matched the query."}
        except Exception:
            return {"success": False, "error": str(DatabaseError.UPDATE_FAILED)}

    def delete_one(self, collection_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deletes a single document in the specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to filter the document.

        Returns:
            dict: A dictionary containing the success status and a message or error.
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            if result.deleted_count > 0:
                return {"success": True, "message": "Document deleted successfully."}
            else:
                return {"success": False, "error": "No document matched the query."}
        except Exception:
            return {"success": False, "error": str(DatabaseError.DELETE_FAILED)}

    def delete_many(self, collection_name: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deletes multiple documents in the specified collection.

        Args:
            collection_name (str): The name of the collection.
            query (Dict[str, Any]): The query to filter the documents.

        Returns:
            dict: A dictionary containing the success status and the number of documents deleted.
        """
        try:
            collection = self.db[collection_name]
            result = collection.delete_many(query)
            return {"success": True, "message": f"{result.deleted_count} documents deleted."}
        except Exception:
            return {"success": False, "error": str(DatabaseError.DELETE_FAILED)}