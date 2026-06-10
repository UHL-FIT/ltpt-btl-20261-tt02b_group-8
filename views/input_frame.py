import customtkinter as ctk

class InputFrame(ctk.CTkFrame):

    def __init__(self, parent, colors, open_calendar_callback):

        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        self.colors = colors

        self.open_calendar_callback = open_calendar_callback

        self.create_widgets()

    def create_widgets(self):

        self.grid_columnconfigure(1, weight=1)

        self.grid_columnconfigure(3, weight=1)

        type_label = ctk.CTkLabel(self, text="Loại giao dịch:", text_color=self.colors["text_color"])

        type_label.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        self.type_combobox = ctk.CTkComboBox(self, values=["Thu nhập", "Chi tiêu"], height=36)

        self.type_combobox.grid(row=0, column=1, padx=12, pady=12, sticky="ew")

        self.type_combobox.set("Thu nhập")

        date_label = ctk.CTkLabel(self, text="Ngày:", text_color=self.colors["text_color"])

        date_label.grid(row=0, column=2, padx=12, pady=12, sticky="w")

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

        description_label = ctk.CTkLabel(self, text="Nội dung:", text_color=self.colors["text_color"])

        description_label.grid(row=1, column=0, padx=12, pady=12, sticky="w")

        self.description_entry = ctk.CTkEntry(self, placeholder_text="VD: Tiền ăn, tiền học...", height=36)

        self.description_entry.grid(row=1, column=1, padx=12, pady=12, sticky="ew")

        amount_label = ctk.CTkLabel(self, text="Số tiền:", text_color=self.colors["text_color"])

        amount_label.grid(row=1, column=2, padx=12, pady=12, sticky="w")

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="VD: 50000", height=36)

        self.amount_entry.grid(row=1, column=3, padx=12, pady=12, sticky="ew")

        self.amount_entry.bind("<KeyRelease>", self.format_amount_input)

        category_label = ctk.CTkLabel(self, text="Danh mục:", text_color=self.colors["text_color"])

        category_label.grid(row=2, column=0, padx=12, pady=12, sticky="w")

        self.category_combobox = ctk.CTkComboBox(

            self,

            values=["Ăn uống", "Học tập", "Di chuyển", "Mua sắm", "Lương", "Thưởng", "Khác"],

            height=36

        )

        self.category_combobox.grid(row=2, column=1, padx=12, pady=12, sticky="ew")

        self.category_combobox.set("Khác")

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

    def get_input_data(self, selected_date):

        transaction_type = self.type_combobox.get()

        date = selected_date.strftime("%d/%m/%Y")

        description = self.description_entry.get()

        amount = self.amount_entry.get()

        category = self.category_combobox.get()

        return transaction_type, date, description, amount, category

    def set_date_text(self, selected_date):

        self.date_button.configure(text=selected_date.strftime("%d/%m/%Y"))

    def set_input_data(self, transaction_type, selected_date, description, amount, category):

        self.type_combobox.set(transaction_type)

        self.set_date_text(selected_date)

        self.description_entry.delete(0, "end")

        self.description_entry.insert(0, description)

        self.amount_entry.delete(0, "end")

        self.amount_entry.insert(0, amount)

        self.category_combobox.set(category or "Khác")

    def clear_input(self, selected_date):

        self.type_combobox.set("Thu nhập")

        self.set_date_text(selected_date)

        self.description_entry.delete(0, "end")

        self.amount_entry.delete(0, "end")

        self.category_combobox.set("Khác")
