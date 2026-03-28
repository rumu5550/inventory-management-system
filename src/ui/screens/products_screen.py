import customtkinter as ctk
from src.ui.screens.product_dialog import ProductDialog

class ProductsScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=35, pady=(40, 30), sticky="ew")

        self.title_label = ctk.CTkLabel(self.header_frame, text="Inventory Management", 
                                        font=("Roboto", 28, "bold"))
        self.title_label.pack(side="left")

        self.add_button = ctk.CTkButton(self.header_frame, text="+ Add New Product", 
                                        width=180, height=45, corner_radius=10,
                                        fg_color="#27AE60", hover_color="#219150", 
                                        font=("Roboto", 14, "bold"),
                                        command=self._add_product_dialog)
        self.add_button.pack(side="right", padx=(20, 0))

        self.search_entry = ctk.CTkEntry(self.header_frame, placeholder_text="Search inventory by name, category, or brand...", 
                                           width=380, height=45, corner_radius=10, border_width=1)
        self.search_entry.pack(side="right")
        self.search_entry.bind("<KeyRelease>", self._on_search)

        self.table_container = ctk.CTkFrame(self, fg_color="transparent")
        self.table_container.grid(row=1, column=0, padx=35, pady=(0, 35), sticky="nsew")
        self.table_container.grid_columnconfigure(0, weight=1)
        self.table_container.grid_rowconfigure(0, weight=1)

        self.table_frame = ctk.CTkScrollableFrame(self.table_container, label_text="Live Stock Inventory", 
                                                  label_font=("Roboto", 16, "bold"), label_anchor="w",
                                                  corner_radius=15, border_width=1, border_color="gray25")
        self.table_frame.grid(row=0, column=0, sticky="nsew")

        self._refresh_table()

    def _refresh_table(self, products=None):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        if products is None:
            products = self.app.product_manager.products.values()

        headers = ["ID", "Name", "Category", "Price", "Quantity", "Actions"]
        for col, text in enumerate(headers):
            lbl = ctk.CTkLabel(self.table_frame, text=text.upper(), 
                                font=("Roboto", 12, "bold"), text_color="gray60")
            lbl.grid(row=0, column=col, padx=15, pady=15, sticky="w")

        for row, product in enumerate(products, start=1):
            ctk.CTkLabel(self.table_frame, text=product.product_id, font=("Roboto", 13)).grid(row=row, column=0, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.table_frame, text=product.name, font=("Roboto", 14, "bold")).grid(row=row, column=1, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.table_frame, text=product.category, font=("Roboto", 13)).grid(row=row, column=2, padx=15, pady=10, sticky="w")
            ctk.CTkLabel(self.table_frame, text=f"${product.price:.2f}", font=("Roboto", 14, "bold"), text_color="#F1C40F").grid(row=row, column=3, padx=15, pady=10, sticky="w")
            
            qty_color = "#E74C3C" if product.quantity < 10 else "gray90"
            ctk.CTkLabel(self.table_frame, text=str(product.quantity), font=("Roboto", 14), text_color=qty_color).grid(row=row, column=4, padx=15, pady=10, sticky="w")
            
            action_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
            action_frame.grid(row=row, column=5, padx=10, pady=10)
            
            ctk.CTkButton(action_frame, text="✏️ Edit", width=70, height=35, corner_radius=8,
                          fg_color="#3498DB", hover_color="#2980B9", 
                          command=lambda p=product: self._edit_product(p)).pack(side="left", padx=5)
            ctk.CTkButton(action_frame, text="🗑️ Delete", width=70, height=35, corner_radius=8, fg_color="#E74C3C", hover_color="#C0392B", 
                          command=lambda pid=product.product_id: self._delete_product(pid)).pack(side="left", padx=5)

    def _on_search(self, event=None):
        query = self.search_entry.get()
        results = self.app.product_manager.search_products(query)
        self._refresh_table(results)

    def _add_product_dialog(self):
        """Opens a dialog to add a new product manually."""
        ProductDialog(self.winfo_toplevel(), self.app, on_save=self._refresh_table)

    def _edit_product(self, product):
        """Opens a dialog to edit an existing product."""
        ProductDialog(self.winfo_toplevel(), self.app, product=product, on_save=self._refresh_table)

    def _delete_product(self, product_id):
        if self.app.product_manager.delete_product(product_id):
            self._refresh_table()
