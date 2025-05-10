import os
import time
import re
import csv
import shutil
import datetime
import matplotlib.pyplot as plt

class Customer:
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email):
        self.ma_khach_hang = ma_khach_hang
        self.ten_khach_hang = ten_khach_hang
        self.so_dien_thoai = so_dien_thoai
        self.email = email
    
    def __str__(self):
        return f"{self.ma_khach_hang} - {self.ten_khach_hang}"
    
class LoyalCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email, diem_tich_luy=0, tong_gia_tri_mua_hang=0, so_lan_mua_hang=0):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)
        self.diem_tich_luy = int(diem_tich_luy) if isinstance(diem_tich_luy, str) else diem_tich_luy
        self.tong_gia_tri_mua_hang = float(tong_gia_tri_mua_hang) if isinstance(tong_gia_tri_mua_hang, str) else tong_gia_tri_mua_hang
        self.so_lan_mua_hang = int(so_lan_mua_hang) if isinstance(so_lan_mua_hang, str) else so_lan_mua_hang
    
    def __str__(self):
        return f"{super().__str__()} | Điểm tích lũy: {self.diem_tich_luy} | Số lần mua: {self.so_lan_mua_hang} | Tổng giá trị: {self.tong_gia_tri_mua_hang:,.0f}"
    
    def to_dict(self):
        return {
            "Loai": "Loyal",
            "MaKH": self.ma_khach_hang,
            "TenKH": self.ten_khach_hang,
            "SDT": self.so_dien_thoai,
            "Email": self.email,
            "SoLanMua": self.so_lan_mua_hang,
            "TongGiaTri": self.tong_gia_tri_mua_hang,
            "DiemTichLuy": self.diem_tich_luy
        }
    
    @classmethod
    def from_dict(cls, row):
        diem_tich_luy = int(row.get("DiemTichLuy", 0)) if row.get("DiemTichLuy") else 0
        tong_gia_tri = float(row.get("TongGiaTri", 0)) if row.get("TongGiaTri") else 0
        so_lan_mua = int(row.get("SoLanMua", 0)) if row.get("SoLanMua") else 0
        
        return cls(
            ma_khach_hang=row["MaKH"],
            ten_khach_hang=row["TenKH"],
            so_dien_thoai=row["SDT"],
            email=row["Email"],
            diem_tich_luy=diem_tich_luy,
            tong_gia_tri_mua_hang=tong_gia_tri,
            so_lan_mua_hang=so_lan_mua
        )
    
    # Thêm phương thức để chuyển đổi từ CasualCustomer
    @classmethod
    def from_casual_customer(cls, casual_customer, diem_tich_luy=0):
        return cls(
            ma_khach_hang=casual_customer.ma_khach_hang,
            ten_khach_hang=casual_customer.ten_khach_hang,
            so_dien_thoai=casual_customer.so_dien_thoai,
            email=casual_customer.email,
            diem_tich_luy=diem_tich_luy,
            tong_gia_tri_mua_hang=casual_customer.tong_gia_tri_mua_hang,
            so_lan_mua_hang=casual_customer.so_lan_mua_hang
        )

class CasualCustomer(Customer):
    def __init__(self, ma_khach_hang, ten_khach_hang, so_dien_thoai, email, so_lan_mua_hang=0, tong_gia_tri_mua_hang=0):
        super().__init__(ma_khach_hang, ten_khach_hang, so_dien_thoai, email)
        self.so_lan_mua_hang = int(so_lan_mua_hang) if isinstance(so_lan_mua_hang, str) else so_lan_mua_hang
        self.tong_gia_tri_mua_hang = float(tong_gia_tri_mua_hang) if isinstance(tong_gia_tri_mua_hang, str) else tong_gia_tri_mua_hang
    
    def tinh_trung_binh_gia_tri(self):
        if self.so_lan_mua_hang == 0:
            return 0
        return self.tong_gia_tri_mua_hang / self.so_lan_mua_hang
    
    def __str__(self):
        return f"{super().__str__()} | Số lần mua: {self.so_lan_mua_hang}, Tổng giá trị: {self.tong_gia_tri_mua_hang:,.0f}"
    
    def to_dict(self):
        return {
            "Loai": "Casual",
            "MaKH": self.ma_khach_hang,
            "TenKH": self.ten_khach_hang,
            "SDT": self.so_dien_thoai,
            "Email": self.email,
            "SoLanMua": self.so_lan_mua_hang,
            "TongGiaTri": self.tong_gia_tri_mua_hang,
            "DiemTichLuy": ""
        }
    
    @classmethod
    def from_dict(cls, row):
        so_lan_mua = int(row.get("SoLanMua", 0)) if row.get("SoLanMua") else 0
        tong_gia_tri = float(row.get("TongGiaTri", 0)) if row.get("TongGiaTri") else 0
        
        return cls(
            ma_khach_hang=row["MaKH"],
            ten_khach_hang=row["TenKH"],
            so_dien_thoai=row["SDT"],
            email=row["Email"],
            so_lan_mua_hang=so_lan_mua,
            tong_gia_tri_mua_hang=tong_gia_tri
        )
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def nhap_sdt():
    while True:
        sdt = input("Số điện thoại (10 số): ")
        if sdt.isdigit() and len(sdt) == 10:
            return sdt
        print("\033[91mSố điện thoại không hợp lệ. Vui lòng nhập lại.\033[0m")

def kiem_tra_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def nhap_email():
    while True:
        email = input("Email: ").strip()
        if kiem_tra_email(email):
            return email
        print("\033[91mEmail không hợp lệ. Vui lòng nhập lại.\033[0m")

def nhap_ten():
    while True:
        ten = input("Tên KH: ").strip()
        if len(ten) > 0 and all(c.isalpha() or c.isspace() for c in ten):
            return ten
        print("\033[91mTên không hợp lệ. Tên chỉ được chứa chữ cái và khoảng trắng.\033[0m")

def nhap_ma_khach_hang():
    while True:
        ma = input("Mã KH: ").strip().upper()
        if len(ma) > 0 and not ma.isspace():
            return ma
        print("\033[91mMã khách hàng không được để trống.\033[0m")

def loading(msg="Đang xử lý", dot_count=3, delay=0.4):
    print(f"\033[93m{msg}\033[0m", end="")
    for _ in range(dot_count):
        print(".", end="", flush=True)
        time.sleep(delay)
    print()

def xac_nhan(msg="Bạn có chắc chắn không?"):
    while True:
        choice = input(f"\033[93m{msg} (y/n): \033[0m").lower().strip()
        if choice == 'y':
            return True
        if choice == 'n':
            return False
        print("\033[91mVui lòng nhập 'y' hoặc 'n'.\033[0m")

