import customtkinter as ctk
from tkinter import messagebox

class CustomerScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        self.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(self, text="Customer Management", 
                                         font=("Roboto", 30, "bold"), anchor="w")
        self.header_label.pack(pady=(40, 20), padx=35, anchor="w")

        # Form to add customer
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(pady=10, padx=35, fill="x")
        
        self.name_entry = self._create_input(form_frame, "Name", 0)
        self.email_entry = self._create_input(form_frame, "Email", 1)
        self.phone_entry = self._create_input(form_frame, "Phone", 2)
        self.addr_entry = self._create_input(form_frame, "Address", 3)
        
        self.add_btn = ctk.CTkButton(form_frame, text="Add Customer", command=self._add_customer)
        self.add_btn.grid(row=0, column=4, padx=10, pady=20)

        # List of customers
        self.list_frame = ctk.CTkScrollableFrame(self, label_text="Customer List")
        self.list_frame.pack(pady=20, padx=35, fill="both", expand=True)

        self._refresh_list()

    def _create_input(self, master, placeholder, col):
        entry = ctk.CTkEntry(master, placeholder_text=placeholder, width=150)
        entry.grid(row=0, column=col, padx=10, pady=20)
        return entry

    def _add_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        addr = self.addr_entry.get()
        
        if not name or not email:
            messagebox.showerror("Error", "Name and Email are required")
            return
            
        cid = f"CUST-{len(self.app.customer_manager.customers) + 1}"
        success, msg = self.app.customer_manager.add_customer(cid, name, email, phone, addr)
        
        if success:
            messagebox.showinfo("Success", msg)
            self._refresh_list()
            self.name_entry.delete(0, 'end')
            self.email_entry.delete(0, 'end')
            self.phone_entry.delete(0, 'end')
            self.addr_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", msg)

    def _refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        customers = self.app.customer_manager.get_all_customers()
        for i, cust in enumerate(customers):
            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{cust.name} ({cust.email})", width=300, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(row, text=cust.phone, width=150).pack(side="left", padx=10)
            ctk.CTkButton(row, text="Delete", width=60, fg_color="red", 
                          command=lambda c=cust.customer_id: self._delete_customer(c)).pack(side="right", padx=10)

    def _delete_customer(self, cid):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?"):
            self.app.customer_manager.delete_customer(cid)
            self._refresh_list()
