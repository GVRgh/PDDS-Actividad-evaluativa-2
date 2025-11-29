from typing import List, Dict
from utils.database_connection import DatabaseConnection

class FavoriteRepository:
    
    def __init__(self, db_path: str = "db.json"):
        self.db = DatabaseConnection(db_path)
        self.db.connect()

    def all(self) -> List[Dict]:
        return self.db.get_favorites() or []

    def exists(self, user_id: int, product_id: int) -> bool:
        favorites = self.all()
        return any(f.get("user_id") == user_id and f.get("product_id") == product_id for f in favorites)

    def add(self, user_id: int, product_id: int) -> Dict:
        if self.exists(user_id, product_id):
            raise ValueError("Favorite already exists")

        new_fav = {"user_id": user_id, "product_id": product_id}
        self.db.add_favorite(new_fav)
        return new_fav

    def remove(self, user_id: int, product_id: int) -> bool:
        return self.db.remove_favorite(user_id, product_id)

    def save_all(self, favorites_list: List[Dict]):
        self.db.save_favorites(favorites_list)