# Thêm hai hàm mới để đọc và ghi dữ liệu khách hàng từ/vào file CSV
def read_customers_from_csv(filename):
    """
    Đọc dữ liệu khách hàng từ file CSV
    
    Args:
        filename (str): Đường dẫn đến file CSV
        
    Returns:
        list: Danh sách các dict chứa thông tin khách hàng
    """
    customers = []
    if not os.path.exists(filename):
        return customers  # Trả về danh sách rỗng nếu file không tồn tại
    
    try:
        with open(filename, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                customers.append(row)
        return customers
    except Exception as e:
        print(f"\033[91mLỗi khi đọc file CSV: {e}\033[0m")
        return []

def write_customers_to_csv(filename, customers):
    """
    Ghi danh sách khách hàng vào file CSV
    
    Args:
        filename (str): Đường dẫn đến file CSV
        customers (list): Danh sách các đối tượng khách hàng
        
    Returns:
        bool: True nếu ghi thành công, False nếu có lỗi
    """
    # Đảm bảo thư mục tồn tại
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Chuẩn bị dữ liệu để ghi
    customer_dicts = []
    for customer in customers:
        # Giả sử mỗi đối tượng khách hàng có phương thức to_dict()
        customer_dicts.append(customer.to_dict())
    
    # Xác định các trường dữ liệu từ khách hàng đầu tiên hoặc sử dụng các trường cố định
    fieldnames = ["Loai", "MaKH", "TenKH", "SDT", "Email", "DiemTichLuy", "SoLanMua", "TongGiaTri"]
    
    try:
        with open(filename, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(customer_dicts)
        return True
    except Exception as e:
        print(f"\033[91mLỗi khi ghi file CSV: {e}\033[0m")
        return False
def ghi_log(hanh_dong, khach_hang, log_file='log.txt'):
    try: 
        with open(log_file, 'a', encoding='utf-8') as f:
            thoi_gian = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            loai = "Loyal" if isinstance(khach_hang, LoyalCustomer) else "Casual"
            f.write(f"[{thoi_gian}] {hanh_dong} khách hàng: {khach_hang.ma_khach_hang} - {khach_hang.ten_khach_hang} - {loai}\n")
    except Exception as e:
        print(f"\033[91mLỗi ghi log: {e}\033[0m")

class ManageCustomer:
    def __init__(self, filename='khachhang.csv'):
        self.danh_sach_khach_hang = []
        self.filename = filename
        self.doc_file()

    def doc_file(self):
        """Đọc dữ liệu khách hàng từ file CSV"""
        if not os.path.exists(self.filename):
            # Tạo file mới nếu chưa tồn tại
            try:
                with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri', 'DiemTichLuy']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                print(f"\033[92mĐã tạo file dữ liệu mới: {self.filename}\033[0m")
            except Exception as e:
                print(f"\033[91mLỗi tạo file mới: {e}\033[0m")
            return
        
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        if row['Loai'] == 'Loyal':
                            kh = LoyalCustomer.from_dict(row)
                        else:
                            kh = CasualCustomer.from_dict(row)
                        self.danh_sach_khach_hang.append(kh)
                    except Exception as e:
                        print(f"\033[91mLỗi đọc dòng dữ liệu: {e}\033[0m")
                        continue
            print(f"\033[92mĐÃ ĐỌC {len(self.danh_sach_khach_hang)} KHÁCH HÀNG TỪ FILE\033[0m")
        except Exception as e:
            print(f"\033[91mLỗi đọc file: {e}\033[0m")
            # Tạo bản sao lưu của file lỗi và tạo file mới
            if os.path.exists(self.filename):
                corrupt_file = f"{self.filename}.corrupt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                try:
                    shutil.copy(self.filename, corrupt_file)
                    print(f"\033[93mĐã lưu file lỗi tại: {corrupt_file}\033[0m")
                    # Tạo file mới
                    with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                        fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri', 'DiemTichLuy']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                    print(f"\033[92mĐã tạo file dữ liệu mới: {self.filename}\033[0m")
                except Exception as e2:
                    print(f"\033[91mKhông thể khôi phục file lỗi: {e2}\033[0m")

    def ghi_file(self):
        """Ghi danh sách khách hàng vào file CSV"""
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['Loai', 'MaKH', 'TenKH', 'SDT', 'Email', 'SoLanMua', 'TongGiaTri', 'DiemTichLuy']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for kh in self.danh_sach_khach_hang:
                    writer.writerow(kh.to_dict())
                print("\033[92mLưu file thành công\033[0m")
                return True
        except Exception as e:
            print(f"\033[91mLỗi ghi file: {e}\033[0m")
            return False      

    def la_ma_kh_hop_le(self, ma_kh):
        """Kiểm tra mã khách hàng có hợp lệ không"""
        if not ma_kh or not isinstance(ma_kh, str):
            return False
        # Kiểm tra không rỗng và không chỉ chứa khoảng trắng
        return len(ma_kh.strip()) > 0

    def la_ten_kh_hop_le(self, ten_kh):
        """Kiểm tra tên khách hàng có hợp lệ không"""
        if not ten_kh or not isinstance(ten_kh, str):
            return False
        # Kiểm tra không rỗng và không chỉ chứa khoảng trắng
        return len(ten_kh.strip()) > 0
        
    def la_sdt_hop_le(self, sdt):
        """Kiểm tra số điện thoại có hợp lệ không"""
        if not sdt or not isinstance(sdt, str):
            return False
        return sdt.isdigit() and len(sdt) == 10

    def la_email_hop_le(self, email):
        """Kiểm tra email có hợp lệ không"""
        if not email:  # Email có thể để trống
            return True
        if not isinstance(email, str):
            return False
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def tim_kiem(self, loai=None, ten_chua=None, tong_gia_min=None, tong_gia_max=None, 
                 so_lan_mua_min=None,ten_chinh_xac=None, ma_kh=None, sdt_chua=None, email_chua=None, 
                 diem_tich_luy_min=None):
        """Hàm tìm kiếm với nhiều tiêu chí"""
       
        # Chuyển đổi giá trị số sang số nếu được cung cấp
        if tong_gia_min is not None:
            try:
                tong_gia_min = float(tong_gia_min)
            except (ValueError, TypeError):
                print("\033[91mGiá trị tối thiểu không hợp lệ!\033[0m")
                return []
                
        if tong_gia_max is not None:
            try:
                tong_gia_max = float(tong_gia_max)
            except (ValueError, TypeError):
                print("\033[91mGiá trị tối đa không hợp lệ!\033[0m")
                return []
                
        if so_lan_mua_min is not None:
            try:
                so_lan_mua_min = int(so_lan_mua_min)
            except (ValueError, TypeError):
                print("\033[91mSố lần mua tối thiểu không hợp lệ!\033[0m")
                return []
                
        if diem_tich_luy_min is not None:
            try:
                diem_tich_luy_min = int(diem_tich_luy_min)
            except (ValueError, TypeError):
                print("\033[91mĐiểm tích lũy tối thiểu không hợp lệ!\033[0m")
                return []
        
        ket_qua = []
        for kh in self.danh_sach_khach_hang:
            # Kiểm tra loại khách hàng
            if loai and not ((loai == 'Loyal' and isinstance(kh, LoyalCustomer)) or (loai == 'Casual' and isinstance(kh, CasualCustomer))):
                continue
                
            # Kiểm tra thông tin cơ bản
            if ten_chinh_xac and ten_chinh_xac.lower() != kh.ten_khach_hang.lower():
                continue
            if ten_chua and ten_chua.lower() not in kh.ten_khach_hang.lower():
                continue
            if ma_kh and kh.ma_khach_hang != ma_kh:
                continue
            if sdt_chua and sdt_chua not in kh.so_dien_thoai:
                continue
            if email_chua and (not kh.email or email_chua.lower() not in kh.email.lower()):
                continue
            
            # Kiểm tra thông tin đặc biệt cho cả hai loại khách hàng
            if tong_gia_min is not None:
                # Đảm bảo kh có thuộc tính tong_gia_tri_mua_hang trước khi so sánh
                if not hasattr(kh, 'tong_gia_tri_mua_hang') or kh.tong_gia_tri_mua_hang < tong_gia_min:
                    continue
                    
            if tong_gia_max is not None:
                # Đảm bảo kh có thuộc tính tong_gia_tri_mua_hang trước khi so sánh
                if not hasattr(kh, 'tong_gia_tri_mua_hang') or kh.tong_gia_tri_mua_hang > tong_gia_max:
                    continue
                    
            if so_lan_mua_min is not None:
                # Đảm bảo kh có thuộc tính so_lan_mua_hang trước khi so sánh
                if not hasattr(kh, 'so_lan_mua_hang') or kh.so_lan_mua_hang < so_lan_mua_min:
                    continue
                
            if diem_tich_luy_min is not None:
                if not isinstance(kh, LoyalCustomer) or not hasattr(kh, 'diem_tich_luy') or kh.diem_tich_luy < diem_tich_luy_min:
                   continue       
                
            ket_qua.append(kh)
        return ket_qua

    def them_khach_hang(self, khach_hang):
        # Kiểm tra thông tin bắt buộc
        if not self.la_ma_kh_hop_le(khach_hang.ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
            
        if not self.la_ten_kh_hop_le(khach_hang.ten_khach_hang):
            print("\033[91mTên khách hàng không hợp lệ!\033[0m")
            return False
        
        if not self.la_sdt_hop_le(khach_hang.so_dien_thoai):
            print("\033[91mSố điện thoại không hợp lệ!\033[0m")
            return False
        
        if not self.la_email_hop_le(khach_hang.email):
            print("\033[91mEmail không hợp lệ!\033[0m")
            return False
            
        # Kiểm tra trùng lặp
        for kh in self.danh_sach_khach_hang:
            if kh.ma_khach_hang == khach_hang.ma_khach_hang:
                print("\033[91mMã khách hàng đã tồn tại!\033[0m")
                return False
            if kh.so_dien_thoai == khach_hang.so_dien_thoai:
                print("\033[91mSố điện thoại đã tồn tại!\033[0m")
                return False
        
            if kh.email and khach_hang.email and kh.email == khach_hang.email:
                print("\033[91mEmail đã tồn tại!\033[0m")
                return False

        # Đảm bảo thiết lập giá trị mặc định cho cả hai loại khách hàng
        if isinstance(khach_hang, LoyalCustomer):
            if not hasattr(khach_hang, 'so_lan_mua_hang') or khach_hang.so_lan_mua_hang is None:
                khach_hang.so_lan_mua_hang = 0
            if not hasattr(khach_hang, 'tong_gia_tri_mua_hang') or khach_hang.tong_gia_tri_mua_hang is None:
                khach_hang.tong_gia_tri_mua_hang = 0
            # Đảm bảo khởi tạo diem_tich_luy
            if not hasattr(khach_hang, 'diem_tich_luy') or khach_hang.diem_tich_luy is None:
                khach_hang.diem_tich_luy = 0
        elif isinstance(khach_hang, CasualCustomer):  # Thêm khởi tạo cho CasualCustomer
            if not hasattr(khach_hang, 'so_lan_mua_hang') or khach_hang.so_lan_mua_hang is None:
                khach_hang.so_lan_mua_hang = 0
            if not hasattr(khach_hang, 'tong_gia_tri_mua_hang') or khach_hang.tong_gia_tri_mua_hang is None:
                khach_hang.tong_gia_tri_mua_hang = 0

        self.danh_sach_khach_hang.append(khach_hang)
        self.ghi_file()
        ghi_log("Thêm", khach_hang)
        print("\033[92m✔ Thêm khách hàng thành công.\033[0m")
        return True
        
    def sua_thong_tin(self, ma_khach_hang, ten_moi=None, email_moi=None, sdt_moi=None):
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
        
        # Kiểm tra tên mới nếu có
        if ten_moi and not self.la_ten_kh_hop_le(ten_moi):
            print("\033[91mTên khách hàng mới không hợp lệ!\033[0m")
            return False
            
        # Kiểm tra số điện thoại mới nếu có
        if sdt_moi and not self.la_sdt_hop_le(sdt_moi):
            print("\033[91mSố điện thoại mới không hợp lệ!\033[0m")
            return False
        
        # Kiểm tra email mới nếu có
        if email_moi and not self.la_email_hop_le(email_moi):
            print("\033[91mEmail mới không hợp lệ!\033[0m")
            return False
    
        # Tìm khách hàng cần sửa
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
        if not kh:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False
        
        # Kiểm tra trùng lặp số điện thoại 
        if sdt_moi and sdt_moi != kh.so_dien_thoai:
            if any(k.so_dien_thoai == sdt_moi for k in self.danh_sach_khach_hang if k.ma_khach_hang != ma_khach_hang):
               print("\033[91mSố điện thoại đã tồn tại!\033[0m")
               return False
    
        # Kiểm tra trùng lặp email 
        if email_moi and email_moi != kh.email:
            # Chỉ kiểm tra với các khách hàng khác có email
            if any(k.email and k.email == email_moi for k in self.danh_sach_khach_hang if k.ma_khach_hang != ma_khach_hang):
               print("\033[91mEmail đã tồn tại!\033[0m")
               return False
    
        # Cập nhật thông tin khi đã kiểm tra xong
        changed = False  # Cờ đánh dấu xem có gì thay đổi không
    
        if ten_moi and ten_moi != kh.ten_khach_hang:
            kh.ten_khach_hang = ten_moi
            changed = True
        
        if email_moi and email_moi != kh.email:
            kh.email = email_moi
            changed = True
        
        if sdt_moi and sdt_moi != kh.so_dien_thoai:
            kh.so_dien_thoai = sdt_moi
            changed = True
    
        # Chỉ lưu file và ghi log khi có sự thay đổi
        if changed:
            self.ghi_file()
            ghi_log('Sửa', kh)
            print("\033[92m✔ Cập nhật thành công.\033[0m")
            return True
        else:
            print("\033[93mKhông có thông tin nào được thay đổi.\033[0m")
            return True  # Vẫn trả về True vì không có lỗi xảy ra
            
    def xoa_khach_hang(self, ma_khach_hang):
        # Kiểm tra tính hợp lệ của mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False
    
        # Tìm khách hàng cần xóa
        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)
    
        # Kiểm tra khách hàng có tồn tại không
        if not kh:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False
    
        # Hiển thị thông tin khách hàng trước khi xóa để người dùng xác nhận
        print("\nThông tin khách hàng cần xóa:")
        self.in_thong_tin(kh)
    
        # Xác nhận trước khi xóa
        confirm = input("\033[91mBạn có chắc chắn muốn xoá khách hàng này? (y/n): \033[0m")
    
        if confirm.lower() in ['y', 'yes']:  # Chấp nhận cả 'y' và 'yes'
            # Thực hiện xóa khách hàng
            self.danh_sach_khach_hang.remove(kh)
        
            # Cập nhật file và ghi log
            self.ghi_file()
            ghi_log('Xóa', kh)
        
            print("\033[92m✔ Xóa thành công.\033[0m")
            return True
        else:
            print("\033[93mĐã hủy xóa khách hàng.\033[0m")
            return False

    def cap_nhat_mua_hang(self, ma_khach_hang, so_lan_mua, gia_tri):
        # Kiểm tra mã khách hàng
        if not self.la_ma_kh_hop_le(ma_khach_hang):
            print("\033[91mMã khách hàng không hợp lệ!\033[0m")
            return False

        # Kiểm tra giá trị đầu vào
        try:
            so_lan_mua = int(so_lan_mua)
            gia_tri = float(gia_tri)
        except ValueError:
            print("\033[91mSố lần mua hoặc giá trị không hợp lệ!\033[0m")
            return False

        if so_lan_mua < 0 or gia_tri < 0:
            print("\033[91mGiá trị mua hàng không hợp lệ.\033[0m")
            return False

        kh = next((k for k in self.danh_sach_khach_hang if k.ma_khach_hang == ma_khach_hang), None)

        if kh is None:
            print("\033[91mKhông tìm thấy khách hàng.\033[0m")
            return False

        # Xử lý khách hàng thân thiết
        if isinstance(kh, LoyalCustomer):
            if gia_tri < 2000000:
                print("\033[91mGiá trị mua hàng tối thiểu cho khách hàng thân thiết là 2.000.000 VND!\033[0m")
                return False
            # Đảm bảo khách hàng thân thiết có thuộc tính theo dõi số lần mua và tổng giá trị
            if not hasattr(kh, 'so_lan_mua_hang'):
                kh.so_lan_mua_hang = 0
            if not hasattr(kh, 'tong_gia_tri_mua_hang'):
                kh.tong_gia_tri_mua_hang = 0
            if not hasattr(kh, 'diem_tich_luy'):
                kh.diem_tich_luy = 0

            # Cập nhật số lần mua và tổng giá trị
            kh.so_lan_mua_hang += so_lan_mua
            kh.tong_gia_tri_mua_hang += gia_tri

            # Quy đổi điểm tích lũy: 10.000 VND = 1 điểm
            diem_moi = int(gia_tri // 10000)
            kh.diem_tich_luy += diem_moi

            print(f"\033[94m✨ Cập nhật thành công:\033[0m")
            print(f"\033[94m💰 +{diem_moi} điểm tích lũy (tổng: {kh.diem_tich_luy} điểm)\033[0m")
            print(f"\033[94m💵 Tổng giá trị mua hàng: {kh.tong_gia_tri_mua_hang:,.0f} VND\033[0m")

            ghi_log('Cập nhật mua hàng và điểm tích lũy', kh)
            self.ghi_file()
            return True
        
        # Xử lý khách hàng vãng lai (CasualCustomer)
        else:
            # Đảm bảo khách hàng vãng lai có thuộc tính theo dõi số lần mua và tổng giá trị
            if not hasattr(kh, 'so_lan_mua_hang'):
                kh.so_lan_mua_hang = 0
            if not hasattr(kh, 'tong_gia_tri_mua_hang'):
                kh.tong_gia_tri_mua_hang = 0
                
            # Cập nhật số lần mua và tổng giá trị
            kh.so_lan_mua_hang += so_lan_mua
            kh.tong_gia_tri_mua_hang += gia_tri
            
            # Kiểm tra điều kiện nâng cấp: tổng giá trị > 2.000.000 VND và số lần mua ≥ 3
            if kh.tong_gia_tri_mua_hang > 2000000 and kh.so_lan_mua_hang >= 3:
                # Quy đổi điểm tích lũy theo tỷ lệ 10.000 VND = 1 điểm
                diem_tich_luy = int(kh.tong_gia_tri_mua_hang // 10000)
                
                # Xóa khách hàng vãng lai
                self.danh_sach_khach_hang.remove(kh)
                
                # Tạo khách hàng thân thiết mới với cùng thông tin cơ bản
                kh_moi = LoyalCustomer(kh.ma_khach_hang, kh.ten_khach_hang, kh.so_dien_thoai, kh.email, diem_tich_luy)
                
                # Thêm thông tin về số lần mua và tổng giá trị mua hàng
                kh_moi.so_lan_mua_hang = kh.so_lan_mua_hang
                kh_moi.tong_gia_tri_mua_hang = kh.tong_gia_tri_mua_hang
                
                self.danh_sach_khach_hang.append(kh_moi)
                
                print(f"\033[94m✨ Khách hàng đã được nâng cấp thành khách hàng thân thiết!\033[0m")
                print(f"\033[94m🎁 Điểm tích lũy khởi đầu: {diem_tich_luy} điểm\033[0m")
                ghi_log('Chuyển sang khách thân thiết', kh_moi)
            else:
                # Chưa đủ điều kiện nâng cấp
                print(f"\033[93mĐiều kiện nâng cấp: Tổng giá trị > 2.000.000 VND và số lần mua ≥ 3\033[0m")
                if kh.tong_gia_tri_mua_hang <= 2000000:
                    print(f"\033[93mKhách hàng cần mua thêm {2000000 - kh.tong_gia_tri_mua_hang:,.0f} VND để đủ điều kiện.\033[0m")
                if kh.so_lan_mua_hang < 3:
                    print(f"\033[93mKhách hàng cần mua thêm {3 - kh.so_lan_mua_hang} lần để đủ điều kiện.\033[0m")
                ghi_log('Cập nhật mua hàng', kh)
            
            self.ghi_file()
            print("\033[92m✔ Cập nhật mua hàng thành công.\033[0m")
            return True

    def hien_thi_danh_sach(self, key_sort=None, reverse=False, loai=None):
        
        
        ds_hien_thi = self.danh_sach_khach_hang.copy()
    
        # Lọc theo loại nếu được chỉ định
        if loai == 'Loyal':
            ds_hien_thi = [kh for kh in ds_hien_thi if isinstance(kh, LoyalCustomer)]
        elif loai == 'Casual':
            ds_hien_thi = [kh for kh in ds_hien_thi if isinstance(kh, CasualCustomer)]
    
        # Kiểm tra xem danh sách có rỗng không
        if not ds_hien_thi:
            print("\033[93mKhông có khách hàng nào phù hợp với điều kiện.\033[0m")
            return
    
        # Sắp xếp dữ liệu
        if key_sort:
            if key_sort == 'diem_tich_luy' and loai != 'Casual':
                # Chỉ áp dụng sắp xếp theo điểm tích lũy cho khách hàng thân thiết
                # hoặc cho danh sách tổng hợp (sắp xếp khách thân thiết trước)
                ds_loyal = [kh for kh in ds_hien_thi if isinstance(kh, LoyalCustomer)]
                ds_casual = [kh for kh in ds_hien_thi if isinstance(kh, CasualCustomer)]
                ds_loyal.sort(key=lambda x: x.diem_tich_luy, reverse=reverse)
                ds_hien_thi = ds_loyal + ds_casual if not reverse else ds_casual + ds_loyal
            elif key_sort == 'tong_gia_tri_mua_hang' and loai != 'Loyal':
                # Chỉ áp dụng sắp xếp theo tổng giá trị cho khách hàng vãng lai
                # hoặc cho danh sách tổng hợp (sắp xếp khách vãng lai trước)
                ds_loyal = [kh for kh in ds_hien_thi if isinstance(kh, LoyalCustomer)]
                ds_casual = [kh for kh in ds_hien_thi if isinstance(kh, CasualCustomer)]
                ds_casual.sort(key=lambda x: x.tong_gia_tri_mua_hang, reverse=reverse)
                ds_hien_thi = ds_casual + ds_loyal if not reverse else ds_casual + ds_loyal
            else:
                # Sắp xếp theo các trường thông thường (chung cho cả hai loại)
                try:
                   ds_hien_thi.sort(key=lambda x: getattr(x, key_sort, ''), reverse=reverse)
                except AttributeError:
                   print(f"\033[93mCảnh báo: Trường '{key_sort}' không tồn tại ở một số khách hàng. Sắp xếp có thể không chính xác.\033[0m")

            # Hiển thị tiêu đề
            loai_title = "THÂN THIẾT" if loai == 'Loyal' else "VÃNG LAI" if loai == 'Casual' else "TẤT CẢ"
            print(f"\n📋 DANH SÁCH KHÁCH HÀNG {loai_title}")
    
            # Tiêu đề cột tùy theo loại khách hàng
            if loai == 'Loyal':
               header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Điểm tích lũy':<15}"
               print("\033[96m" + header + "\033[0m")
               print("-" * len(header))
        
               for kh in ds_hien_thi:
                  print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.diem_tich_luy:<15}| {kh.tong_gia_tri_mua_hang:15,.0f}")
    
            elif loai == 'Casual':
               header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Số lần mua':<12} | {'Tổng giá trị':<15}"
               print("\033[96m" + header + "\033[0m")
               print("-" * len(header))
        
               for kh in ds_hien_thi:
                 print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.so_lan_mua_hang:<12} | {kh.tong_gia_tri_mua_hang:15,.0f}")
    
            else:
               # Hiển thị danh sách kết hợp
               header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Loại KH':<10} | {'Chi tiết':<20}"
               print("\033[96m" + header + "\033[0m")
               print("-" * len(header))
        
               for kh in ds_hien_thi:
                    if isinstance(kh, LoyalCustomer):
                      chi_tiet = f"SL: {kh.tong_gia_tri_mua_hang:}, Điểm TL: {kh.diem_tich_luy}"
                      loai_kh = "Thân thiết"
                    else:
                      chi_tiet = f"SL: {kh.so_lan_mua_hang}, GT: {kh.tong_gia_tri_mua_hang:,.0f}"
                      loai_kh = "Vãng lai"
            
                    print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {loai_kh:<10} | {chi_tiet:<20}")
    
            print(f"\nTổng số: {len(ds_hien_thi)} khách hàng")
    def in_thong_tin(self, kh):
        
        if isinstance(kh, CasualCustomer):
           print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | Vãng lai | SL: {kh.so_lan_mua_hang}, GT: {kh.tong_gia_tri_mua_hang:,.0f} VND")
        else:
           print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | Thân thiết | Điểm TL: {kh.diem_tich_luy}")        
    def thong_ke(self):
        """Thống kê số lượng và doanh thu theo loại khách hàng và chi tiết từng khách hàng"""
        # Đếm số lượng khách hàng theo loại
        loyal_customers = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, LoyalCustomer)]
        casual_customers = [kh for kh in self.danh_sach_khach_hang if isinstance(kh, CasualCustomer)]
        loyal = len(loyal_customers)
        casual = len(casual_customers)
        
        # Tính tổng doanh thu từng loại khách hàng
        doanh_thu_loyal = sum(kh.tong_gia_tri_mua_hang for kh in loyal_customers)
        doanh_thu_casual = sum(kh.tong_gia_tri_mua_hang for kh in casual_customers)
        tong_doanh_thu = doanh_thu_loyal + doanh_thu_casual
        
        # Tính trung bình cho từng loại khách hàng
        tb_loyal = doanh_thu_loyal / loyal if loyal else 0
        tb_casual = doanh_thu_casual / casual if casual else 0
        tb_chung = tong_doanh_thu / (loyal + casual) if (loyal + casual) else 0
        
        # Tính trung bình điểm tích lũy cho khách thân thiết
        tb_diem = sum(kh.diem_tich_luy for kh in loyal_customers) / loyal if loyal else 0

        print("\n=== THỐNG KÊ KHÁCH HÀNG ===")
        print(f"Tổng số khách hàng: {loyal + casual}")
        print(f"- Khách hàng thân thiết: {loyal}")
        print(f"- Khách hàng vãng lai: {casual}")
        
        print(f"\nTổng doanh thu của siêu thị: {tong_doanh_thu:,.0f} VND")
        print(f"- Doanh thu từ khách hàng thân thiết: {doanh_thu_loyal:,.0f} VND")
        print(f"- Doanh thu từ khách hàng vãng lai: {doanh_thu_casual:,.0f} VND")
        
        print(f"\nTrung bình giá trị mua hàng:")
        print(f"- Tất cả khách hàng: {tb_chung:,.0f} VND")
        print(f"- Khách hàng thân thiết: {tb_loyal:,.0f} VND")
        print(f"- Khách hàng vãng lai: {tb_casual:,.0f} VND")
        
        print(f"\nTrung bình điểm tích lũy của khách thân thiết: {tb_diem:,.0f} điểm")

        # Lưu thống kê tổng hợp ra file CSV
        try:
            with open('thongke_tong_hop.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Loại', 'Số lượng', 'Doanh thu', 'Trung bình giá trị mua hàng', 'Trung bình điểm tích lũy'])
                writer.writerow(['Loyal', loyal, f"{doanh_thu_loyal:.0f}", f"{tb_loyal:.0f} VND", f"{tb_diem:.0f} điểm"])
                writer.writerow(['Casual', casual, f"{doanh_thu_casual:.0f}", f"{tb_casual:.0f} VND", "-"])
                writer.writerow(['Tổng', loyal + casual, f"{tong_doanh_thu:.0f}", f"{tb_chung:.0f} VND", "-"])
            print("✅ Đã lưu thống kê tổng hợp vào file: thongke_tong_hop.csv")
        except Exception as e:
            print(f"\033[91mLỗi khi lưu file thống kê: {e}\033[0m")

        print("\n=== THỐNG KÊ CHI TIẾT TỪNG KHÁCH HÀNG ===")
        
        # Tạo file CSV cho thống kê chi tiết
        try:
            with open('thongke_chi_tiet.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Mã KH', 'Tên KH', 'Loại KH', 'Số lần mua', 'Tổng giá trị', 'TB/lần mua', 'Điểm TL'])
                
                # Hiển thị thông tin khách hàng thân thiết
                if loyal_customers:
                    print("\n\033[96m=== KHÁCH HÀNG THÂN THIẾT ===\033[0m")
                    header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'Số lần mua':<12} | {'Tổng giá trị':<15} | {'TB/lần mua':<15} | {'Điểm TL':<10}"
                    print("\033[96m" + header + "\033[0m")
                    print("-" * len(header))
                    
                    for kh in loyal_customers:
                        # Tính giá trị trung bình trên mỗi lần mua hàng
                        tb_lan_mua = kh.tong_gia_tri_mua_hang / kh.so_lan_mua_hang if kh.so_lan_mua_hang > 0 else 0
                        
                        # Hiển thị thông tin chi tiết
                        print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_lan_mua_hang:<12} | {kh.tong_gia_tri_mua_hang:15,.0f} | {tb_lan_mua:15,.0f} | {kh.diem_tich_luy:<10}")
                        
                        # Ghi vào file CSV
                        writer.writerow([
                            kh.ma_khach_hang,
                            kh.ten_khach_hang,
                            'Thân thiết',
                            kh.so_lan_mua_hang,
                            f"{kh.tong_gia_tri_mua_hang:.0f}",
                            f"{tb_lan_mua:.0f}",
                            kh.diem_tich_luy
                        ])
                
                # Hiển thị thông tin khách hàng vãng lai
                if casual_customers:
                    print("\n\033[93m=== KHÁCH HÀNG VÃNG LAI ===\033[0m")
                    header = f"{'Mã KH':<10} | {'Tên KH':<20} | {'Số lần mua':<12} | {'Tổng giá trị':<15} | {'TB/lần mua':<15}"
                    print("\033[93m" + header + "\033[0m")
                    print("-" * len(header))
                    
                    for kh in casual_customers:
                        # Tính giá trị trung bình trên mỗi lần mua hàng
                        tb_lan_mua = kh.tong_gia_tri_mua_hang / kh.so_lan_mua_hang if kh.so_lan_mua_hang > 0 else 0
                        
                        # Hiển thị thông tin chi tiết
                        print(f"{kh.ma_khach_hang:<10} | {kh.ten_khach_hang:<20} | {kh.so_lan_mua_hang:<12} | {kh.tong_gia_tri_mua_hang:15,.0f} | {tb_lan_mua:15,.0f}")
                        
                        # Ghi vào file CSV
                        writer.writerow([
                            kh.ma_khach_hang,
                            kh.ten_khach_hang,
                            'Vãng lai',
                            kh.so_lan_mua_hang,
                            f"{kh.tong_gia_tri_mua_hang:.0f}",
                            f"{tb_lan_mua:.0f}",
                            '-'
                        ])
                        
            print("✅ Đã lưu thống kê chi tiết vào file: thongke_chi_tiet.csv")
        except Exception as e:
            print(f"\033[91mLỗi khi lưu file thống kê chi tiết: {e}\033[0m")          

    def thong_ke_khach_hang_than_thiet(self):
        """Thống kê khách hàng thân thiết để tặng quà Tết"""
        # Lọc khách hàng thân thiết có điểm tích lũy > 500
        kh_tiem_nang = [kh for kh in self.danh_sach_khach_hang 
                       if isinstance(kh, LoyalCustomer) and kh.diem_tich_luy > 500]
        
        if not kh_tiem_nang:
            print("\033[93mKhông có khách hàng thân thiết nào có đủ điểm (>500) để nhận quà Tết.\033[0m")
            return []
            
        # Sắp xếp theo điểm tích lũy giảm dần
        kh_tiem_nang.sort(key=lambda kh: kh.diem_tich_luy, reverse=True)
        
        # Giới hạn top 10 khách hàng
        top_10 = kh_tiem_nang[:10]

        print("\n🎁 DANH SÁCH KHÁCH HÀNG ĐƯỢC NHẬN QUÀ TẾT 🎁")
        print(f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Điểm tích lũy':<15}")
        print("-" * 85)
        
        for i, kh in enumerate(top_10, 1):
            print(f"{i}. {kh.ma_khach_hang:<8} | {kh.ten_khach_hang:<20} | {kh.so_dien_thoai:<12} | {kh.email:<25} | {kh.diem_tich_luy:<15}")

        # Lưu danh sách ra file CSV
        with open("khach_hang_tet.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["MaKH", "TenKH", "SDT", "Email", "DiemTichLuy"])
            for kh in top_10:
                writer.writerow([
                    kh.ma_khach_hang,
                    kh.ten_khach_hang,
                    kh.so_dien_thoai,
                    kh.email,
                    kh.diem_tich_luy
                ])
        print("✅ Đã lưu danh sách vào file: khach_hang_tet.csv")
        
        return top_10

def main():
    """Hàm chính điều khiển luồng chương trình"""
    # Khởi tạo đối tượng quản lý một lần duy nhất
    ql = ManageCustomer()

    while True:
        # Menu chính cải tiến với màu sắc và định dạng
        print("\033[96m╔══════════════════════════════════════════════════════════════════════════╗\033[0m")
        print("\033[96m║                        HỆ THỐNG QUẢN LÝ KHÁCH HÀNG                       ║\033[0m")
        print("\033[96m╠══════════════════════════════════════════════════════════════════════════╣\033[0m")
        print("\033[93m║ 1. Thêm mới / Sửa thông tin / Xóa khách hàng/Cập nhật mua hàng cho khách ║\033[0m")
        print("\033[93m║ 2. Tìm kiếm khách hàng                                                   ║\033[0m")
        print("\033[93m║ 3. Hiển thị danh sách khách hàng                                         ║\033[0m")
        print("\033[93m║ 4. Tính tổng doanh thu                                                   ║\033[0m")
        print("\033[93m║ 5. Hiển thị top 3 khách hàng mua nhiều nhất                              ║\033[0m")
        print("\033[93m║ 6. Thống kê KH thân thiết để tặng quà Tết                                ║\033[0m")
        print("\033[91m║ 0. Thoát chương trình                                                    ║\033[0m")
        print("\033[96m╚══════════════════════════════════════════════════════════════════════════╝\033[0m")
        choice = input("\033[95m>> Chọn chức năng (0-6): \033[0m")

        if choice == '1':
            # Menu quản lý thêm/sửa/xóa, truyền đối tượng quản lý vào
            sub_menu_quan_ly(ql)
        elif choice == '2':
            # Tìm kiếm khách hàng
            tim_kiem_khach_hang(ql)
        elif choice == '3':
            # Hiển thị danh sách khách hàng
            hien_thi_danh_sach(ql)
        elif choice == '4':
            # Tính tổng doanh thu
            loading()
            ql.thong_ke()
        elif choice == '5':
            # Hiển thị top khách hàng mua nhiều nhất
            loading()
            ql.hien_thi_top_khach_hang(n=3)
        elif choice == '6':
            # Thống kê khách hàng thân thiết để tặng quà Tết
            loading()
            ql.thong_ke_khach_hang_than_thiet()
        elif choice == '0':
            print("\033[92mCảm ơn bạn đã sử dụng chương trình. Tạm biệt!\033[0m")
            break
        else:
            print("\033[91m❌ Lựa chọn không hợp lệ. Vui lòng chọn lại!\033[0m")
        
        # Dừng màn hình để người dùng xem kết quả
        if choice != '0':
            input("\nNhấn Enter để tiếp tục...")
            clear_screen()

def sub_menu_quan_ly(ql):
    """Menu con cho chức năng quản lý khách hàng"""
    while True:
        print("\033[96m╔═════════════════════════════════════════════════╗\033[0m")
        print("\033[96m║                QUẢN LÝ KHÁCH HÀNG               ║\033[0m")
        print("\033[96m╠═════════════════════════════════════════════════╣\033[0m")
        print("\033[93m║ 1. Thêm khách hàng mới                          ║\033[0m")
        print("\033[93m║ 2. Sửa thông tin khách hàng                     ║\033[0m")
        print("\033[93m║ 3. Xóa khách hàng                               ║\033[0m")
        print("\033[93m║ 4. Cập nhật mua hàng cho khách                  ║\033[0m")
        print("\033[91m║ 0. Quay lại menu chính                          ║\033[0m")
        print("\033[96m╚═════════════════════════════════════════════════╝\033[0m")
        choice = input("\033[95m>> Chọn chức năng (0-4): \033[0m")

        if choice == '1':
            them_khach_hang(ql)
        elif choice == '2':
            sua_thong_tin_khach_hang(ql)
        elif choice == '3':
            xoa_khach_hang(ql)
        elif choice == '4':
            cap_nhat_mua_hang(ql)
        elif choice == '0':
            clear_screen()
            return
        else:
            print("\033[91m❌ Lựa chọn không hợp lệ. Vui lòng chọn lại!\033[0m")
        
        if choice != '0':
            input("\nNhấn Enter để tiếp tục...")
            clear_screen()

def nhap_so_nguyen(prompt, mac_dinh=0):
    """Hàm trợ giúp để nhập và kiểm tra số nguyên"""
    while True:
        value = input(prompt)
        if not value:  # Nếu để trống, trả về giá trị mặc định
            return mac_dinh
        try:
            return int(value)
        except ValueError:
            print("\033[91mVui lòng nhập một số nguyên hợp lệ!\033[0m")

def nhap_so_thuc(prompt, mac_dinh=0.0):
    """Hàm trợ giúp để nhập và kiểm tra số thực"""
    while True:
        value = input(prompt)
        if not value:  # Nếu để trống, trả về giá trị mặc định
            return mac_dinh
        try:
            return float(value)
        except ValueError:
            print("\033[91mVui lòng nhập một số hợp lệ!\033[0m")

def them_khach_hang(ql):
    """Chức năng thêm khách hàng mới"""
    print("\n=== THÊM KHÁCH HÀNG MỚI ===")
    
    ma = input("Mã KH: ")
    if not ma:
        print("\033[91mMã khách hàng không được để trống!\033[0m")
        return
        
    ten = nhap_ten()
    sdt = nhap_sdt()
    email = nhap_email()

    # Hiển thị menu chọn loại khách hàng
    print("\nChọn loại khách hàng:")
    print("1. Loyal (Thân thiết)")
    print("2. Casual (Vãng lai)")

    loai = None  # Khởi tạo loại trước vòng lặp
    while True:
        loai_choice = input(">> Nhập lựa chọn (1 hoặc 2): ").strip()
        if loai_choice == '1':
            loai = 'loyal'
            break
        elif loai_choice == '2':
            loai = 'casual'
            break
        else:
            print("\033[91mLựa chọn không hợp lệ. Vui lòng chọn 1 hoặc 2.\033[0m")

    # Tạo khách hàng tương ứng với giá trị mặc định cho số lần mua và tổng giá trị
    if loai == 'loyal':
        kh = LoyalCustomer(ma, ten, sdt, email)
    elif loai == 'casual':
        kh = CasualCustomer(ma, ten, sdt, email, 0, 0.0)  # Khởi tạo với giá trị mặc định
    else:
        print("\033[91mLỗi: Loại khách hàng không xác định.\033[0m")
        return

    loading()
    ql.them_khach_hang(kh)
def sua_thong_tin_khach_hang(ql):
    """Chức năng sửa thông tin khách hàng"""
    print("\n=== SỬA THÔNG TIN KHÁCH HÀNG ===")
    ma = input("Nhập mã KH cần sửa: ")
    if not ma:
        print("\033[91mMã khách hàng không được để trống!\033[0m")
        return
        
    kh = ql.tim_kiem(ma_kh=ma)
    if not kh:
        print("\033[91mKhông tìm thấy khách hàng.\033[0m")
        return
    
    kh = kh[0] 
    print(f"\nThông tin hiện tại:")
    ql.in_thong_tin(kh)
    
    # Hiển thị thông tin hiện tại để người dùng dễ xem
    print("\nNhập thông tin mới (để trống nếu giữ nguyên):")
    
    if input("Bạn có muốn sửa tên không? (y/n): ").strip().lower() == 'y':
        ten_moi = nhap_ten()
    else:
        ten_moi = kh.ten_khach_hang 
        
    if input("Bạn có muốn sửa email không? (y/n): ").strip().lower() == 'y':
        email_moi = nhap_email()
    else:
        email_moi = kh.email       
        
    if input("Bạn có muốn sửa số điện thoại không? (y/n): ").strip().lower() == 'y':
        sdt_moi = nhap_sdt()                
    else:
        sdt_moi = kh.so_dien_thoai
        
    loading()
    ql.sua_thong_tin(ma, ten_moi, email_moi, sdt_moi)

def xoa_khach_hang(ql):
    """Chức năng xóa khách hàng"""
    print("\n=== XÓA KHÁCH HÀNG ===")
    ma = input("Nhập mã KH cần xóa: ")
    if not ma:
        print("\033[91mMã khách hàng không được để trống!\033[0m")
        return
        
    # Kiểm tra xem khách hàng có tồn tại không 
    kh = ql.tim_kiem(ma_kh=ma)
    if not kh:
        print("\033[91mKhông tìm thấy khách hàng với mã này.\033[0m")
        return
        
    # Hiển thị thông tin khách hàng để xác nhận
    print("\nThông tin khách hàng sẽ bị xóa:")
    ql.in_thong_tin(kh[0])
    
    loading()
    ql.xoa_khach_hang(ma)

def cap_nhat_mua_hang(ql):
    """Chức năng cập nhật mua hàng cho khách hàng"""
    print("\n=== CẬP NHẬT MUA HÀNG ===")
    ma = input("Nhập mã KH: ")
    if not ma:
        print("\033[91mMã khách hàng không được để trống!\033[0m")
        return
       
    kh = ql.tim_kiem(ma_kh=ma)
    if not kh:
        print("\033[91mKhông tìm thấy khách hàng.\033[0m")
        return
    
    kh = kh[0]  
    print(f"\nKhách hàng: {kh.ten_khach_hang} ({kh.ma_khach_hang})")
    
    # Hiển thị thông tin khách hàng theo loại
    if isinstance(kh, LoyalCustomer):
        print(f"Loại: Khách hàng thân thiết (Loyal)")
        
        # Nhập cả số lần mua và giá trị đơn hàng cho khách thân thiết
        so_lan = nhap_so_nguyen("Số lần mua: ")
        gia_tri = nhap_so_thuc("Tổng giá trị đơn hàng: ")
        
        # Quy đổi điểm tích lũy từ giá trị mua hàng
        diem_quy_doi = int(gia_tri // 10000)
        print(f"Quy đổi: +{diem_quy_doi} điểm tích lũy (10.000 VND = 1 điểm)")
        print(f"Điểm hiện tại: {kh.diem_tich_luy}, Sau cập nhật: {kh.diem_tich_luy + diem_quy_doi}")
    else:
        print(f"Loại: Khách hàng vãng lai (Casual)")
        
        # Khách vãng lai cần cả số lần và giá trị
        so_lan = nhap_so_nguyen("Số lần mua: ")
        gia_tri = nhap_so_thuc("Tổng giá trị đơn hàng: ")
        
        # Hiển thị thông tin điều kiện nâng cấp
        if kh.tong_gia_tri_mua_hang + gia_tri > 2000000:
            print("\033[92m✨ Khách hàng sẽ được nâng cấp thành khách hàng thân thiết!\033[0m")
        else:
            con_lai = 2000000 - (kh.tong_gia_tri_mua_hang + gia_tri)
            print(f"\033[93mSau giao dịch này, khách hàng cần mua thêm {con_lai:,.0f} VND để trở thành khách hàng thân thiết.\033[0m")
    
    # Xác nhận cập nhật
    if input("\nXác nhận cập nhật mua hàng? (y/n): ").strip().lower() != 'y':
        print("\033[93mĐã hủy cập nhật mua hàng.\033[0m")
        return
        
    loading()
    ql.cap_nhat_mua_hang(ma, so_lan, gia_tri)
def tim_kiem_khach_hang(ql):
    """Chức năng tìm kiếm khách hàng"""
    print("\n=== TÌM KIẾM KHÁCH HÀNG ===")
    print("Chọn loại tìm kiếm:")
    print("1. Tìm theo mã khách hàng")
    print("2. Tìm theo tên")
    print("3. Tìm kiếm nâng cao")
    
    option = input(">> Chọn tùy chọn (1-3): ")
    
    if option == '1':
        ma_kh = input("Nhập mã khách hàng: ")
        if not ma_kh:
            print("\033[91mMã khách hàng không được để trống!\033[0m")
            return
            
        loading()
        ket_qua = ql.tim_kiem(ma_kh=ma_kh)
        
    elif option == '2':
        ten = input("Nhập tên khách hàng (nhập chính xác): ")
        if not ten:
            print("\033[91mTên tìm kiếm không được để trống!\033[0m")
            return
           
        loading()
        ket_qua = ql.tim_kiem(ten_chinh_xac=ten)
        
    elif option == '3':
        # Tìm kiếm nâng cao với nhiều điều kiện
        print("\nChọn loại khách hàng:")
        print("1. Loyal (Thân thiết)")
        print("2. Casual (Vãng lai)")
        print("3. Bỏ qua lọc theo loại")

        loai = None  # Khởi tạo loại mặc định
        loai_input = input(">> Nhập lựa chọn (1/2/3): ").strip()
        if loai_input == '1':
            loai = "Loyal"
        elif loai_input == '2':
            loai = "Casual"
        elif loai_input == '3' or loai_input == '':
            loai = None
        else:
            print("\033[91mLựa chọn không hợp lệ. Sử dụng giá trị mặc định (tất cả loại).\033[0m")

        # Thu thập các điều kiện tìm kiếm
        ten_chua = input("Tên chứa (bỏ trống nếu không): ")
        email_chua = input("Email chứa (bỏ trống nếu không): ")
        ma_kh = input("Mã KH (bỏ trống nếu không): ")
        sdt_chua = input("SĐT chứa (bỏ trống nếu không): ")
        
        # Sử dụng các hàm trợ giúp để nhập số
        tong_gia_min = nhap_so_thuc("Tổng giá trị tối thiểu (bỏ trống nếu không): ", None)
        tong_gia_max = nhap_so_thuc("Tổng giá trị tối đa (bỏ trống nếu không): ", None)
        so_lan_mua_min = nhap_so_nguyen("Số lần mua tối thiểu (bỏ trống nếu không): ", None)
        
        loading()
        ket_qua = ql.tim_kiem(
            loai=loai,
            ten_chua=ten_chua,
            email_chua=email_chua,
            ma_kh=ma_kh,
            sdt_chua=sdt_chua,
            tong_gia_min=tong_gia_min,
            tong_gia_max=tong_gia_max,
            so_lan_mua_min=so_lan_mua_min
        )
    else:
        print("\033[91mLựa chọn không hợp lệ!\033[0m")
        return
        
    # Hiển thị kết quả tìm kiếm
    if ket_qua:
        print(f"\n🔍 Kết quả tìm kiếm ({len(ket_qua)} khách hàng):")
        # In tiêu đề cột
        print(f"{'Mã KH':<10} | {'Tên KH':<20} | {'SĐT':<12} | {'Email':<25} | {'Loại':<10} | {'Chi tiết':<20}")
        print("-" * 105)
        
        for kh in ket_qua:
            ql.in_thong_tin(kh)
    else:
        print("\033[91mKhông tìm thấy khách hàng phù hợp với điều kiện tìm kiếm.\033[0m")

def hien_thi_danh_sach(ql):
    """Chức năng hiển thị danh sách khách hàng"""
    print("\n=== HIỂN THỊ DANH SÁCH KHÁCH HÀNG ===")
    # Thêm tùy chọn lọc theo loại
    print("\nChọn loại khách hàng để hiển thị:")
    print("1. Loyal (Thân thiết)")
    print("2. Casual (Vãng lai)")
    print("3. Tất cả khách hàng")
    
    loai = None
    loai_choice = input(">> Nhập lựa chọn (1/2/3): ").strip()
    if loai_choice == '1':
        loai = 'Loyal'
    elif loai_choice == '2':
        loai = 'Casual'
    elif loai_choice != '3' and loai_choice != '':
        print("\033[93mLựa chọn không hợp lệ, hiển thị tất cả khách hàng.\033[0m")
        
    # Tùy chọn sắp xếp
    print("\nSắp xếp theo:")
    print("1. Mã khách hàng")
    print("2. Tên khách hàng")
    print("3. Số điện thoại")
    print("4. Tổng giá trị mua hàng ")
    print("5. Điểm tích lũy (chỉ áp dụng cho khách thân thiết)")
    
    sort_field_map = {
        '1': 'ma_kh',
        '2': 'ten_kh',
        '3': 'sdt',
        '4': 'tong_gia_tri',
        '5': 'diem_tich_luy'
    }
    
    sort_choice = input(">> Chọn trường sắp xếp (1-5): ")
    if sort_choice in sort_field_map:
        sort_field = sort_field_map[sort_choice]
    else:
        print("\033[93mLựa chọn không hợp lệ, sắp xếp theo mã khách hàng.\033[0m")
        sort_field = 'ma_khach_hang'
    
    # Thứ tự sắp xếp
    order = input("Sắp xếp tăng dần (asc) hay giảm dần (desc)? ").strip().lower()
    if order not in ['asc', 'desc']:
        print("\033[93mLựa chọn không hợp lệ, sắp xếp tăng dần.\033[0m")
        order = 'asc'
    
    loading()
    ql.hien_thi_danh_sach(key_sort=sort_field, reverse=(order == 'desc'), loai=loai)

if __name__ == '__main__':
    main()        
