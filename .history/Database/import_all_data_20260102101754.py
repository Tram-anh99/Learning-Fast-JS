#!/usr/bin/env python3
"""
Script import dữ liệu từ Excel vào PostgreSQL Database

Usage:
    cd Database
    python3 import_all_data.py
    
Author: Tram-anh99
Date: 02/01/2026
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
import sys

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',  # hoặc 'nongsan_db'
    'user': 'postgres',
    'password': '123456'
}

def connect_db():
    """Kết nối database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Kết nối database thành công")
        return conn
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        sys.exit(1)

def import_chu_so_huu(conn):
    """Import tổ chức/cá nhân từ msvt_chusohuu.xlsx"""
    print("\n📥 Import Chủ sở hữu...")
    
    file_path = 'msvt/msvt_chusohuu.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    df = pd.read_excel(file_path)
    print(f"   Đọc được {len(df)} rows")
    
    cursor = conn.cursor()
    
    # Chuẩn bị dữ liệu
    data = []
    for _, row in df.iterrows():
        data.append((
            row.get('MaSoThue', None),
            row.get('TenToChuc', 'N/A'),
            row.get('LoaiToChuc', 'Cá nhân'),
            row.get('DienThoai', None),
            row.get('Email', None),
            row.get('DiaChi', None)
        ))
    
    # Insert với ON CONFLICT DO NOTHING
    query = """
        INSERT INTO nongsan.to_chuc_ca_nhan 
        (ma_to_chuc, ten_to_chuc, loai_to_chuc, dien_thoai, email, dia_chi)
        VALUES %s
        ON CONFLICT (ma_to_chuc) DO NOTHING
    """
    
    execute_values(cursor, query, data)
    conn.commit()
    
    print(f"✅ Import {cursor.rowcount} tổ chức/cá nhân")
    cursor.close()

def import_loai_cay(conn):
    """Import loại cây từ msvt_caytrong.xlsx"""
    print("\n📥 Import Loại cây...")
    
    file_path = 'msvt/msvt_caytrong.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    df = pd.read_excel(file_path)
    print(f"   Đọc được {len(df)} rows")
    
    cursor = conn.cursor()
    
    data = []
    for _, row in df.iterrows():
        data.append((
            row.get('MaLoaiCay', None),
            row.get('TenLoaiCay', 'N/A'),
            row.get('TenKhoaHoc', None),
            row.get('PhanLoai', None),
            row.get('MoTa', None)
        ))
    
    query = """
        INSERT INTO nongsan.loai_cay 
        (ma_loai_cay, ten_loai_cay, ten_khoa_hoc, phan_loai, mo_ta)
        VALUES %s
        ON CONFLICT (ma_loai_cay) DO NOTHING
    """
    
    execute_values(cursor, query, data)
    conn.commit()
    
    print(f"✅ Import {cursor.rowcount} loại cây")
    cursor.close()

def import_vung_trong(conn):
    """Import vùng trồng từ msvt_thongtinvungtrong.xlsx"""
    print("\n📥 Import Vùng trồng...")
    
    file_path = 'msvt/msvt_thongtinvungtrong.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    df = pd.read_excel(file_path)
    print(f"   Đọc được {len(df)} rows")
    
    cursor = conn.cursor()
    
    for _, row in df.iterrows():
        # Get chu_so_huu_id from ma_to_chuc
        ma_to_chuc = row.get('MaSoThue')
        if ma_to_chuc:
            cursor.execute(
                "SELECT id FROM nongsan.to_chuc_ca_nhan WHERE ma_to_chuc = %s",
                (ma_to_chuc,)
            )
            result = cursor.fetchone()
            chu_so_huu_id = result[0] if result else None
        else:
            chu_so_huu_id = None
        
        # Get loai_cay_id from ma_loai_cay
        ma_loai_cay = row.get('MaLoaiCay')
        if ma_loai_cay:
            cursor.execute(
                "SELECT id FROM nongsan.loai_cay WHERE ma_loai_cay = %s",
                (ma_loai_cay,)
            )
            result = cursor.fetchone()
            loai_cay_id = result[0] if result else None
        else:
            loai_cay_id = None
        
        # Insert vung_trong
        cursor.execute("""
            INSERT INTO nongsan.vung_trong 
            (ma_vung, ten_vung, dia_chi, dien_tich, chu_so_huu_id, loai_cay_id, trang_thai_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ma_vung) DO NOTHING
        """, (
            row.get('MaVung', 'MSVT_AUTO'),
            row.get('TenVung', 'N/A'),
            row.get('DiaChi', None),
            row.get('DienTich', None),
            chu_so_huu_id,
            loai_cay_id,
            1  # Default: Hoạt động
        ))
    
    conn.commit()
    print(f"✅ Import {cursor.rowcount} vùng trồng")
    cursor.close()

