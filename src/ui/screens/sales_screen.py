import customtkinter as ctk
from tkinter import messagebox, ttk

class SalesScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        self.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(self, text="Sales Management", 
                                         font=("Roboto", 30, "bold"), anchor="w")
        self.header_label.pack(pady=(40, 20), padx=35, anchor="w")

        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=35, pady=10)
        
        self.tab_new = tabview.add("New Order")
        self.tab_history = tabview.add("Order History")
        
        self._setup_new_order_tab()
        self._setup_history_tab()

    def _setup_new_order_tab(self):
        # Customer search by phone
        cust_frame = ctk.CTkFrame(self.tab_new)
        cust_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(cust_frame, text="Customer Phone:").grid(row=0, column=0, padx=10, pady=10)
        self.phone_entry = ctk.CTkEntry(cust_frame, placeholder_text="Enter Phone Number", width=200)
        self.phone_entry.grid(row=0, column=1, padx=10, pady=10)
        self.phone_entry.bind("<KeyRelease>", self._on_phone_change)
        
        self.cust_info_var = ctk.StringVar(value="Searching...")
        self.cust_info_lbl = ctk.CTkLabel(cust_frame, textvariable=self.cust_info_var, text_color="gray70")
        self.cust_info_lbl.grid(row=0, column=2, padx=10, pady=10)

        # Product search
        prod_search_frame = ctk.CTkFrame(self.tab_new)
        prod_search_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(prod_search_frame, text="Product Search:").grid(row=0, column=0, padx=10, pady=10)
        self.prod_search_entry = ctk.CTkEntry(prod_search_frame, placeholder_text="Type product name...", width=300)
        self.prod_search_entry.grid(row=0, column=1, padx=10, pady=10)
        self.prod_search_entry.bind("<KeyRelease>", self._on_prod_search)
        
        self.qty_entry = ctk.CTkEntry(prod_search_frame, placeholder_text="Qty", width=60)
        self.qty_entry.grid(row=0, column=2, padx=10, pady=10)
        
        ctk.CTkButton(prod_search_frame, text="Add Item", command=self._add_to_cart).grid(row=0, column=3, padx=10, pady=10)

        # Product results suggestions
        self.prod_results_frame = ctk.CTkScrollableFrame(self.tab_new, height=100, label_text="Search Results")
        self.prod_results_frame.pack(pady=5, padx=20, fill="x")
        self.selected_prod_id = None

        # Cart Table
        self.cart_items = []
        self.cart_frame = ctk.CTkScrollableFrame(self.tab_new, label_text="Items in Cart")
        self.cart_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.total_lbl = ctk.CTkLabel(self.tab_new, text="Total: $0.00", font=("Roboto", 20, "bold"))
        self.total_lbl.pack(pady=10, padx=20, anchor="e")
        
        ctk.CTkButton(self.tab_new, text="Place Order", fg_color="green", command=self._place_order).pack(pady=20, padx=20, side="right")

    def _on_phone_change(self, event=None):
        phone = self.phone_entry.get()
        if not phone:
            self.cust_info_var.set("")
            return
            
        customer = self.app.customer_manager.get_customer_by_phone(phone)
        if customer:
            self.cust_info_var.set(f"Found: {customer.name}")
        else:
            self.cust_info_var.set("New Customer (will be created)")

    def _on_prod_search(self, event=None):
        query = self.prod_search_entry.get()
        for widget in self.prod_results_frame.winfo_children():
            widget.destroy()
            
        if not query:
            return
            
        results = self.app.product_manager.search_products(query)
        for prod in results[:5]: # Show top 5
            btn = ctk.CTkButton(self.prod_results_frame, text=f"{prod.name} (${prod.price}) - Stock: {prod.quantity}", 
                                fg_color="transparent", text_color=("gray10", "gray90"),
                                anchor="w", command=lambda p=prod: self._select_product(p))
            btn.pack(fill="x", pady=1)

    def _select_product(self, product):
        self.selected_prod_id = product.product_id
        self.prod_search_entry.delete(0, 'end')
        self.prod_search_entry.insert(0, product.name)
        # Clear results
        for widget in self.prod_results_frame.winfo_children():
            widget.destroy()

    def _add_to_cart(self):
        if not self.selected_prod_id:
            messagebox.showerror("Error", "Please select a product from search results")
            return
            
        qty = self.qty_entry.get()
        if not qty or not qty.isdigit():
            messagebox.showerror("Error", "Invalid quantity")
            return
            
        product = self.app.product_manager.products[self.selected_prod_id]
        
        self.cart_items.append({
            "product_id": self.selected_prod_id,
            "name": product.name,
            "quantity": int(qty),
            "price": product.price
        })
        self._refresh_cart()
        # Reset product selection
        self.selected_prod_id = None
        self.prod_search_entry.delete(0, 'end')
        self.qty_entry.delete(0, 'end')

    def _refresh_cart(self):
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        
        total = 0
        for i, item in enumerate(self.cart_items):
            row = ctk.CTkFrame(self.cart_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=item['name'], width=200, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"x{item['quantity']}", width=50).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"${item['price']*item['quantity']:.2f}", width=100).pack(side="left", padx=10)
            ctk.CTkButton(row, text="X", width=30, fg_color="red", command=lambda idx=i: self._remove_from_cart(idx)).pack(side="right", padx=5)
            total += item['price']*item['quantity']
        
        self.total_lbl.configure(text=f"Total: ${total:.2f}")

    def _remove_from_cart(self, index):
        self.cart_items.pop(index)
        self._refresh_cart()

    def _place_order(self):
        phone = self.phone_entry.get()
        if not phone or not self.cart_items:
            messagebox.showerror("Error", "Enter phone and add items")
            return
            
        customer = self.app.customer_manager.get_customer_by_phone(phone)
        if not customer:
            # Auto create customer
            cid = f"CUST-{len(self.app.customer_manager.customers) + 1}"
            name = self.app.customer_manager.get_next_customer_name()
            self.app.customer_manager.add_customer(cid, name, "", phone, "")
            customer = self.app.customer_manager.get_customer_by_phone(phone)
            
        cid = customer.customer_id
        oid = f"ORD-{len(self.app.sales_manager.orders) + 1}"
        
        success, msg = self.app.sales_manager.create_order(oid, cid, self.cart_items)
        if success:
            messagebox.showinfo("Success", f"{msg}\nInvoice INV-{oid} generated.")
            self.cart_items = []
            self.phone_entry.delete(0, 'end')
            self.cust_info_var.set("")
            self._refresh_cart()
            self._refresh_history()
        else:
            messagebox.showerror("Error", msg)

    def _setup_history_tab(self):
        self.hist_frame = ctk.CTkScrollableFrame(self.tab_history)
        self.hist_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self._refresh_history()

    def _refresh_history(self):
        for widget in self.hist_frame.winfo_children():
            widget.destroy()
            
        orders = self.app.sales_manager.get_order_history()
        for order in orders:
            row = ctk.CTkFrame(self.hist_frame)
            row.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(row, text=f"{order.order_id}", width=80, font=("bold", 12)).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"{order.date}", width=150).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=f"${order.total_amount:.2f}", width=100).pack(side="left", padx=10)
            ctk.CTkLabel(row, text=order.status, width=100, text_color="green").pack(side="left", padx=10)
            ctk.CTkButton(row, text="Invoice", width=80, command=lambda o=order.order_id: self._show_invoice(o)).pack(side="right", padx=10)

    def _show_invoice(self, oid):
        inv_id = f"INV-{oid}"
        invoice = self.app.sales_manager.invoices.get(inv_id)
        if invoice:
            messagebox.showinfo("Invoice", f"Invoice ID: {inv_id}\nOrder: {oid}\nTotal: ${invoice.total_amount:.2f}\nDate: {invoice.date}")
        else:
            messagebox.showerror("Error", "Invoice not found")
