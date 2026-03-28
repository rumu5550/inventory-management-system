import customtkinter as ctk
import sys
from src.services.auth_service import AuthService
from src.services.product_manager import ProductManager
from src.services.customer_manager import CustomerManager
from src.services.sales_manager import SalesManager
from src.services.analytics_service import AnalyticsService

from src.ui.screens.login_screen import LoginScreen
from src.ui.main_layout import MainLayout
from src.ui.screens.dashboard_screen import DashboardScreen
from src.ui.screens.products_screen import ProductsScreen
from src.ui.screens.customer_screen import CustomerScreen
from src.ui.screens.sales_screen import SalesScreen
from src.ui.screens.report_screen import ReportScreen

class InventoryApp(ctk.CTk):
    """Main application controller for the Inventory Management System."""
    def __init__(self):
        super().__init__()

        self.title("Inventory Management System")
        self.window_width = 1200
        self.window_height = 800
        
        self.after(10, self._center_window)
        self.state('zoomed')
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.auth_service = AuthService()
        self.product_manager = ProductManager()
        self.customer_manager = CustomerManager()
        self.sales_manager = SalesManager(self.product_manager)
        self.analytics_service = AnalyticsService(self.product_manager, self.sales_manager)

        self.current_user = None
        self.current_screen = None
        self.main_layout = None

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.show_login()

    def on_closing(self):
        """Gracefully closes the application."""
        self.destroy()
        sys.exit(0)

    def _center_window(self):
        """Calculates and sets the window position to the center of the screen."""
        self.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (self.window_width // 2)
        y = (screen_height // 2) - (self.window_height // 2)
        
        # Final geometry setting
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

    def show_login(self):
        """Shows the standalone login screen."""
        self.clear_main_layout()
        self.switch_screen(LoginScreen)

    def on_login_success(self, user):
        """Called when login is successful."""
        self.current_user = user
        self.setup_main_layout()
        self.show_dashboard()

    def setup_main_layout(self):
        """Initializes the persistent sidebar layout."""
        if self.current_screen:
            self.current_screen.pack_forget()
            self.current_screen.destroy()
            
        self.main_layout = MainLayout(self, self)
        self.main_layout.pack(fill="both", expand=True)

    def show_dashboard(self):
        """Shows the dashboard within the persistent layout."""
        if self.main_layout:
            self.main_layout.show_content(DashboardScreen)

    def show_products(self):
        """Shows the product list within the persistent layout."""
        if self.main_layout:
            self.main_layout.show_content(ProductsScreen)

    def show_customers(self):
        """Shows the customer management screen."""
        if self.main_layout:
            self.main_layout.show_content(CustomerScreen)

    def show_sales(self):
        """Shows the sales management screen."""
        if self.main_layout:
            self.main_layout.show_content(SalesScreen)

    def show_reports(self):
        """Shows the reports and analytics screen."""
        if self.main_layout:
            self.main_layout.show_content(ReportScreen)

    def on_logout(self):
        """Handles logout: clears layout and returns to login."""
        self.current_user = None
        self.show_login()

    def clear_main_layout(self):
        """Clears the persistent main layout if it exists."""
        if self.main_layout and self.main_layout.winfo_exists():
            self.main_layout.pack_forget()
            self.main_layout.destroy()
        self.main_layout = None

    def switch_screen(self, screen_class):
        """Switches standalone screens (like Login)."""
        if self.current_screen and self.current_screen.winfo_exists():
            self.current_screen.pack_forget()
            self.current_screen.destroy()
            
        self.current_screen = screen_class(self, self)
        self.current_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
