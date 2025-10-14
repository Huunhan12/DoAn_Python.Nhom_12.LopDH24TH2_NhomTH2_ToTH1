import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
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
lbl_title = tk.Label(root, text="QUẢN LÝ ĐIỂM SINH VIÊN", font=("Arial", 18, "bold"))
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
    text = widget.get().title()  # Viết hoa chữ đầu tiên của mỗi từ
    widget.delete(0, tk.END)
    widget.insert(0, text)
# --- Hàng 1: Mã số, Họ tên, Lớp ---
tk.Label(frame_info, text="Mã số sinh viên:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_maso = tk.Entry(frame_info, width=10)
entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")
entry_maso.bind("<KeyRelease>", to_uppercase)  # Gọi hàm chuyển chữ in hoa khi nhập

tk.Label(frame_info, text="Họ và tên:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_hoten = tk.Entry(frame_info, width=20)
entry_hoten.grid(row=0, column=3, padx=5, pady=5, sticky="w")
entry_hoten.bind("<KeyRelease>", capitalize_words)  # Gọi hàm viết hoa chữ cái đầu cho mỗi từ khi nhập

tk.Label(frame_info, text="Lớp:").grid(row=0, column=7, padx=10, pady=5, sticky="w")
entry_lop = tk.Entry(frame_info, width=10)
entry_lop.grid(row=0, column=8, padx=5, pady=5, sticky="w")
entry_lop.bind("<KeyRelease>", to_uppercase)  # Gọi hàm chuyển chữ in hoa khi nhập

# --- Hàng 2: Ngày sinh ---

tk.Label(frame_info, text="Ngày sinh").grid(row=1, column=0, padx=5, pady=5,
sticky="w")
date_entry = DateEntry(frame_info, width=12, background="darkblue",
foreground="white", date_pattern="yyyy-mm-dd")
date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# ====== Danh sách môn học ======
mon_hoc_list = ["Chuyên đề Python", "Phân tích thiết kế hệ thống thông tin",
                 "Quản trị mạng", "Lịch sử Đảng Cộng sản Việt Nam", 
                 "Lý thuyết đồ thị", "Lập trình .NET"]

tk.Label(frame_info, text="Môn học:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
combo_monhoc = ttk.Combobox(frame_info, values=mon_hoc_list, state="readonly", width=18)
combo_monhoc.grid(row=1, column=3, padx=5, pady=5, sticky="w")
combo_monhoc.current(0)  # chọn mặc định là môn đầu tiên trong danh sách
# --- Hàng 3: Điểm ---  
tk.Label(frame_info, text="Điểm quá trình:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_diemqt = tk.Entry(frame_info, width=10)   
entry_diemqt.grid(row=2, column=1, padx=5, pady=5, sticky="w")
tk.Label(frame_info, text="Điểm thi:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
entry_diemthi = tk.Entry(frame_info, width=10)
entry_diemthi.grid(row=2, column=3, padx=5, pady=5, sticky="w")
# ====== Frame nút chức năng ======
frame_buttons = tk.Frame(root)  
frame_buttons.pack(pady=5)
# --- Nút Thêm ---
def add_record():
    maso = entry_maso.get().strip()
    hoten = entry_hoten.get().strip()
    lop = entry_lop.get().strip()
    ngaysinh = date_entry.get_date().strftime('%d/%m/%Y')
    monhoc = combo_monhoc.get()
    diemqt = entry_diemqt.get().strip()
    diemthi = entry_diemthi.get().strip()

    # Kiểm tra dữ liệu nhập
    if not (maso and hoten and lop and diemqt and diemthi):
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
        return
    try:
        diemqt = float(diemqt)
        diemthi = float(diemthi)
        if not (0 <= diemqt <= 10 and 0 <= diemthi <= 10):
            raise ValueError
    except ValueError:
        messagebox.showerror("Lỗi", "Điểm phải là số từ 0 đến 10.")
        return

    # Tính điểm trung bình
    diemtb = round((diemqt + diemthi) / 2, 2)

    # Thêm vào bảng
    tree.insert("", "end", values=(maso, hoten, lop, ngaysinh, monhoc, diemqt, diemthi, diemtb))

btn_add = tk.Button(frame_buttons, text="Thêm", command=add_record, width=10)
btn_add.grid(row=0, column=0, padx=10)

def clear_entries():
    entry_maso.delete(0, tk.END)
    entry_hoten.delete(0, tk.END)
    entry_lop.delete(0, tk.END)
    entry_diemqt.delete(0, tk.END)
    entry_diemthi.delete(0, tk.END)
    combo_monhoc.current(0)
    entry_ngaysinh.set_date('2000-01-01')
    entry_maso.focus()

btn_new = tk.Button(frame_buttons, text="Nhập TT mới", width=10, bg="#00BCD4", fg="white", command=clear_entries)
btn_new.grid(row=0, column=3, padx=10)
  
# --- Nút Xóa ---
def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn bản ghi để xóa.")
        return
    for item in selected_item:
        tree.delete(item)
btn_delete = tk.Button(frame_buttons, text="Xóa", command=delete_record, width=10)
btn_delete.grid(row=0, column=1, padx=10)
# --- Nút Thoát ---
def exit_app():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn thoát?"):
        root.destroy()
btn_exit = tk.Button(frame_buttons, text="Thoát", command=exit_app, width=10)
btn_exit.grid(row=0, column=2, padx=10) 

# ====== Hàm mở cửa sổ tìm kiếm ======
def open_search_window():
    search_win = tk.Toplevel(root)
    search_win.title("Tìm kiếm sinh viên")
    search_win.geometry("900x500")
    search_win.resizable(False, False)

    # --- Tiêu đề ---
    tk.Label(search_win, text="TÌM KIẾM SINH VIÊN", font=("Arial", 16, "bold")).pack(pady=10)

    # --- Frame nhập mã số ---
    frame_search = tk.Frame(search_win)
    frame_search.pack(pady=5)

    tk.Label(frame_search, text="Nhập mã số sinh viên:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
    entry_search_maso = tk.Entry(frame_search, width=30)
    entry_search_maso.grid(row=0, column=1, padx=5, pady=5)
    entry_search_maso.bind("<KeyRelease>", to_uppercase)  # Gọi hàm chuyển chữ in hoa khi nhập

    # --- Nút tìm kiếm ---
    tk.Button(frame_search, text="Tìm kiếm", width=12, bg="#4CAF50", fg="white",
              font=("Arial", 10, "bold"), command=lambda: search_student()).grid(row=0, column=2, padx=10)

    # --- Bảng hiển thị kết quả ---
    columns = ("Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi", "Điểm TB")
    tree_result = ttk.Treeview(search_win, columns=columns, show="headings", height=15)

    for col in columns:
        tree_result.heading(col, text=col.title())
        tree_result.column(col, width=110, anchor="center")

    tree_result.pack(fill="both", padx=10, pady=10)

    # --- Hàm tìm kiếm sinh viên ---
    def search_student():
        maso = entry_search_maso.get().strip()
        if not maso:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập mã số sinh viên!")
            return

        # Xóa dữ liệu cũ trong bảng kết quả
        for item in tree_result.get_children():
            tree_result.delete(item)

        # Tìm tất cả các dòng có mã số trùng khớp trong bảng chính
        found = False
        for row in tree.get_children():
            values = tree.item(row, "values")
            if values[0].lower() == maso.lower():  # so sánh không phân biệt hoa thường
                tree_result.insert("", "end", values=values)
                found = True

        if not found:
            messagebox.showinfo("Không tìm thấy", f"Không tìm thấy sinh viên có mã số: {maso}")
         # --- Hàm sửa thông tin sinh viên ---
    def edit_student():
        selected_item = tree_result.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một sinh viên để sửa!")
            return

        item_id = selected_item[0]
        values = list(tree_result.item(item_id, "values"))

        edit_win = tk.Toplevel(search_win)
        edit_win.title("Sửa thông tin sinh viên")
        edit_win.geometry("350x400")

        labels = ["Mã số", "Họ và tên", "Lớp", "Ngày sinh", "Môn học", "Điểm quá trình", "Điểm thi"]
        entries = {}

        for i, (lbl, val) in enumerate(zip(labels, values)):
            tk.Label(edit_win, text=lbl + ":", font=("Arial", 10, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            e = tk.Entry(edit_win, width=30)
            e.grid(row=i, column=1, padx=10, pady=5)
            e.insert(0, val)
            entries[lbl] = e

        def save_changes():
            try:
                # Cập nhật giá trị mới
                diemqt = float(entries["Điểm quá trình"].get())
                diemthi = float(entries["Điểm thi"].get())
                diemtb = round((diemqt + diemthi) / 2, 2)
                new_values = [
                    entries["Mã số"].get(),
                    entries["Họ và tên"].get(),
                    entries["Lớp"].get(),
                    entries["Ngày sinh"].get(),
                    entries["Môn học"].get(),
                    diemqt,
                    diemthi,
                    diemtb
                ]

                # Cập nhật trong bảng kết quả
                tree_result.item(item_id, values=new_values)

                # Đồng bộ sang bảng chính (tree)
                for row in tree.get_children():
                    row_values = tree.item(row, "values")
                    if row_values[0] == values[0] and row_values[4] == values[4]:  # cùng mã + cùng môn
                        tree.item(row, values=new_values)
                        break

                messagebox.showinfo("Thành công", "Cập nhật thông tin sinh viên thành công!")
                edit_win.destroy()

            except ValueError:
                messagebox.showerror("Lỗi", "Điểm quá trình và điểm thi phải là số!")

        tk.Button(edit_win, text="Lưu thay đổi", bg="#2196F3", fg="white", width=15, command=save_changes).grid(row=len(labels), columnspan=2, pady=10)

    # --- Nút Sửa và Thoát ---
    frame_buttons_search = tk.Frame(search_win)
    frame_buttons_search.pack(pady=5)

    tk.Button(frame_buttons_search, text="Sửa thông tin", width=15, bg="#FF0000", fg="white",
              font=("Arial", 10, "bold"), command=edit_student).grid(row=0, column=0, padx=10)

    tk.Button(frame_buttons_search, text="Thoát", width=15, bg="#D90000", fg="white",
              font=("Arial", 10, "bold"), command=search_win.destroy).grid(row=0, column=1, padx=10)
  
#--- Nút Tìm kiếm ở cuwar sổ chính---
btn_search = tk.Button(frame_buttons, text="Tìm kiếm", width=10, bg="#9C27B0", fg="white", command=open_search_window)
btn_search.grid(row=0, column=5, padx=5, pady=5)

# ====== Frame bảng hiển thị ======
frame_table = tk.Frame(root)
frame_table.pack(pady=10, padx=10, fill='both', expand=True)



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

tree.pack(fill="both", padx=10, pady=10)

# Cho phép bảng tự co giãn khi thay đổi kích thước cửa sổ
frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

root.mainloop()