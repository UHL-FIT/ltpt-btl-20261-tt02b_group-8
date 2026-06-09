# Import customtkinter để tạo frame
import customtkinter as ctk

# Import ttk để dùng Treeview
from tkinter import ttk


# Tạo lớp TableFrame, quản lý bảng hiển thị dữ liệu
class TableFrame(ctk.CTkFrame):
    # Hàm khởi tạo TableFrame
    def __init__(self, parent, colors, select_callback):
        # Gọi hàm khởi tạo của CTkFrame
        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        # Lưu bảng màu
        self.colors = colors

        # Lưu hàm xử lý khi chọn dòng
        self.select_callback = select_callback

        # Gọi hàm tạo bảng
        self.create_widgets()

    # Hàm tạo giao diện bảng
    def create_widgets(self):
        # Cho hàng 0 tự co giãn
        self.grid_rowconfigure(0, weight=1)

        # Cho cột 0 tự co giãn
        self.grid_columnconfigure(0, weight=1)

        # Cài đặt style cho bảng
        self.setup_treeview_style()

        # Tạo frame con chứa bảng
        table_frame = ctk.CTkFrame(self, fg_color=self.colors["table_bg"], corner_radius=10)
        table_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        # Cho bảng co giãn trong frame con
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Tạo bảng Treeview, thêm cột category để hiển thị danh mục
        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "type", "date", "category", "description", "amount"),
            show="headings",
            style="Custom.Treeview"
        )

        # Đặt tiêu đề các cột
        self.table.heading("id", text="ID")
        self.table.heading("type", text="Loại")
        self.table.heading("date", text="Ngày")
        self.table.heading("category", text="Danh mục")
        self.table.heading("description", text="Nội dung")
        self.table.heading("amount", text="Số tiền")

        # Cấu hình căn chỉnh và độ rộng cột
        self.table.column("id", anchor="center", width=60, stretch=False)
        self.table.column("type", anchor="center", width=150, stretch=True)
        self.table.column("date", anchor="center", width=140, stretch=True)
        self.table.column("category", anchor="center", width=150, stretch=True)
        self.table.column("description", anchor="w", width=360, stretch=True)
        self.table.column("amount", anchor="e", width=180, stretch=True)

        # Đặt bảng lên giao diện
        self.table.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        # Gắn sự kiện khi chọn dòng
        self.table.bind("<<TreeviewSelect>>", self.on_select_row)

    # Hàm cài đặt giao diện cho bảng
    def setup_treeview_style(self):
        # Tạo đối tượng style
        style = ttk.Style()

        # Dùng theme clam để dễ chỉnh màu
        style.theme_use("clam")

        # Cấu hình style cho nội dung bảng
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

        # Cấu hình style cho tiêu đề bảng
        style.configure(
            "Custom.Treeview.Heading",
            background=self.colors["header_bg"],
            foreground=self.colors["text_color"],
            borderwidth=0,
            relief="flat",
            font=("Arial", 12, "bold"),
            padding=(12, 10)
        )

        # Cấu hình màu khi chọn dòng
        style.map(
            "Custom.Treeview",
            background=[("selected", self.colors["selected_color"])],
            foreground=[("selected", "#ffffff")]
        )

    # Hàm định dạng tiền có dấu phẩy
    def format_money(self, amount):
        # Thử xử lý số tiền
        try:
            # Chuyển amount thành chuỗi, xóa dấu phẩy và khoảng trắng
            amount = str(amount).replace(",", "").strip()

            # Nếu amount rỗng thì trả về rỗng
            if amount == "":
                return ""

            # Chuyển amount sang số nguyên
            number = int(float(amount))

            # Trả về số tiền có dấu phẩy
            return f"{number:,}"
        except ValueError:
            # Nếu lỗi thì trả về giá trị gốc
            return amount

    # Hàm hiển thị dữ liệu lên bảng
    def show_data(self, transactions):
        # Xóa dữ liệu cũ
        for row in self.table.get_children():
            self.table.delete(row)

        # Duyệt từng giao dịch
        for transaction in transactions:
            # Nếu là Thu nhập thì gắn tag income
            if transaction["type"] == "Thu nhập":
                tag = "income"
            else:
                tag = "expense"

            # Thêm giao dịch vào bảng
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

        # Cấu hình màu chữ cho Thu nhập
        self.table.tag_configure("income", background=self.colors["table_bg"], foreground=self.colors["income_color"])

        # Cấu hình màu chữ cho Chi tiêu
        self.table.tag_configure("expense", background=self.colors["table_bg"], foreground=self.colors["expense_color"])

    # Hàm xử lý khi người dùng chọn một dòng
    def on_select_row(self, event):
        # Lấy dòng đang chọn
        selected_row = self.table.selection()

        # Nếu không có dòng nào được chọn thì thoát
        if len(selected_row) == 0:
            return

        # Lấy dữ liệu dòng được chọn
        values = self.table.item(selected_row[0], "values")

        # Gửi dữ liệu về MainView xử lý
        self.select_callback(values)

    # Hàm bỏ chọn dòng
    def clear_selection(self):
        # Duyệt các dòng đang chọn
        for item in self.table.selection():
            self.table.selection_remove(item)

    # Hàm tự resize cột
    def auto_resize_columns(self):
        # Lấy độ rộng bảng hiện tại
        total_width = self.table.winfo_width()

        # Nếu bảng quá nhỏ thì không resize
        if total_width < 300:
            return

        # Resize từng cột theo tỷ lệ
        self.table.column("id", width=60, stretch=False)
        self.table.column("type", width=int(total_width * 0.14))
        self.table.column("date", width=int(total_width * 0.14))
        self.table.column("category", width=int(total_width * 0.15))
        self.table.column("description", width=int(total_width * 0.35))
        self.table.column("amount", width=int(total_width * 0.17))
