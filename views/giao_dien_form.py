import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class GiaoDienForm(tk.Toplevel):

    def __init__(self, parent, ham_callback, du_lieu=None, index=None):

        super().__init__(parent)

        self.ham_callback = ham_callback

        self.index = index

        self.title("Form Chi Tiêu")

        self.geometry("400x350")

        tk.Label(self, text="Ngày").pack(pady=5)

        self.o_ngay = tk.Entry(self)

        self.o_ngay.pack()

        tk.Label(self, text="Danh mục").pack(pady=5)

        self.o_danh_muc = tk.Entry(self)

        self.o_danh_muc.pack()

        tk.Label(self, text="Số tiền").pack(pady=5)

        self.o_so_tien = tk.Entry(self)

        self.o_so_tien.pack()

        tk.Label(self, text="Loại").pack(pady=5)

        self.combo_loai = ttk.Combobox(
            self,
            values=["Thu", "Chi"],
            state="readonly"
        )

        self.combo_loai.pack()

        tk.Label(self, text="Ghi chú").pack(pady=5)

        self.o_ghi_chu = tk.Entry(self)

        self.o_ghi_chu.pack()

        tk.Button(
            self,
            text="Lưu",
            command=self.luu_du_lieu
        ).pack(pady=15)

        if du_lieu:
            self.hien_du_lieu(du_lieu)

    def hien_du_lieu(self, du_lieu):

        self.o_ngay.insert(0, du_lieu["Ngay"])

        self.o_danh_muc.insert(0, du_lieu["DanhMuc"])

        self.o_so_tien.insert(0, du_lieu["SoTien"])

        self.combo_loai.set(du_lieu["Loai"])

        self.o_ghi_chu.insert(0, du_lieu["GhiChu"])

    def luu_du_lieu(self):

        if self.o_ngay.get() == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập ngày")
            return

        if self.o_so_tien.get() == "":
            messagebox.showerror("Lỗi", "Vui lòng nhập số tiền")
            return

        try:
            so_tien = float(self.o_so_tien.get())

        except:
            messagebox.showerror("Lỗi", "Số tiền phải là số")
            return

        du_lieu = {
            "Ngay": self.o_ngay.get(),
            "DanhMuc": self.o_danh_muc.get(),
            "SoTien": so_tien,
            "Loai": self.combo_loai.get(),
            "GhiChu": self.o_ghi_chu.get()
        }

        self.ham_callback(du_lieu, self.index)

        self.destroy()