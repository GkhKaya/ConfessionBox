from typing import Dict, List
from datetime import datetime
from pymongo import MongoClient
from utils.enum.ProjectError import DatabaseError
from Core.Manager.DatabaseManager import DatabaseManager

class PrivateConfessionViewModel:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="confessiondb"):
        self.db_url = db_url
        self.db_name = db_name
        self.db_manager = DatabaseManager(db_url, db_name)
        
    @staticmethod
    def get_private_confessions() -> List[Dict]:
        """
        MongoDB'den 'is_open' değeri False olan tüm itirafları getirir.
        """
        query = {"is_open": False}
        try:
            # PrivateConfessionViewModel örneği oluşturuluyor
            view_model = PrivateConfessionViewModel()
            private_confessions = view_model.db_manager.find_all("confessions", query)
            return private_confessions
        except Exception as e:
            print(f"Error fetching private confessions: {str(e)}")
            return []