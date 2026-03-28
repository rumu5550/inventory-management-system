# src/services/stock_service.py
from datetime import datetime
from . import shared_data
from .database_manager import save_to_json

def update_stock(p_id, amount, mode="change", product_manager=None):
    # 1. First search in the friend's inventory (inventory.json)
    for item in shared_data.inventory:
        if str(item.get("id")) == str(p_id):
            if mode == "set":
                item["qty"] = amount
            else:
                if item["qty"] + amount < 0:
                    return False, "Error: Not enough stock!"
                item["qty"] += amount
            
            save_to_json()
            return True, f"Success! {item['name']} New Qty: {item['qty']}"

    # 2. If not found, search in the main product manager (products.json)
    if product_manager:
        # ProductManager stores products in a dict keyed by product_id
        if p_id in product_manager.products:
            product = product_manager.products[p_id]
            if mode == "set":
                product.quantity = amount
            else:
                if product.quantity + amount < 0:
                    return False, "Error: Not enough stock!"
                product.quantity += amount
            
            product_manager.save_products()
            return True, f"Success! {product.name} New Qty: {product.quantity}"

    return False, f"Product ID '{p_id}' not found in any database"

def get_low_stock_list(product_manager=None):
    low_stock = [p for p in shared_data.inventory if p["qty"] < 5]
    if product_manager:
        low_stock_main = [p.to_dict() for p in product_manager.products.values() if p.quantity < 5]
        # Normalize keys for the UI if needed, but for now we'll just return both
        for p in low_stock_main:
            p['id'] = p.get('product_id')
            p['qty'] = p.get('quantity')
            low_stock.append(p)
    return low_stock

def get_expired_items():
    """Checks which items are past today's date"""
    today = datetime.now().strftime("%Y-%m-%d")
    expired = []
    # Currently only inventory.json has expiry dates
    for item in shared_data.inventory:
        if item.get("expiry") and item["expiry"] < today:
            expired.append(f"• {item['name']} (ID: {item['id']})")
    return expired
