# src/services/supplier_service.py
import re
from . import shared_data
from . import database_manager

def validate_supplier(name, phone, email, address):
    """Full validation for all supplier fields."""
    if not name.strip() or not phone.strip():
        return False, "Name and Phone cannot be empty!"

    if not name.replace(" ", "").isalpha():
        return False, "Name must contain letters only!"
    
    if not phone.isdigit():
        return False, "Phone must contain numbers only!"

    email = email.strip()
    if email and email.lower() != "n/a" and email != "":
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            return False, "Invalid Email format! (e.g., user@mail.com)"

    address = address.strip()
    if address and address.lower() != "n/a" and address != "":
        if len(address) < 5:
            return False, "Address is too short (min 5 chars)!"
        
    return True, None

def add_supplier(name, phone, email="N/A", address="N/A"):
    name = name.strip()
    phone = phone.strip()

    # VALIDATION RULES
    if not name or not phone:
        return False, "Error: Name and Phone are required!"
    
    if not name.replace(" ", "").isalpha():
        return False, "Error: Name must contain only letters!"
    
    if not phone.isdigit():
        return False, "Error: Phone must contain only numbers!"

    new_sup = {"name": name, "phone": phone, "email": email, "address": address}
    shared_data.suppliers.append(new_sup)
    
    database_manager.save_to_json() 
    return True, f"Success: {name} registered!"

def get_supplier_names():
    names = [s["name"] for s in shared_data.suppliers]
    return names if names else []

def update_supplier(old_name, new_name, new_phone, new_email, new_address):
    success, error_msg = validate_supplier(new_name, new_phone, new_email, new_address)
    if not success:
        return False, error_msg
    
    for s in shared_data.suppliers:
        if s["name"] == old_name:
            s["name"] = new_name.strip()
            s["phone"] = new_phone.strip()
            s["email"] = new_email.strip() if new_email.strip() else "N/A"
            s["address"] = new_address.strip() if new_address.strip() else "N/A"
            database_manager.save_to_json()
            return True, f"Supplier '{s['name']}' updated!"
           
    return False, "Supplier not found."

def delete_supplier(name):
    """Removes a supplier from the list based on their name."""
    initial_count = len(shared_data.suppliers)
    shared_data.suppliers = [s for s in shared_data.suppliers if s["name"] != name]
    
    if len(shared_data.suppliers) < initial_count:
        database_manager.save_to_json()
        return True, f"Supplier '{name}' deleted."
    return False, "Supplier not found."

def get_supplier_details(name):
    for s in shared_data.suppliers:
        if s["name"] == name:
            return s
    return None
