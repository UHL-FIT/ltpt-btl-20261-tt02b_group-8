import customtkinter as ctk

class ButtonFrame(ctk.CTkFrame):

    def __init__(

        self,

        parent,

        colors,

        add_callback,

        update_callback,

        delete_callback,

        clear_callback,

        summary_callback,

        import_csv_callback,

        export_csv_callback

    ):

        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        self.add_callback = add_callback

        self.update_callback = update_callback

        self.delete_callback = delete_callback

        self.clear_callback = clear_callback

        self.summary_callback = summary_callback

        self.import_csv_callback = import_csv_callback

        self.export_csv_callback = export_csv_callback

        self.create_widgets()

    def create_widgets(self):

        for i in range(7):

            self.grid_columnconfigure(i, weight=1)

        add_button = ctk.CTkButton(self, text="Thêm giao dịch", height=40, command=self.add_callback)

        add_button.grid(row=0, column=0, padx=10, pady=12, sticky="ew")

        update_button = ctk.CTkButton(self, text="Sửa thông tin", height=40, command=self.update_callback)

        update_button.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        delete_button = ctk.CTkButton(

            self,

            text="Xóa thông tin",

            height=40,

            fg_color="#2b4bc0",

            hover_color="#2638a9",

            command=self.delete_callback

        )

        delete_button.grid(row=0, column=2, padx=10, pady=12, sticky="ew")

        clear_button = ctk.CTkButton(

            self,

            text="Bỏ chọn",

            height=40,

            fg_color="#4b5563",

            hover_color="#374151",

            command=self.clear_callback

        )

        clear_button.grid(row=0, column=3, padx=10, pady=12, sticky="ew")

        summary_button = ctk.CTkButton(

            self,

            text="Xem tổng quan",

            height=40,

            fg_color="#2563eb",

            hover_color="#1d4ed8",

            command=self.summary_callback

        )

        summary_button.grid(row=0, column=4, padx=10, pady=12, sticky="ew")

        import_csv_button = ctk.CTkButton(

            self,

            text="Nhập CSV",

            height=40,

            fg_color="#7c3aed",

            hover_color="#6d28d9",

            command=self.import_csv_callback

        )

        import_csv_button.grid(row=0, column=5, padx=10, pady=12, sticky="ew")

        export_csv_button = ctk.CTkButton(

            self,

            text="Xuất CSV",

            height=40,

            fg_color="#0891b2",

            hover_color="#0e7490",

            command=self.export_csv_callback

        )

        export_csv_button.grid(row=0, column=6, padx=10, pady=12, sticky="ew")
