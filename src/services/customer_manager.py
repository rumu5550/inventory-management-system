from src.models.customer import Customer
from src.storage.json_store import JsonStore

class CustomerManager:
    """Manages customer data."""
    def __init__(self):
        self.store = JsonStore("customers")
        self.customers = {c['customer_id']: Customer.from_dict(c) for c in self.store.load()}

    def add_customer(self, customer_id, name, email, phone, address):
        if customer_id in self.customers:
            return False, "Customer ID already exists"
        customer = Customer(customer_id, name, email, phone, address)
        self.customers[customer_id] = customer
        self.save_customers()
        return True, "Customer added"

    def update_customer(self, customer_id, **kwargs):
        if customer_id in self.customers:
            customer = self.customers[customer_id]
            for key, value in kwargs.items():
                if hasattr(customer, key):
                    setattr(customer, key, value)
            self.save_customers()
            return True, "Customer updated"
        return False, "Customer not found"

    def delete_customer(self, customer_id):
        if customer_id in self.customers:
            del self.customers[customer_id]
            self.save_customers()
            return True, "Customer deleted"
        return False, "Customer not found"

    def get_all_customers(self):
        return list(self.customers.values())

    def get_customer_by_phone(self, phone):
        """Finds a customer by their phone number."""
        for cust in self.customers.values():
            if cust.phone == phone:
                return cust
        return None

    def get_next_customer_name(self):
        """Generates the next 'Customer-N' name."""
        count = 1
        while True:
            name = f"Customer-{count}"
            # Check if this name already exists
            exists = any(c.name == name for c in self.customers.values())
            if not exists:
                return name
            count += 1

    def save_customers(self):
        self.store.save([c.to_dict() for c in self.customers.values()])
