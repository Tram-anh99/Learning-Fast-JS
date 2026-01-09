#!/usr/bin/env python3
"""
========== IMPORT DỮ LIỆU MSVT, GIỐNG, CƠ SỞ ==========

Import dữ liệu từ 3 thư mục:
- msvt: Thị trường, quan hệ vùng trồng - thị trường
- giong: Giống cây trồng, bảo hộ giống
- coso: Các cơ sở (đóng gói, giống, phân bón, thuốc BVTV)

Author: GitHub Copilot
Date: 09/01/2026
Version: 1.0
"""

import pandas as pd
import psycopg2
import os
from datetime import datetime

# ========== CẤU HÌNH DATABASE ==========
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': '123456'
}


def connect_db():
    """Kết nối đến PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Kết nối database thành công")
        return conn
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return None


def check_table_exists(conn, table_name):
    """Kiểm tra xem bảng có tồn tại trong database không"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'nongsan' 
            AND table_name = %s
        )
    """, (table_name,))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists


def import_msvt_thitruong(conn):
    """Import thị trường xuất khẩu"""
    print("\n📥 Import Thị trường xuất khẩu...")
    
    file_path = 'msvt/msvt_thitruong.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️ File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"   Đọc được {len(df)} thị trường")
        
        # Kiểm tra bảng tồn tại
        if not check_table_exists(conn, 'thi_truong'):
            print("   ⚠️ Bảng 'thi_truong' chưa tồn tại, tạo bảng...")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nongsan.thi_truong (
                    id SERIAL PRIMARY KEY,
                    ma_thi_truong VARCHAR(20) UNIQUE NOT NULL,
                    ten_thi_truong VARCHAR(200) NOT NULL,
                    quoc_gia VARCHAR(100),
                    mo_ta TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cursor.close()
            print("   ✅ Đã tạo bảng 'thi_truong'")
        
        cursor = conn.cursor()
        imported = 0
        
        for idx, row in df.iterrows():
            tt_id = row.get('thitruong_ID')
            ten_tt = row.get('tenthitruong')
            
            if pd.notna(tt_id) and pd.notna(ten_tt):
                ma_tt = f"TT{int(tt_id):03d}"
                
                try:
                    cursor.execute("""
                        INSERT INTO nongsan.thi_truong (ma_thi_truong, ten_thi_truong, quoc_gia)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (ma_thi_truong) DO NOTHING
                    """, (ma_tt, str(ten_tt).strip(), str(ten_tt).strip()))
                    imported += 1
                except Exception as e:
                    conn.rollback()
                    if idx < 3:
                        print(f"      ⚠️ Row {idx}: {str(e)[:60]}...")
        
        conn.commit()
        cursor.close()
        print(f"   ✅ Import {imported} thị trường")
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        conn.rollback()


def import_msvt_vungtrong_thitruong(conn):
    """Import quan hệ vùng trồng - thị trường"""
    print("\n📥 Import Quan hệ Vùng trồng - Thị trường...")
    
    file_path = 'msvt/msvt_thitruongvungtrong.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️ File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"   Đọc được {len(df)} quan hệ")
        
        # Kiểm tra và tạo bảng
        if not check_table_exists(conn, 'vung_trong_thi_truong'):
            print("   ⚠️ Bảng 'vung_trong_thi_truong' chưa tồn tại, tạo bảng...")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nongsan.vung_trong_thi_truong (
                    id SERIAL PRIMARY KEY,
                    vung_trong_id INTEGER,
                    thi_truong_id INTEGER,
                    ma_vung_puc VARCHAR(50),
                    ten_vung VARCHAR(200),
                    dien_tich DECIMAL(10, 2),
                    nguoi_dai_dien VARCHAR(200),
                    xa VARCHAR(100),
                    huyen VARCHAR(100),
                    tinh VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cursor.close()
            print("   ✅ Đã tạo bảng 'vung_trong_thi_truong'")
        
        cursor = conn.cursor()
        imported = 0
        
        for idx, row in df.iterrows():
            ma_vung_puc = row.get('mavungtrong_puc')
            ten_vung = row.get('tenvungtrong')
            
            if pd.notna(ma_vung_puc) and pd.notna(ten_vung):
                try:
                    cursor.execute("""
                        INSERT INTO nongsan.vung_trong_thi_truong 
                        (ma_vung_puc, ten_vung, dien_tich, nguoi_dai_dien, xa, huyen, tinh)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (
                        str(ma_vung_puc),
                        str(ten_vung).strip(),
                        float(row.get('dientich')) if pd.notna(row.get('dientich')) else None,
                        str(row.get('nguoidaidien')) if pd.notna(row.get('nguoidaidien')) else None,
                        str(row.get('xa')) if pd.notna(row.get('xa')) else None,
                        str(row.get('huyen')) if pd.notna(row.get('huyen')) else None,
                        str(row.get('tinh')) if pd.notna(row.get('tinh')) else None
                    ))
                    imported += 1
                except Exception as e:
                    conn.rollback()
                    if idx < 3:
                        print(f"      ⚠️ Row {idx}: {str(e)[:60]}...")
        
        conn.commit()
        cursor.close()
        print(f"   ✅ Import {imported} quan hệ vùng trồng - thị trường")
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        conn.rollback()


