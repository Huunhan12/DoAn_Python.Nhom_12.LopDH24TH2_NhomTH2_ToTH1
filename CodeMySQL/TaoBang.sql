-- Đầu tiên chạy use Database
use QL_DiemSSV ;
-- Tạo bảng SINHVIEN
CREATE TABLE SINHVIEN (
    MaSV VARCHAR(10) PRIMARY KEY, -- Mã số sinh viên là Khóa chính
    HoTen NVARCHAR(50) NOT NULL,
    Lop VARCHAR(10) NOT NULL,
    NgaySinh DATE NOT NULL,
    GioiTinh NVARCHAR(5) NOT NULL
);
-- Tạo bảng DIEM
CREATE TABLE DIEM (
    MaSV VARCHAR(10) NOT NULL,
    TenMon NVARCHAR(50) NOT NULL,
    DiemQT DECIMAL(4, 2) NOT NULL CHECK (DiemQT >= 0 AND DiemQT <= 10),
    DiemThi DECIMAL(4, 2) NOT NULL CHECK (DiemThi >= 0 AND DiemThi <= 10),
    
    -- Thiết lập Khóa chính ghép: 1 sinh viên, 1 môn học -> 1 bản ghi điểm
    PRIMARY KEY (MaSV, TenMon),
    
    -- Thiết lập Khóa ngoại liên kết với bảng SINHVIEN
    FOREIGN KEY (MaSV) REFERENCES SINHVIEN(MaSV)
        ON DELETE CASCADE -- Nếu xóa SV, điểm của SV đó cũng bị xóa
        ON UPDATE CASCADE -- Nếu cập nhật MaSV, MaSV trong bảng DIEM cũng được cập nhật
);


