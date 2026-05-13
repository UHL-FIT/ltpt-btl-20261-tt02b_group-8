import tkinter as tk

class GiaoDienAbout(tk.Toplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Thông Tin")

        self.geometry("300x200")

        tk.Label(
            self,
            text="QUẢN LÝ CHI TIÊU CÁ NHÂN",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tk.Label(
            self,
            text="Phiên bản: 1.0"
        ).pack()

        tk.Label(
            self,
            text="Sử dụng Tkinter + Pandas"
        ).pack(pady=5)

        tk.Label(
            self,
            text="Nhóm sinh viên thực hiện"
        ).pack(pady=5)