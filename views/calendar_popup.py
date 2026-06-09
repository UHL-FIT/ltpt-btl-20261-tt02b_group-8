# Import customtkinter để tạo popup đẹp
import customtkinter as ctk

# Import datetime để xử lý ngày tháng
from datetime import datetime

# Import calendar để tạo lịch tháng
import calendar


# Tạo lớp CalendarPopup, kế thừa từ CTkToplevel
class CalendarPopup(ctk.CTkToplevel):
    # Hàm khởi tạo popup lịch
    def __init__(self, parent, selected_date, on_date_selected, colors):
        # Gọi hàm khởi tạo của CTkToplevel
        super().__init__(parent)

        # Lưu cửa sổ cha
        self.parent = parent

        # Lưu ngày đang được chọn
        self.selected_date = selected_date

        # Lưu hàm callback khi chọn ngày
        self.on_date_selected = on_date_selected

        # Lưu bảng màu
        self.colors = colors

        # Lưu tháng hiện tại
        self.current_month = selected_date.month

        # Lưu năm hiện tại
        self.current_year = selected_date.year

        # Đặt tiêu đề popup
        self.title("Chọn ngày")

        # Đặt kích thước popup
        self.geometry("360x390")

        # Không cho thay đổi kích thước popup
        self.resizable(False, False)

        # Đặt màu nền popup
        self.configure(fg_color=self.colors["bg_main"])

        # Cho popup nằm trên cửa sổ chính
        self.transient(parent)

        # Bắt người dùng xử lý popup trước
        self.grab_set()

        # Gọi hàm vẽ lịch
        self.draw_calendar()

    # Hàm vẽ lịch
    def draw_calendar(self):
        # Xóa các widget cũ trong popup
        for widget in self.winfo_children():
            # Xóa từng widget
            widget.destroy()

        # Tạo frame chính trong popup
        main_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors["frame_color"],
            corner_radius=14
        )

        # Đặt frame chính lên popup
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # Tạo frame header chứa nút tháng trước, tháng sau
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )

        # Đặt header lên giao diện
        header_frame.pack(fill="x", padx=10, pady=(10, 5))

        # Tạo nút tháng trước
        prev_button = ctk.CTkButton(
            header_frame,
            text="<",
            width=42,
            height=34,
            command=self.prev_month
        )

        # Đặt nút tháng trước bên trái
        prev_button.pack(side="left")

        # Tạo label hiển thị tháng/năm
        month_year_label = ctk.CTkLabel(
            header_frame,
            text=f"Tháng {self.current_month} / {self.current_year}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["text_color"]
        )

        # Đặt label tháng/năm ở giữa
        month_year_label.pack(side="left", expand=True)

        # Tạo nút tháng sau
        next_button = ctk.CTkButton(
            header_frame,
            text=">",
            width=42,
            height=34,
            command=self.next_month
        )

        # Đặt nút tháng sau bên phải
        next_button.pack(side="right")

        # Tạo frame chứa thứ trong tuần
        week_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )

        # Đặt frame thứ trong tuần lên giao diện
        week_frame.pack(fill="x", padx=10, pady=5)

        # Danh sách thứ trong tuần
        week_days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]

        # Duyệt danh sách thứ
        for i, day_name in enumerate(week_days):
            # Tạo label cho từng thứ
            label = ctk.CTkLabel(
                week_frame,
                text=day_name,
                width=42,
                text_color=self.colors["sub_text_color"],
                font=ctk.CTkFont(size=13, weight="bold")
            )

            # Đặt label thứ lên giao diện
            label.grid(row=0, column=i, padx=2, pady=2)

        # Tạo frame chứa các ngày trong tháng
        days_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )

        # Đặt frame ngày lên giao diện
        days_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Lấy ma trận lịch của tháng hiện tại
        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)

        # Duyệt từng tuần
        for row_index, week in enumerate(month_calendar):
            # Duyệt từng ngày trong tuần
            for col_index, day in enumerate(week):
                # Nếu day bằng 0 tức là ô trống
                if day == 0:
                    # Tạo label trống
                    empty_label = ctk.CTkLabel(
                        days_frame,
                        text="",
                        width=42,
                        height=36
                    )

                    # Đặt label trống lên giao diện
                    empty_label.grid(row=row_index, column=col_index, padx=2, pady=2)

                # Nếu là ngày thật
                else:
                    # Kiểm tra ngày này có phải ngày đang chọn không
                    is_selected = (
                        day == self.selected_date.day
                        and self.current_month == self.selected_date.month
                        and self.current_year == self.selected_date.year
                    )

                    # Tạo nút ngày
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

                    # Đặt nút ngày lên giao diện
                    day_button.grid(row=row_index, column=col_index, padx=2, pady=2)

        # Tạo nút chọn hôm nay
        today_button = ctk.CTkButton(
            main_frame,
            text="Hôm nay",
            height=36,
            fg_color="#4b5563",
            hover_color="#374151",
            command=self.choose_today
        )

        # Đặt nút hôm nay lên giao diện
        today_button.pack(fill="x", padx=10, pady=(5, 12))

    # Hàm chuyển sang tháng trước
    def prev_month(self):
        # Giảm tháng đi 1
        self.current_month -= 1

        # Nếu tháng nhỏ hơn 1
        if self.current_month < 1:
            # Chuyển về tháng 12
            self.current_month = 12

            # Giảm năm đi 1
            self.current_year -= 1

        # Vẽ lại lịch
        self.draw_calendar()

    # Hàm chuyển sang tháng sau
    def next_month(self):
        # Tăng tháng lên 1
        self.current_month += 1

        # Nếu tháng lớn hơn 12
        if self.current_month > 12:
            # Chuyển về tháng 1
            self.current_month = 1

            # Tăng năm lên 1
            self.current_year += 1

        # Vẽ lại lịch
        self.draw_calendar()

    # Hàm chọn một ngày cụ thể
    def choose_date(self, day):
        # Tạo ngày được chọn
        selected_date = datetime(self.current_year, self.current_month, day)

        # Gửi ngày được chọn về MainView
        self.on_date_selected(selected_date)

        # Đóng popup
        self.destroy()

    # Hàm chọn ngày hôm nay
    def choose_today(self):
        # Lấy ngày hôm nay
        selected_date = datetime.today()

        # Gửi ngày hôm nay về MainView
        self.on_date_selected(selected_date)

        # Đóng popup
        self.destroy()