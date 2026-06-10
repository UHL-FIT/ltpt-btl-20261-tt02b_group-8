import customtkinter as ctk

class DashboardFrame(ctk.CTkFrame):

    def __init__(self, parent, colors):

        super().__init__(parent, fg_color="transparent")

        self.colors = colors

        self.income_value_label = None

        self.expense_value_label = None

        self.balance_value_label = None

        self.count_value_label = None

        self.create_widgets()

    def create_widgets(self):

        for i in range(4):

            self.grid_columnconfigure(i, weight=1)

        self.income_value_label = self.create_card(

            column=0,

            title="Tổng thu nhập",

            value="0 đ",

            color=self.colors["income_color"],

            icon="+"

        )

        self.expense_value_label = self.create_card(

            column=1,

            title="Tổng chi tiêu",

            value="0 đ",

            color=self.colors["expense_color"],

            icon="-"

        )

        self.balance_value_label = self.create_card(

            column=2,

            title="Số dư còn lại",

            value="0 đ",

            color="#60a5fa",

            icon="="

        )

        self.count_value_label = self.create_card(

            column=3,

            title="Số giao dịch",

            value="0",

            color="#fbbf24",

            icon="#"

        )

    def create_card(self, column, title, value, color, icon):

        card = ctk.CTkFrame(

            self,

            fg_color=self.colors["card_bg"],

            corner_radius=18,

            border_width=1,

            border_color=self.colors["border_color"]

        )

        card.grid(row=0, column=column, padx=8, pady=6, sticky="ew")

        icon_label = ctk.CTkLabel(

            card,

            text=icon,

            width=34,

            height=34,

            fg_color=color,

            corner_radius=17,

            text_color="white",

            font=ctk.CTkFont(size=18, weight="bold")

        )

        icon_label.grid(row=0, column=0, rowspan=2, padx=(14, 8), pady=16)

        title_label = ctk.CTkLabel(

            card,

            text=title,

            text_color=self.colors["sub_text_color"],

            font=ctk.CTkFont(size=13)

        )

        title_label.grid(row=0, column=1, padx=(4, 14), pady=(14, 0), sticky="w")

        value_label = ctk.CTkLabel(

            card,

            text=value,

            text_color=color,

            font=ctk.CTkFont(size=20, weight="bold")

        )

        value_label.grid(row=1, column=1, padx=(4, 14), pady=(0, 14), sticky="w")

        card.grid_columnconfigure(1, weight=1)

        return value_label

    def format_money(self, amount):

        try:

            return f"{int(float(amount)):,} đ"

        except ValueError:

            return "0 đ"

    def update_data(self, total_income, total_expense, balance, transaction_count):

        self.income_value_label.configure(text=self.format_money(total_income))

        self.expense_value_label.configure(text=self.format_money(total_expense))

        balance_color = self.colors["income_color"] if balance >= 0 else self.colors["expense_color"]

        self.balance_value_label.configure(text=self.format_money(balance), text_color=balance_color)

        self.count_value_label.configure(text=str(transaction_count))
