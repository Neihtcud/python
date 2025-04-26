import csv
import datetime

class NhanVien:
    def __init__(self, ma_nv, ho_ten, cccd):
        self.ma_nv = ma_nv
        self.ho_ten = ho_ten
        self.cccd = cccd

    def tinh_thu_nhap(self):
        pass

    def loai_nhan_vien(self):
        pass

    def to_dict(self):
        return {
            "MaNV": self.ma_nv,
            "HoTen": self.ho_ten,
            "CCCD": self.cccd,
            "Loai": self.loai_nhan_vien(),
            "ThuNhap": self.tinh_thu_nhap()
        }

    def __str__(self):
        return f"{self.ma_nv} - {self.ho_ten} - {self.cccd}"

class NhanVienFullTime(NhanVien):
    def __init__(self, ma_nv, ho_ten, cccd, so_ngay_lam, luong_ngay):
        super().__init__(ma_nv, ho_ten, cccd)
        self.so_ngay_lam = so_ngay_lam
        self.luong_ngay = luong_ngay

    def tinh_thu_nhap(self):
        tien_thuong = 0
        tien_phat = 0
        if self.so_ngay_lam > 24:
            tien_thuong = (self.so_ngay_lam - 24) * 0.1 * self.luong_ngay
        if self.so_ngay_lam < 22:
            tien_phat = 1000000
        elif self.so_ngay_lam < 24:
            tien_phat = 500000
        return self.so_ngay_lam * self.luong_ngay + tien_thuong - tien_phat

    def loai_nhan_vien(self):
        return "FullTime"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "SoNgayLam": self.so_ngay_lam,
            "LuongNgay": self.luong_ngay
        })
        return data

class NhanVienPartTime(NhanVien):
    def __init__(self, ma_nv, ho_ten, cccd, so_gio_lam, luong_gio):
        super().__init__(ma_nv, ho_ten, cccd)
        self.so_gio_lam = so_gio_lam
        self.luong_gio = luong_gio

    def tinh_thu_nhap(self):
        tien_thuong = 0
        if self.so_gio_lam > 140:
            tien_thuong = 1000000
        elif self.so_gio_lam > 100:
            tien_thuong = 500000
        return self.so_gio_lam * self.luong_gio + tien_thuong

    def loai_nhan_vien(self):
        return "PartTime"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "SoGioLam": self.so_gio_lam,
            "LuongGio": self.luong_gio
        })
        return data

