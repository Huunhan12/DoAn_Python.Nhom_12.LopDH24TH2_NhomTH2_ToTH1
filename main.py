# main.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector # Vẫn cần import để xử lý lỗi
# === IMPORT TỪ CÁC FILE KHÁC ===
from utils import center_window, to_uppercase, capitalize_words, open_search_window
from db_operations import (
    load_initial_data, 
    add_record_to_db, 
    delete_record_from_db,
    search_student_db,
    edit_student_db
)
from LienKet import connect_db # Chỉ cần connect_db để truyền vào hàm tìm kiếm

# ====== Cửa sổ chính ======
root = tk.Tk()
root.title("Quản lý điểm sinh viên")
center_window(root, 900, 500)
root.resizable(False, False)

# ====== TIÊU ĐỀ và FRAME NHẬP THÔNG TIN (Giữ nguyên) ======
lbl_title = tk.Label(root, text="QUẢN LÝ ĐIỂM SINH VIÊN", font=("Arial", 20, "bold"), fg="#1E88E5")
lbl_title.pack(pady=10)

frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill='x')

# --- Hàng 1: Mã số, Họ tên, Lớp ---
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


# --- Nút Thêm ---
def add_record():
    maso = entry_maso.get().strip().upper() 
    hoten = entry_hoten.get().strip()
    lop = entry_lop.get().strip().upper()
    ngaysinh_sql = date_entry.get_date().strftime('%Y-%m-%d')
    ngaysinh_display = date_entry.get() 
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

    # 2. Gọi hàm xử lý DB
    success = add_record_to_db(maso, hoten, lop, ngaysinh_sql, monhoc, gioitinh, diemqt, diemthi, tree, ngaysinh_display)
    
    # 3. Chỉ xóa thông tin điểm nếu thêm thành công
    if success:
        entry_diemqt.delete(0, tk.END)
        entry_diemthi.delete(0, tk.END)


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
    date_entry.set_date() 
    entry_maso.focus()

btn_new = tk.Button(frame_buttons, text="Nhập TT mới", width=12, bg="#03A9F4", fg="white", font=("Arial", 10, "bold"), command=clear_entries)
btn_new.grid(row=0, column=3, padx=10)
 
# --- Nút Xóa ---
def delete_record():
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi để xóa.")
        return
    
    if messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc chắn muốn xóa {len(selected_items)} bản ghi đã chọn?"):
        delete_record_from_db(selected_items, tree)

btn_delete = tk.Button(frame_buttons, text="Xóa", command=delete_record, width=12, bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
btn_delete.grid(row=0, column=1, padx=10)

# --- Nút Thoát ---
def exit_app():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát?"):
        root.destroy()
btn_exit = tk.Button(frame_buttons, text="Thoát", command=exit_app, width=12, bg="#D90000", fg="white", font=("Arial", 10, "bold"))
btn_exit.grid(row=0, column=2, padx=10) 


#--- Nút Tìm kiếm ở cửa sổ chính---
def open_search():
    """Gọi hàm mở cửa sổ tìm kiếm từ utils.py và truyền các hàm DB cần thiết."""
    open_search_window(
        root, 
        connect_db, 
        search_student_db, 
        edit_student_db, 
        capitalize_words, 
        to_uppercase,
        tree # Truyền Treeview chính để đồng bộ
    )

btn_search = tk.Button(frame_buttons, text="Tìm kiếm/Sửa", width=12, bg="#9C27B0", fg="white", font=("Arial", 10, "bold"), command=open_search)
btn_search.grid(row=0, column=4, padx=10)


# ====== Frame bảng hiển thị ======
frame_table = tk.Frame(root)
frame_table.pack(pady=10, padx=10, fill='both', expand=True)
# --- Thanh cuộn ---
scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical")
scrollbar_x = ttk.Scrollbar(frame_table, orient="horizontal")

# --- Bảng Treeview (Khởi tạo) ---
columns = ("Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi", "Điểm TB")
tree = ttk.Treeview(frame_table, columns=columns, show='headings', height=15)

for col in columns:
    tree.heading(col, text=col.title())
    tree.column(col, width=110, anchor="center")
tree.column("Họ và tên", width=150)

# --- Đặt vị trí bảng và thanh cuộn ---
tree.grid(row=0, column=0, sticky="nsew")
scrollbar_y.config(command=tree.yview)
scrollbar_y.grid(row=0, column=1, sticky="ns")

scrollbar_x.config(command=tree.xview)
scrollbar_x.grid(row=1, column=0, sticky="ew")

# Cho phép bảng tự co giãn khi thay đổi kích thước cửa sổ
frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

# ====== Tải dữ liệu ban đầu ======
initial_data = load_initial_data()
for record in initial_data:
    tree.insert("", "end", values=record)

if __name__ == "__main__":
    root.mainloop()