from pymongo import MongoClient
from typing import Type, TypeVar, List, Dict, Any, Optional
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class DatabaseManager():
     def __init__(self, database_name: str):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[database_name]

     def fetch_all(self, collection_name: str, model: Type[T]) -> List[T]:
        collection = self.db[collection_name]
        documents = collection.find()
        return [model(**doc) for doc in documents]
     
     def fetch_one(self, collection_name: str, query: Dict[str, Any], model: Type[T]) -> Optional[T]:
        collection = self.db[collection_name]
        document = collection.find_one(query)
        if document:
            return model(**document)
        return None
    
     def insert_one(self, collection_name: str, data: T) -> str:
        collection = self.db[collection_name]
        result = collection.insert_one(data.dict())
        return str(result.inserted_id)
     
     def insert_many(self, collection_name: str, data_list: List[T]) -> List[str]:
       
        collection = self.db[collection_name]
        result = collection.insert_many([data.dict() for data in data_list])
        return [str(id) for id in result.inserted_ids]

     def update_one(self, collection_name: str, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
       
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update_data})
        return result.modified_count

     def delete_one(self, collection_name: str, query: Dict[str, Any]) -> int:
       
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count

     def delete_many(self, collection_name: str, query: Dict[str, Any]) -> int:
       
        collection = self.db[collection_name]
        result = collection.delete_many(query)
        return result.deleted_count
