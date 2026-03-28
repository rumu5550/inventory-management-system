import customtkinter as ctk
from src.services import stock_service

class StockScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        # Header
        self.header_label = ctk.CTkLabel(self, text="Stock Control Center", 
                                         font=("Roboto", 30, "bold"), anchor="w")
        self.header_label.pack(pady=(40, 20), padx=35, anchor="w")

        # Main Scrollable Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=25, pady=10)

        # --- Quick Stats Cards ---
        stats_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=10)
        
        # We can reuse the stat card logic but inline for simplicity here
        self._create_action_card(stats_frame)
        self._create_status_card(stats_frame)

    def _create_action_card(self, master):
        card = ctk.CTkFrame(master, corner_radius=15, border_width=1, border_color="gray25")
        card.pack(side="left", padx=10, fill="both", expand=True)

        ctk.CTkLabel(card, text="Update Inventory Levels", 
                     font=("Roboto", 18, "bold")).pack(pady=(20, 15), padx=20)

        self.id_entry = ctk.CTkEntry(card, placeholder_text="Product ID / Batch", 
                                     height=40, width=220)
        self.id_entry.pack(pady=5, padx=20)

        self.amt_entry = ctk.CTkEntry(card, placeholder_text="Amount (e.g. 10 or -5)", 
                                      height=40, width=220)
        self.amt_entry.pack(pady=5, padx=20)

        update_btn = ctk.CTkButton(card, text="Apply Changes", 
                                   height=40, corner_radius=10,
                                   fg_color="#3498DB", hover_color="#2980B9",
                                   command=self.handle_update)
        update_btn.pack(pady=(15, 20), padx=20, fill="x")

    def _create_status_card(self, master):
        card = ctk.CTkFrame(master, corner_radius=15, border_width=1, border_color="gray25")
        card.pack(side="left", padx=10, fill="both", expand=True)

        ctk.CTkLabel(card, text="Management Actions", 
                     font=("Roboto", 18, "bold")).pack(pady=(20, 15), padx=20)

        ctk.CTkButton(card, text="Check Expiry Dates", 
                      height=40, corner_radius=10,
                      fg_color="#E74C3C", hover_color="#C0392B",
                      command=self.check_expiry_ui).pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(card, text="Low Stock Alerts", 
                      height=40, corner_radius=10,
                      fg_color="#F39C12", hover_color="#D35400",
                      command=self.check_low_stock_ui).pack(pady=5, padx=20, fill="x")

        self.result_label = ctk.CTkLabel(card, text="Ready", font=("Roboto", 13), text_color="gray60")
        self.result_label.pack(pady=(10, 20), padx=20)

    def handle_update(self):
        p_id = self.id_entry.get().strip()
        try:
            amt = int(self.amt_entry.get().strip())
            success, message = stock_service.update_stock(p_id, amt, 
                                                          product_manager=self.app.product_manager)
            self.result_label.configure(text=message, 
                                        text_color="#2ECC71" if success else "#E74C3C")
        except ValueError:
            self.result_label.configure(text="Enter a valid number!", text_color="#E74C3C")

    def check_expiry_ui(self):
        expired_list = stock_service.get_expired_items()
        if expired_list:
            msg = "EXPIRED ITEMS:\n" + "\n".join(expired_list)
            self.result_label.configure(text=msg, text_color="#E74C3C")
        else:
            self.result_label.configure(text="No expired items!", text_color="#2ECC71")

    def check_low_stock_ui(self):
        low_items = stock_service.get_low_stock_list(product_manager=self.app.product_manager)
        if low_items:
            names = [f"• {i['name']} ({i['qty']} left)" for i in low_items]
            msg = "LOW STOCK ALERTS:\n" + "\n".join(names)
            self.result_label.configure(text=msg, text_color="#F39C12")
        else:
            self.result_label.configure(text="Stock levels healthy!", text_color="#2ECC71")
