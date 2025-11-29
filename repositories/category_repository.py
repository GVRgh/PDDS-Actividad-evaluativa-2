from utils.database_connection import DatabaseConnection

class CategoryRepository:
    def __init__(self, db_path='db.json'):
        self.db = DatabaseConnection(db_path)
        self.db.connect()

    def get_all(self):
        return self.db.get_categories()

    def get_by_id(self, category_id):
        categories = self.db.get_categories()
        return next((c for c in categories if c['id'] == category_id), None)

    def get_next_id(self):
        categories = self.db.get_categories()
        if not categories:
            return 1
        return max(c['id'] for c in categories) + 1

    def exists_by_name(self, name):
        categories = self.db.get_categories()
        return any(c['name'].lower() == name.lower() for c in categories)

    def add(self, name):
        if self.exists_by_name(name):
            raise ValueError("Category already exists")

        new_category = {
            'id': self.get_next_id(),
            'name': name
        }
        self.db.add_category(new_category)
        return new_category

    def remove_by_name(self, name):
        if not self.exists_by_name(name):
            return False
        self.db.remove_category(name)
        return True
