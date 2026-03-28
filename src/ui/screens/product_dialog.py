import customtkinter as ctk

class ProductDialog(ctk.CTkToplevel):
    """A modal dialog for adding or editing a product."""
    def __init__(self, master, app_controller, product=None, on_save=None):
        super().__init__(master)
        self.app = app_controller
        self.product = product
        self.on_save = on_save

        self.title("Edit Product" if product else "Add New Product")
        self.geometry("700x520")
        self.resizable(False, False)
        
        self.grab_set()
        self.focus_set()

        # Main Container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=30, pady=25)

        # Title
        self.title_label = ctk.CTkLabel(self.container, text="Product Details", font=("Roboto", 24, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Grid Configuration for Inputs
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # Row 1: ID and Name
        self.id_entry = self._create_field("Product ID (Unique)", 1, 0, product.product_id if product else "")
        if product: self.id_entry.configure(state="disabled")
        self.name_entry = self._create_field("Product Name", 1, 1, product.name if product else "")

        # Row 2: Category and Brand
        self.category_entry = self._create_field("Category", 2, 0, product.category if product else "")
        self.brand_entry = self._create_field("Brand", 2, 1, product.brand if product else "")

        # Row 3: Price and Quantity
        self.price_entry = self._create_field("Price ($)", 3, 0, str(product.price) if product else "")
        self.qty_entry = self._create_field("Quantity in Stock", 3, 1, str(product.quantity) if product else "")

        # Error Label
        self.error_label = ctk.CTkLabel(self.container, text="", text_color="#E74C3C", font=("Roboto", 13))
        self.error_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Buttons Frame
        self.btn_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.btn_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)

        self.save_button = ctk.CTkButton(self.btn_frame, text="Save Product", height=45, corner_radius=10,
                                         fg_color="#27AE60", hover_color="#219150", 
                                         font=("Roboto", 14, "bold"),
                                         command=self._save_event)
        self.save_button.grid(row=0, column=0, padx=10, sticky="ew")

        self.cancel_button = ctk.CTkButton(self.btn_frame, text="Cancel", height=45, corner_radius=10,
                                           fg_color="gray30", hover_color="gray20",
                                           font=("Roboto", 14, "bold"),
                                           command=self.destroy)
        self.cancel_button.grid(row=0, column=1, padx=10, sticky="ew")

    def _create_field(self, label_text, row, col, default_value):
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.grid(row=row, column=col, padx=15, pady=10, sticky="nsew")
        
        lbl = ctk.CTkLabel(frame, text=label_text, font=("Roboto", 13, "bold"), anchor="w")
        lbl.pack(fill="x", pady=(0, 5))
        
        entry = ctk.CTkEntry(frame, height=40, corner_radius=8)
        entry.insert(0, default_value)
        entry.pack(fill="x")
        return entry

    def _save_event(self):
        try:
            pid = self.id_entry.get().strip()
            name = self.name_entry.get().strip()
            category = self.category_entry.get().strip()
            brand = self.brand_entry.get().strip()
            price_str = self.price_entry.get().strip()
            qty_str = self.qty_entry.get().strip()

            # Validation
            if not all([pid, name, category, brand, price_str, qty_str]):
                raise ValueError("All fields are required")

            price = float(price_str)
            quantity = int(qty_str)

            if price < 0 or quantity < 0:
                raise ValueError("Price and Quantity must be positive")

            # Logic: Add or Update
            if self.product:
                success, message = self.app.product_manager.update_product(
                    pid, name=name, category=category, brand=brand, price=price, quantity=quantity
                )
            else:
                success, message = self.app.product_manager.add_product(
                    pid, name, category, brand, price, quantity
                )

            if success:
                if self.on_save: self.on_save()
                self.destroy()
            else:
                self.error_label.configure(text=f"Error: {message}")

        except ValueError as e:
            self.error_label.configure(text=f"Validation: {str(e)}")
        except Exception as e:
            self.error_label.configure(text=f"System Error: {str(e)}")
