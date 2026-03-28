class Customer:
    """Represents a customer in the system."""
    def __init__(self, customer_id, name, email, phone, address):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            customer_id=data.get("customer_id"),
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address")
        )
