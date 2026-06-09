# Import customtkinter để tạo cửa sổ thêm/sửa giao dịch
import customtkinter as ctk

# Import messagebox để hiện thông báo
from tkinter import messagebox

# Import datetime để xử lý ngày tháng
from datetime import datetime

# Import popup lịch đã có sẵn trong project
from views.calendar_popup import CalendarPopup


# Lớp TransactionDialog dùng chung cho cả thêm và sửa giao dịch
class TransactionDialog(ctk.CTkToplevel):
    # Hàm khởi tạo cửa sổ
    def __init__(self, parent, colors, title, initial_data, on_save):
        # Gọi hàm khởi tạo của CTkToplevel
        super().__init__(parent)

        # Lưu cửa sổ cha
        self.parent = parent

        # Lưu bảng màu dùng chung
        self.colors = colors

        # Lưu dữ liệu ban đầu, nếu thêm mới thì initial_data = None
        self.initial_data = initial_data

        # Lưu hàm xử lý khi bấm Lưu
        self.on_save = on_save

        # Lưu popup lịch đang mở
        self.calendar_window = None

        # Ngày mặc định là hôm nay
        self.selected_date = datetime.today()

        # Nếu là sửa giao dịch thì lấy ngày từ dữ liệu cũ
        if self.initial_data is not None:
            try:
                self.selected_date = datetime.strptime(self.initial_data.get("date", ""), "%d/%m/%Y")
            except ValueError:
                self.selected_date = datetime.today()

        # Đặt tiêu đề cửa sổ
        self.title(title)

        # Đặt kích thước cửa sổ
        self.geometry("560x470")

        # Không cho thay đổi kích thước cửa sổ
        self.resizable(False, False)

        # Đặt màu nền
        self.configure(fg_color=self.colors["bg_main"])

        # Cho cửa sổ này nằm trên cửa sổ chính
        self.transient(parent)

        # Bắt người dùng xử lý cửa sổ này trước
        self.grab_set()

        # Tạo giao diện
        self.create_widgets()

        # Đổ dữ liệu cũ lên form nếu là sửa
        self.fill_initial_data()

    # Hàm tạo giao diện cửa sổ thêm/sửa
    def create_widgets(self):
        # Tạo frame chính
        main_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["frame_color"],
            corner_radius=16
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Cho cột nhập liệu co giãn
        main_frame.grid_columnconfigure(1, weight=1)

        # Tiêu đề form
        title_label = ctk.CTkLabel(
            main_frame,
            text=self.title(),
            text_color=self.colors["text_color"],
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=16, pady=(18, 16), sticky="w")

        # Label loại giao dịch
        type_label = ctk.CTkLabel(main_frame, text="Loại giao dịch:", text_color=self.colors["text_color"])
        type_label.grid(row=1, column=0, padx=16, pady=10, sticky="w")

        # Combobox chọn loại giao dịch
        self.type_combobox = ctk.CTkComboBox(
            main_frame,
            values=["Thu nhập", "Chi tiêu"],
            height=38
        )
        self.type_combobox.grid(row=1, column=1, padx=16, pady=10, sticky="ew")
        self.type_combobox.set("Thu nhập")

        # Label ngày
        date_label = ctk.CTkLabel(main_frame, text="Ngày:", text_color=self.colors["text_color"])
        date_label.grid(row=2, column=0, padx=16, pady=10, sticky="w")

        # Nút chọn ngày
        self.date_button = ctk.CTkButton(
            main_frame,
            text=self.selected_date.strftime("%d/%m/%Y"),
            height=38,
            fg_color="#2b2d31",
            hover_color="#34373d",
            text_color="white",
            anchor="w",
            command=self.open_calendar
        )
        self.date_button.grid(row=2, column=1, padx=16, pady=10, sticky="ew")

        # Label danh mục
        category_label = ctk.CTkLabel(main_frame, text="Danh mục:", text_color=self.colors["text_color"])
        category_label.grid(row=3, column=0, padx=16, pady=10, sticky="w")

        # Combobox chọn danh mục
        self.category_combobox = ctk.CTkComboBox(
            main_frame,
            values=["Ăn uống", "Học tập", "Di chuyển", "Mua sắm", "Lương", "Thưởng", "Khác"],
            height=38
        )
        self.category_combobox.grid(row=3, column=1, padx=16, pady=10, sticky="ew")
        self.category_combobox.set("Khác")

        # Label nội dung
        description_label = ctk.CTkLabel(main_frame, text="Nội dung:", text_color=self.colors["text_color"])
        description_label.grid(row=4, column=0, padx=16, pady=10, sticky="w")

        # Ô nhập nội dung
        self.description_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="VD: Tiền ăn, tiền học...",
            height=38
        )
        self.description_entry.grid(row=4, column=1, padx=16, pady=10, sticky="ew")

        # Label số tiền
        amount_label = ctk.CTkLabel(main_frame, text="Số tiền:", text_color=self.colors["text_color"])
        amount_label.grid(row=5, column=0, padx=16, pady=10, sticky="w")

        # Ô nhập số tiền
        self.amount_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="VD: 50000",
            height=38
        )
        self.amount_entry.grid(row=5, column=1, padx=16, pady=10, sticky="ew")

        # Gắn sự kiện tự thêm dấu phẩy khi nhập tiền
        self.amount_entry.bind("<KeyRelease>", self.format_amount_input)

        # Frame chứa nút
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=6, column=0, columnspan=2, padx=16, pady=(20, 16), sticky="ew")

        # Cho 2 nút co đều
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        # Nút hủy
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Hủy",
            height=40,
            fg_color="#4b5563",
            hover_color="#374151",
            command=self.destroy
        )
        cancel_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        # Nút lưu
        save_button = ctk.CTkButton(
            button_frame,
            text="Lưu",
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.save_data
        )
        save_button.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    # Hàm đổ dữ liệu cũ lên form khi sửa giao dịch
    def fill_initial_data(self):
        # Nếu không có dữ liệu ban đầu thì không cần làm gì
        if self.initial_data is None:
            return

        # Gán loại giao dịch
        self.type_combobox.set(self.initial_data.get("type", "Thu nhập"))

        # Gán ngày
        self.date_button.configure(text=self.selected_date.strftime("%d/%m/%Y"))

        # Gán danh mục
        self.category_combobox.set(self.initial_data.get("category", "Khác"))

        # Gán nội dung
        self.description_entry.delete(0, "end")
        self.description_entry.insert(0, self.initial_data.get("description", ""))

        # Gán số tiền
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, self.format_money(self.initial_data.get("amount", "")))

    # Hàm mở popup lịch
    def open_calendar(self):
        # Nếu lịch đang mở thì không mở thêm
        if self.calendar_window is not None and self.calendar_window.winfo_exists():
            self.calendar_window.focus()
            return

        # Tạo popup lịch
        self.calendar_window = CalendarPopup(
            parent=self,
            selected_date=self.selected_date,
            on_date_selected=self.on_date_selected,
            colors=self.colors
        )

    # Hàm nhận ngày đã chọn từ popup lịch
    def on_date_selected(self, selected_date):
        # Cập nhật ngày đang chọn
        self.selected_date = selected_date

        # Cập nhật text trên nút ngày
        self.date_button.configure(text=self.selected_date.strftime("%d/%m/%Y"))

    # Hàm format tiền có dấu phẩy
    def format_money(self, amount):
        try:
            amount = str(amount).replace(",", "").strip()

            if amount == "":
                return ""

            return f"{int(float(amount)):,}"
        except ValueError:
            return str(amount)

    # Hàm tự thêm dấu phẩy khi nhập số tiền
    def format_amount_input(self, event=None):
        current_text = self.amount_entry.get()
        clean_text = current_text.replace(",", "").strip()

        if clean_text == "":
            return

        if not clean_text.isdigit():
            return

        formatted_text = f"{int(clean_text):,}"

        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, formatted_text)

    # Hàm lấy dữ liệu trên form
    def get_form_data(self):
        return {
            "type": self.type_combobox.get(),
            "date": self.selected_date.strftime("%d/%m/%Y"),
            "category": self.category_combobox.get(),
            "description": self.description_entry.get(),
            "amount": self.amount_entry.get()
        }

    # Hàm lưu dữ liệu
    def save_data(self):
        # Lấy dữ liệu trên form
        form_data = self.get_form_data()

        # Gọi hàm on_save ở MainView
        success, message = self.on_save(form_data)

        # Nếu thành công thì thông báo và đóng cửa sổ
        if success:
            messagebox.showinfo("Thông báo", message)
            self.destroy()

        # Nếu thất bại thì báo lỗi, không đóng cửa sổ
        else:
            messagebox.showerror("Lỗi", message)
