import customtkinter as ctk

class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        self.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(self, text=f"Dashboard Overview", 
                                         font=("Roboto", 30, "bold"), anchor="w")
        self.header_label.pack(pady=(40, 10), padx=35, anchor="w")

        self.welcome_label = ctk.CTkLabel(self, text=f"Welcome back, {self.app.current_user.username}!", 
                                          font=("Roboto", 16), text_color="gray70", anchor="w")
        self.welcome_label.pack(pady=(0, 50), padx=35, anchor="w")

        self._load_stats()

    def _load_stats(self):
        summary = self.app.product_manager.get_summary()

        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(pady=10, padx=25, fill="x")

        self._create_stat_card(stats_frame, "Total Items", str(summary['total_products']), 0, "#3498DB")
        self._create_stat_card(stats_frame, "Total Stock", str(summary['total_stock']), 1, "#2ECC71")
        self._create_stat_card(stats_frame, "Inventory Value", f"${summary['total_value']:.2f}", 2, "#F1C40F")

    def _create_stat_card(self, master, label_text, value_text, column, accent_color):
        card = ctk.CTkFrame(master, width=280, height=180, corner_radius=15, border_width=1, border_color="gray25")
        card.grid(row=0, column=column, padx=20, pady=15)
        card.grid_propagate(False)
        
        lbl = ctk.CTkLabel(card, text=label_text, font=("Roboto", 16, "bold"), text_color="gray75")
        lbl.pack(pady=(45, 10), padx=20)
        
        val = ctk.CTkLabel(card, text=value_text, font=("Roboto", 32, "bold"), text_color=accent_color)
        val.pack(pady=(0, 45), padx=20)
