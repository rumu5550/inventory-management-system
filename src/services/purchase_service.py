# src/services/purchase_service.py
from datetime import datetime
from . import shared_data
from .stock_service import update_stock
from . import database_manager

def create_purchase_order(sup_name, product_id, qty, product_manager=None):
    """
    Handles the entire purchase process: 
    1. Updates Inventory (Supports both bridge databases)
    2. Logs History 
    3. Saves to File
    """
    # Update the Stock through the bridged service
    success, msg = update_stock(product_id, int(qty), product_manager=product_manager)
    
    if success:
        # We'll log the purchase history in the friend's history file for consistency
        order = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "supplier": sup_name,
            "p_id": product_id,
            "qty": int(qty),
            "status": "Received"
        }
        
        shared_data.purchase_history.append(order)
        database_manager.save_to_json()
        
        return True, f"Success! Added {qty} units to {product_id}."
    
    return False, msg
