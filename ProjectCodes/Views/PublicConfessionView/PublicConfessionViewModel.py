from typing import Dict, List
from datetime import datetime
from pymongo import MongoClient
from utils.enum.ProjectError import DatabaseError
from Core.Manager.DatabaseManager import DatabaseManager
from bson import ObjectId  # ObjectId'yi import ediyoruz

class PublicConfessionViewModel:
    def __init__(self, db_url="mongodb://localhost:27017/", db_name="confessiondb"):
        self.db_url = db_url
        self.db_name = db_name
        self.db_manager = DatabaseManager(db_url, db_name)
        
    @staticmethod
    def get_public_confessions() -> List[Dict]:
        query = {"is_open": True}  # Açık olan itirafları almak için sorgu
        try:
            # PrivateConfessionViewModel örneği oluşturuluyor
            view_model = PublicConfessionViewModel()
            confessions = view_model.db_manager.find_all("confessions", query)
            
            # Her itiraf için yazar bilgisini ekliyoruz
            for confession in confessions:
                user_id = confession.get("user_id")
                if user_id:
                    # `user_id` ObjectId olarak kullanılmalı
                    try:
                        user_id = ObjectId(user_id)  # user_id'yi ObjectId'ye dönüştürüyoruz
                    except Exception as e:
                        confession['author_name'] = "Unknown"
                        print(f"Geçersiz user_id formatı: {user_id}")  # Loglama yapılabilir
                        continue
                    
                    # Yazar bilgilerini alıyoruz
                    user = view_model.db_manager.find_one("users", {"_id": user_id})
                    if user:
                        username = user.get("username")
                        if username:
                            confession['author_name'] = username  # Yazar adı
                        else:
                            confession['author_name'] = "Unknown"
                            print(f"Username bulunamadı: {user_id}")  # Loglama yapılabilir
                    else:
                        confession['author_name'] = "Unknown"
                        print(f"Kullanıcı bulunamadı: {user_id}")  # Loglama yapılabilir
                else:
                    confession['author_name'] = "Unknown"
                    print("User ID bulunamadı.")  # Loglama yapılabilir
                
            return confessions
        except Exception as e:
            print(f"Veritabanından itiraflar alınırken hata oluştu: {str(e)}")
            return []