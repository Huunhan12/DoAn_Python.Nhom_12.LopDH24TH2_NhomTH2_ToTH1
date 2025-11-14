# utils.py
"""
utils.py tập trung vào việc hỗ trợ giao diện người dùng và điều phối chức năng phụ.
Cung cấp hàm center_window() để định vị cửa sổ ứng dụng ngay giữa màn hình.
Cung cấp hàm to_uppercase() để tự động chuyển chữ thường thành chữ in hoa trong các trường nhập liệu.
Cung cấp hàm capitalize_words() để viết hoa chữ cái đầu tiên của mỗi từ trong các trường nhập liệu.
Hàm open_search_window() chịu trách nhiệm xây dựng và quản lý cửa sổ "Tìm kiếm và Sửa đổi điểm sinh viên".
Hàm handle_edit() là hàm xử lý sự kiện khi người dùng nhấn nút "Sửa thông tin" sau khi đã chọn một bản ghi điểm từ bảng kết quả tìm kiếm (tree_result).
Hàm save_changes() là hàm xử lý logic khi người dùng đã nhập xong dữ liệu mới và nhấn "Lưu thay đổi" trong cửa sổ sửa chi tiết (edit_win).
"""
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
# Tệp này sẽ sử dụng hàm connect_db từ db_operations.py (hoặc main.py sẽ import)
# Để giữ tính độc lập, ta sẽ nhận các hàm sửa/tìm kiếm từ main.py khi mở cửa sổ.

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=900, h=500):
    """Canh giữa cửa sổ theo kích thước màn hình."""
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Hàm tự động chuyển chữ in hoa ======
def to_uppercase(event):
    """Gắn vào <KeyRelease> để chuyển đổi chữ in hoa."""
    widget = event.widget
    text = widget.get().upper()
    widget.delete(0, tk.END)
    widget.insert(0, text)

# ====== Hàm viết hoa chữ cái đầu cho mỗi từ ======
def capitalize_words(event):
    """Gắn vào <KeyRelease> để viết hoa chữ cái đầu mỗi từ."""
    widget = event.widget
    text = widget.get().title()
    widget.delete(0, tk.END)
    widget.insert(0, text)


