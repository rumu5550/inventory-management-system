# src/services/database_manager.py
import json
import os
from . import shared_data

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FILE = os.path.join(BASE_DIR, "data", "inventory.json")

def save_to_json():
    data = {
        "inventory": shared_data.inventory,
        "suppliers": shared_data.suppliers,
        "purchase_history": shared_data.purchase_history
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4) 

def load_from_json():
    if not os.path.exists(DATA_FILE):
        print(f"DEBUG: Data file NOT FOUND at: {DATA_FILE}")
        shared_data.inventory = []
        shared_data.suppliers = []
        shared_data.purchase_history = []
        return

    try:
        with open(DATA_FILE, "r") as f:
            content = json.load(f)
           
            shared_data.inventory = content.get("inventory", [])
            shared_data.suppliers = content.get("suppliers", [])
            shared_data.purchase_history = content.get("purchase_history", [])
            print(f"DEBUG: Loaded {len(shared_data.inventory)} products from {DATA_FILE}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"DEBUG: Error loading data: {e}")
        shared_data.inventory = []
        shared_data.suppliers = []
        shared_data.purchase_history = []