def import_phan_bon(conn):
    """Import phân bón từ DanhMuc_PhanBon_DuocPhep_LuuHanh.xlsx"""
    print("\n📥 Import Phân bón...")
    
    file_path = 'phanbon/DanhMuc_PhanBon_DuocPhep_LuuHanh.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        print(f"   Đọc được {len(df)} rows")
        
        cursor = conn.cursor()
        
        imported = 0
        for idx, row in df.iterrows():
            if idx >= 100:  # Giới hạn 100 rows để test
                break
            
            try:
                cursor.execute("""
                    INSERT INTO nongsan.phan_bon 
                    (ma_phan_bon, ten_phan_bon, thanh_phan, don_vi, loai_phan_bon_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (ma_phan_bon) DO NOTHING
                """, (
                    f"PB{idx:04d}",
                    row.get('TenPhanBon', row.get('Tên phân bón', 'N/A')),
                    row.get('ThanhPhan', row.get('Thành phần', None)),
                    row.get('DonVi', row.get('Đơn vị', 'kg')),
                    1  # Default: Phân đạm
                ))
                imported += 1
            except Exception as e:
                print(f"   ⚠️  Row {idx}: {e}")
                continue
        
        conn.commit()
        print(f"✅ Import {imported} phân bón")
        cursor.close()
    except Exception as e:
        print(f"❌ Lỗi import phân bón: {e}")

def import_thuoc_bvtv(conn):
    """Import thuốc BVTV từ 23.10.24_Phu luc 1_TBVTV DUOC SU DUNG.xlsx"""
    print("\n📥 Import Thuốc BVTV...")
    
    file_path = 'ThuocBaoVeThucVat/23.10.24_Phu luc 1_TBVTV DUOC SU DUNG.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️  File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        print(f"   Đọc được {len(df)} rows")
        
        cursor = conn.cursor()
        
        imported = 0
        for idx, row in df.iterrows():
            if idx >= 100:  # Giới hạn 100 rows
                break
            
            try:
                # Determine nhom_thuoc_id based on ten_thuoc
                ten_thuoc = str(row.get('TenThuoc', row.get('Tên thuốc', ''))).lower()
                if 'sâu' in ten_thuoc:
                    nhom_thuoc_id = 1  # Trừ sâu
                elif 'nấm' in ten_thuoc or 'bệnh' in ten_thuoc:
                    nhom_thuoc_id = 2  # Diệt nấm
                elif 'cỏ' in ten_thuoc:
                    nhom_thuoc_id = 3  # Diệt cỏ
                else:
                    nhom_thuoc_id = 1  # Default
                
                cursor.execute("""
                    INSERT INTO nongsan.thuoc_bvtv 
                    (ma_thuoc, ten_thuoc, ten_hoat_chat, ham_luong, dang_bao_che, trang_thai_su_dung, nhom_thuoc_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ma_thuoc) DO NOTHING
                """, (
                    f"TB{idx:04d}",
                    row.get('TenThuoc', row.get('Tên thuốc', 'N/A')),
                    row.get('HoatChat', row.get('Hoạt chất', None)),
                    row.get('HamLuong', row.get('Hàm lượng', None)),
                    row.get('DangBaoChe', row.get('Dạng bào chế', 'EC')),
                    'Được phép',
                    nhom_thuoc_id
                ))
                imported += 1
            except Exception as e:
                print(f"   ⚠️  Row {idx}: {e}")
                continue
        
        conn.commit()
        print(f"✅ Import {imported} thuốc BVTV")
        cursor.close()
    except Exception as e:
        print(f"❌ Lỗi import thuốc BVTV: {e}")

