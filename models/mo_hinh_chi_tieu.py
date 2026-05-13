import pandas as pd
import os

class MoHinhChiTieu:

    def __init__(self, duong_dan="data/chi_tieu.csv"):

        self.duong_dan = duong_dan

        if not os.path.exists(self.duong_dan):

            df = pd.DataFrame(columns=[
                "Ngay",
                "DanhMuc",
                "SoTien",
                "Loai",
                "GhiChu"
            ])

            df.to_csv(self.duong_dan, index=False)

    def tai_du_lieu(self):
        return pd.read_csv(self.duong_dan)

    def luu_du_lieu(self, df):
        df.to_csv(self.duong_dan, index=False)

    def them_chi_tieu(self, du_lieu):

        df = self.tai_du_lieu()

        dong_moi = pd.DataFrame([du_lieu])

        df = pd.concat([df, dong_moi], ignore_index=True)

        self.luu_du_lieu(df)

    def cap_nhat_chi_tieu(self, index, du_lieu):

        df = self.tai_du_lieu()

        df.loc[index, "Ngay"] = du_lieu["Ngay"]
        df.loc[index, "DanhMuc"] = du_lieu["DanhMuc"]
        df.loc[index, "SoTien"] = du_lieu["SoTien"]
        df.loc[index, "Loai"] = du_lieu["Loai"]
        df.loc[index, "GhiChu"] = du_lieu["GhiChu"]

        self.luu_du_lieu(df)

    def xoa_chi_tieu(self, index):

        df = self.tai_du_lieu()

        df = df.drop(index)

        df = df.reset_index(drop=True)

        self.luu_du_lieu(df)

    def thong_ke(self):

        df = self.tai_du_lieu()

        tong_thu = df[df["Loai"] == "Thu"]["SoTien"].sum()

        tong_chi = df[df["Loai"] == "Chi"]["SoTien"].sum()

        so_du = tong_thu - tong_chi

        return {
            "tong_thu": tong_thu,
            "tong_chi": tong_chi,
            "so_du": so_du
        }