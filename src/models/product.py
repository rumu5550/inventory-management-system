class Product:
    """Represents a product item in the inventory."""
    def __init__(self, product_id, name, category, brand, price, quantity, description=""):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.brand = brand
        self.price = float(price)
        self.quantity = int(quantity)
        self.description = description

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "price": self.price,
            "quantity": self.quantity,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data.get("product_id"),
            name=data.get("name"),
            category=data.get("category"),
            brand=data.get("brand"),
            price=data.get("price"),
            quantity=data.get("quantity"),
            description=data.get("description", "")
        )