# ====== Hàm mở cửa sổ tìm kiếm/sửa (Cần truyền các hàm xử lý DB) ======
def open_search_window(root, connect_db_func, search_student_func, edit_student_func, capitalize_words_func, to_uppercase_func, tree_main):
    """
    Mở cửa sổ tìm kiếm và sửa đổi điểm.
    Cần truyền các hàm xử lý DB vào để đảm bảo logic DB nằm ở db_operations.py.
    """
    # Khởi tạo cửa sổ
    search_win = tk.Toplevel(root)
    search_win.title("Tìm kiếm và Sửa đổi điểm sinh viên")
    center_window(search_win, 900, 500)
    search_win.grab_set()

    tk.Label(search_win, text="TÌM KIẾM SINH VIÊN", font=("Arial", 16, "bold"), fg="#9C27B0").pack(pady=10)
    
    # Khung nhập liệu tìm kiếm
    frame_search = tk.Frame(search_win)
    frame_search.pack(pady=5)

    tk.Label(frame_search, text="Nhập mã số sinh viên:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
    entry_search_maso = tk.Entry(frame_search, width=30)
    entry_search_maso.grid(row=0, column=1, padx=5, pady=5)
    entry_search_maso.bind("<KeyRelease>", to_uppercase_func) 
    entry_search_maso.focus()
    
    # --- Nút tìm kiếm (sử dụng search_student_func, cần định nghĩa) ---
    def handle_search():
        search_student_func(entry_search_maso.get(), tree_result)
        
    tk.Button(frame_search, text="Tìm kiếm", width=12, bg="#4CAF50", fg="white",
             font=("Arial", 10, "bold"), command=handle_search).grid(row=0, column=2, padx=10)

    # --- KHUNG CHỨA BẢNG VÀ THANH CUỘN (Sử dụng GRID cho layout bảng) ---
    frame_table_search = tk.Frame(search_win)
    frame_table_search.pack(fill='both', expand=True, padx=10, pady=5)
    frame_table_search.grid_rowconfigure(0, weight=1)
    frame_table_search.grid_columnconfigure(0, weight=1)

    # Cấu hình Treeview
    columns = ("Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi", "Điểm TB")
    tree_result = ttk.Treeview(frame_table_search, columns=columns, show="headings", height=10)

    for col in columns:
        tree_result.heading(col, text=col.title())
        tree_result.column(col, width=110, anchor="center")
    tree_result.column("Họ và tên", width=150)

    # --- Thanh cuộn dọc ---
    scrollbar_y = ttk.Scrollbar(frame_table_search, orient="vertical", command=tree_result.yview)
    tree_result.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    # --- Thanh cuộn ngang (Nếu cần) ---
    scrollbar_x = ttk.Scrollbar(frame_table_search, orient="horizontal", command=tree_result.xview)
    tree_result.configure(xscrollcommand=scrollbar_x.set)
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # Đặt vị trí bảng trong Frame chứa
    tree_result.grid(row=0, column=0, sticky="nsew")
    # --- Hàm xử lý sửa đổi (sử dụng edit_student_func) ---
    def handle_edit():
        selected_item = tree_result.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một bản ghi điểm để sửa!")
            return
        
        item_id = selected_item[0]
        values = tree_result.item(item_id, "values")
        
        # Gọi hàm edit_student_func được truyền vào
        edit_student_func(search_win, connect_db_func, values, item_id, tree_result, tree_main, capitalize_words_func)

    # Hàm xử lý nút Tìm kiếm (Gọi hàm tìm kiếm từ db_operations)
    def handle_search():
        maso = entry_search_maso.get().strip().upper()
        if not maso:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã số sinh viên!")
            return
        
        # Xóa dữ liệu cũ
        for item in tree_result.get_children():
            tree_result.delete(item)
            
        # Gọi hàm tìm kiếm từ db_operations.py
        records = search_student_func(maso)
        
        if records:
            for record in records:
                tree_result.insert("", "end", values=record)
        else:
            messagebox.showinfo("Không tìm thấy", f"Không tìm thấy sinh viên có mã số: {maso}")

    # Nút tìm kiếm
    tk.Button(frame_search, text="Tìm kiếm", width=12, bg="#4CAF50", fg="white",
                font=("Arial", 10, "bold"), command=handle_search).grid(row=0, column=2, padx=10)
    
    # Hàm xử lý nút Sửa (Gọi hàm sửa từ db_operations)
    def handle_edit():
        selected_item = tree_result.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một bản ghi điểm để sửa!")
            return

        item_id = selected_item[0]
        values = list(tree_result.item(item_id, "values")) 
        
        # Mở cửa sổ sửa thông tin sinh viên
        edit_win = tk.Toplevel(search_win)
        edit_win.title("Sửa thông tin sinh viên")
        edit_win.geometry("400x400")
        edit_win.grab_set()

        labels = ["Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi"]
        entries = {}
        editable_fields = ["Họ và tên", "Điểm quá trình", "Điểm thi"]

        for i, (lbl, val) in enumerate(zip(labels, values)):
            tk.Label(edit_win, text=lbl + ":", font=("Arial", 10, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if lbl in editable_fields:
                e = tk.Entry(edit_win, width=30)
                e.insert(0, str(val))
                e.grid(row=i, column=1, padx=10, pady=5)
                entries[lbl] = e
                if lbl == "Họ và tên":
                    e.bind("<KeyRelease>", capitalize_words_func)
            else:
                tk.Label(edit_win, text=str(val), width=30, anchor="w").grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entries[lbl] = val

        def save_changes():
            try:
                # Lấy giá trị mới
                new_hoten = entries["Họ và tên"].get().strip().title()
                diemqt = float(entries["Điểm quá trình"].get())
                diemthi = float(entries["Điểm thi"].get())
                
                if not (0 <= diemqt <= 10 and 0 <= diemthi <= 10):
                    messagebox.showerror("Lỗi", "Điểm phải là số từ 0 đến 10.")
                    return
                
                # Giá trị gốc (Khóa chính)
                maso_goc = values[0]
                monhoc_goc = values[4]
                
                diemtb = round((diemqt + diemthi) / 2, 2)
                
                # Gọi hàm cập nhật từ db_operations.py
                success = edit_student_func(maso_goc, monhoc_goc, new_hoten, diemqt, diemthi)

                if success:
                    # Đồng bộ giao diện cửa sổ tìm kiếm
                    new_values = [maso_goc, new_hoten, values[2], values[3], monhoc_goc, diemqt, diemthi, diemtb]
                    tree_result.item(item_id, values=new_values)
                    
                    # Đồng bộ Treeview chính (tree_main)
                    for row in tree_main.get_children():
                        row_values = tree_main.item(row, "values")
                        if row_values[0] == maso_goc and row_values[4] == monhoc_goc: 
                            tree_main.item(row, values=new_values)
                            break
                            
                    messagebox.showinfo("Thành công", "Cập nhật thông tin sinh viên thành công!")
                    edit_win.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Điểm quá trình và điểm thi phải là số!")
                
        tk.Button(edit_win, text="Lưu thay đổi", bg="#2196F3", fg="white", width=15, command=save_changes).grid(row=len(labels), columnspan=2, pady=10)


    # Nút Sửa và Thoát
    frame_buttons_search = tk.Frame(search_win)
    frame_buttons_search.pack(pady=5)

    tk.Button(frame_buttons_search, text="Sửa thông tin", width=15, bg="#FF2B2B", fg="white",
                font=("Arial", 10, "bold"), command=handle_edit).grid(row=0, column=0, padx=10)

    tk.Button(frame_buttons_search, text="Thoát", width=15, bg="#FF2B2B", fg="white",
                font=("Arial", 10, "bold"), command=search_win.destroy).grid(row=0, column=1, padx=10)