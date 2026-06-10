import customtkinter as ctk

from datetime import datetime

import calendar

class CalendarPopup(ctk.CTkToplevel):

    def __init__(self, parent, selected_date, on_date_selected, colors):

        super().__init__(parent)

        self.parent = parent

        self.selected_date = selected_date

        self.on_date_selected = on_date_selected

        self.colors = colors

        self.current_month = selected_date.month

        self.current_year = selected_date.year

        self.title("Chọn ngày")

        self.geometry("360x390")

        self.resizable(False, False)

        self.configure(fg_color=self.colors["bg_main"])

        self.transient(parent)

        self.grab_set()

        self.draw_calendar()

    def draw_calendar(self):

        for widget in self.winfo_children():

            widget.destroy()

        main_frame = ctk.CTkFrame(

            self,

            fg_color=self.colors["frame_color"],

            corner_radius=14

        )

        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        header_frame = ctk.CTkFrame(

            main_frame,

            fg_color="transparent"

        )

        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        prev_button = ctk.CTkButton(

            header_frame,

            text="<",

            width=42,

            height=34,

            command=self.prev_month

        )

        prev_button.pack(side="left")

        month_year_label = ctk.CTkLabel(

            header_frame,

            text=f"Tháng {self.current_month} / {self.current_year}",

            font=ctk.CTkFont(size=16, weight="bold"),

            text_color=self.colors["text_color"]

        )

        month_year_label.pack(side="left", expand=True)

        next_button = ctk.CTkButton(

            header_frame,

            text=">",

            width=42,

            height=34,

            command=self.next_month

        )

        next_button.pack(side="right")

        week_frame = ctk.CTkFrame(

            main_frame,

            fg_color="transparent"

        )

        week_frame.pack(fill="x", padx=10, pady=5)

        week_days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]

        for i, day_name in enumerate(week_days):

            label = ctk.CTkLabel(

                week_frame,

                text=day_name,

                width=42,

                text_color=self.colors["sub_text_color"],

                font=ctk.CTkFont(size=13, weight="bold")

            )

            label.grid(row=0, column=i, padx=2, pady=2)

        days_frame = ctk.CTkFrame(

            main_frame,

            fg_color="transparent"

        )

        days_frame.pack(fill="both", expand=True, padx=10, pady=5)

        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)

        for row_index, week in enumerate(month_calendar):

            for col_index, day in enumerate(week):

                if day == 0:

                    empty_label = ctk.CTkLabel(

                        days_frame,

                        text="",

                        width=42,

                        height=36

                    )

                    empty_label.grid(row=row_index, column=col_index, padx=2, pady=2)

                else:

                    is_selected = (

                        day == self.selected_date.day

                        and self.current_month == self.selected_date.month

                        and self.current_year == self.selected_date.year

                    )

                    day_button = ctk.CTkButton(

                        days_frame,

                        text=str(day),

                        width=42,

                        height=36,

                        fg_color="#2f6fed" if is_selected else "#2b2d31",

                        hover_color="#3b82f6",

                        text_color="white",

                        command=lambda d=day: self.choose_date(d)

                    )

                    day_button.grid(row=row_index, column=col_index, padx=2, pady=2)

        today_button = ctk.CTkButton(

            main_frame,

            text="Hôm nay",

            height=36,

            fg_color="#4b5563",

            hover_color="#374151",

            command=self.choose_today

        )

        today_button.pack(fill="x", padx=10, pady=(5, 12))

    def prev_month(self):

        self.current_month -= 1

        if self.current_month < 1:

            self.current_month = 12

            self.current_year -= 1

        self.draw_calendar()

    def next_month(self):

        self.current_month += 1

        if self.current_month > 12:

            self.current_month = 1

            self.current_year += 1

        self.draw_calendar()

    def choose_date(self, day):

        selected_date = datetime(self.current_year, self.current_month, day)

        self.on_date_selected(selected_date)

        self.destroy()

    def choose_today(self):

        selected_date = datetime.today()

        self.on_date_selected(selected_date)

        self.destroy()
