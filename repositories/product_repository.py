from typing import List, Optional, Dict
from utils.database_connection import DatabaseConnection

class ProductRepository:
    
    def __init__(self, db_path: str = "db.json"):
        self.db = DatabaseConnection(db_path)
        self.db.connect()

    def _reload(self) -> List[Dict]:
        return self.db.get_products() or []

    def all(self) -> List[Dict]:
        return self._reload()

    def get_by_id(self, product_id: int) -> Optional[Dict]:
        products = self._reload()
        return next((p for p in products if p.get("id") == product_id), None)

    def filter_by_category(self, category: str) -> List[Dict]:
        if not category:
            return []
        products = self._reload()
        return [p for p in products if p.get("category", "").lower() == category.lower()]

    def next_id(self) -> int:
        products = self._reload()
        if not products:
            return 1
        max_id = max((p.get("id", 0) for p in products), default=0)
        return max_id + 1

    def add(self, product_data: Dict) -> Dict:
        products = self._reload()

        for p in products:
            if p.get("name") == product_data.get("name") and p.get("category") == product_data.get("category"):
                # If duplicate, raise ValueError so endpoint can return 400
                raise ValueError("Product already exists")

        new_id = self.next_id()
        product = {
            "id": new_id,
            "name": product_data["name"],
            "category": product_data["category"],
            "price": product_data["price"]
        }

        self.db.add_product(product)
        return product
