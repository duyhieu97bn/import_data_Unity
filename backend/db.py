import sqlite3
import os
import config

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(config.LOCAL_EXCEL_FILE)), "data.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS records (
            stt INTEGER PRIMARY KEY,
            clb TEXT DEFAULT '', ngay TEXT DEFAULT '', thang TEXT DEFAULT '',
            nam TEXT DEFAULT '', ngayThangNam TEXT DEFAULT '',
            quyenSo TEXT DEFAULT '', soBN TEXT DEFAULT '', maKH TEXT DEFAULT '',
            hoTenKH TEXT DEFAULT '', ngaySinh TEXT DEFAULT '', sdt TEXT DEFAULT '',
            maGoi TEXT DEFAULT '', sale TEXT DEFAULT '', ptChamSoc TEXT DEFAULT '',
            phanBo1 TEXT DEFAULT '', loaiThe1 TEXT DEFAULT '',
            loaiThe2 TEXT DEFAULT '', phanBo2 TEXT DEFAULT '', csNhap TEXT DEFAULT '',
            tongSS REAL DEFAULT 0, ptGym REAL DEFAULT 0, pttl REAL DEFAULT 0,
            daily REAL DEFAULT 0, boi REAL DEFAULT 0, ptTang REAL DEFAULT 0,
            buoiPtCoDinh REAL DEFAULT 0, soThang REAL DEFAULT 0,
            tongSoThang REAL DEFAULT 0, congThangBL REAL DEFAULT 0,
            congThangTang REAL DEFAULT 0, congNgayTang REAL DEFAULT 0,
            goiTap TEXT DEFAULT '', khungGioTap TEXT DEFAULT '',
            chuyenNhuong TEXT DEFAULT '', soHD TEXT DEFAULT '',
            soThangBuoi TEXT DEFAULT '', ngayBatDau TEXT DEFAULT '',
            ngayKetThuc TEXT DEFAULT '', tinhTrang TEXT DEFAULT '',
            tongSoNgay REAL DEFAULT 0, tongNgayDaDi REAL DEFAULT 0,
            tongSoNgayConLai REAL DEFAULT 0, quaTang TEXT DEFAULT '',
            donGiaNiemYet REAL DEFAULT 0, tongTienBaoLuu REAL DEFAULT 0,
            tongTienBuoiDay REAL DEFAULT 0, tongTien REAL DEFAULT 0,
            mucUuDai REAL DEFAULT 0, soTienKHGiam REAL DEFAULT 0,
            tong REAL DEFAULT 0, soTienDVPhaiThu REAL DEFAULT 0,
            bnDatCoc TEXT DEFAULT '', tenGoiNangCap TEXT DEFAULT '',
            soTienKHNangCap TEXT DEFAULT '', khDaDatCoc TEXT DEFAULT '',
            tongDatCocNangCap TEXT DEFAULT '', conPhaiThuKH TEXT DEFAULT '',
            phanTramSaleDT REAL DEFAULT 0, datCoc TEXT DEFAULT '',
            ttPhanThieu TEXT DEFAULT '', dongFull TEXT DEFAULT '',
            phiPos TEXT DEFAULT '', doanhThu TEXT DEFAULT '',
            hinhThucTT TEXT DEFAULT '', daNhanTM TEXT DEFAULT '',
            ckChung TEXT DEFAULT '', tongTienCKChung TEXT DEFAULT '',
            trangThai TEXT DEFAULT '', tongGoiTap TEXT DEFAULT '',
            loai TEXT DEFAULT '', luot TEXT DEFAULT '', nguon TEXT DEFAULT '',
            daNhapTimeSoft TEXT DEFAULT '', ghiChu TEXT DEFAULT '',
            daKichHoat TEXT DEFAULT '', tongHopDayShowGX TEXT DEFAULT '',
            thangHoanThienHD TEXT DEFAULT ''
        );

        CREATE TABLE IF NOT EXISTS goi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            maGoi TEXT NOT NULL,
            clb TEXT DEFAULT '', loaiThe TEXT DEFAULT '',
            maGoiHoatDong TEXT DEFAULT '',
            phanBo TEXT DEFAULT '', maLoaiTheTarget TEXT DEFAULT '',
            maLoaiTheLocPT TEXT DEFAULT '', thoiGian TEXT DEFAULT '',
            thoiGian2 TEXT DEFAULT '', giaNiemYet REAL DEFAULT 0,
            giaNiemYetGD REAL DEFAULT 0, ghiChu TEXT DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_goi_maGoi ON goi(maGoi);
    """)
    conn.commit()
    conn.close()
