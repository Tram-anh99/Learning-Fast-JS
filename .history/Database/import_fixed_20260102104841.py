#!/usr/bin/env python3
"""
========== IMPORT DỮ LIỆU TỪ EXCEL VÀO DATABASE ==========

Script này import dữ liệu từ file Excel vào PostgreSQL database
Đã được cập nhật để khớp với schema database thực tế

Cách sử dụng:
    cd Database
    python3 import_fixed.py

Author: Tram-anh99
Date: 02/01/2026
Version: 2.0 (Fixed column names)
"""

import pandas as pd  # Thư viện đọc Excel file
import psycopg2      # Thư viện kết nối PostgreSQL
from psycopg2.extras import execute_values  # Bulk insert optimization
import os
import sys

# ========== CẤU HÌNH DATABASE ==========
DB_CONFIG = {
    'host': 'localhost',        # Database server address
    'port': 5432,               # PostgreSQL standard port (đã fix từ 5433)
    'database': 'postgres',     # Database name
    'user': 'postgres',         # Username
    'password': '123456'        # Password
}

def connect_db():
    """
    Kết nối đến PostgreSQL database
    
    Returns:
        connection object nếu thành công
        sys.exit(1) nếu lỗi
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Kết nối database thành công")
        return conn
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        print("   Kiểm tra:")
        print("   1. PostgreSQL đã chạy? (pg_isready)")
        print("   2. Port 5432 đúng?")
        print("   3. Username/password đúng?")
        sys.exit(1)

def import_loai_cay(conn):
    """
    Import loại cây trồng từ msvt_caytrong.xlsx
    
    Database table: nongsan.loai_cay
    Actual columns: ma_cay, ten_cay, ten_khoa_hoc, nhom_cay_id, mo_ta
    
    Args:
        conn: Database connection object
    """
    print("\n📥 Import Loại cây trồng...")
    
    file_path = 'msvt/msvt_caytrong.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    try:
        # Đọc Excel file với pandas
        df = pd.read_excel(file_path)
        print(f"   Đọc được {len(df)} rows từ Excel")
        
        cursor = conn.cursor()
        data = []
        
        # Duyệt qua từng row trong Excel
        for _, row in df.iterrows():
            # Skip rows có ma_cay rỗng (required field)
            ma_cay = row.get('MaLoaiCay', None)
            if not ma_cay or pd.isna(ma_cay):
                continue
                
            data.append((
                ma_cay,                              # ma_cay: Mã loại cây (VD: LC001)
                row.get('TenLoaiCay', 'N/A'),       # ten_cay: Tên loại cây
                row.get('TenKhoaHoc', None),        # ten_khoa_hoc: Tên khoa học
                None,                                # nhom_cay_id: Nhóm cây (chưa có data)
                row.get('MoTa', None)               # mo_ta: Mô tả
            ))
        
        # Bulk insert với execute_values (nhanh hơn loop)
        query = """
            INSERT INTO nongsan.loai_cay 
            (ma_cay, ten_cay, ten_khoa_hoc, nhom_cay_id, mo_ta)
            VALUES %s
            ON CONFLICT (ma_cay) DO NOTHING
        """
        # ON CONFLICT DO NOTHING: Bỏ qua nếu ma_cay đã tồn tại
        
        execute_values(cursor, query, data)
        conn.commit()
        
        print(f"✅ Import thành công {len(data)} loại cây")
        cursor.close()
        
    except Exception as e:
        print(f"❌ Lỗi import loại cây: {e}")
        conn.rollback()

def import_to_chuc_ca_nhan(conn):
    """
    Import tổ chức/cá nhân (chủ sở hữu) từ msvt_chusohuu.xlsx
    
    Database table: nongsan.to_chuc_ca_nhan
    Columns: ma_to_chuc, ten_to_chuc, loai_to_chuc, dien_thoai, email, dia_chi
    """
    print("\n📥 Import Tổ chức/Cá nhân...")
    
    file_path = 'msvt/msvt_chusohuu.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"   Đọc được {len(df)} rows từ Excel")
        
        cursor = conn.cursor()
        data = []
        
        for _, row in df.iterrows():
            # ma_to_chuc là required field
            ma_to_chuc = row.get('MaSoThue', None)
            if not ma_to_chuc or pd.isna(ma_to_chuc):
                continue
            
            data.append((
                str(ma_to_chuc),                     # ma_to_chuc: Mã số thuế
                row.get('TenToChuc', 'N/A'),         # ten_to_chuc: Tên tổ chức
                row.get('LoaiToChuc', 'Cá nhân'),   # loai_to_chuc: Loại (Cá nhân/Doanh nghiệp)
                row.get('DienThoai', None),          # dien_thoai: Số điện thoại
                row.get('Email', None),              # email: Email liên hệ
                row.get('DiaChi', None)              # dia_chi: Địa chỉ
            ))
        
        query = """
            INSERT INTO nongsan.to_chuc_ca_nhan 
            (ma_to_chuc, ten_to_chuc, loai_to_chuc, dien_thoai, email, dia_chi)
            VALUES %s
            ON CONFLICT (ma_to_chuc) DO NOTHING
        """
        
        execute_values(cursor, query, data)
        conn.commit()
        
        print(f"✅ Import thành công {len(data)} tổ chức/cá nhân")
        cursor.close()
        
    except Exception as e:
        print(f"❌ Lỗi import tổ chức: {e}")
        conn.rollback()

def import_vung_trong(conn):
    """
    Import vùng trồng từ msvt_thongtinvungtrong.xlsx
    
    Database table: nongsan.vung_trong
    Note: Cần lookup chu_so_huu_id và loai_cay_id từ ma_to_chuc và ma_cay
    """
    print("\n📥 Import Vùng trồng...")
    
    file_path = 'msvt/msvt_thongtinvungtrong.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"   Đọc được {len(df)} rows từ Excel")
        
        cursor = conn.cursor()
        imported = 0
        
        for _, row in df.iterrows():
            ma_vung = row.get('MaVung', None)
            if not ma_vung or pd.isna(ma_vung):
                continue
            
            # Lookup chu_so_huu_id from ma_to_chuc
            chu_so_huu_id = None
            ma_to_chuc = row.get('MaSoThue', None)
            if ma_to_chuc and not pd.isna(ma_to_chuc):
                cursor.execute(
                    "SELECT id FROM nongsan.to_chuc_ca_nhan WHERE ma_to_chuc = %s",
                    (str(ma_to_chuc),)
                )
                result = cursor.fetchone()
                chu_so_huu_id = result[0] if result else None
            
            # Insert vung_trong
            cursor.execute("""
                INSERT INTO nongsan.vung_trong 
                (ma_vung, ten_vung, dia_chi, dien_tich, chu_so_huu_id, trang_thai_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (ma_vung) DO NOTHING
            """, (
                str(ma_vung),                        # ma_vung: Mã vùng trồng MSVT
                row.get('TenVung', 'N/A'),          # ten_vung: Tên vùng
                row.get('DiaChi', None),            # dia_chi: Địa chỉ
                row.get('DienTich', None),          # dien_tich: Diện tích (ha)
                chu_so_huu_id,                      # chu_so_huu_id: FK to to_chuc_ca_nhan
                1                                    # trang_thai_id: 1 = Hoạt động
            ))
            imported += 1
        
        conn.commit()
        print(f"✅ Import thành công {imported} vùng trồng")
        cursor.close()
        
    except Exception as e:
        print(f"❌ Lỗi import vùng trồng: {e}")
        conn.rollback()

def import_phan_bon(conn):
    """
    Import phân bón từ DanhMuc_PhanBon_DuocPhep_LuuHanh.xlsx
    
    Database table: nongsan.phan_bon
    Columns: ma_phan_bon, ten_phan_bon, thanh_phan, don_vi, loai_phan_bon_id
    """
    print("\n📥 Import Phân bón...")
    
    file_path = 'phanbon/DanhMuc_PhanBon_DuocPhep_LuuHanh.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        print(f"   Đọc được {len(df)} rows từ Excel")
        print(f"   Columns: {df.columns.tolist()}")
        
        cursor = conn.cursor()
        imported = 0
        
        # Limit 100 rows để test
        for idx, row in df.iterrows():
            if idx >= 100:
                break
            
            try:
                # Generate ma_phan_bon
                ma_phan_bon = f"PB{idx+1:04d}"  # PB0001, PB0002, ...
                
                # Try multiple column names (Excel có thể có tên khác nhau)
                ten_phan_bon = (
                    row.get('TenPhanBon') or 
                    row.get('Tên phân bón') or 
                    row.get('Ten phan bon') or
                    'N/A'
                )
                
                thanh_phan = (
                    row.get('ThanhPhan') or
                    row.get('Thành phần') or
                    row.get('Thanh phan') or
                    None
                )
                
                cursor.execute("""
                    INSERT INTO nongsan.phan_bon 
                    (ma_phan_bon, ten_phan_bon, thanh_phan, don_vi, loai_phan_bon_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (ma_phan_bon) DO NOTHING
                """, (
                    ma_phan_bon,           # ma_phan_bon: Mã phân bón
                    ten_phan_bon,          # ten_phan_bon: Tên phân bón
                    thanh_phan,            # thanh_phan: Thành phần hóa học
                    'kg',                  # don_vi: Đơn vị tính
                    1                      # loai_phan_bon_id: 1 = Phân đạm (default)
                ))
                imported += 1
                
            except Exception as e:
                print(f"   ⚠️  Row {idx}: {str(e)[:50]}")
                continue
        
        conn.commit()
        print(f"✅ Import thành công {imported} phân bón")
        cursor.close()
        
    except Exception as e:
        print(f"❌ Lỗi import phân bón: {e}")
        conn.rollback()

def import_thuoc_bvtv(conn):
    """
    Import thuốc bảo vệ thực vật từ Excel
    
    Database table: nongsan.thuoc_bvtv
    Columns: ma_thuoc, ten_thuoc, ten_hoat_chat, ham_luong, nhom_thuoc_id, dang_bao_che, trang_thai_su_dung
    """
    print("\n📥 Import Thuốc BVTV...")
    
    file_path = 'ThuocBaoVeThucVat/23.10.24_Phu luc 1_TBVTV DUOC SU DUNG.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        print(f"   Đọc được {len(df)} rows từ Excel")
        
        cursor = conn.cursor()
        imported = 0
        
        for idx, row in df.iterrows():
            if idx >= 100:  # Limit 100
                break
            
            try:
                ma_thuoc = f"TB{idx+1:04d}"  # TB0001, TB0002, ...
                
                # Get ten_thuoc
                ten_thuoc = (
                    row.get('TenThuoc') or
                    row.get('Tên thuốc') or
                    row.get('Ten thuoc') or
                    'N/A'
                )
                
                # Auto-detect nhom_thuoc_id based on ten_thuoc
                ten_lower = str(ten_thuoc).lower()
                if 'sâu' in ten_lower or 'sau' in ten_lower:
                    nhom_thuoc_id = 1  # Trừ sâu
                elif 'nấm' in ten_lower or 'nam' in ten_lower or 'bệnh' in ten_lower or 'benh' in ten_lower:
                    nhom_thuoc_id = 2  # Diệt nấm
                elif 'cỏ' in ten_lower or 'co' in ten_lower:
                    nhom_thuoc_id = 3  # Diệt cỏ
                else:
                    nhom_thuoc_id = 1  # Default
                
                cursor.execute("""
                    INSERT INTO nongsan.thuoc_bvtv 
                    (ma_thuoc, ten_thuoc, ten_hoat_chat, ham_luong, nhom_thuoc_id, trang_thai_su_dung)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ma_thuoc) DO NOTHING
                """, (
                    ma_thuoc,                                    # ma_thuoc: Mã thuốc
                    ten_thuoc,                                   # ten_thuoc: Tên thuốc
                    row.get('HoatChat', row.get('Hoạt chất', None)),  # ten_hoat_chat
                    row.get('HamLuong', row.get('Hàm lượng', None)),  # ham_luong
                    nhom_thuoc_id,                              # nhom_thuoc_id: Nhóm thuốc
                    'Được phép'                                  # trang_thai_su_dung: Trạng thái
                ))
                imported += 1
                
            except Exception as e:
                print(f"   ⚠️  Row {idx}: {str(e)[:50]}")
                continue
        
        conn.commit()
        print(f"✅ Import thành công {imported} thuốc BVTV")
        cursor.close()
        
    except Exception as e:
        print(f"❌ Lỗi import thuốc BVTV: {e}")
        conn.rollback()

def check_data(conn):
    """
    Kiểm tra số lượng dữ liệu đã import
    """
    print("\n" + "="*70)
    print("📊 KIỂM TRA DỮ LIỆU TRONG DATABASE")
    print("="*70)
    
    cursor = conn.cursor()
    
    tables = [
        'loai_hoat_dong',
        'trang_thai_vung', 
        'loai_phan_bon',
        'nhom_thuoc_bvtv',
        'to_chuc_ca_nhan',
        'loai_cay',
        'vung_trong',
        'phan_bon',
        'thuoc_bvtv',
        'lich_su_canh_tac'
    ]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM nongsan.{table}")
        count = cursor.fetchone()[0]
        status = "✅" if count > 0 else "⚠️"
        print(f"{status} {table:30} {count:>6} rows")
    
    print("="*70)
    cursor.close()

def main():
    """
    Main function - orchestrate import process
    """
    print("="*70)
    print("🚀 IMPORT DỮ LIỆU TỪ EXCEL VÀO DATABASE")
    print("="*70)
    
    # Connect to database
    conn = connect_db()
    
    try:
        # Import theo thứ tự phụ thuộc
        # 1. Import lookup tables (đã có từ import_all_data.py cũ)
        # 2. Import master data
        import_to_chuc_ca_nhan(conn)  # Trước tiên import chủ sở hữu
        import_loai_cay(conn)         # Import loại cây
        import_vung_trong(conn)       # Import vùng trồng (cần chu_so_huu_id)
        import_phan_bon(conn)         # Import phân bón
        import_thuoc_bvtv(conn)       # Import thuốc BVTV
        
        # Check results
        check_data(conn)
        
        print("\n✅ HOÀN TẤT IMPORT DỮ LIỆU!")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình import: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("\n🔒 Đã đóng kết nối database")

if __name__ == "__main__":
    main()
