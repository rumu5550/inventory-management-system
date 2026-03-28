import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        self.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(self, text="Reports & Analytics", 
                                         font=("Roboto", 30, "bold"), anchor="w")
        self.header_label.pack(pady=(40, 20), padx=35, anchor="w")

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=35, pady=10)
        
        self.tab_sales = tabview.add("Sales Trend")
        self.tab_products = tabview.add("Top Products")
        self.tab_purchase = tabview.add("Purchase Trend")
        self.tab_profit = tabview.add("Profit/Loss")
        
        self._plot_sales_trend()
        self._plot_top_products()
        self._plot_purchase_trend()
        self._plot_profit_loss()

    def _plot_sales_trend(self):
        data = self.app.analytics_service.get_sales_report()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(data['dates'], data['amounts'], marker='o', color='#3498DB')
        ax.set_title("Sales Trend (Last 7 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        self._embed_fig(self.tab_sales, fig)

    def _plot_top_products(self):
        data = self.app.analytics_service.get_sales_report()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(data['top_products'], data['top_quantities'], color='#2ECC71')
        ax.set_title("Top Selling Products")
        ax.set_ylabel("Quantity Sold")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        self._embed_fig(self.tab_products, fig)

    def _plot_purchase_trend(self):
        data = self.app.analytics_service.get_purchase_report()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(data['dates'], data['amounts'], marker='s', color='#F1C40F')
        ax.set_title("Purchase Trend (Wait for teammate's integration)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        self._embed_fig(self.tab_purchase, fig)

    def _plot_profit_loss(self):
        data = self.app.analytics_service.get_profit_loss()
        fig, ax = plt.subplots(figsize=(6, 4))
        labels = ['Revenue', 'Cost', 'Profit']
        values = [data['revenue'], data['cost'], data['profit']]
        colors = ['#3498DB', '#E74C3C', '#2ECC71']
        
        ax.bar(labels, values, color=colors)
        ax.set_title("Profit/Loss Summary")
        ax.set_ylabel("Amount ($)")
        plt.tight_layout()
        
        self._embed_fig(self.tab_profit, fig)

    def _embed_fig(self, master, fig):
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
