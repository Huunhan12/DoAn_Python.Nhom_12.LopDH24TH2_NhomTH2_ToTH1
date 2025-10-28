import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from LienKet import connect_db # Import hàm kết nối từ file liên kết
import mysql.connector
# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=900, h=500):
    """Canh giữa cửa sổ theo kích thước màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý điểm sinh viên")
center_window(root, 900, 500)
root.resizable(False, False)

# ====== Tiêu đề ======
lbl_title = tk.Label(root, text="QUẢN LÝ ĐIỂM SINH VIÊN", font=("Arial", 20, "bold"), fg="#1E88E5")
lbl_title.pack(pady=10)

# ====== Frame nhập thông tin ======
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill='x')

# ====== Hàm tự động chuyển chữ in hoa ======
def to_uppercase(event):
    widget = event.widget
    text = widget.get().upper()
    widget.delete(0, tk.END)
    widget.insert(0, text)

# ====== Hàm viết hoa chữ cái đầu cho mỗi từ ======
def capitalize_words(event):
    widget = event.widget
    text = widget.get().title()
    widget.delete(0, tk.END)
    widget.insert(0, text)

# --- Hàng 1: Mã số, Họ tên ---
tk.Label(frame_info, text="Mã số sinh viên:",font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_maso = tk.Entry(frame_info, width=15)
entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")
entry_maso.bind("<KeyRelease>", to_uppercase) 

tk.Label(frame_info, text="Họ và tên:",font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_hoten = tk.Entry(frame_info, width=20)
entry_hoten.grid(row=0, column=3, padx=5, pady=5, sticky="w")
entry_hoten.bind("<KeyRelease>", capitalize_words)

tk.Label(frame_info, text="Lớp:",font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10, pady=5, sticky="w")
entry_lop = tk.Entry(frame_info, width=10)
entry_lop.grid(row=0, column=5, padx=5, pady=5, sticky="w")
entry_lop.bind("<KeyRelease>", to_uppercase) 

# --- Hàng 2: Ngày sinh, giới tính, môn học ---
tk.Label(frame_info, text="Ngày sinh: ",font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
date_entry = DateEntry(frame_info, width=12, background="darkblue",
                             foreground="white", date_pattern="dd/mm/yyyy")
date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_info, text="Giới tính:",font=("Arial", 10, "bold")).grid(row=1, column=2, padx=5, pady=5, sticky="w")
combo_gioitinh = ttk.Combobox(frame_info, values=["Nam", "Nữ"], state="readonly", width=17)
combo_gioitinh.grid(row=1, column=3, padx=5, pady=5, sticky="w")
combo_gioitinh.current(0)

# ====== Danh sách môn học ======
mon_hoc_list = ["Chuyên đề Python", "Phân tích thiết kế hệ thống thông tin",
                "Quản trị mạng", "Lịch sử Đảng Cộng sản Việt Nam", 
                "Lý thuyết đồ thị", "Lập trình .NET"]

tk.Label(frame_info, text="Môn học:",font=("Arial", 10, "bold")).grid(row=1, column=4, padx=5, pady=5, sticky="w")
combo_monhoc = ttk.Combobox(frame_info, values=mon_hoc_list, state="readonly", width=27)
combo_monhoc.grid(row=1, column=5, padx=5, pady=5, sticky="w")
combo_monhoc.current(0) 

# --- Hàng 3: Điểm --- 
tk.Label(frame_info, text="Điểm quá trình:",font=("Arial", 10, "bold")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_diemqt = tk.Entry(frame_info, width=15)  
entry_diemqt.grid(row=2, column=1, padx=5, pady=5, sticky="w")
tk.Label(frame_info, text="Điểm thi:",font=("Arial", 10, "bold")).grid(row=2, column=2, padx=5, pady=5, sticky="w")
entry_diemthi = tk.Entry(frame_info, width=20)
entry_diemthi.grid(row=2, column=3, padx=5, pady=5, sticky="w")


# ====== Frame nút chức năng ======
frame_buttons = tk.Frame(root) 
frame_buttons.pack(pady=10)


# --- Nút Thêm (CÓ TÍCH HỢP MYSQL) ---
def add_record():
    maso = entry_maso.get().strip().upper() 
    hoten = entry_hoten.get().strip()
    lop = entry_lop.get().strip().upper()
    # NgaySinh format YYYY-MM-DD cho SQL
    ngaysinh_sql = date_entry.get_date().strftime('%Y-%m-%d')
    ngaysinh_display = date_entry.get() # NgaySinh format DD/MM/YYYY cho Treeview
    monhoc = combo_monhoc.get()
    gioitinh = combo_gioitinh.get()
    diemqt_str = entry_diemqt.get().strip()
    diemthi_str = entry_diemthi.get().strip()

    # 1. Kiểm tra dữ liệu nhập & Giá trị điểm
    if not (maso and hoten and lop and diemqt_str and diemthi_str):
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
        return
    
    try:
        diemqt = float(diemqt_str)
        diemthi = float(diemthi_str)
        if not (0 <= diemqt <= 10 and 0 <= diemthi <= 10):
            raise ValueError
    except ValueError:
        messagebox.showerror("Lỗi", "Điểm phải là số từ 0 đến 10.")
        return

    # 2. Xử lý Database
    conn = connect_db()
    if conn is None: return
        
    cursor = conn.cursor()
    
    try:
        # 2a. INSERT/UPDATE vào SINHVIEN
        # Kiểm tra xem sinh viên đã tồn tại chưa
        check_sv_sql = "SELECT MaSV FROM SINHVIEN WHERE MaSV = %s"
        cursor.execute(check_sv_sql, (maso,))
        if cursor.fetchone() is None:
            # Thêm thông tin sinh viên mới
            sv_sql = "INSERT INTO SINHVIEN (MaSV, HoTen, Lop, NgaySinh, GioiTinh) VALUES (%s, %s, %s, %s, %s)"
            sv_data = (maso, hoten, lop, ngaysinh_sql, gioitinh) 
            cursor.execute(sv_sql, sv_data)
        else:
            # Cập nhật thông tin SV (Họ tên, Lớp, Giới tính, NgaySinh có thể thay đổi)
            update_sv_sql = "UPDATE SINHVIEN SET HoTen=%s, Lop=%s, NgaySinh=%s, GioiTinh=%s WHERE MaSV=%s"
            cursor.execute(update_sv_sql, (hoten, lop, ngaysinh_sql, gioitinh, maso))

        # 2b. INSERT điểm vào bảng DIEM (sẽ báo lỗi IntegrityError nếu trùng MaSV + TenMon)
        diem_sql = "INSERT INTO DIEM (MaSV, TenMon, DiemQT, DiemThi) VALUES (%s, %s, %s, %s)"
        diem_data = (maso, monhoc, diemqt, diemthi)
        cursor.execute(diem_sql, diem_data)

        conn.commit()
        
        # 3. Cập nhật Treeview
        diemtb = round((diemqt + diemthi) / 2, 2)
        tree.insert("", "end", values=(maso, hoten, lop, ngaysinh_display, monhoc, diemqt, diemthi, diemtb))
        
        messagebox.showinfo("Thành công", "Đã thêm điểm sinh viên thành công!")
      # CHỈ XÓA THÔNG TIN ĐIỂM
        entry_diemqt.delete(0, tk.END)
        entry_diemthi.delete(0, tk.END)

    except mysql.connector.IntegrityError as e:
        # Bắt lỗi trùng lặp Khóa chính ghép (MaSV, TenMon)
        conn.rollback() # <<< PHẢI ROLLBACK NGAY SAU KHI BẮT LỖI >>>
        
        # Kiểm tra chi tiết lỗi (thường là lỗi 1062 trong MySQL)
        if e.errno == 1062 or "Duplicate entry" in str(e): 
             messagebox.showwarning("Trùng lặp", f"Sinh viên **{hoten}** đã có điểm môn **{monhoc}**.\nVui lòng sửa hoặc nhập môn khác.")
        else:
             # Xử lý các lỗi IntegrityError khác (ví dụ: lỗi khóa ngoại)
             messagebox.showerror("Lỗi SQL", f"Lỗi toàn vẹn dữ liệu: {e}")
             
    except mysql.connector.Error as e:
        # Bắt các lỗi SQL khác (ví dụ: DataError, OperationalError...)
        conn.rollback()
        messagebox.showerror("Lỗi SQL", f"Lỗi cơ sở dữ liệu: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

btn_add = tk.Button(frame_buttons, text="Thêm", command=add_record, width=12, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_add.grid(row=0, column=0, padx=10)

# --- Nút Nhập TT mới ---
def clear_entries():
    entry_maso.delete(0, tk.END)
    entry_hoten.delete(0, tk.END)
    entry_lop.delete(0, tk.END)
    entry_diemqt.delete(0, tk.END)
    entry_diemthi.delete(0, tk.END)
    combo_monhoc.current(0)
    combo_gioitinh.current(0)
    date_entry.set_date() # Đặt lại ngày hiện tại
    entry_maso.focus()

btn_new = tk.Button(frame_buttons, text="Nhập TT mới", width=12, bg="#03A9F4", fg="white", font=("Arial", 10, "bold"), command=clear_entries)
btn_new.grid(row=0, column=3, padx=10)
 
# --- Nút Xóa (CÓ TÍCH HỢP MYSQL) ---
def delete_record():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi để xóa.")
        return
    
    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa {len(selected_items)} bản ghi đã chọn?"):
        conn = connect_db()
        if conn is None: return
            
        cursor = conn.cursor()
        success_count = 0
        
        try:
            for item in selected_items:
                values = tree.item(item, "values")
                maso = values[0]
                monhoc = values[4]
                
                # Xóa điểm trong bảng DIEM (vì MaSV, TenMon là PK của DIEM)
                sql = "DELETE FROM DIEM WHERE MaSV = %s AND TenMon = %s"
                cursor.execute(sql, (maso, monhoc))
                
                # Xóa trong Treeview
                tree.delete(item)
                success_count += 1

            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa thành công {success_count} bản ghi.")
            
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi SQL", f"Lỗi khi xóa bản ghi: {e}")
            conn.rollback()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

btn_delete = tk.Button(frame_buttons, text="Xóa", command=delete_record, width=12, bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
btn_delete.grid(row=0, column=1, padx=10)

# --- Nút Thoát ---
def exit_app():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát?"):
        root.destroy()
btn_exit = tk.Button(frame_buttons, text="Thoát", command=exit_app, width=12, bg="#D90000", fg="white", font=("Arial", 10, "bold"))
btn_exit.grid(row=0, column=2, padx=10) 


# ====== Hàm mở cửa sổ tìm kiếm ======
def open_search_window():
    search_win = tk.Toplevel(root)
    search_win.title("Tìm kiếm và Sửa đổi điểm sinh viên")
    center_window(search_win, 900, 500)
    search_win.grab_set()

    tk.Label(search_win, text="TÌM KIẾM SINH VIÊN", font=("Arial", 16, "bold"), fg="#9C27B0").pack(pady=10)

    frame_search = tk.Frame(search_win)
    frame_search.pack(pady=5)

    tk.Label(frame_search, text="Nhập mã số sinh viên:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
    entry_search_maso = tk.Entry(frame_search, width=30)
    entry_search_maso.grid(row=0, column=1, padx=5, pady=5)
    entry_search_maso.bind("<KeyRelease>", to_uppercase) 
    entry_search_maso.focus()

    # --- Bảng hiển thị kết quả ---
    columns = ("Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi", "Điểm TB")
    tree_result = ttk.Treeview(search_win, columns=columns, show="headings", height=10)

    for col in columns:
        tree_result.heading(col, text=col.title())
        tree_result.column(col, width=110, anchor="center")
    tree_result.column("Họ và tên", width=150)
    
    scrollbar = ttk.Scrollbar(search_win, orient="vertical", command=tree_result.yview)
    tree_result.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=(0, 10))
    tree_result.pack(fill="x", padx=(10, 0), pady=(0, 10))


    # --- Hàm tìm kiếm sinh viên (TỪ MYSQL) ---
    def search_student():
        maso = entry_search_maso.get().strip().upper()
        if not maso:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã số sinh viên!")
            return

        for item in tree_result.get_children():
            tree_result.delete(item)
        
        conn = connect_db()
        if conn is None: return
        cursor = conn.cursor()
        
        # Lấy điểm của sinh viên đó
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
            
            if not records:
                messagebox.showinfo("Không tìm thấy", f"Không tìm thấy sinh viên có mã số: {maso}")
                return
                
            for record in records:
                tree_result.insert("", "end", values=record)
                
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi SQL", f"Lỗi tìm kiếm: {e}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # --- Nút tìm kiếm ---
    tk.Button(frame_search, text="Tìm kiếm", width=12, bg="#4CAF50", fg="white",
              font=("Arial", 10, "bold"), command=search_student).grid(row=0, column=2, padx=10)
    
    # --- Hàm sửa thông tin sinh viên (CẬP NHẬT VÀO MYSQL) ---
    def edit_student():
        selected_item = tree_result.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một bản ghi điểm để sửa!")
            return

        item_id = selected_item[0]
        # Lấy giá trị hiện tại
        values = list(tree_result.item(item_id, "values")) 
        
        edit_win = tk.Toplevel(search_win)
        edit_win.title("Sửa thông tin sinh viên")
        edit_win.geometry("400x400")
        edit_win.grab_set()

        labels = ["Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi"]
        entries = {}
        editable_fields = ["Họ và tên", "Điểm quá trình", "Điểm thi"] # Các trường cho phép sửa

        for i, (lbl, val) in enumerate(zip(labels, values)):
            tk.Label(edit_win, text=lbl + ":", font=("Arial", 10, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if lbl in editable_fields:
                e = tk.Entry(edit_win, width=30)
                e.insert(0, str(val))
                e.grid(row=i, column=1, padx=10, pady=5)
                entries[lbl] = e
                if lbl == "Họ và tên":
                    e.bind("<KeyRelease>", capitalize_words)
            else:
                # Dùng Label để hiển thị thông tin không sửa (Mã số, Lớp, Ngày sinh, Môn học)
                tk.Label(edit_win, text=str(val), width=30, anchor="w").grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entries[lbl] = val # Lưu giá trị gốc

        def save_changes():
            conn = connect_db()
            if conn is None: return
            cursor = conn.cursor()
            
            try:
                # 1. Lấy giá trị mới
                new_hoten = entries["Họ và tên"].get().strip().title() # Dùng .title() để đảm bảo
                diemqt = float(entries["Điểm quá trình"].get())
                diemthi = float(entries["Điểm thi"].get())
                
                if not (0 <= diemqt <= 10 and 0 <= diemthi <= 10):
                    messagebox.showerror("Lỗi", "Điểm phải là số từ 0 đến 10.")
                    return

                # Giá trị gốc (Khóa chính)
                maso_goc = values[0]
                monhoc_goc = values[4]
                
                diemtb = round((diemqt + diemthi) / 2, 2)
                
                # 2. Cập nhật Họ Tên (SINHVIEN)
                update_sv_sql = "UPDATE SINHVIEN SET HoTen = %s WHERE MaSV = %s"
                cursor.execute(update_sv_sql, (new_hoten, maso_goc))

                # 3. Cập nhật điểm (DIEM)
                update_diem_sql = "UPDATE DIEM SET DiemQT = %s, DiemThi = %s WHERE MaSV = %s AND TenMon = %s"
                diem_data = (diemqt, diemthi, maso_goc, monhoc_goc)
                cursor.execute(update_diem_sql, diem_data)
                
                conn.commit()
                
                # 4. Đồng bộ giao diện
                new_values = [
                    maso_goc, new_hoten, values[2], values[3], # Giữ nguyên Lớp, Ngày sinh
                    monhoc_goc, diemqt, diemthi, diemtb
                ]
                
                tree_result.item(item_id, values=new_values)

                # Đồng bộ Treeview chính
                for row in tree.get_children():
                    row_values = tree.item(row, "values")
                    if row_values[0] == maso_goc and row_values[4] == monhoc_goc: 
                        tree.item(row, values=new_values)
                        break
                
                messagebox.showinfo("Thành công", "Cập nhật thông tin sinh viên thành công!")
                edit_win.destroy()

            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi SQL", f"Lỗi cập nhật cơ sở dữ liệu: {e}")
                conn.rollback()
            except ValueError:
                messagebox.showerror("Lỗi", "Điểm quá trình và điểm thi phải là số!")
            finally:
                if conn and conn.is_connected():
                    cursor.close()
                    conn.close()

        tk.Button(edit_win, text="Lưu thay đổi", bg="#2196F3", fg="white", width=15, command=save_changes).grid(row=len(labels), columnspan=2, pady=10)

    # --- Nút Sửa và Thoát ---
    frame_buttons_search = tk.Frame(search_win)
    frame_buttons_search.pack(pady=5)

    tk.Button(frame_buttons_search, text="Sửa thông tin", width=15, bg="#FF2B2B", fg="white",
              font=("Arial", 10, "bold"), command=edit_student).grid(row=0, column=0, padx=10)

    tk.Button(frame_buttons_search, text="Thoát", width=15, bg="#FF2B2B", fg="white",
              font=("Arial", 10, "bold"), command=search_win.destroy).grid(row=0, column=1, padx=10)
    
#--- Nút Tìm kiếm ở cửa sổ chính---
btn_search = tk.Button(frame_buttons, text="Tìm kiếm/Sửa", width=12, bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), command=open_search_window)
btn_search.grid(row=0, column=4, padx=10)


# ====== Frame bảng hiển thị ======
frame_table = tk.Frame(root)
frame_table.pack(pady=10, padx=10, fill='both', expand=True)
# --- Thanh cuộn ---
scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical")
scrollbar_x = ttk.Scrollbar(frame_table, orient="horizontal")


# --- Bảng Treeview ---
columns = ("Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi", "Điểm TB")
tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show='headings',
    height=15
)
for col in columns:
    tree.heading(col, text=col.title())
    tree.column(col, width=110, anchor="center")
tree.column("Họ và tên", width=150)

tree.pack(fill="both", padx=10, pady=10)


# ====== Hàm tải dữ liệu ban đầu khi khởi động ứng dụng (READ từ MySQL) ======
def load_initial_data():
    conn = connect_db()
    if conn is None: return
        
    cursor = conn.cursor()
    
    # Lấy thông tin sinh viên và điểm, tính Điểm TB ngay trong SQL
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
        
        for record in records:
            tree.insert("", "end", values=record)
            
    except mysql.connector.Error as e:
        print(f"Lỗi khi tải dữ liệu ban đầu: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# --- Đặt vị trí bảng và thanh cuộn ---
tree.grid(row=0, column=0, sticky="nsew")
scrollbar_y.config(command=tree.yview)
scrollbar_y.grid(row=0, column=1, sticky="ns")

scrollbar_x.config(command=tree.xview)
scrollbar_x.grid(row=1, column=0, sticky="ew")

# Cho phép bảng tự co giãn khi thay đổi kích thước cửa sổ
frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

# Chạy hàm tải dữ liệu sau khi định nghĩa Treeview
load_initial_data() 

root.mainloop()