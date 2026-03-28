from datetime import datetime

class SalesOrder:
    """Represents a sales order."""
    def __init__(self, order_id, customer_id, items, total_amount, status="Pending", date=None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items  # List of {"product_id": id, "quantity": q, "price": p}
        self.total_amount = float(total_amount)
        self.status = status
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "items": self.items,
            "total_amount": self.total_amount,
            "status": self.status,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            order_id=data.get("order_id"),
            customer_id=data.get("customer_id"),
            items=data.get("items"),
            total_amount=data.get("total_amount"),
            status=data.get("status", "Pending"),
            date=data.get("date")
        )
