import customtkinter as ctk

from tkinter import messagebox

from datetime import datetime

from views.calendar_popup import CalendarPopup

class TransactionDialog(ctk.CTkToplevel):

    def __init__(self, parent, colors, title, initial_data, on_save):

        super().__init__(parent)

        self.parent = parent

        self.colors = colors

        self.initial_data = initial_data

        self.on_save = on_save

        self.calendar_window = None

        self.selected_date = datetime.today()

        if self.initial_data is not None:

            try:

                self.selected_date = datetime.strptime(self.initial_data.get("date", ""), "%d/%m/%Y")

            except ValueError:

                self.selected_date = datetime.today()

        self.title(title)

        self.geometry("560x470")

        self.resizable(False, False)

        self.configure(fg_color=self.colors["bg_main"])

        self.transient(parent)

        self.grab_set()

        self.create_widgets()

        self.fill_initial_data()

    def create_widgets(self):

        main_frame = ctk.CTkFrame(

            self,

            fg_color=self.colors["frame_color"],

            corner_radius=16

        )

        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        main_frame.grid_columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(

            main_frame,

            text=self.title(),

            text_color=self.colors["text_color"],

            font=ctk.CTkFont(size=22, weight="bold")

        )

        title_label.grid(row=0, column=0, columnspan=2, padx=16, pady=(18, 16), sticky="w")

        type_label = ctk.CTkLabel(main_frame, text="Loại giao dịch:", text_color=self.colors["text_color"])

        type_label.grid(row=1, column=0, padx=16, pady=10, sticky="w")

        self.type_combobox = ctk.CTkComboBox(

            main_frame,

            values=["Thu nhập", "Chi tiêu"],

            height=38

        )

        self.type_combobox.grid(row=1, column=1, padx=16, pady=10, sticky="ew")

        self.type_combobox.set("Thu nhập")

        date_label = ctk.CTkLabel(main_frame, text="Ngày:", text_color=self.colors["text_color"])

        date_label.grid(row=2, column=0, padx=16, pady=10, sticky="w")

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

        category_label = ctk.CTkLabel(main_frame, text="Danh mục:", text_color=self.colors["text_color"])

        category_label.grid(row=3, column=0, padx=16, pady=10, sticky="w")

        self.category_combobox = ctk.CTkComboBox(

            main_frame,

            values=["Ăn uống", "Học tập", "Di chuyển", "Mua sắm", "Lương", "Thưởng", "Khác"],

            height=38

        )

        self.category_combobox.grid(row=3, column=1, padx=16, pady=10, sticky="ew")

        self.category_combobox.set("Khác")

        description_label = ctk.CTkLabel(main_frame, text="Nội dung:", text_color=self.colors["text_color"])

        description_label.grid(row=4, column=0, padx=16, pady=10, sticky="w")

        self.description_entry = ctk.CTkEntry(

            main_frame,

            placeholder_text="VD: Tiền ăn, tiền học...",

            height=38

        )

        self.description_entry.grid(row=4, column=1, padx=16, pady=10, sticky="ew")

        amount_label = ctk.CTkLabel(main_frame, text="Số tiền:", text_color=self.colors["text_color"])

        amount_label.grid(row=5, column=0, padx=16, pady=10, sticky="w")

        self.amount_entry = ctk.CTkEntry(

            main_frame,

            placeholder_text="VD: 50000",

            height=38

        )

        self.amount_entry.grid(row=5, column=1, padx=16, pady=10, sticky="ew")

        self.amount_entry.bind("<KeyRelease>", self.format_amount_input)

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")

        button_frame.grid(row=6, column=0, columnspan=2, padx=16, pady=(20, 16), sticky="ew")

        button_frame.grid_columnconfigure(0, weight=1)

        button_frame.grid_columnconfigure(1, weight=1)

        cancel_button = ctk.CTkButton(

            button_frame,

            text="Hủy",

            height=40,

            fg_color="#4b5563",

            hover_color="#374151",

            command=self.destroy

        )

        cancel_button.grid(row=0, column=0, padx=(0, 8), sticky="ew")

        save_button = ctk.CTkButton(

            button_frame,

            text="Lưu",

            height=40,

            fg_color="#2563eb",

            hover_color="#1d4ed8",

            command=self.save_data

        )

        save_button.grid(row=0, column=1, padx=(8, 0), sticky="ew")

    def fill_initial_data(self):

        if self.initial_data is None:

            return

        self.type_combobox.set(self.initial_data.get("type", "Thu nhập"))

        self.date_button.configure(text=self.selected_date.strftime("%d/%m/%Y"))

        self.category_combobox.set(self.initial_data.get("category", "Khác"))

        self.description_entry.delete(0, "end")

        self.description_entry.insert(0, self.initial_data.get("description", ""))

        self.amount_entry.delete(0, "end")

        self.amount_entry.insert(0, self.format_money(self.initial_data.get("amount", "")))

    def open_calendar(self):

        if self.calendar_window is not None and self.calendar_window.winfo_exists():

            self.calendar_window.focus()

            return

        self.calendar_window = CalendarPopup(

            parent=self,

            selected_date=self.selected_date,

            on_date_selected=self.on_date_selected,

            colors=self.colors

        )

    def on_date_selected(self, selected_date):

        self.selected_date = selected_date

        self.date_button.configure(text=self.selected_date.strftime("%d/%m/%Y"))

    def format_money(self, amount):

        try:

            amount = str(amount).replace(",", "").strip()

            if amount == "":

                return ""

            return f"{int(float(amount)):,}"

        except ValueError:

            return str(amount)

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

    def get_form_data(self):

        return {

            "type": self.type_combobox.get(),

            "date": self.selected_date.strftime("%d/%m/%Y"),

            "category": self.category_combobox.get(),

            "description": self.description_entry.get(),

            "amount": self.amount_entry.get()

        }

    def save_data(self):

        form_data = self.get_form_data()

        success, message = self.on_save(form_data)

        if success:

            messagebox.showinfo("Thông báo", message)

            self.destroy()

        else:

            messagebox.showerror("Lỗi", message)
