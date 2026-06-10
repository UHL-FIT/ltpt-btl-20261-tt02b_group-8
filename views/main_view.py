import customtkinter as ctk

from tkinter import messagebox, filedialog

import tkinter as tk

import os

from datetime import datetime

from controllers.main_controller import MainController

from views.dashboard_frame import DashboardFrame

from views.button_frame import ButtonFrame

from views.search_frame import SearchFrame

from views.table_frame import TableFrame

from views.transaction_dialog import TransactionDialog

class MainView(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.controller = MainController()

        self.selected_id = None

        self.selected_transaction = None

        self.current_transactions = []

        self.transaction_window = None

        self.report_frame = None

        self.title("Quản Lý Thu Chi Cá Nhân")

        self.geometry("1250x760")

        self.minsize(1050, 620)

        ctk.set_appearance_mode("Dark")

        ctk.set_default_color_theme("blue")

        self.colors = {

            "bg_main": "#111827",

            "frame_color": "#1f2937",

            "card_bg": "#243244",

            "border_color": "#374151",

            "table_bg": "#18212f",

            "header_bg": "#253044",

            "text_color": "#ffffff",

            "sub_text_color": "#cbd5e1",

            "selected_color": "#2563eb",

            "income_color": "#22c55e",

            "expense_color": "#ef4444"

        }

        self.configure(fg_color=self.colors["bg_main"])

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(4, weight=1)

        self.create_widgets()

        self.refresh_all()

    def create_widgets(self):

        title_label = ctk.CTkLabel(

            self,

            text="QUẢN LÝ THU CHI CÁ NHÂN",

            font=ctk.CTkFont(size=30, weight="bold"),

            text_color=self.colors["text_color"]

        )

        title_label.grid(row=0, column=0, padx=22, pady=(18, 6), sticky="ew")

        self.dashboard_frame = DashboardFrame(

            parent=self,

            colors=self.colors

        )

        self.dashboard_frame.grid(row=1, column=0, padx=14, pady=(4, 8), sticky="ew")

        self.button_frame = ButtonFrame(

            parent=self,

            colors=self.colors,

            add_callback=self.open_add_window,

            update_callback=self.open_update_window,

            delete_callback=self.delete_transaction,

            clear_callback=self.clear_selection,

            summary_callback=self.show_summary,

            import_csv_callback=self.import_csv_data,

            export_csv_callback=self.export_csv_data

        )

        self.button_frame.grid(row=2, column=0, padx=22, pady=8, sticky="ew")

        self.search_frame = SearchFrame(

            parent=self,

            colors=self.colors,

            search_callback=self.apply_search,

            reset_callback=self.reset_search

        )

        self.search_frame.grid(row=3, column=0, padx=22, pady=8, sticky="ew")

        self.table_frame = TableFrame(

            parent=self,

            colors=self.colors,

            select_callback=self.select_row

        )

        self.table_frame.grid(row=4, column=0, padx=22, pady=(8, 22), sticky="nsew")

        self.bind("<Configure>", self.auto_resize_columns)

    def update_dashboard(self):

        total_income = self.controller.get_total_income()

        total_expense = self.controller.get_total_expense()

        balance = self.controller.get_balance()

        transaction_count = len(self.controller.get_transaction_list())

        self.dashboard_frame.update_data(total_income, total_expense, balance, transaction_count)

    def show_transaction_list(self, transactions=None):

        if transactions is None:

            transactions = self.controller.get_transaction_list()

        self.current_transactions = transactions

        self.table_frame.show_data(transactions)

    def refresh_all(self):

        self.update_dashboard()

        if hasattr(self, "search_frame"):

            self.apply_search()

        else:

            self.show_transaction_list()

    def apply_search(self):

        keyword, transaction_type, category, date_from, date_to, min_amount, max_amount = self.search_frame.get_search_data()

        transactions = self.controller.search_transactions(

            keyword,

            transaction_type,

            category,

            date_from,

            date_to,

            min_amount,

            max_amount

        )

        self.show_transaction_list(transactions)

        self.selected_id = None

        self.selected_transaction = None

        self.table_frame.clear_selection()

    def reset_search(self):

        self.show_transaction_list()

        self.selected_id = None

        self.selected_transaction = None

        self.table_frame.clear_selection()

    def import_csv_data(self):

        file_path = filedialog.askopenfilename(

            title="Chọn file CSV để nhập",

            filetypes=[("CSV file", "*.csv"), ("All files", "*.*")]

        )

        if not file_path:

            return

        replace_data = messagebox.askyesno(

            "Cách nhập dữ liệu",

            "Bạn có muốn XÓA dữ liệu hiện tại và thay bằng file CSV vừa chọn không?\n\n"

            "Chọn Yes: Ghi đè toàn bộ dữ liệu.\n"

            "Chọn No: Thêm dữ liệu CSV vào danh sách hiện tại."

        )

        try:

            success, message = self.controller.import_transactions_from_csv(file_path, replace_data)

            if success:

                self.selected_id = None

                self.selected_transaction = None

                self.refresh_all()

                messagebox.showinfo("Thành công", message)

        except Exception as error:

            messagebox.showerror("Lỗi", f"Không thể nhập CSV:\n{error}")

    def export_csv_data(self):

        file_path = filedialog.asksaveasfilename(

            title="Lưu file CSV",

            defaultextension=".csv",

            filetypes=[("CSV file", "*.csv")]

        )

        if not file_path:

            return

        try:

            self.controller.export_transactions_to_csv(file_path, self.current_transactions)

            messagebox.showinfo("Thành công", "Đã xuất CSV thành công!")

        except Exception as error:

            messagebox.showerror("Lỗi", f"Không thể xuất CSV:\n{error}")

    def open_add_window(self):

        if self.transaction_window is not None and self.transaction_window.winfo_exists():

            self.transaction_window.focus()

            return

        self.transaction_window = TransactionDialog(

            parent=self,

            colors=self.colors,

            title="Thêm giao dịch",

            initial_data=None,

            on_save=self.save_new_transaction

        )

    def save_new_transaction(self, form_data):

        success, message = self.controller.add_transaction(

            form_data["type"],

            form_data["date"],

            form_data["description"],

            form_data["amount"],

            form_data["category"]

        )

        if success:

            self.selected_id = None

            self.selected_transaction = None

            self.refresh_all()

        return success, message

    def open_update_window(self):

        if self.selected_id is None or self.selected_transaction is None:

            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để sửa!")

            return

        if self.transaction_window is not None and self.transaction_window.winfo_exists():

            self.transaction_window.focus()

            return

        self.transaction_window = TransactionDialog(

            parent=self,

            colors=self.colors,

            title="Sửa giao dịch",

            initial_data=self.selected_transaction,

            on_save=self.save_updated_transaction

        )

    def save_updated_transaction(self, form_data):

        success, message = self.controller.update_transaction(

            self.selected_id,

            form_data["type"],

            form_data["date"],

            form_data["description"],

            form_data["amount"],

            form_data["category"]

        )

        if success:

            self.selected_id = None

            self.selected_transaction = None

            self.refresh_all()

        return success, message

    def delete_transaction(self):

        if self.selected_id is None:

            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng để xóa!")

            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giao dịch này không?")

        if confirm:

            success, message = self.controller.delete_transaction(self.selected_id)

            if success:

                messagebox.showinfo("Thông báo", message)

                self.clear_selection()

                self.refresh_all()

    def select_row(self, values):

        self.selected_id = values[0]

        self.selected_transaction = {

            "id": values[0],

            "type": values[1],

            "date": values[2],

            "category": values[3],

            "description": values[4],

            "amount": values[5]

        }

    def clear_selection(self):

        self.selected_id = None

        self.selected_transaction = None

        self.table_frame.clear_selection()

    def format_money(self, amount):

        try:

            return f"{int(float(amount)):,}"

        except ValueError:

            return "0"

    def show_summary(self):

        total_income = self.controller.get_total_income()

        total_expense = self.controller.get_total_expense()

        balance = self.controller.get_balance()

        expenses_by_category = self.controller.get_expenses_by_category(self.current_transactions)

        expense_percentages = self.controller.get_category_expense_percentages(self.current_transactions)

        monthly_expenses = self.controller.get_monthly_expense_summary(self.current_transactions)

        summary_window = ctk.CTkToplevel(self)

        summary_window.title("Tổng quan tài chính")

        summary_window.geometry("620x560")

        summary_window.configure(fg_color=self.colors["bg_main"])

        summary_window.transient(self)

        content_frame = ctk.CTkFrame(summary_window, fg_color=self.colors["frame_color"], corner_radius=14)

        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        title_label = ctk.CTkLabel(

            content_frame,

            text="TỔNG QUAN TÀI CHÍNH",

            font=ctk.CTkFont(size=22, weight="bold"),

            text_color=self.colors["text_color"]

        )

        title_label.pack(pady=(20, 15))

        income_label = ctk.CTkLabel(

            content_frame,

            text=f"Tổng thu nhập: {self.format_money(total_income)} đ",

            text_color=self.colors["income_color"],

            font=ctk.CTkFont(size=17, weight="bold")

        )

        income_label.pack(anchor="w", padx=35, pady=8)

        expense_label = ctk.CTkLabel(

            content_frame,

            text=f"Tổng chi tiêu: {self.format_money(total_expense)} đ",

            text_color=self.colors["expense_color"],

            font=ctk.CTkFont(size=17, weight="bold")

        )

        expense_label.pack(anchor="w", padx=35, pady=8)

        balance_color = self.colors["income_color"] if balance >= 0 else self.colors["expense_color"]

        balance_label = ctk.CTkLabel(

            content_frame,

            text=f"Số dư còn lại: {self.format_money(balance)} đ",

            text_color=balance_color,

            font=ctk.CTkFont(size=17, weight="bold")

        )

        balance_label.pack(anchor="w", padx=35, pady=8)

        category_title = ctk.CTkLabel(

            content_frame,

            text="Chi tiêu theo danh mục:",

            text_color=self.colors["text_color"],

            font=ctk.CTkFont(size=16, weight="bold")

        )

        category_title.pack(anchor="w", padx=35, pady=(14, 8))

        if expense_percentages:

            for category, (amount, percent) in sorted(expense_percentages.items(), key=lambda x: x[1][0], reverse=True):

                label = ctk.CTkLabel(

                    content_frame,

                    text=f"- {category}: {self.format_money(amount)} đ ({percent}%)",

                    text_color=self.colors["sub_text_color"],

                    font=ctk.CTkFont(size=14)

                )

                label.pack(anchor="w", padx=45)

        else:

            no_category_label = ctk.CTkLabel(

                content_frame,

                text="- Chưa có giao dịch chi tiêu",

                text_color=self.colors["sub_text_color"],

                font=ctk.CTkFont(size=14)

            )

            no_category_label.pack(anchor="w", padx=45)

        month_title = ctk.CTkLabel(

            content_frame,

            text="Chi tiêu theo tháng:",

            text_color=self.colors["text_color"],

            font=ctk.CTkFont(size=16, weight="bold")

        )

        month_title.pack(anchor="w", padx=35, pady=(14, 8))

        if monthly_expenses:

            for month, amount in sorted(monthly_expenses.items(), key=lambda x: datetime.strptime(x[0], "%m/%Y")):

                label = ctk.CTkLabel(

                    content_frame,

                    text=f"- {month}: {self.format_money(amount)} đ",

                    text_color=self.colors["sub_text_color"],

                    font=ctk.CTkFont(size=14)

                )

                label.pack(anchor="w", padx=45)

        else:

            no_month_label = ctk.CTkLabel(

                content_frame,

                text="- Chưa có giao dịch chi tiêu",

                text_color=self.colors["sub_text_color"],

                font=ctk.CTkFont(size=14)

            )

            no_month_label.pack(anchor="w", padx=45)

        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")

        button_frame.pack(fill="x", padx=35, pady=(20, 0))

        for i in range(3):

            button_frame.grid_columnconfigure(i, weight=1)

        print_button = ctk.CTkButton(

            button_frame,

            text="Xem báo cáo",

            height=40,

            fg_color="#2563eb",

            hover_color="#1d4ed8",

            command=self.print_summary_report

        )

        print_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        word_button = ctk.CTkButton(

            button_frame,

            text="Xuất Word",

            height=40,

            fg_color="#16a34a",

            hover_color="#15803d",

            command=self.export_summary_word

        )

        word_button.grid(row=0, column=1, sticky="ew", padx=6)

        pdf_button = ctk.CTkButton(

            button_frame,

            text="Xuất PDF",

            height=40,

            fg_color="#dc2626",

            hover_color="#b91c1c",

            command=self.export_summary_pdf

        )

        pdf_button.grid(row=0, column=2, sticky="ew", padx=(6, 0))

    def export_summary_word(self):

        file_path = filedialog.asksaveasfilename(

            title="Lưu báo cáo Word",

            defaultextension=".docx",

            filetypes=[("Word document", "*.docx")]

        )

        if not file_path:

            return

        try:

            self.controller.export_report_to_word(file_path, self.current_transactions)

            messagebox.showinfo("Thành công", "Đã xuất báo cáo Word thành công!")

        except ModuleNotFoundError:

            messagebox.showerror("Thiếu thư viện", "Bạn cần cài thư viện: pip install python-docx")

        except Exception as error:

            messagebox.showerror("Lỗi", f"Không thể xuất Word:\\n{error}")

    def export_summary_pdf(self):

        file_path = filedialog.asksaveasfilename(

            title="Lưu báo cáo PDF",

            defaultextension=".pdf",

            filetypes=[("PDF file", "*.pdf")]

        )

        if not file_path:

            return

        try:

            self.controller.export_report_to_pdf(file_path, self.current_transactions)

            messagebox.showinfo("Thành công", "Đã xuất báo cáo PDF thành công!")

        except ModuleNotFoundError:

            messagebox.showerror("Thiếu thư viện", "Bạn cần cài thư viện: pip install reportlab")

        except Exception as error:

            messagebox.showerror("Lỗi", f"Không thể xuất PDF:\\n{error}")

    def print_summary_report(self):

        report_text = self.controller.generate_report(self.current_transactions)

        report_window = ctk.CTkToplevel(self)

        report_window.title("Báo cáo thu chi")

        report_window.geometry("820x620")

        report_window.configure(fg_color=self.colors["bg_main"])

        report_window.transient(self)

        report_window.grab_set()

        report_frame = ctk.CTkFrame(report_window, fg_color=self.colors["frame_color"], corner_radius=14)

        report_frame.pack(fill="both", expand=True, padx=12, pady=12)

        report_label = ctk.CTkLabel(

            report_frame,

            text="BÁO CÁO THU CHI",

            font=ctk.CTkFont(size=20, weight="bold"),

            text_color=self.colors["text_color"]

        )

        report_label.pack(pady=(12, 12))

        text_widget = tk.Text(

            report_frame,

            wrap="word",

            bg=self.colors["table_bg"],

            fg=self.colors["text_color"],

            insertbackground=self.colors["text_color"],

            font=("Arial", 12),

            relief="flat",

            borderwidth=0

        )

        text_widget.insert("1.0", report_text)

        text_widget.configure(state="disabled")

        text_widget.pack(fill="both", expand=True, side="left", padx=(12, 0), pady=12)

        scrollbar = tk.Scrollbar(report_frame, command=text_widget.yview)

        scrollbar.pack(side="right", fill="y", padx=(0, 12), pady=12)

        text_widget.configure(yscrollcommand=scrollbar.set)

        button_frame = ctk.CTkFrame(report_frame, fg_color="transparent")

        button_frame.pack(fill="x", padx=12, pady=(0, 12))

        for i in range(3):

            button_frame.grid_columnconfigure(i, weight=1)

        word_button = ctk.CTkButton(

            button_frame,

            text="Xuất Word",

            height=40,

            fg_color="#16a34a",

            hover_color="#15803d",

            command=self.export_summary_word

        )

        word_button.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        pdf_button = ctk.CTkButton(

            button_frame,

            text="Xuất PDF",

            height=40,

            fg_color="#dc2626",

            hover_color="#b91c1c",

            command=self.export_summary_pdf

        )

        pdf_button.grid(row=0, column=1, sticky="ew", padx=6)

        close_button = ctk.CTkButton(

            button_frame,

            text="Đóng",

            height=40,

            fg_color="#4b5563",

            hover_color="#374151",

            command=report_window.destroy

        )

        close_button.grid(row=0, column=2, sticky="ew", padx=(6, 0))

    def auto_resize_columns(self, event=None):

        if hasattr(self, "table_frame"):

            self.table_frame.auto_resize_columns()
