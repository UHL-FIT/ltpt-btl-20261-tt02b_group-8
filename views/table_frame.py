import customtkinter as ctk

from tkinter import ttk

class TableFrame(ctk.CTkFrame):

    def __init__(self, parent, colors, select_callback):

        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        self.colors = colors

        self.select_callback = select_callback

        self.create_widgets()

    def create_widgets(self):

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.setup_treeview_style()

        table_frame = ctk.CTkFrame(self, fg_color=self.colors["table_bg"], corner_radius=10)

        table_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        table_frame.grid_rowconfigure(0, weight=1)

        table_frame.grid_columnconfigure(0, weight=1)

        self.table = ttk.Treeview(

            table_frame,

            columns=("id", "type", "date", "category", "description", "amount"),

            show="headings",

            style="Custom.Treeview"

        )

        self.table.heading("id", text="ID")

        self.table.heading("type", text="Loại")

        self.table.heading("date", text="Ngày")

        self.table.heading("category", text="Danh mục")

        self.table.heading("description", text="Nội dung")

        self.table.heading("amount", text="Số tiền")

        self.table.column("id", anchor="center", width=60, stretch=False)

        self.table.column("type", anchor="center", width=150, stretch=True)

        self.table.column("date", anchor="center", width=140, stretch=True)

        self.table.column("category", anchor="center", width=150, stretch=True)

        self.table.column("description", anchor="w", width=360, stretch=True)

        self.table.column("amount", anchor="e", width=180, stretch=True)

        self.table.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        self.table.bind("<<TreeviewSelect>>", self.on_select_row)

    def setup_treeview_style(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(

            "Custom.Treeview",

            background=self.colors["table_bg"],

            foreground=self.colors["text_color"],

            fieldbackground=self.colors["table_bg"],

            borderwidth=0,

            relief="flat",

            rowheight=42,

            font=("Arial", 12),

            padding=8

        )

        style.configure(

            "Custom.Treeview.Heading",

            background=self.colors["header_bg"],

            foreground=self.colors["text_color"],

            borderwidth=0,

            relief="flat",

            font=("Arial", 12, "bold"),

            padding=(12, 10)

        )

        style.map(

            "Custom.Treeview",

            background=[("selected", self.colors["selected_color"])],

            foreground=[("selected", "#ffffff")]

        )

    def format_money(self, amount):

        try:

            amount = str(amount).replace(",", "").strip()

            if amount == "":

                return ""

            number = int(float(amount))

            return f"{number:,}"

        except ValueError:

            return amount

    def show_data(self, transactions):

        for row in self.table.get_children():

            self.table.delete(row)

        for transaction in transactions:

            if transaction["type"] == "Thu nhập":

                tag = "income"

            else:

                tag = "expense"

            self.table.insert(

                "",

                "end",

                values=(

                    transaction.get("id", ""),

                    transaction.get("type", ""),

                    transaction.get("date", ""),

                    transaction.get("category", "Khác"),

                    transaction.get("description", ""),

                    self.format_money(transaction.get("amount", "0"))

                ),

                tags=(tag,)

            )

        self.table.tag_configure("income", background=self.colors["table_bg"], foreground=self.colors["income_color"])

        self.table.tag_configure("expense", background=self.colors["table_bg"], foreground=self.colors["expense_color"])

    def on_select_row(self, event):

        selected_row = self.table.selection()

        if len(selected_row) == 0:

            return

        values = self.table.item(selected_row[0], "values")

        self.select_callback(values)

    def clear_selection(self):

        for item in self.table.selection():

            self.table.selection_remove(item)

    def auto_resize_columns(self):

        total_width = self.table.winfo_width()

        if total_width < 300:

            return

        self.table.column("id", width=60, stretch=False)

        self.table.column("type", width=int(total_width * 0.14))

        self.table.column("date", width=int(total_width * 0.14))

        self.table.column("category", width=int(total_width * 0.15))

        self.table.column("description", width=int(total_width * 0.35))

        self.table.column("amount", width=int(total_width * 0.17))
