# Import customtkinter de tao giao dien tim kiem
import customtkinter as ctk

from datetime import datetime

# Import popup lich de chon ngay
from views.calendar_popup import CalendarPopup


# Tao lop SearchFrame, quan ly khu vuc tim kiem giao dich
class SearchFrame(ctk.CTkFrame):
    # Ham khoi tao SearchFrame
    def __init__(self, parent, colors, search_callback, reset_callback):
        # Goi ham khoi tao cua CTkFrame
        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        # Luu bang mau dung chung
        self.colors = colors

        # Luu ham tim kiem duoc truyen tu MainView
        self.search_callback = search_callback

        # Luu ham dat lai tim kiem duoc truyen tu MainView
        self.reset_callback = reset_callback

        # Tao giao dien tim kiem
        self.create_widgets()

    # Ham tao cac widget tim kiem
    def create_widgets(self):
        # Cho cac cot co gian deu
        for i in range(10):
            self.grid_columnconfigure(i, weight=1)

        # Tao label tim kiem
        search_label = ctk.CTkLabel(
            self,
            text="Tìm kiếm:",
            text_color=self.colors["text_color"]
        )
        search_label.grid(row=0, column=0, padx=(12, 6), pady=12, sticky="w")

        # Tao o nhap tu khoa tim kiem
        self.keyword_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nhập nội dung, ngày, số tiền, danh mục...",
            height=36
        )
        self.keyword_entry.grid(row=0, column=1, padx=6, pady=12, sticky="ew", columnspan=2)

        # Khi go phim thi tu dong tim kiem ngay
        self.keyword_entry.bind("<KeyRelease>", lambda event: self.search_callback())

        # Tao label loc loai
        type_label = ctk.CTkLabel(
            self,
            text="Loại:",
            text_color=self.colors["text_color"]
        )
        type_label.grid(row=0, column=3, padx=(10, 6), pady=12, sticky="w")

        # Tao combobox loc loai giao dich
        self.type_filter = ctk.CTkComboBox(
            self,
            values=["Tất cả", "Thu nhập", "Chi tiêu"],
            height=36,
            command=lambda value: self.search_callback()
        )
        self.type_filter.grid(row=0, column=4, padx=6, pady=12, sticky="ew")
        self.type_filter.set("Tất cả")

        # Tao label loc danh muc
        category_label = ctk.CTkLabel(
            self,
            text="Danh mục:",
            text_color=self.colors["text_color"]
        )
        category_label.grid(row=0, column=5, padx=(10, 6), pady=12, sticky="w")

        # Tao combobox loc danh muc
        self.category_filter = ctk.CTkComboBox(
            self,
            values=["Tất cả", "Ăn uống", "Học tập", "Di chuyển", "Mua sắm", "Lương", "Thưởng", "Khác"],
            height=36,
            command=lambda value: self.search_callback()
        )
        self.category_filter.grid(row=0, column=6, padx=6, pady=12, sticky="ew")
        self.category_filter.set("Tất cả")

        # Tao nut tim kiem
        search_button = ctk.CTkButton(
            self,
            text="Tìm",
            height=36,
            width=90,
            command=self.search_callback
        )
        search_button.grid(row=0, column=7, padx=(10, 6), pady=12)

        # Tao nut dat lai
        reset_button = ctk.CTkButton(
            self,
            text="Đặt lại",
            height=36,
            width=90,
            fg_color="#4b5563",
            hover_color="#374151",
            command=self.reset_search
        )
        reset_button.grid(row=0, column=8, padx=(6, 12), pady=12)

        # Tao loc nhanh theo ngay va so tien
        date_from_label = ctk.CTkLabel(
            self,
            text="Từ ngày:",
            text_color=self.colors["text_color"]
        )
        date_from_label.grid(row=1, column=0, padx=(12, 6), pady=(0, 10), sticky="w")

        self.date_from_button = ctk.CTkButton(
            self,
            text="Chọn ngày",
            height=36,
            fg_color="#2b2d31",
            hover_color="#34373d",
            command=lambda: self.open_calendar("from")
        )
        self.date_from_button.grid(row=1, column=1, padx=6, pady=(0, 10), sticky="ew")

        date_to_label = ctk.CTkLabel(
            self,
            text="Đến ngày:",
            text_color=self.colors["text_color"]
        )
        date_to_label.grid(row=1, column=2, padx=(10, 6), pady=(0, 10), sticky="w")

        self.date_to_button = ctk.CTkButton(
            self,
            text="Chọn ngày",
            height=36,
            fg_color="#2b2d31",
            hover_color="#34373d",
            command=lambda: self.open_calendar("to")
        )
        self.date_to_button.grid(row=1, column=3, padx=6, pady=(0, 10), sticky="ew")

        min_amount_label = ctk.CTkLabel(
            self,
            text="Tiền từ:",
            text_color=self.colors["text_color"]
        )
        min_amount_label.grid(row=1, column=4, padx=(10, 6), pady=(0, 10), sticky="w")

        self.min_amount_entry = ctk.CTkEntry(
            self,
            placeholder_text="0",
            height=36
        )
        self.min_amount_entry.grid(row=1, column=5, padx=6, pady=(0, 10), sticky="ew")

        max_amount_label = ctk.CTkLabel(
            self,
            text="Đến:",
            text_color=self.colors["text_color"]
        )
        max_amount_label.grid(row=1, column=6, padx=(10, 6), pady=(0, 10), sticky="w")

        self.max_amount_entry = ctk.CTkEntry(
            self,
            placeholder_text="0",
            height=36
        )
        self.max_amount_entry.grid(row=1, column=7, padx=6, pady=(0, 10), sticky="ew")

        apply_filters_button = ctk.CTkButton(
            self,
            text="Áp dụng lọc",
            height=36,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.search_callback
        )
        apply_filters_button.grid(row=1, column=8, padx=(10, 6), pady=(0, 10), sticky="ew")

        self.date_from = None
        self.date_to = None

    # Ham lay dieu kien tim kiem hien tai
    def get_search_data(self):
        keyword = self.keyword_entry.get()
        transaction_type = self.type_filter.get()
        category = self.category_filter.get()
        min_amount = self.min_amount_entry.get().replace(",", "").strip()
        max_amount = self.max_amount_entry.get().replace(",", "").strip()

        return (
            keyword,
            transaction_type,
            category,
            self.date_from.strftime("%d/%m/%Y") if self.date_from else None,
            self.date_to.strftime("%d/%m/%Y") if self.date_to else None,
            min_amount,
            max_amount
        )

    # Ham xoa dieu kien tim kiem
    def reset_search(self):
        self.keyword_entry.delete(0, "end")
        self.type_filter.set("Tất cả")
        self.category_filter.set("Tất cả")
        self.date_from = None
        self.date_to = None
        self.date_from_button.configure(text="Chọn ngày")
        self.date_to_button.configure(text="Chọn ngày")
        self.min_amount_entry.delete(0, "end")
        self.max_amount_entry.delete(0, "end")

        self.reset_callback()

    # Ham mo popup lich voi truong ngay tuong ung
    def open_calendar(self, target):
        CalendarPopup(
            parent=self,
            selected_date=self.date_from if target == "from" and self.date_from else (self.date_to if target == "to" and self.date_to else datetime.today()),
            on_date_selected=lambda selected: self.on_date_selected(selected, target),
            colors=self.colors
        )

    # Ham xu ly ngay duoc chon tu popup lich
    def on_date_selected(self, selected_date, target):
        date_text = selected_date.strftime("%d/%m/%Y")
        if target == "from":
            self.date_from = selected_date
            self.date_from_button.configure(text=date_text)
        else:
            self.date_to = selected_date
            self.date_to_button.configure(text=date_text)
