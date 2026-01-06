import sqlite3
from models import Product

class Database:
    def __init__(self, db_file="inventory.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                quantity INTEGER DEFAULT 0,
                price REAL DEFAULT 0.0,
                description TEXT
            )
        """)
        self.conn.commit()

    def insert_product(self, name, category, quantity, price, description):
        self.cursor.execute("INSERT INTO products (name, category, quantity, price, description) VALUES (?, ?, ?, ?, ?)",
                            (name, category, quantity, price, description))
        self.conn.commit()

    def fetch_all_products(self):
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()
        return [Product(*row) for row in rows]

    def update_product(self, id, name, category, quantity, price, description):
        self.cursor.execute("UPDATE products SET name=?, category=?, quantity=?, price=?, description=? WHERE id=?",
                            (name, category, quantity, price, description, id))
        self.conn.commit()

    def delete_product(self, id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (id,))
        self.conn.commit()

    def search_products(self, query):
        self.cursor.execute("SELECT * FROM products WHERE name LIKE ? OR category LIKE ?", ('%' + query + '%', '%' + query + '%'))
        rows = self.cursor.fetchall()
        return [Product(*row) for row in rows]
        
    def get_total_valuation(self):
        self.cursor.execute("SELECT SUM(quantity * price) FROM products")
        result = self.cursor.fetchone()[0]
        return result if result else 0.0

    def get_low_stock_products(self, threshold=5):
        self.cursor.execute("SELECT * FROM products WHERE quantity < ?", (threshold,))
        rows = self.cursor.fetchall()
        return [Product(*row) for row in rows]

    def __del__(self):
        self.conn.close()
