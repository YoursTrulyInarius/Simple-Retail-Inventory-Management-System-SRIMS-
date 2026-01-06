from database import Database
import os

def test_database():
    if os.path.exists("test_inventory.db"):
        os.remove("test_inventory.db")
    
    db = Database("test_inventory.db")
    
    # Test Insert
    db.insert_product("Test Item", "Category A", 10, 5.0, "Description")
    products = db.fetch_all_products()
    assert len(products) == 1
    assert products[0].name == "Test Item"
    
    # Test Update
    db.update_product(products[0].id, "Updated Item", "Category B", 20, 10.0, "New Desc")
    products = db.fetch_all_products()
    assert products[0].name == "Updated Item"
    assert products[0].quantity == 20
    
    # Test Search
    results = db.search_products("Updated")
    assert len(results) == 1
    
    # Test Low Stock
    db.insert_product("Low Stock Item", "Category A", 2, 5.0, "Desc")
    low_stock = db.get_low_stock_products(5)
    assert len(low_stock) == 1
    assert low_stock[0].name == "Low Stock Item"
    
    # Test Valuation
    # Item 1: 20 * 10.0 = 200.0
    # Item 2: 2 * 5.0 = 10.0
    # Total: 210.0
    valuation = db.get_total_valuation()
    assert valuation == 210.0
    
    # Test Delete
    db.delete_product(products[0].id)
    products = db.fetch_all_products()
    assert len(products) == 1
    
    print("All database tests passed!")
    db.conn.close()
    os.remove("test_inventory.db")

if __name__ == "__main__":
    test_database()
