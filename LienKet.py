import mysql.connector
from tkinter import messagebox

# ====== Kết nối MySQL (MySQL Connection) ======
def connect_db():
    """
    Thiết lập kết nối đến cơ sở dữ liệu QL_DiemSV.
    
    LƯU Ý: Thay đổi user và password nếu cần thiết.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",        # Thay bằng user MySQL của bạn
            password="123456",  # Thay bằng password MySQL của bạn
            database="QL_DiemSV"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối MySQL: {err}")
        messagebox.showerror("Lỗi Kết Nối", f"Không thể kết nối đến MySQL.\nKiểm tra lại host, user, password và tên database 'QL_DiemSV'.\nLỗi: {err}")
        return None

if __name__ == "__main__":
    # Mã kiểm tra kết nối khi chạy riêng file này
    test_conn = connect_db()
    if test_conn:
        print("Kết nối MySQL thành công!")
        test_conn.close()
    else:
        print("Kết nối MySQL thất bại.")