class QLNV:
    def __init__(self):
        self.ds_nv = []

    def them_nhan_vien(self, nv):
        self.ds_nv.append(nv)

    def tim_nhan_vien(self, ma_nv):
        for nv in self.ds_nv:
            if nv.ma_nv == ma_nv:
                return nv
        return None

    def tim_kiem_nhan_vien(self, tu_khoa):
        ket_qua = []
        tu_khoa = tu_khoa.lower()
        for nv in self.ds_nv:
            if (tu_khoa in nv.ma_nv.lower() or
                tu_khoa in nv.ho_ten.lower() or
                tu_khoa in nv.cccd.lower()):
                ket_qua.append(nv)
        return ket_qua

    def sua_nhan_vien(self, ma_nv):
        nv = self.tim_nhan_vien(ma_nv)
        if nv:
            nv.ho_ten = input("Nhập họ tên mới: ")
            nv.cccd = input("Nhập CCCD mới: ")
            if isinstance(nv, NhanVienFullTime):
                nv.so_ngay_lam = int(input("Nhập số ngày làm mới: "))
                nv.luong_ngay = int(input("Nhập lương theo ngày mới: "))
            elif isinstance(nv, NhanVienPartTime):
                nv.so_gio_lam = int(input("Nhập số giờ làm mới: "))
                nv.luong_gio = int(input("Nhập lương theo giờ mới: "))
        else:
            print("Không tìm thấy nhân viên")

    def xoa_nhan_vien(self, ma_nv):
        nv = self.tim_nhan_vien(ma_nv)
        if nv:
            self.ds_nv.remove(nv)
        else:
            print("Không tìm thấy nhân viên")

    def ghi_file_csv(self, filename):
        if not self.ds_nv:
            print("Danh sách rỗng.")
            return
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.ds_nv[0].to_dict().keys())
            writer.writeheader()
            for nv in self.ds_nv:
                writer.writerow(nv.to_dict())

    def doc_file_csv(self, filename):
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Loai'] == 'FullTime':
                        nv = NhanVienFullTime(row['MaNV'], row['HoTen'], row['CCCD'], int(row['SoNgayLam']), int(row['LuongNgay']))
                    else:
                        nv = NhanVienPartTime(row['MaNV'], row['HoTen'], row['CCCD'], int(row['SoGioLam']), int(row['LuongGio']))
                    self.ds_nv.append(nv)
        except FileNotFoundError:
            print("Không tìm thấy file")

    def menu_nhap_nhan_vien(self):
        while True:
            print("1. Nhập nhân viên FullTime")
            print("2. Nhập nhân viên PartTime")
            print("0. Quay lại menu chính")
            loai = input("Chọn loại nhân viên (1-2) hoặc 0 để quay lại: ")

            if loai == "0":
                break

            ma_nv = input("Nhập mã nhân viên: ")
            if self.tim_nhan_vien(ma_nv):
                print("❌ Mã nhân viên đã tồn tại!")
                continue

            ho_ten = input("Nhập họ tên: ")
            cccd = input("Nhập số CCCD: ")

            if loai == "1":
                so_ngay_lam = int(input("Nhập số ngày làm trong tháng: "))
                luong_ngay = int(input("Nhập lương theo ngày: "))
                nv = NhanVienFullTime(ma_nv, ho_ten, cccd, so_ngay_lam, luong_ngay)
            elif loai == "2":
                so_gio_lam = int(input("Nhập số giờ làm trong tháng: "))
                luong_gio = int(input("Nhập lương theo giờ: "))
                nv = NhanVienPartTime(ma_nv, ho_ten, cccd, so_gio_lam, luong_gio)
            else:
                print("❌ Lựa chọn không hợp lệ.")
                continue

            self.them_nhan_vien(nv)

            tiep = input("👉 Nhập tiếp? (Enter để tiếp tục, 'k' để dừng): ")
            if tiep.lower() == 'k':
                break

    def xuat_danh_sach(self):
        for nv in self.ds_nv:
            print(nv, "| Thu nhập:", nv.tinh_thu_nhap())

    def loc_theo_loai(self, loai_nv):
        ket_qua = [nv for nv in self.ds_nv if nv.loai_nhan_vien().lower() == loai_nv.lower()]
        for nv in ket_qua:
            print(nv, "| Thu nhập:", nv.tinh_thu_nhap())

    def loc_theo_thu_nhap(self, muc_luong):
        ket_qua = [nv for nv in self.ds_nv if nv.tinh_thu_nhap() >= muc_luong]
        for nv in ket_qua:
            print(nv, "| Thu nhập:", nv.tinh_thu_nhap())

    def sap_xep_theo_thu_nhap(self):
        self.ds_nv.sort(key=lambda nv: nv.tinh_thu_nhap(), reverse=True)
        print("\n📉 Danh sách đã được sắp xếp theo thu nhập giảm dần:")
        self.xuat_danh_sach()

    def thong_ke_cong_ty(self):
        tong_nv = len(self.ds_nv)
        fulltime = [nv for nv in self.ds_nv if nv.loai_nhan_vien() == "FullTime"]
        parttime = [nv for nv in self.ds_nv if nv.loai_nhan_vien() == "PartTime"]
        thu_nhap_full = sum(nv.tinh_thu_nhap() for nv in fulltime)
        thu_nhap_part = sum(nv.tinh_thu_nhap() for nv in parttime)

        print(f"📊 Tổng số nhân viên: {tong_nv}")
        print(f"📊 Số nhân viên FullTime: {len(fulltime)}")
        print(f"📊 Số nhân viên PartTime: {len(parttime)}")
        print(f"📊 Thu nhập trung bình toàn công ty: {thu_nhap_full + thu_nhap_part:.0f} / {tong_nv} = {(thu_nhap_full + thu_nhap_part) / tong_nv if tong_nv else 0:.0f} VND")

    def xuat_file_thong_ke(self, filename):
        tong_nv = len(self.ds_nv)
        fulltime = [nv for nv in self.ds_nv if nv.loai_nhan_vien() == "FullTime"]
        parttime = [nv for nv in self.ds_nv if nv.loai_nhan_vien() == "PartTime"]
        thu_nhap_full = sum(nv.tinh_thu_nhap() for nv in fulltime)
        thu_nhap_part = sum(nv.tinh_thu_nhap() for nv in parttime)
        tb_full = thu_nhap_full / len(fulltime) if fulltime else 0
        tb_part = thu_nhap_part / len(parttime) if parttime else 0
        tb_all = (thu_nhap_full + thu_nhap_part) / tong_nv if tong_nv else 0

        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Thông tin", "Giá trị"])
            writer.writerow(["Tổng số nhân viên", tong_nv])
            writer.writerow(["Số nhân viên FullTime", f"{len(fulltime)} ({len(fulltime)/tong_nv*100:.0f}%)" if tong_nv else "0 (0%)"])
            writer.writerow(["Số nhân viên PartTime", f"{len(parttime)} ({len(parttime)/tong_nv*100:.0f}%)" if tong_nv else "0 (0%)"])
            writer.writerow(["Thu nhập trung bình toàn công ty", f"{tb_all:,.0f} VNĐ"])
            writer.writerow(["Thu nhập trung bình FullTime", f"{tb_full:,.0f} VNĐ"])
            writer.writerow(["Thu nhập trung bình PartTime", f"{tb_part:,.0f} VNĐ"])
        print(f"✅ Đã xuất file thống kê vào: {filename}")

