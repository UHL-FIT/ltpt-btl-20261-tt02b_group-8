# Import customtkinter de tao giao dien
import customtkinter as ctk


# Tao lop ButtonFrame, quan ly cac nut chuc nang
class ButtonFrame(ctk.CTkFrame):
    # Ham khoi tao ButtonFrame
    def __init__(
        self,
        parent,
        colors,
        add_callback,
        update_callback,
        delete_callback,
        clear_callback,
        summary_callback
    ):
        # Goi ham khoi tao cua CTkFrame
        super().__init__(parent, fg_color=colors["frame_color"], corner_radius=14)

        # Luu cac ham callback
        self.add_callback = add_callback
        self.update_callback = update_callback
        self.delete_callback = delete_callback
        self.clear_callback = clear_callback
        self.summary_callback = summary_callback

        # Tao cac nut
        self.create_widgets()

    # Ham tao cac nut chuc nang
    def create_widgets(self):
        # Cho 5 cot co gian deu
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

        # Tao nut them giao dich, khi bam se mo cua so them
        add_button = ctk.CTkButton(self, text="Thêm giao dịch", height=40, command=self.add_callback)
        add_button.grid(row=0, column=0, padx=10, pady=12, sticky="ew")

        # Tao nut sua thong tin, khi bam se mo cua so sua
        update_button = ctk.CTkButton(self, text="Sửa thông tin", height=40, command=self.update_callback)
        update_button.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        # Tao nut xoa thong tin
        delete_button = ctk.CTkButton(
            self,
            text="Xóa thông tin",
            height=40,
            fg_color="#c0392b",
            hover_color="#a93226",
            command=self.delete_callback
        )
        delete_button.grid(row=0, column=2, padx=10, pady=12, sticky="ew")

        # Tao nut bo chon dong dang chon
        clear_button = ctk.CTkButton(
            self,
            text="Bỏ chọn",
            height=40,
            fg_color="#4b5563",
            hover_color="#374151",
            command=self.clear_callback
        )
        clear_button.grid(row=0, column=3, padx=10, pady=12, sticky="ew")

        # Tao nut xem tong quan tai chinh
        summary_button = ctk.CTkButton(
            self,
            text="Xem tổng quan",
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.summary_callback
        )
        summary_button.grid(row=0, column=4, padx=10, pady=12, sticky="ew")
