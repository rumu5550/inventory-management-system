from src.models.sales_order import SalesOrder
from src.models.invoice import Invoice
from src.storage.json_store import JsonStore
from datetime import datetime

class SalesManager:
    """Manages sales orders and invoice generation."""
    def __init__(self, product_manager):
        self.product_manager = product_manager
        self.order_store = JsonStore("sales_orders")
        self.invoice_store = JsonStore("invoices")
        
        self.orders = {o['order_id']: SalesOrder.from_dict(o) for o in self.order_store.load()}
        self.invoices = {i['invoice_id']: Invoice.from_dict(i) for i in self.invoice_store.load()}

    def create_order(self, order_id, customer_id, items):
        """
        items: list of {"product_id": id, "quantity": q}
        """
        if order_id in self.orders:
            return False, "Order ID already exists"

        total_amount = 0
        order_items = []
        
        for item in items:
            pid = item['product_id']
            qty = int(item['quantity'])
            
            if pid not in self.product_manager.products:
                return False, f"Product {pid} not found"
            
            product = self.product_manager.products[pid]
            if product.quantity < qty:
                return False, f"Insufficient stock for {product.name}"
            
            price = product.price
            total_amount += price * qty
            order_items.append({
                "product_id": pid,
                "name": product.name,
                "quantity": qty,
                "price": price
            })

        order = SalesOrder(order_id, customer_id, order_items, total_amount, status="Completed")
        
        # Deduct stock
        for item in items:
            self.product_manager.update_product(item['product_id'], 
                                              quantity=self.product_manager.products[item['product_id']].quantity - int(item['quantity']))
        
        self.orders[order_id] = order
        self.save_orders()
        
        # Generate Invoice
        invoice_id = f"INV-{order_id}"
        self.generate_invoice(invoice_id, order_id, total_amount)
        
        return True, f"Order {order_id} created and completed"

    def generate_invoice(self, invoice_id, order_id, total_amount):
        invoice = Invoice(invoice_id, order_id, total_amount)
        self.invoices[invoice_id] = invoice
        self.save_invoices()
        return invoice

    def get_order_history(self):
        return sorted(self.orders.values(), key=lambda x: x.date, reverse=True)

    def save_orders(self):
        self.order_store.save([o.to_dict() for o in self.orders.values()])

    def save_invoices(self):
        self.invoice_store.save([i.to_dict() for i in self.invoices.values()])
