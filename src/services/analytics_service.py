from datetime import datetime, timedelta
import collections

class AnalyticsService:
    """Provides data for reports and charts."""
    def __init__(self, product_manager, sales_manager):
        self.product_manager = product_manager
        self.sales_manager = sales_manager

    def get_inventory_report(self):
        """Data for inventory charts."""
        products = self.product_manager.products.values()
        categories = {}
        for p in products:
            categories[p.category] = categories.get(p.category, 0) + p.quantity
        
        return {
            "categories": list(categories.keys()),
            "stock_levels": list(categories.values())
        }

    def get_sales_report(self):
        """Show sales trend and top selling products."""
        orders = self.sales_manager.get_order_history()
        
        # Sales trend (last 7 days)
        today = datetime.now().date()
        trend_data = {}
        for i in range(7):
            day = today - timedelta(days=i)
            trend_data[day.strftime("%Y-%m-%d")] = 0.0
            
        for order in orders:
            order_date = datetime.strptime(order.date, "%Y-%m-%d %H:%M:%S").date()
            date_str = order_date.strftime("%Y-%m-%d")
            if date_str in trend_data:
                trend_data[date_str] += order.total_amount
                
        sorted_trend = sorted(trend_data.items())
        
        # Top selling products
        product_sales = {}
        for order in orders:
            for item in order.items:
                name = item['name']
                product_sales[name] = product_sales.get(name, 0) + item['quantity']
        
        # Sort and take top 5
        items_list = list(product_sales.items())
        items_list.sort(key=lambda x: x[1], reverse=True)
        top_selling = items_list[:5]
        
        return {
            "dates": [x[0] for x in sorted_trend],
            "amounts": [x[1] for x in sorted_trend],
            "top_products": [x[0] for x in top_selling],
            "top_quantities": [x[1] for x in top_selling]
        }

    def get_purchase_report(self):
        """Mocked purchase trend - to be integrated later."""
        today = datetime.now().date()
        dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        mock_data = [100, 150, 80, 200, 170, 250, 190] # Example trend
        return {
            "dates": dates,
            "amounts": mock_data
        }

    def get_profit_loss(self):
        """Visual summary of profit/loss."""
        orders = self.sales_manager.get_order_history()
        total_revenue = sum(o.total_amount for o in orders)
        
        # Mocking cost of goods sold as 60% of revenue for demonstration
        total_cost = total_revenue * 0.6
        profit = total_revenue - total_cost
        
        return {
            "revenue": total_revenue,
            "cost": total_cost,
            "profit": profit
        }
