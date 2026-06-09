# Import customtkinter de tao giao dien dashboard
import customtkinter as ctk


# Tao lop DashboardFrame, hien thi cac the tong quan tai chinh
class DashboardFrame(ctk.CTkFrame):
    # Ham khoi tao DashboardFrame
    def __init__(self, parent, colors):
        # Goi ham khoi tao cua CTkFrame
        super().__init__(parent, fg_color="transparent")

        # Luu bang mau dung chung
        self.colors = colors

        # Luu cac label gia tri de cap nhat sau nay
        self.income_value_label = None
        self.expense_value_label = None
        self.balance_value_label = None
        self.count_value_label = None

        # Tao giao dien dashboard
        self.create_widgets()

    # Ham tao cac the dashboard
    def create_widgets(self):
        # Tao 4 cot co gian deu nhau
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Tao the Tong thu nhap
        self.income_value_label = self.create_card(
            column=0,
            title="Tổng thu nhập",
            value="0 đ",
            color=self.colors["income_color"],
            icon="+"
        )

        # Tao the Tong chi tieu
        self.expense_value_label = self.create_card(
            column=1,
            title="Tổng chi tiêu",
            value="0 đ",
            color=self.colors["expense_color"],
            icon="-"
        )

        # Tao the So du con lai
        self.balance_value_label = self.create_card(
            column=2,
            title="Số dư còn lại",
            value="0 đ",
            color="#60a5fa",
            icon="="
        )

        # Tao the So giao dich
        self.count_value_label = self.create_card(
            column=3,
            title="Số giao dịch",
            value="0",
            color="#fbbf24",
            icon="#"
        )

    # Ham tao mot the thong tin trong dashboard
    def create_card(self, column, title, value, color, icon):
        # Tao frame the thong tin
        card = ctk.CTkFrame(
            self,
            fg_color=self.colors["card_bg"],
            corner_radius=18,
            border_width=1,
            border_color=self.colors["border_color"]
        )

        # Dat the len dashboard
        card.grid(row=0, column=column, padx=8, pady=6, sticky="ew")

        # Tao khung nho chua icon
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

        # Dat icon len the
        icon_label.grid(row=0, column=0, rowspan=2, padx=(14, 8), pady=16)

        # Tao label tieu de
        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color=self.colors["sub_text_color"],
            font=ctk.CTkFont(size=13)
        )

        # Dat label tieu de len the
        title_label.grid(row=0, column=1, padx=(4, 14), pady=(14, 0), sticky="w")

        # Tao label gia tri
        value_label = ctk.CTkLabel(
            card,
            text=value,
            text_color=color,
            font=ctk.CTkFont(size=20, weight="bold")
        )

        # Dat label gia tri len the
        value_label.grid(row=1, column=1, padx=(4, 14), pady=(0, 14), sticky="w")

        # Cho cot gia tri co gian
        card.grid_columnconfigure(1, weight=1)

        # Tra ve label gia tri de cap nhat sau
        return value_label

    # Ham dinh dang so tien co dau phay
    def format_money(self, amount):
        # Thu chuyen so tien sang dang so
        try:
            # Chuyen so tien sang int va them dau phay
            return f"{int(float(amount)):,} đ"

        # Neu loi thi tra ve 0 dong
        except ValueError:
            return "0 đ"

    # Ham cap nhat du lieu tren dashboard
    def update_data(self, total_income, total_expense, balance, transaction_count):
        # Cap nhat tong thu nhap
        self.income_value_label.configure(text=self.format_money(total_income))

        # Cap nhat tong chi tieu
        self.expense_value_label.configure(text=self.format_money(total_expense))

        # Chon mau so du theo am/duong
        balance_color = self.colors["income_color"] if balance >= 0 else self.colors["expense_color"]

        # Cap nhat mau va gia tri so du
        self.balance_value_label.configure(text=self.format_money(balance), text_color=balance_color)

        # Cap nhat so giao dich
        self.count_value_label.configure(text=str(transaction_count))
