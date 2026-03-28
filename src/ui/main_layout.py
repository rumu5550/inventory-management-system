import customtkinter as ctk

class MainLayout(ctk.CTkFrame):
    """A layout that provides a persistent sidebar and a content area."""
    def __init__(self, master, app_controller):
        super().__init__(master)
        self.app = app_controller

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="IMS Admin", font=("Roboto", 26, "bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(35, 45))

        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="  📊 Dashboard", 
                                           height=45, corner_radius=10,
                                           fg_color="transparent", text_color=("gray10", "gray90"), 
                                           hover_color=("gray70", "gray30"), anchor="w", 
                                           command=lambda: self.app.show_dashboard())
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=12, sticky="ew")

        self.btn_products = ctk.CTkButton(self.sidebar_frame, text="  📦 Inventory List", 
                                          height=45, corner_radius=10,
                                          fg_color="transparent", text_color=("gray10", "gray90"), 
                                          hover_color=("gray70", "gray30"), anchor="w", 
                                          command=lambda: self.app.show_products())
        self.btn_products.grid(row=2, column=0, padx=20, pady=12, sticky="ew")

        self.btn_customers = ctk.CTkButton(self.sidebar_frame, text="  👥 Customers", 
                                           height=45, corner_radius=10,
                                           fg_color="transparent", text_color=("gray10", "gray90"), 
                                           hover_color=("gray70", "gray30"), anchor="w", 
                                           command=lambda: self.app.show_customers())
        self.btn_customers.grid(row=3, column=0, padx=20, pady=12, sticky="ew")

        self.btn_sales = ctk.CTkButton(self.sidebar_frame, text="  💰 Sales Orders", 
                                       height=45, corner_radius=10,
                                       fg_color="transparent", text_color=("gray10", "gray90"), 
                                       hover_color=("gray70", "gray30"), anchor="w", 
                                       command=lambda: self.app.show_sales())
        self.btn_sales.grid(row=4, column=0, padx=20, pady=12, sticky="ew")

        self.btn_reports = ctk.CTkButton(self.sidebar_frame, text="  📈 Reports", 
                                         height=45, corner_radius=10,
                                         fg_color="transparent", text_color=("gray10", "gray90"), 
                                         hover_color=("gray70", "gray30"), anchor="w", 
                                         command=lambda: self.app.show_reports())
        self.btn_reports.grid(row=5, column=0, padx=20, pady=12, sticky="ew")

        self.btn_stock = ctk.CTkButton(self.sidebar_frame, text="  📦 Stock Control", 
                                       height=45, corner_radius=10,
                                       fg_color="transparent", text_color=("gray10", "gray90"), 
                                       hover_color=("gray70", "gray30"), anchor="w", 
                                       command=lambda: self.app.show_stock())
        self.btn_stock.grid(row=6, column=0, padx=20, pady=12, sticky="ew")

        self.btn_purchases = ctk.CTkButton(self.sidebar_frame, text="  🛒 Purchases", 
                                           height=45, corner_radius=10,
                                           fg_color="transparent", text_color=("gray10", "gray90"), 
                                           hover_color=("gray70", "gray30"), anchor="w", 
                                           command=lambda: self.app.show_purchases())
        self.btn_purchases.grid(row=7, column=0, padx=20, pady=12, sticky="ew")

        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="  🚪 Logout", 
                                        height=45, corner_radius=10,
                                        fg_color="transparent", text_color="#E74C3C", 
                                        hover_color=("gray70", "gray30"), anchor="w", 
                                        command=lambda: self.app.on_logout())
        self.btn_logout.grid(row=9, column=0, padx=20, pady=40, sticky="ew")

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

    def show_content(self, screen_class):
        """Displays a screen inside the content area."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        screen = screen_class(self.content_frame, self.app)
        screen.pack(fill="both", expand=True)
