from src.models.product import Product
from src.storage.json_store import JsonStore

class ProductManager:
    """Manages product management logic: add, edit, delete, search, filter."""
    def __init__(self):
        self.store = JsonStore("products")
        self.products = {p['product_id']: Product.from_dict(p) for p in self.store.load()}

    def add_product(self, product_id, name, category, brand, price, quantity, description=""):
        if product_id in self.products:
            return False, "Product ID already exists"
        product = Product(product_id, name, category, brand, price, quantity, description)
        self.products[product_id] = product
        self.save_products()
        return True, "Product added"

    def update_product(self, product_id, **kwargs):
        if product_id in self.products:
            product = self.products[product_id]
            for key, value in kwargs.items():
                if hasattr(product, key):
                   setattr(product, key, value)
            self.save_products()
            return True, "Product updated"
        return False, "Product not found"

    def delete_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            self.save_products()
            return True, "Product deleted"
        return False, "Product not found"

    def search_products(self, query):
        """Search products by name, category, or brand."""
        query = query.lower()
        results = [p for p in self.products.values() if 
                  query in p.name.lower() or 
                  query in p.category.lower() or 
                  query in p.brand.lower()]
        return results

    def filter_products(self, category=None, brand=None):
        results = list(self.products.values())
        if category:
            results = [p for p in results if p.category == category]
        if brand:
            results = [p for p in results if p.brand == brand]
        return results

    def get_summary(self):
        """Returns a summary report of the inventory."""
        total_products = len(self.products)
        total_stock = sum(p.quantity for p in self.products.values())
        total_value = sum(p.price * p.quantity for p in self.products.values())
        
        categories = {}
        for p in self.products.values():
            categories[p.category] = categories.get(p.category, 0) + p.quantity
            
        return {
            "total_products": total_products,
            "total_stock": total_stock,
            "total_value": total_value,
            "top_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True)[:5]
        }

    def save_products(self):
        self.store.save([p.to_dict() for p in self.products.values()])
