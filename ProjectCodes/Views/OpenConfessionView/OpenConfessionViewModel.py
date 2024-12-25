from typing import List
from datetime import datetime
from PyQt5.QtCore import Qt
from Model.ConfessionModel import ConfessionModel  
from Core.Manager.DatabaseManager import DatabaseManager
from utils.widgets.ConfessionCard import CardWidget  


class OpenConfessionViewModel:
    def __init__(self):
        self.database_manager = DatabaseManager(db_name="confessions_database")  # Veritabanı adı tanımlandı

    def get_confessions(self) -> List[CardWidget]:
        """
        Fetches confessions from the database and converts them into CardWidgets.

        Returns:
            List[CardWidget]: A list of CardWidget instances.
        """
        # Veritabanından verileri getir
        confessions_data = self.database_manager.find_all("confessions")
       

        card_widgets = []
        for confession_data in confessions_data:
            try:
                # ConfessionModel'e dönüştür
                confession = ConfessionModel(
                    text=confession_data.get("text"),
                    user_id=confession_data.get("user_id"),
                    created_at=datetime.strptime(confession_data.get("created_at"), "%Y-%m-%d %H:%M:%S")
                    if confession_data.get("created_at")
                    else None,
                )
                
                # Eksik veri kontrolü
                if not confession.text or not confession.user_id or not confession.created_at:
                    continue
                
                # CardWidget oluştur
                text = confession.text
                author = confession.user_id
                date = confession.created_at.strftime("%d.%m.%Y %H:%M:%S")
                
                card_widget = CardWidget(text, date, author)
                card_widgets.append(card_widget)
            except Exception as e:
                print(f"Error processing confession: {e}")
                continue  # Hata durumunda devam et

        return card_widgets