def menu():
    qlnv = QLNV()
    while True:
        print("\n========= MENU =========")
        print("1. ➕ Thêm nhân viên mới")
        print("2. 🛠️ Cập nhật thông tin nhân viên")
        print("3. 🗑️ Xoá nhân viên")
        print("4. 🔍 Tìm kiếm nhân viên (mã, tên, CCCD)")
        print("5. 📑 Hiển thị danh sách nhân viên")
        print("6. 📂 Đọc danh sách từ file CSV")
        print("7. 💾 Ghi danh sách ra file CSV")
        print("8. 📊 Thống kê toàn công ty")
        print("9. 📉 Sắp xếp theo thu nhập giảm dần")
        print("10. 🔎 Lọc nhân viên theo loại hoặc mức lương")
        print("11. 📄 Xuất file thống kê")
        print("0. 🚪 Thoát chương trình")
        chon = input("\n👉 Chọn chức năng (0-11): ")

        if chon == "1":
            qlnv.menu_nhap_nhan_vien()
        elif chon == "2":
            ma = input("Nhập mã nhân viên cần sửa: ")
            qlnv.sua_nhan_vien(ma)
        elif chon == "3":
            ma = input("Nhập mã nhân viên cần xoá: ")
            qlnv.xoa_nhan_vien(ma)
        elif chon == "4":
            tu_khoa = input("🔍 Nhập mã, tên hoặc CCCD để tìm kiếm: ")
            ket_qua = qlnv.tim_kiem_nhan_vien(tu_khoa)
            if ket_qua:
                print("\n✅ Kết quả tìm kiếm:")
                for nv in ket_qua:
                    print(nv, "| Thu nhập:", nv.tinh_thu_nhap())
            else:
                print("❌ Không tìm thấy nhân viên nào.")
        elif chon == "5":
            qlnv.xuat_danh_sach()
        elif chon == "6":
            tenfile = input("Nhập tên file CSV để đọc: ")
            qlnv.doc_file_csv(tenfile)
        elif chon == "7":
            tenfile = input("Nhập tên file CSV để ghi: ")
            qlnv.ghi_file_csv(tenfile)
        elif chon == "8":
            qlnv.thong_ke_cong_ty()
        elif chon == "9":
            qlnv.sap_xep_theo_thu_nhap()
        elif chon == "10":
            loai = input("Nhập loại nhân viên cần lọc (FullTime/PartTime hoặc để trống): ")
            if loai:
                qlnv.loc_theo_loai(loai)
            else:
                muc = float(input("Nhập mức thu nhập tối thiểu: "))
                qlnv.loc_theo_thu_nhap(muc)
        elif chon == "11":
            tenfile = input("Nhập tên file để lưu thống kê: ")
            qlnv.xuat_file_thong_ke(tenfile)
        elif chon == "0":
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    menu()