def import_static_data(conn):
    """Import dữ liệu tĩnh (loại hoạt động, trạng thái, etc.)"""
    print("\n📥 Import dữ liệu tĩnh...")
    
    cursor = conn.cursor()
    
    # 1. Loại hoạt động
    loai_hoat_dong = [
        ('GIEO_TRONG', 'Gieo trồng', 'fa-seed', '#22c55e'),
        ('BON_PHAN', 'Bón phân', 'fa-spray-can', '#3b82f6'),
        ('PHUN_THUOC', 'Phun thuốc BVTV', 'fa-spray-can', '#f59e0b'),
        ('TUOI_NUOC', 'Tưới nước', 'fa-water', '#06b6d4'),
        ('THU_HOACH', 'Thu hoạch', 'fa-wheat', '#8b5cf6'),
        ('KHAC', 'Hoạt động khác', 'fa-ellipsis', '#64748b')
    ]
    
    for item in loai_hoat_dong:
        cursor.execute("""
            INSERT INTO nongsan.loai_hoat_dong (ma_loai, ten_loai, icon, mau_sac)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ma_loai) DO NOTHING
        """, item)
    
    print(f"✅ Import {len(loai_hoat_dong)} loại hoạt động")
    
    # 2. Trạng thái vùng
    trang_thai = [
        ('CHO_DUYET', 'Chờ duyệt', '#fbbf24', 'Vùng mới tạo chờ phê duyệt'),
        ('HOAT_DONG', 'Hoạt động', '#22c55e', 'Vùng đang canh tác'),
        ('CANH_BAO', 'Cảnh báo', '#f97316', 'Có vấn đề cần xử lý'),
        ('THU_HOI', 'Thu hồi', '#ef4444', 'Vùng bị thu hồi MSVT')
    ]
    
    for item in trang_thai:
        cursor.execute("""
            INSERT INTO nongsan.trang_thai_vung (ma_trang_thai, ten_trang_thai, mau_sac, mo_ta)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ma_trang_thai) DO NOTHING
        """, item)
    
    print(f"✅ Import {len(trang_thai)} trạng thái vùng")
    
    # 3. Loại phân bón
    loai_phan_bon = [
        ('DAM', 'Phân đạm', 'Phân cung cấp Nitơ (N)'),
        ('LAN', 'Phân lân', 'Phân cung cấp Phospho (P)'),
        ('KALI', 'Phân kali', 'Phân cung cấp Kali (K)'),
        ('HUU_CO', 'Phân hữu cơ', 'Phân vi sinh, compost')
    ]
    
    for item in loai_phan_bon:
        cursor.execute("""
            INSERT INTO nongsan.loai_phan_bon (ma_loai, ten_loai, mo_ta)
            VALUES (%s, %s, %s)
            ON CONFLICT (ma_loai) DO NOTHING
        """, item)
    
    print(f"✅ Import {len(loai_phan_bon)} loại phân bón")
    
    # 4. Nhóm thuốc BVTV
    nhom_thuoc = [
        ('TRU_SAU', 'Thuốc trừ sâu', 'Diệt sâu hại'),
        ('DIET_NAM', 'Thuốc diệt nấm', 'Phòng trừ bệnh nấm'),
        ('DIET_CO', 'Thuốc diệt cỏ', 'Diệt cỏ dại'),
        ('TRU_BO_KEN', 'Thuốc trừ bọ kẹn', 'Diệt bọ kẹn, rệp'),
        ('DIET_CHUOT', 'Thuốc diệt chuột', 'Diệt chuột gây hại'),
        ('DIEU_HOA_SINH_TRUONG', 'Chất điều hòa sinh trưởng', 'Kích thích sinh trưởng')
    ]
    
    for item in nhom_thuoc:
        cursor.execute("""
            INSERT INTO nongsan.nhom_thuoc_bvtv (ma_nhom, ten_nhom, mo_ta)
            VALUES (%s, %s, %s)
            ON CONFLICT (ma_nhom) DO NOTHING
        """, item)
    
    print(f"✅ Import {len(nhom_thuoc)} nhóm thuốc BVTV")
    
    conn.commit()
    cursor.close()

def check_data(conn):
    """Kiểm tra dữ liệu đã import"""
    print("\n📊 Kiểm tra dữ liệu...")
    
    cursor = conn.cursor()
    
    tables = [
        'to_chuc_ca_nhan',
        'loai_cay',
        'vung_trong',
        'loai_hoat_dong',
        'trang_thai_vung',
        'loai_phan_bon',
        'phan_bon',
        'nhom_thuoc_bvtv',
        'thuoc_bvtv'
    ]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM nongsan.{table}")
        count = cursor.fetchone()[0]
        print(f"   {table:25} {count:5} rows")
    
    cursor.close()

def main():
    """Main function"""
    print("=" * 60)
    print("🚀 IMPORT DỮ LIỆU VÀO DATABASE")
    print("=" * 60)
    
    conn = connect_db()
    
    try:
        # Import theo thứ tự dependency
        import_static_data(conn)
        import_chu_so_huu(conn)
        import_loai_cay(conn)
        import_vung_trong(conn)
        import_phan_bon(conn)
        import_thuoc_bvtv(conn)
        
        # Check kết quả
        check_data(conn)
        
        print("\n" + "=" * 60)
        print("✅ HOÀN THÀNH IMPORT DỮ LIỆU")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
