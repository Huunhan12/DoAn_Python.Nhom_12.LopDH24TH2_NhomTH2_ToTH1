# db_operations.py
"""
db_operations.py
Module này chứa các hàm thao tác với cơ sở dữ liệu MySQL cho ứng dụng Quản lý điểm sinh viên.
Nó sử dụng hàm connect_db từ LienKet.py để kết nối đến cơ sở dữ liệu.
Các hàm bao gồm: load_initial_data, add_record_to_db, delete_record_from_db,
search_student_db, edit_student_db.

Hàm load_initial_data() là hàm chịu trách nhiệm đọc và lấy toàn bộ dữ liệu sinh viên và điểm từ cơ sở dữ liệu MySQL khi ứng dụng được khởi động.
Chức năng chính của hàm add_record_to_db() là Thêm mới (CREATE) hoặc Cập nhật (UPDATE) thông tin sinh viên và điểm số vào cơ sở dữ liệu.
Chức năng của hàm delete_record_from_db() là xóa vĩnh viễn (DELETE) một hoặc nhiều bản ghi điểm sinh viên khỏi cơ sở dữ liệu MySQL và cập nhật giao diện Treeview.
Chức năng của hàm search_student_db() là tìm kiếm và trích xuất (READ) tất cả các bản ghi điểm của một sinh viên cụ thể dựa trên Mã sinh viên (MaSV).
Chức năng của hàm edit_student_db() là cập nhật (UPDATE) thông tin Họ Tên và Điểm của một sinh viên trong cơ sở dữ liệu MySQL.
"""

import mysql.connector
from tkinter import messagebox
from LienKet import connect_db # Import hàm kết nối DB

