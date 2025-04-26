import csv
import os
import shutil
import time
import matplotlib.pyplot as plt

# =========================
# Các lớp Khách hàng
# =========================
class Customer:
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email):
        self.ma_khach_hang = ma_khach_hang
        self.ten_khach_hang = ten_khach_hang
        self.so_dien_thoai = so_dien_thoai
        self.email = email

class LoyalCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)

class CasualCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email, so_lan_mua_hang=0, tong_gia_tri_mua_hang=0):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)
        self.so_lan_mua_hang = so_lan_mua_hang
        self.tong_gia_tri_mua_hang = tong_gia_tri_mua_hang

# =========================
# Lớp quản lý khách hàng
# =========================
class ManageCustomer:
    def __init__(self, filename='khachhang.csv'):
        self.danh_sach_khach_hang = []
        self.filename = filename
        self.doc_file()

    def doc_file(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Loai'] == 'Loyal':
                    kh = LoyalCustomer(row['MaKH'], row['TenKH'], row['SDT'], row['Email'])
                else:
                    so_lan_mua = int(row['SoLanMua']) if row['SoLanMua'] else 0
                    tong_gia_tri = float(row['TongGiaTri']) if row['TongGiaTri'] else 0
                    kh = CasualCustomer(row['MaKH'], row['TenKH'], row['SDT'], row['Email'], so_lan_mua, tong_gia_tri)
                self.danh_sach_khach_hang.append(kh)

    def backup_file(self):
        if os.path.exists(self.filename):
            shutil.copy(self.filename, f"backup_{self.filename}")

    def ghi_file(self):
        self.backup_file()
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for kh in self.danh_sach_khach_hang:
                if isinstance(kh, LoyalCustomer):
                    writer.writerow({'Loai': 'Loyal', 'MaKH': kh.ma_khach_hang, 'TenKH': kh.ten_khach_hang,
                                     'SDT': kh.so_dien_thoai, 'Email': kh.email})
                else:
                    writer.writerow({'Loai': 'Casual', 'MaKH': kh.ma_khach_hang, 'TenKH': kh.ten_khach_hang,
                                     'SDT': kh.so_dien_thoai, 'Email': kh.email,
                                     'SoLanMua': kh.so_lan_mua_hang, 'TongGiaTri': kh.tong_gia_tri_mua_hang})

    def tim_kiem(self, ma_kh=None, ten=None, sdt=None, email=None):
        ket_qua = []
        for kh in self.danh_sach_khach_hang:
            if (not ma_kh or ma_kh.lower() in kh.ma_khach_hang.lower()) and \
               (not ten or ten.lower() in kh.ten_khach_hang.lower()) and \
               (not sdt or sdt in kh.so_dien_thoai) and \
               (not email or email.lower() in kh.email.lower()):
                ket_qua.append(kh)
        return ket_qua

    def them_khach_hang(self, khach_hang):
        if self.tim_kiem(ma_kh=khach_hang.ma_khach_hang):
            print("\033[91mMã khách hàng đã tồn tại!\033[0m")
            return
        self.danh_sach_khach_hang.append(khach_hang)
        self.ghi_file()
        print("\033[92m✔ Thêm khách hàng thành công.\033[0m")

    def sua_thong_tin(self, ma_khach_hang, ten_moi, email_moi):
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if kh:
            kh.ten_khach_hang = ten_moi
            kh.email = email_moi
            self.ghi_file()
            print("\033[92m✔ Cập nhật thành công.\033[0m")
        else:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")

    def xoa_khach_hang(self, ma_khach_hang):
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if kh:
            confirm = input("\033[91mBạn có chắc chắn muốn xoá khách hàng này? (y/n): \033[0m")
            if confirm.lower() == 'y':
                self.danh_sach_khach_hang.remove(kh)
                self.ghi_file()
                print("\033[92m✔ Xóa thành công.\033[0m")
        else:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")

    def cap_nhat_mua_hang(self, ma_khach_hang, so_lan_mua, gia_tri):
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if isinstance(kh, CasualCustomer):
            kh.so_lan_mua_hang += so_lan_mua
            kh.tong_gia_tri_mua_hang += gia_tri
            if kh.tong_gia_tri_mua_hang > 2000000:
                self.danh_sach_khach_hang.remove(kh)
                kh_moi = LoyalCustomer(kh.ma_khach_hang, kh.ten_khach_hang, kh.so_dien_thoai, kh.email)
                self.danh_sach_khach_hang.append(kh_moi)
                print("\033[94mKhách hàng đã trở thành khách thân thiết!\033[0m")
            self.ghi_file()
            print("\033[92m✔ Cập nhật mua hàng thành công.\033[0m")
        else:
            print("\033[91mKhông áp dụng cho khách thân thiết.\033[0m")

    def hien_thi_danh_sach(self, key_sort=None, reverse=False):
        if key_sort:
            self.danh_sach_khach_hang.sort(key=lambda x: getattr(x, key_sort, ''), reverse=reverse)

        header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Số lần':<8} | {'Tổng tiền':<10} | {'Loại':<7}"
        print("\033[96m" + header + "\033[0m")
        print("-" * len(header))
        for kh in self.danh_sach_khach_hang:
            self.in_thong_tin(kh)

    def in_thong_tin(self, kh):
        if isinstance(kh, CasualCustomer):
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.so_lan_mua_hang:<8} | {kh.tong_gia_tri_mua_hang:<10,.0f} | Casual")
        else:
            print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {'-':<8} | {'-':<10} | Loyal")

    def thong_ke(self):
        loyal = sum(1 for kh in self.danh_sach_khach_hang if isinstance(kh, LoyalCustomer))
        casual = sum(1 for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer))
        doanh_thu = sum(kh.tong_gia_tri_mua_hang for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer))

        with open('thongke.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Loại', 'Số lượng', 'Doanh thu'])
            writer.writerow(['Loyal', loyal, '-'])
            writer.writerow(['Casual', casual, doanh_thu])

        labels = ['Loyal', 'Casual']
        values = [loyal, casual]
        plt.bar(labels, values, color=['green', 'blue'])
        plt.title('Thống kê số lượng khách hàng')
        plt.xlabel('Loại khách hàng')
        plt.ylabel('Số lượng')
        plt.show()

    def top_khach_hang(self, kieu='gia_tri'):
        casuals = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        if kieu == 'gia_tri':
            casuals.sort(key=lambda x: x.tong_gia_tri_mua_hang, reverse=True)
        else:
            casuals.sort(key=lambda x: x.so_lan_mua_hang, reverse=True)
        return casuals[:3]

