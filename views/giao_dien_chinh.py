import tkinter as tk
from tkinter import ttk

class GiaoDienChinh(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("Quản Lý Chi Tiêu Cá Nhân")

        self.geometry("900x500")

        tieu_de = tk.Label(
            self,
            text="QUẢN LÝ CHI TIÊU CÁ NHÂN",
            font=("Arial", 18, "bold")
        )

        tieu_de.pack(pady=10)

        khung_nut = tk.Frame(self)

        khung_nut.pack(pady=10)

        self.nut_them = tk.Button(
            khung_nut,
            text="Thêm",
            width=12
        )

        self.nut_them.grid(row=0, column=0, padx=5)

        self.nut_sua = tk.Button(
            khung_nut,
            text="Sửa",
            width=12
        )

        self.nut_sua.grid(row=0, column=1, padx=5)

        self.nut_xoa = tk.Button(
            khung_nut,
            text="Xóa",
            width=12
        )

        self.nut_xoa.grid(row=0, column=2, padx=5)

        self.nut_thong_ke = tk.Button(
            khung_nut,
            text="Thống Kê",
            width=12
        )

        self.nut_thong_ke.grid(row=0, column=3, padx=5)

        self.nut_about = tk.Button(
            khung_nut,
            text="About",
            width=12
        )

        self.nut_about.grid(row=0, column=4, padx=5)

        cot = (
            "Ngay",
            "DanhMuc",
            "SoTien",
            "Loai",
            "GhiChu"
        )

        self.bang = ttk.Treeview(
            self,
            columns=cot,
            show="headings"
        )

        for c in cot:

            self.bang.heading(c, text=c)

            self.bang.column(c, width=150)

        self.bang.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        self.label_thong_ke = tk.Label(
            self,
            text="Thống kê",
            font=("Arial", 12, "bold")
        )

        self.label_thong_ke.pack(pady=10)