# ====== Tải dữ liệu ban đầu (READ) ======
def load_initial_data():
    """Tải tất cả điểm và thông tin SV từ DB."""
    conn = connect_db()
    if conn is None: return []
        
    cursor = conn.cursor()
    sql = """
    SELECT 
        SV.MaSV, SV.HoTen, SV.Lop, DATE_FORMAT(SV.NgaySinh, '%d/%m/%Y'), 
        D.TenMon, D.DiemQT, D.DiemThi, ROUND((D.DiemQT + D.DiemThi) / 2, 2) AS DiemTB
    FROM SINHVIEN AS SV
    JOIN DIEM AS D ON SV.MaSV = D.MaSV
    """
    try:
        cursor.execute(sql)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        print(f"Lỗi khi tải dữ liệu ban đầu: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ====== Thêm/Cập nhật bản ghi (CREATE/UPDATE) ======
def add_record_to_db(maso, hoten, lop, ngaysinh_sql, monhoc, gioitinh, diemqt, diemthi, tree_main, ngaysinh_display):
    """Thêm điểm vào DB và cập nhật Treeview."""
    conn = connect_db()
    if conn is None: return False
        
    cursor = conn.cursor()
    
    try:
        # 1. INSERT/UPDATE vào SINHVIEN
        check_sv_sql = "SELECT MaSV FROM SINHVIEN WHERE MaSV = %s"
        cursor.execute(check_sv_sql, (maso,))
        if cursor.fetchone() is None:
            # Thêm thông tin sinh viên mới
            sv_sql = "INSERT INTO SINHVIEN (MaSV, HoTen, Lop, NgaySinh, GioiTinh) VALUES (%s, %s, %s, %s, %s)"
            sv_data = (maso, hoten, lop, ngaysinh_sql, gioitinh) 
            cursor.execute(sv_sql, sv_data)
        else:
            # Cập nhật thông tin SV (nếu đã tồn tại)
            update_sv_sql = "UPDATE SINHVIEN SET HoTen=%s, Lop=%s, NgaySinh=%s, GioiTinh=%s WHERE MaSV=%s"
            cursor.execute(update_sv_sql, (hoten, lop, ngaysinh_sql, gioitinh, maso))

        # 2. INSERT điểm vào bảng DIEM (sẽ báo lỗi IntegrityError nếu trùng MaSV + TenMon)
        diem_sql = "INSERT INTO DIEM (MaSV, TenMon, DiemQT, DiemThi) VALUES (%s, %s, %s, %s)"
        diem_data = (maso, monhoc, diemqt, diemthi)
        cursor.execute(diem_sql, diem_data)

        conn.commit()
        
        # 3. Cập nhật Treeview
        diemtb = round((diemqt + diemthi) / 2, 2)
        tree_main.insert("", "end", values=(maso, hoten, lop, ngaysinh_display, monhoc, diemqt, diemthi, diemtb))
        
        messagebox.showinfo("Thành công", "Đã thêm điểm sinh viên thành công!")
        return True

    except mysql.connector.IntegrityError as e:
        conn.rollback()
        if e.errno == 1062 or "Duplicate entry" in str(e): 
            messagebox.showwarning("Trùng lặp", f"Sinh viên **{hoten}** đã có điểm môn **{monhoc}**.\nVui lòng sửa hoặc nhập môn khác.")
        else:
            messagebox.showerror("Lỗi SQL", f"Lỗi toàn vẹn dữ liệu: {e}")
        return False
             
    except mysql.connector.Error as e:
        conn.rollback()
        messagebox.showerror("Lỗi SQL", f"Lỗi cơ sở dữ liệu: {e}")
        return False
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ====== Xóa bản ghi (DELETE) ======
def delete_record_from_db(selected_items, tree_main):
    """Xóa điểm trong DB dựa trên Treeview items."""
    conn = connect_db()
    if conn is None: return False
    
    cursor = conn.cursor()
    success_count = 0
    
    try:
        for item in selected_items:
            values = tree_main.item(item, "values")
            maso = values[0]
            monhoc = values[4]
            
            # Xóa điểm trong bảng DIEM (vì MaSV, TenMon là PK của DIEM)
            sql = "DELETE FROM DIEM WHERE MaSV = %s AND TenMon = %s"
            cursor.execute(sql, (maso, monhoc))
            
            # Xóa trong Treeview
            tree_main.delete(item)
            success_count += 1

        conn.commit()
        messagebox.showinfo("Thành công", f"Đã xóa thành công {success_count} bản ghi.")
        return True
        
    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi SQL", f"Lỗi khi xóa bản ghi: {e}")
        conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ====== Tìm kiếm bản ghi (READ by MaSV) ======
def search_student_db(maso):
    """Tìm kiếm điểm của sinh viên theo Mã số SV."""
    conn = connect_db()
    if conn is None: return []
    cursor = conn.cursor()
    
    sql = """
    SELECT 
        SV.MaSV, SV.HoTen, SV.Lop, DATE_FORMAT(SV.NgaySinh, '%d/%m/%Y'), 
        D.TenMon, D.DiemQT, D.DiemThi, ROUND((D.DiemQT + D.DiemThi) / 2, 2) AS DiemTB
    FROM SINHVIEN AS SV
    JOIN DIEM AS D ON SV.MaSV = D.MaSV
    WHERE SV.MaSV = %s
    """
    
    try:
        cursor.execute(sql, (maso,))
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi SQL", f"Lỗi tìm kiếm: {e}")
        return []
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# ====== Sửa bản ghi (UPDATE) ======
def edit_student_db(maso_goc, monhoc_goc, new_hoten, diemqt, diemthi):
    """Cập nhật Họ Tên và Điểm vào DB."""
    conn = connect_db()
    if conn is None: return False
    cursor = conn.cursor()
    
    try:
        # 1. Cập nhật Họ Tên (SINHVIEN)
        update_sv_sql = "UPDATE SINHVIEN SET HoTen = %s WHERE MaSV = %s"
        cursor.execute(update_sv_sql, (new_hoten, maso_goc))

        # 2. Cập nhật điểm (DIEM)
        update_diem_sql = "UPDATE DIEM SET DiemQT = %s, DiemThi = %s WHERE MaSV = %s AND TenMon = %s"
        diem_data = (diemqt, diemthi, maso_goc, monhoc_goc)
        cursor.execute(update_diem_sql, diem_data)
        
        conn.commit()
        return True
    
    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi SQL", f"Lỗi cập nhật cơ sở dữ liệu: {e}")
        conn.rollback()
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()