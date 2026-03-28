import customtkinter as ctk

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, app_controller):
        super().__init__(master, fg_color="transparent")
        self.app = app_controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.login_box = ctk.CTkFrame(self, width=420, height=500, corner_radius=20)
        self.login_box.grid(row=1, column=1, padx=40, pady=40)
        self.login_box.grid_propagate(False)

        self.title = ctk.CTkLabel(self.login_box, text="IMS Login", font=("Roboto", 32, "bold"))
        self.title.pack(pady=(50, 40))

        self.username_entry = ctk.CTkEntry(self.login_box, placeholder_text="Username", 
                                           width=320, height=50, corner_radius=10)
        self.username_entry.pack(pady=12, padx=50)

        self.password_entry = ctk.CTkEntry(self.login_box, placeholder_text="Password", 
                                           width=320, height=50, corner_radius=10, show="*")
        self.password_entry.pack(pady=12, padx=50)

        self.login_button = ctk.CTkButton(self.login_box, text="Sign In", 
                                          width=320, height=50, corner_radius=10,
                                          font=("Roboto", 16, "bold"),
                                          command=self._login_event)
        self.login_button.pack(pady=(35, 10), padx=50)

        self.error_label = ctk.CTkLabel(self.login_box, text="", text_color="#E74C3C", font=("Roboto", 13))
        self.error_label.pack(pady=5)

        self.footer_label = ctk.CTkLabel(self.login_box, text="© 2026 Inventory Management System", 
                                         font=("Roboto", 11), text_color="gray")
        self.footer_label.pack(side="bottom", pady=25)

    def _login_event(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.error_label.configure(text="Please fill in all fields")
            return

        success, result = self.app.auth_service.login(username, password)
        if success:
            self.app.on_login_success(result)
        else:
            self.error_label.configure(text=f"Authentication Error: {result}")
