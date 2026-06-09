# Import customtkinter để tạo giao diện
import customtkinter as ctk


# Tạo lớp InputFrame, quản lý phần nhập dữ liệu
class InputFrame(ctk.CTkFrame):
    # Hàm khởi tạo InputFrame
    def __init__(self, parent, colors, open_calendar_callback):
        # Gọi hàm khởi tạo của CTkFrame
        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        # Lưu bảng màu dùng chung
        self.colors = colors

        # Lưu hàm mở lịch được truyền từ MainView
        self.open_calendar_callback = open_calendar_callback

        # Gọi hàm tạo widget
        self.create_widgets()

    # Hàm tạo giao diện nhập liệu
    def create_widgets(self):
        # Cho cột nhập liệu co giãn theo cửa sổ
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Tạo label loại giao dịch
        type_label = ctk.CTkLabel(self, text="Loại giao dịch:", text_color=self.colors["text_color"])
        type_label.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        # Tạo combobox chọn loại giao dịch
        self.type_combobox = ctk.CTkComboBox(self, values=["Thu nhập", "Chi tiêu"], height=36)
        self.type_combobox.grid(row=0, column=1, padx=12, pady=12, sticky="ew")
        self.type_combobox.set("Thu nhập")

        # Tạo label ngày
        date_label = ctk.CTkLabel(self, text="Ngày:", text_color=self.colors["text_color"])
        date_label.grid(row=0, column=2, padx=12, pady=12, sticky="w")

        # Tạo nút chọn ngày
        self.date_button = ctk.CTkButton(
            self,
            text="",
            height=36,
            fg_color="#2b2d31",
            hover_color="#34373d",
            text_color="white",
            anchor="w",
            command=self.open_calendar_callback
        )
        self.date_button.grid(row=0, column=3, padx=12, pady=12, sticky="ew")

        # Tạo label nội dung
        description_label = ctk.CTkLabel(self, text="Nội dung:", text_color=self.colors["text_color"])
        description_label.grid(row=1, column=0, padx=12, pady=12, sticky="w")

        # Tạo ô nhập nội dung
        self.description_entry = ctk.CTkEntry(self, placeholder_text="VD: Tiền ăn, tiền học...", height=36)
        self.description_entry.grid(row=1, column=1, padx=12, pady=12, sticky="ew")

        # Tạo label số tiền
        amount_label = ctk.CTkLabel(self, text="Số tiền:", text_color=self.colors["text_color"])
        amount_label.grid(row=1, column=2, padx=12, pady=12, sticky="w")

        # Tạo ô nhập số tiền
        self.amount_entry = ctk.CTkEntry(self, placeholder_text="VD: 50000", height=36)
        self.amount_entry.grid(row=1, column=3, padx=12, pady=12, sticky="ew")

        # Gắn sự kiện tự format số tiền
        self.amount_entry.bind("<KeyRelease>", self.format_amount_input)

        # Tạo label danh mục
        category_label = ctk.CTkLabel(self, text="Danh mục:", text_color=self.colors["text_color"])
        category_label.grid(row=2, column=0, padx=12, pady=12, sticky="w")

        # Tạo combobox chọn danh mục để phục vụ thống kê chi tiêu theo danh mục
        self.category_combobox = ctk.CTkComboBox(
            self,
            values=["Ăn uống", "Học tập", "Di chuyển", "Mua sắm", "Lương", "Thưởng", "Khác"],
            height=36
        )
        self.category_combobox.grid(row=2, column=1, padx=12, pady=12, sticky="ew")
        self.category_combobox.set("Khác")

    # Hàm tự thêm dấu phẩy khi nhập số tiền
    def format_amount_input(self, event=None):
        # Lấy nội dung hiện tại trong ô số tiền
        current_text = self.amount_entry.get()

        # Xóa dấu phẩy và khoảng trắng
        clean_text = current_text.replace(",", "").strip()

        # Nếu rỗng thì không làm gì
        if clean_text == "":
            return

        # Nếu không phải số thì không format
        if not clean_text.isdigit():
            return

        # Format số tiền có dấu phẩy
        formatted_text = f"{int(clean_text):,}"

        # Xóa dữ liệu cũ
        self.amount_entry.delete(0, "end")

        # Thêm dữ liệu đã format
        self.amount_entry.insert(0, formatted_text)

    # Hàm lấy dữ liệu từ form nhập
    def get_input_data(self, selected_date):
        # Lấy loại giao dịch
        transaction_type = self.type_combobox.get()

        # Lấy ngày đang chọn
        date = selected_date.strftime("%d/%m/%Y")

        # Lấy nội dung
        description = self.description_entry.get()

        # Lấy số tiền
        amount = self.amount_entry.get()

        # Lấy danh mục
        category = self.category_combobox.get()

        # Trả về dữ liệu
        return transaction_type, date, description, amount, category

    # Hàm cập nhật text nút ngày
    def set_date_text(self, selected_date):
        self.date_button.configure(text=selected_date.strftime("%d/%m/%Y"))

    # Hàm đưa dữ liệu từ bảng lên form
    def set_input_data(self, transaction_type, selected_date, description, amount, category):
        # Set loại giao dịch
        self.type_combobox.set(transaction_type)

        # Set ngày
        self.set_date_text(selected_date)

        # Set nội dung
        self.description_entry.delete(0, "end")
        self.description_entry.insert(0, description)

        # Set số tiền
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, amount)

        # Set danh mục
        self.category_combobox.set(category or "Khác")

    # Hàm làm mới form
    def clear_input(self, selected_date):
        # Đưa loại giao dịch về mặc định
        self.type_combobox.set("Thu nhập")

        # Đưa ngày về ngày hiện tại
        self.set_date_text(selected_date)

        # Xóa nội dung
        self.description_entry.delete(0, "end")

        # Xóa số tiền
        self.amount_entry.delete(0, "end")

        # Đưa danh mục về mặc định
        self.category_combobox.set("Khác")