# =========================
# Các hàm phụ trợ
# =========================
def nhap_sdt():
    while True:
        sdt = input("Số điện thoại (10 số): ")
        if sdt.isdigit() and len(sdt) == 10:
            return sdt
        print("\033[91mSố điện thoại không hợp lệ. Vui lòng nhập lại.\033[0m")

def loading():
    print("\033[93mĐang xử lý...\033[0m", end="")
    for _ in range(3):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print()

# =========================
# Main chương trình
# =========================
def main():
    ql = ManageCustomer()

    while True:
        print("\n\033[96m╔══════════════════════════════════════════════╗\033[0m")
        print("\033[96m║             QUẢN LÝ KHÁCH HÀNG                ║\033[0m")
        print("\033[96m╠══════════════════════════════════════════════╣\033[0m")
        print("\033[93m║ 1. Thêm khách hàng                            ║\033[0m")
        print("\033[93m║ 2. Sửa thông tin khách hàng                   ║\033[0m")
        print("\033[93m║ 3. Xóa khách hàng                             ║\033[0m")
        print("\033[93m║ 4. Cập nhật mua hàng                          ║\033[0m")
        print("\033[93m║ 5. Tìm kiếm khách hàng                        ║\033[0m")
        print("\033[93m║ 6. Hiển thị danh sách (có sắp xếp)             ║\033[0m")
        print("\033[93m║ 7. Thống kê và Vẽ biểu đồ                     ║\033[0m")
        print("\033[93m║ 8. Top 3 khách hàng mua nhiều                 ║\033[0m")
        print("\033[91m║ 0. Thoát                                       ║\033[0m")
        print("\033[96m╚══════════════════════════════════════════════╝\033[0m")
        choice = input("\033[95m>> Chọn chức năng (0-8): \033[0m")

        if choice == '1':
            ma = input("Mã KH: ")
            ten = input("Tên KH: ")
            sdt = nhap_sdt()
            email = input("Email: ")
            loai = input("Loại (Loyal/Casual): ").strip().capitalize()
            if loai == 'Loyal':
                kh = LoyalCustomer(ma, ten, sdt, email)
            else:
                kh = CasualCustomer(ma, ten, sdt, email)
            loading()
            ql.them_khach_hang(kh)

        elif choice == '2':
            ma = input("Nhập mã KH cần sửa: ")
            ten_moi = input("Tên mới: ")
            email_moi = input("Email mới: ")
            loading()
            ql.sua_thong_tin(ma, ten_moi, email_moi)

        elif choice == '3':
            ma = input("Nhập mã KH cần xóa: ")
            loading()
            ql.xoa_khach_hang(ma)

        elif choice == '4':
            ma = input("Nhập mã KH: ")
            so_lan = int(input("Số lần mua: "))
            gia_tri = float(input("Tổng giá trị đơn hàng: "))
            loading()
            ql.cap_nhat_mua_hang(ma, so_lan, gia_tri)

        elif choice == '5':
            ma = input("Mã KH (bỏ qua nếu không tìm theo mã): ")
            ten = input("Tên KH (bỏ qua nếu không tìm theo tên): ")
            sdt = input("SĐT (bỏ qua nếu không tìm theo SĐT): ")
            email = input("Email (bỏ qua nếu không tìm theo Email): ")
            ket_qua = ql.tim_kiem(ma_kh=ma, ten=ten, sdt=sdt, email=email)
            loading()
            if ket_qua:
              for kh in ket_qua:
               ql.in_thong_tin(kh)
            else:
               print("\033[91mKhông tìm thấy khách hàng.\033[0m")

        elif choice == '6':
            sort_field = input("Sắp xếp theo trường nào (ma_khach_hang/ten_khach_hang/so_dien_thoai/tong_gia_tri_mua_hang): ")
            order = input("Tăng (asc) hay giảm (desc)? ").strip().lower()
            loading()
            ql.hien_thi_danh_sach(key_sort=sort_field, reverse=(order == 'desc'))

        elif choice == '7':
            loading()
            ql.thong_ke()

        elif choice == '8':
            kieu = input("Lọc theo tổng tiền hay số lần mua (gia_tri/so_lan): ").strip()
            top = ql.top_khach_hang(kieu)
            for kh in top:
                ql.in_thong_tin(kh)

        elif choice == '0':
            print("\033[92mCảm ơn bạn đã sử dụng chương trình. Tạm biệt!\033[0m")
            break
        else:
            print("\033[91m❌ Lựa chọn không hợp lệ. Vui lòng chọn lại!\033[0m")

if __name__ == '__main__':
    main()

