from models.mo_hinh_chi_tieu import MoHinhChiTieu

from views.giao_dien_chinh import GiaoDienChinh
from views.giao_dien_form import GiaoDienForm
from views.giao_dien_about import GiaoDienAbout

from tkinter import messagebox

class DieuKhienChiTieu:

    def __init__(self):

        self.model = MoHinhChiTieu()

        self.view = GiaoDienChinh()

        self.view.nut_them.config(
            command=self.mo_form_them
        )

        self.view.nut_sua.config(
            command=self.mo_form_sua
        )

        self.view.nut_xoa.config(
            command=self.xoa_du_lieu
        )

        self.view.nut_thong_ke.config(
            command=self.hien_thong_ke
        )

        self.view.nut_about.config(
            command=self.hien_about
        )

        self.tai_bang()

    def chay_chuong_trinh(self):

        self.view.mainloop()

    def tai_bang(self):

        for row in self.view.bang.get_children():
            self.view.bang.delete(row)

        df = self.model.tai_du_lieu()

        for index, row in df.iterrows():

            self.view.bang.insert(
                "",
                "end",
                iid=index,
                values=(
                    row["Ngay"],
                    row["DanhMuc"],
                    row["SoTien"],
                    row["Loai"],
                    row["GhiChu"]
                )
            )

    def mo_form_them(self):

        GiaoDienForm(
            self.view,
            self.luu_du_lieu_moi
        )

    def luu_du_lieu_moi(self, du_lieu, index):

        self.model.them_chi_tieu(du_lieu)

        self.tai_bang()

    def mo_form_sua(self):

        selected = self.view.bang.selection()

        if not selected:

            messagebox.showerror(
                "Lỗi",
                "Vui lòng chọn dòng cần sửa"
            )

            return

        index = int(selected[0])

        df = self.model.tai_du_lieu()

        du_lieu = df.loc[index].to_dict()

        GiaoDienForm(
            self.view,
            self.luu_du_lieu_sua,
            du_lieu,
            index
        )

    def luu_du_lieu_sua(self, du_lieu, index):

        self.model.cap_nhat_chi_tieu(
            index,
            du_lieu
        )

        self.tai_bang()

    def xoa_du_lieu(self):

        selected = self.view.bang.selection()

        if not selected:

            messagebox.showerror(
                "Lỗi",
                "Vui lòng chọn dòng cần xóa"
            )

            return

        index = int(selected[0])

        xac_nhan = messagebox.askyesno(
            "Xác nhận",
            "Bạn có chắc muốn xóa?"
        )

        if xac_nhan:

            self.model.xoa_chi_tieu(index)

            self.tai_bang()

    def hien_thong_ke(self):

        thong_ke = self.model.thong_ke()

        noi_dung = (
            f"Tổng thu: {thong_ke['tong_thu']}\n"
            f"Tổng chi: {thong_ke['tong_chi']}\n"
            f"Số dư: {thong_ke['so_du']}"
        )

        self.view.label_thong_ke.config(
            text=noi_dung
        )

    def hien_about(self):

        GiaoDienAbout(self.view)