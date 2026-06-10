import customtkinter as ctk

from datetime import datetime

from views.calendar_popup import CalendarPopup

class SearchFrame(ctk.CTkFrame):

    def __init__(self, parent, colors, search_callback, reset_callback):

        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        self.colors = colors

        self.search_callback = search_callback

        self.reset_callback = reset_callback

        self.create_widgets()

    def create_widgets(self):

        for i in range(10):

            self.grid_columnconfigure(i, weight=1)

        search_label = ctk.CTkLabel(

            self,

            text="Tìm kiếm:",

            text_color=self.colors["text_color"]

        )

        search_label.grid(row=0, column=0, padx=(12, 6), pady=12, sticky="w")

        self.keyword_entry = ctk.CTkEntry(

            self,

            placeholder_text="Nhập nội dung, ngày, số tiền, danh mục...",

            height=36

        )

        self.keyword_entry.grid(row=0, column=1, padx=6, pady=12, sticky="ew", columnspan=2)

        self.keyword_entry.bind("<KeyRelease>", lambda event: self.search_callback())

        type_label = ctk.CTkLabel(

            self,

            text="Loại:",

            text_color=self.colors["text_color"]

        )

        type_label.grid(row=0, column=3, padx=(10, 6), pady=12, sticky="w")

        self.type_filter = ctk.CTkComboBox(

            self,

            values=["Tất cả", "Thu nhập", "Chi tiêu"],

            height=36,

            command=lambda value: self.search_callback()

        )

        self.type_filter.grid(row=0, column=4, padx=6, pady=12, sticky="ew")

        self.type_filter.set("Tất cả")

        category_label = ctk.CTkLabel(

            self,

            text="Danh mục:",

            text_color=self.colors["text_color"]

        )

        category_label.grid(row=0, column=5, padx=(10, 6), pady=12, sticky="w")

        self.category_filter = ctk.CTkComboBox(

            self,

            values=["Tất cả", "Ăn uống", "Học tập", "Di chuyển", "Mua sắm", "Lương", "Thưởng", "Khác"],

            height=36,

            command=lambda value: self.search_callback()

        )

        self.category_filter.grid(row=0, column=6, padx=6, pady=12, sticky="ew")

        self.category_filter.set("Tất cả")

        search_button = ctk.CTkButton(

            self,

            text="Tìm",

            height=36,

            width=90,

            command=self.search_callback

        )

        search_button.grid(row=0, column=7, padx=(10, 6), pady=12)

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

    def open_calendar(self, target):

        CalendarPopup(

            parent=self,

            selected_date=self.date_from if target == "from" and self.date_from else (self.date_to if target == "to" and self.date_to else datetime.today()),

            on_date_selected=lambda selected: self.on_date_selected(selected, target),

            colors=self.colors

        )

    def on_date_selected(self, selected_date, target):

        date_text = selected_date.strftime("%d/%m/%Y")

        if target == "from":

            self.date_from = selected_date

            self.date_from_button.configure(text=date_text)

        else:

            self.date_to = selected_date

            self.date_to_button.configure(text=date_text)