def import_giong_caygiong(conn):
    """Import giống cây trồng"""
    print("\n📥 Import Giống cây trồng...")
    
    file_path = 'giong/gen_caygiong.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️ File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"   Đọc được {len(df)} giống cây")
        
        # Kiểm tra và tạo bảng
        if not check_table_exists(conn, 'giong_cay'):
            print("   ⚠️ Bảng 'giong_cay' chưa tồn tại, tạo bảng...")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nongsan.giong_cay (
                    id SERIAL PRIMARY KEY,
                    ma_giong VARCHAR(20) UNIQUE NOT NULL,
                    ten_cay_trong VARCHAR(200) NOT NULL,
                    ten_khoa_hoc VARCHAR(200),
                    loai_cay_id INTEGER,
                    mo_ta TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cursor.close()
            print("   ✅ Đã tạo bảng 'giong_cay'")
        
        cursor = conn.cursor()
        imported = 0
        
        for idx, row in df.iterrows():
            cay_id = row.get('caytrong_ID')
            ten_cay = row.get('ten_cay_trong')
            
            if pd.notna(cay_id) and pd.notna(ten_cay):
                ma_giong = f"GC{int(cay_id):04d}"
                ten_khoa_hoc = str(row.get('ten_khoa_hoc')) if pd.notna(row.get('ten_khoa_hoc')) else None
                
                try:
                    cursor.execute("""
                        INSERT INTO nongsan.giong_cay (ma_giong, ten_cay_trong, ten_khoa_hoc)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (ma_giong) DO NOTHING
                    """, (ma_giong, str(ten_cay).strip(), ten_khoa_hoc))
                    imported += 1
                except Exception as e:
                    conn.rollback()
                    if idx < 3:
                        print(f"      ⚠️ Row {idx}: {str(e)[:60]}...")
        
        conn.commit()
        cursor.close()
        print(f"   ✅ Import {imported} giống cây")
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        conn.rollback()


def import_giong_baoho(conn):
    """Import giống bảo hộ"""
    print("\n📥 Import Giống bảo hộ (có bằng độc quyền)...")
    
    file_path = 'giong/giong_baoho.xlsx'
    if not os.path.exists(file_path):
        print(f"⚠️ File không tồn tại: {file_path}")
        return
    
    try:
        df = pd.read_excel(file_path)
        print(f"   Đọc được {len(df)} giống bảo hộ")
        
        # Kiểm tra và tạo bảng
        if not check_table_exists(conn, 'giong_bao_ho'):
            print("   ⚠️ Bảng 'giong_bao_ho' chưa tồn tại, tạo bảng...")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nongsan.giong_bao_ho (
                    id SERIAL PRIMARY KEY,
                    so_bang VARCHAR(50) UNIQUE NOT NULL,
                    ma_giong_id VARCHAR(50),
                    ten_giong VARCHAR(200) NOT NULL,
                    loai_cay_id INTEGER,
                    ten_chu_so_huu VARCHAR(200),
                    ngay_bat_dau_hieu_luc DATE,
                    tinh_trang VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cursor.close()
            print("   ✅ Đã tạo bảng 'giong_bao_ho'")
        
        cursor = conn.cursor()
        imported = 0
        
        for idx, row in df.iterrows():
            so_bang = row.get('sobang')
            ten_giong = row.get('tengiong')
            
            if pd.notna(so_bang) and pd.notna(ten_giong):
                try:
                    # Parse date nếu có
                    ngay_bd = None
                    if pd.notna(row.get('ngaydk_bd_hieuluc')):
                        try:
                            ngay_bd = pd.to_datetime(row.get('ngaydk_bd_hieuluc')).date()
                        except:
                            pass
                    
                    cursor.execute("""
                        INSERT INTO nongsan.giong_bao_ho 
                        (so_bang, ma_giong_id, ten_giong, ten_chu_so_huu, ngay_bat_dau_hieu_luc, tinh_trang)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (so_bang) DO NOTHING
                    """, (
                        str(so_bang),
                        str(row.get('giong_ID')) if pd.notna(row.get('giong_ID')) else None,
                        str(ten_giong).strip(),
                        str(row.get('tenchusohuu')) if pd.notna(row.get('tenchusohuu')) else None,
                        ngay_bd,
                        str(row.get('Tình trạng bằng')) if pd.notna(row.get('Tình trạng bằng')) else None
                    ))
                    imported += 1
                except Exception as e:
                    conn.rollback()
                    if idx < 3:
                        print(f"      ⚠️ Row {idx}: {str(e)[:60]}...")
        
        conn.commit()
        cursor.close()
        print(f"   ✅ Import {imported} giống bảo hộ")
        
    except Exception as e:
        print(f"   ❌ Lỗi: {e}")
        conn.rollback()


def import_coso_directory(conn, subdir, table_name, prefix):
    """Import dữ liệu cơ sở từ các thư mục con"""
    print(f"\n📥 Import Cơ sở {subdir}...")
    
    dir_path = f'coso/{subdir}'
    if not os.path.exists(dir_path):
        print(f"⚠️ Thư mục không tồn tại: {dir_path}")
        return
    
    excel_files = [f for f in os.listdir(dir_path) if f.endswith(('.xlsx', '.xls'))]
    if not excel_files:
        print(f"   ⚠️ Không có file Excel nào")
        return
    
    print(f"   Tìm thấy {len(excel_files)} file")
    
    # Kiểm tra và tạo bảng
    if not check_table_exists(conn, table_name):
        print(f"   ⚠️ Bảng '{table_name}' chưa tồn tại, tạo bảng...")
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS nongsan.{table_name} (
                id SERIAL PRIMARY KEY,
                ma_co_so VARCHAR(50) UNIQUE NOT NULL,
                ten_co_so VARCHAR(500) NOT NULL,
                dia_chi TEXT,
                dien_thoai VARCHAR(50),
                email VARCHAR(100),
                loai_hinh VARCHAR(200),
                mo_ta TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        print(f"   ✅ Đã tạo bảng '{table_name}'")
    
    cursor = conn.cursor()
    total_imported = 0
    counter = 1
    
    for file_name in excel_files:
        file_path = os.path.join(dir_path, file_name)
        print(f"\n      📄 {file_name}")
        
        try:
            df = pd.read_excel(file_path)
            print(f"         Đọc được {len(df)} rows")
            
            imported = 0
            # Tìm cột tên cơ sở (có thể có nhiều tên khác nhau)
            possible_name_cols = ['ten', 'ten_co_so', 'tencoso', 'Ten', 'Tên', 'name', 
                                 'ten_doanh_nghiep', 'ten_don_vi', 'doanh_nghiep']
            name_col = None
            
            for col in df.columns:
                col_lower = str(col).lower()
                if any(keyword in col_lower for keyword in ['tên', 'ten', 'name', 'cơ sở', 'co so']):
                    name_col = col
                    break
            
            if not name_col:
                # Nếu không tìm thấy, dùng cột đầu tiên (thường là tên)
                name_col = df.columns[0]
            
            print(f"         Sử dụng cột: {name_col}")
            
            for idx, row in df.iterrows():
                ten_co_so = row.get(name_col)
                
                if pd.notna(ten_co_so) and str(ten_co_so).strip():
                    ma_co_so = f"{prefix}{counter:05d}"
                    counter += 1
                    
                    # Tìm cột địa chỉ
                    dia_chi = None
                    for col in df.columns:
                        if any(keyword in str(col).lower() for keyword in ['địa chỉ', 'dia chi', 'address']):
                            dia_chi = str(row.get(col)) if pd.notna(row.get(col)) else None
                            break
                    
                    # Tìm cột điện thoại
                    dien_thoai = None
                    for col in df.columns:
                        if any(keyword in str(col).lower() for keyword in ['điện thoại', 'dien thoai', 'sdt', 'phone']):
                            dien_thoai = str(row.get(col)) if pd.notna(row.get(col)) else None
                            break
                    
                    try:
                        cursor.execute(f"""
                            INSERT INTO nongsan.{table_name} (ma_co_so, ten_co_so, dia_chi, dien_thoai)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (ma_co_so) DO NOTHING
                        """, (ma_co_so, str(ten_co_so).strip()[:500], dia_chi, dien_thoai))
                        imported += 1
                        total_imported += 1
                    except Exception as e:
                        conn.rollback()
                        if idx < 2:
                            print(f"            ⚠️ Row {idx}: {str(e)[:50]}...")
            
            conn.commit()
            if imported > 0:
                print(f"         ✅ Import {imported} cơ sở")
            
        except Exception as e:
            print(f"         ❌ Lỗi: {str(e)[:80]}")
            conn.rollback()
    
    cursor.close()
    print(f"\n   ✅ Tổng: Import {total_imported} cơ sở từ {len(excel_files)} file")


# ========== MAIN ==========
if __name__ == "__main__":
    print("="*80)
    print("🚀 IMPORT DỮ LIỆU MSVT, GIỐNG, CƠ SỞ")
    print("="*80)
    
    conn = connect_db()
    if not conn:
        exit(1)
    
    try:
        # ========== MSVT ==========
        print("\n" + "="*80)
        print("📁 PHẦN 1: MSVT (Thị trường & Vùng trồng)")
        print("="*80)
        
        import_msvt_thitruong(conn)
        import_msvt_vungtrong_thitruong(conn)
        
        # ========== GIỐNG ==========
        print("\n" + "="*80)
        print("📁 PHẦN 2: GIỐNG CÂY TRỒNG")
        print("="*80)
        
        import_giong_caygiong(conn)
        import_giong_baoho(conn)
        
        # ========== CƠ SỞ ==========
        print("\n" + "="*80)
        print("📁 PHẦN 3: CƠ SỞ KINH DOANH")
        print("="*80)
        
        import_coso_directory(conn, 'cs_donggoi', 'co_so_dong_goi', 'DG')
        import_coso_directory(conn, 'cs_giong', 'co_so_giong', 'GG')
        import_coso_directory(conn, 'cs_pb', 'co_so_phan_bon', 'PB')
        import_coso_directory(conn, 'cs_tbvtv', 'co_so_thuoc_bvtv', 'TB')
        
        # ========== THỐNG KÊ ==========
        print("\n" + "="*80)
        print("📊 THỐNG KÊ DỮ LIỆU SAU IMPORT")
        print("="*80)
        
        cursor = conn.cursor()
        
        tables_to_check = [
            'thi_truong', 'vung_trong_thi_truong',
            'giong_cay', 'giong_bao_ho',
            'co_so_dong_goi', 'co_so_giong', 'co_so_phan_bon', 'co_so_thuoc_bvtv'
        ]
        
        for table in tables_to_check:
            if check_table_exists(conn, table):
                cursor.execute(f"SELECT COUNT(*) FROM nongsan.{table}")
                count = cursor.fetchone()[0]
                print(f"✅ {table:30s}: {count:,} records")
        
        cursor.close()
        
        print("\n" + "="*80)
        print("🎉 HOÀN TẤT IMPORT!")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()
        print("\n🔒 Đã đóng kết nối database")
