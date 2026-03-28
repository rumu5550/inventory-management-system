from datetime import datetime

class Invoice:
    """Represents an invoice for a sales order."""
    def __init__(self, invoice_id, order_id, total_amount, date=None):
        self.invoice_id = invoice_id
        self.order_id = order_id
        self.total_amount = float(total_amount)
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "invoice_id": self.invoice_id,
            "order_id": self.order_id,
            "total_amount": self.total_amount,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            invoice_id=data.get("invoice_id"),
            order_id=data.get("order_id"),
            total_amount=data.get("total_amount"),
            date=data.get("date")
        )
