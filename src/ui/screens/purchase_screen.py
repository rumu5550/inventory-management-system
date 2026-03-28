import customtkinter as ctk
from src.services import supplier_service
from src.services import purchase_service
from src.services import shared_data

class PurchaseScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        # Main Layout: 2 Columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Content areas
        self._setup_order_panel(0)
        self._setup_supplier_panel(1)

    def _setup_order_panel(self, column):
        panel = ctk.CTkScrollableFrame(self, fg_color="transparent")
        panel.grid(row=0, column=column, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(panel, text="Create Purchase Order", 
                     font=("Roboto", 24, "bold"), anchor="w").pack(pady=(20, 15), anchor="w")

        # Select Supplier
        ctk.CTkLabel(panel, text="Supplier Select", font=("Roboto", 14), text_color="gray70").pack(pady=(10, 5), anchor="w")
        sup_list = supplier_service.get_supplier_names()
        if not sup_list: sup_list = ["No Suppliers Found"]
        self.sup_menu = ctk.CTkOptionMenu(panel, values=sup_list, height=40, width=300, 
                                          fg_color="#34495E", button_color="#2C3E50")
        self.sup_menu.pack(pady=5, anchor="w")

        # Product & Quantity
        self.p_id_entry = ctk.CTkEntry(panel, placeholder_text="Product ID", height=40, width=300)
        self.p_id_entry.pack(pady=10, anchor="w")
        
        self.qty_entry = ctk.CTkEntry(panel, placeholder_text="Quantity", height=40, width=300)
        self.qty_entry.pack(pady=10, anchor="w")

        self.res_label = ctk.CTkLabel(panel, text="", font=("Roboto", 13))
        self.res_label.pack(pady=5, anchor="w")

        ctk.CTkButton(panel, text="Confirm Purchase & Receive",
                      height=45, width=300, corner_radius=10,
                      fg_color="#27AE60", hover_color="#219150",
                      command=self.run_purchase).pack(pady=20, anchor="w")

        # History Preview
        ctk.CTkLabel(panel, text="Recent History Log", font=("Roboto", 18, "bold"), anchor="w").pack(pady=(30, 10), anchor="w")
        self.history_frame = ctk.CTkFrame(panel, corner_radius=15, border_width=1, border_color="gray25")
        self.history_frame.pack(fill="both", expand=True, pady=10)
        self.update_history_preview()

    def _setup_supplier_panel(self, column):
        panel = ctk.CTkScrollableFrame(self, fg_color="transparent")
        panel.grid(row=0, column=column, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(panel, text="Supplier Management", 
                     font=("Roboto", 24, "bold"), anchor="w").pack(pady=(20, 15), anchor="w")

        # Form Card
        form_card = ctk.CTkFrame(panel, corner_radius=15, border_width=1, border_color="gray25")
        form_card.pack(fill="x", pady=10)

        ctk.CTkLabel(form_card, text="Quick Register", font=("Roboto", 16, "bold")).pack(pady=15)
        self.s_name = ctk.CTkEntry(form_card, placeholder_text="Full Name", height=40)
        self.s_name.pack(pady=5, padx=20, fill="x")
        self.s_phone = ctk.CTkEntry(form_card, placeholder_text="Phone", height=40)
        self.s_phone.pack(pady=5, padx=20, fill="x")
        
        ctk.CTkButton(form_card, text="Register Supplier", fg_color="#3498DB",
                      height=40, command=self.add_sup).pack(pady=20, padx=20, fill="x")

        # Edit/Delete List
        ctk.CTkLabel(panel, text="Registered Suppliers", font=("Roboto", 18, "bold"), anchor="w").pack(pady=(20, 10), anchor="w")
        self.edit_menu = ctk.CTkOptionMenu(panel, values=supplier_service.get_supplier_names(), height=40, width=300)
        self.edit_menu.pack(pady=10, anchor="w")

        btn_group = ctk.CTkFrame(panel, fg_color="transparent")
        btn_group.pack(fill="x", pady=10)
        
        ctk.CTkButton(btn_group, text="Edit Selected", fg_color="gray30", height=40, width=140,
                      command=self.edit_sup_dialog).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_group, text="Delete", fg_color="#E74C3C", height=40, width=140,
                      command=self.handle_delete).pack(side="left")

    def run_purchase(self):
        try:
            p_id = self.p_id_entry.get().strip()
            qty = self.qty_entry.get().strip()
            if not p_id or not qty:
                self.res_label.configure(text="Error: Fill all fields!", text_color="#E74C3C")
                return
            success, msg = purchase_service.create_purchase_order(self.sup_menu.get(), p_id, int(qty),
                                                                 product_manager=self.app.product_manager)
            self.res_label.configure(text=msg, text_color="#2ECC71" if success else "#E74C3C")
            if success:
                self.p_id_entry.delete(0, 'end'); self.qty_entry.delete(0, 'end')
                self.update_history_preview()
        except ValueError:
            self.res_label.configure(text="Error: Qty must be a number!", text_color="#E74C3C")

    def add_sup(self):
        success, msg = supplier_service.add_supplier(self.s_name.get(), self.s_phone.get())
        if success:
            self.res_label.configure(text=msg, text_color="#2ECC71")
            new_names = supplier_service.get_supplier_names()
            self.sup_menu.configure(values=new_names)
            self.edit_menu.configure(values=new_names)
            self.s_name.delete(0, 'end'); self.s_phone.delete(0, 'end')
        else:
            self.res_label.configure(text=msg, text_color="#E74C3C")

    def handle_delete(self):
        target = self.edit_menu.get()
        success, msg = supplier_service.delete_supplier(target)
        self.res_label.configure(text=msg, text_color="orange" if success else "red")
        if success:
            new_names = supplier_service.get_supplier_names()
            self.sup_menu.configure(values=new_names)
            self.edit_menu.configure(values=new_names)

    def update_history_preview(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        if not shared_data.purchase_history:
            ctk.CTkLabel(self.history_frame, text="No logs available.", text_color="gray50").pack(pady=20)
            return

        for entry in reversed(shared_data.purchase_history[-5:]):
            row = ctk.CTkFrame(self.history_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=8)
            
            ctk.CTkLabel(row, text=f"{entry['qty']}x ID:{entry['p_id']}", font=("Roboto", 13, "bold"), width=100, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=f"from {entry['supplier']}", font=("Roboto", 12), text_color="gray70", anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=entry['date'], font=("Roboto", 11), text_color="gray50").pack(side="right")
            
            ctk.CTkFrame(self.history_frame, height=1, fg_color="gray30").pack(fill="x", padx=10)

    def edit_sup_dialog(self):
        # Implementation of a simple edit dialog could go here, 
        # but for now we'll stick to the friend's core logic accessibility.
        self.res_label.configure(text="Edit feature active in full screen", text_color="gray70")
