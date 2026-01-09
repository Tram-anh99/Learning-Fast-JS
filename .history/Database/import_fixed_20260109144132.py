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
import re  # Regular expression for content detection
from datetime import datetime

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


def detect_header_row(df, max_rows_to_check=10):
    """
    Phát hiện dòng tiêu đề trong DataFrame bằng cách phân tích nội dung
    
    Logic:
    - Dòng tiêu đề thường chứa nhiều từ khóa đặc trưng
    - Dòng tiêu đề có ít giá trị NaN
    - Dòng sau tiêu đề thường là dữ liệu thực
    
    Args:
        df: DataFrame đã đọc từ Excel
        max_rows_to_check: Số dòng đầu tiên để kiểm tra
        
    Returns:
        int: Index của dòng tiêu đề (0-based), hoặc 0 nếu không tìm thấy
    """
    header_keywords = [
        'tên', 'ten', 'name', 'mã', 'ma', 'code', 'stt', 'số', 'so',
        'loại', 'loai', 'type', 'thành phần', 'thanh phan', 'composition',
        'hoạt chất', 'hoat chat', 'active', 'hàm lượng', 'ham luong',
        'đơn vị', 'don vi', 'unit', 'tổ chức', 'to chuc', 'organization',
        'địa chỉ', 'dia chi', 'address', 'quyết định', 'quyet dinh',
        'ngày', 'ngay', 'date', 'đối tượng', 'doi tuong', 'pest', 'crop'
    ]
    
    best_score = 0
    best_row = 0
    
    for idx in range(min(max_rows_to_check, len(df))):
        row = df.iloc[idx]
        score = 0
        
        # Đếm số giá trị không NaN
        non_nan_count = row.notna().sum()
        if non_nan_count < 2:  # Quá ít giá trị → không phải tiêu đề
            continue
            
        # Kiểm tra từ khóa trong mỗi cell
        for cell in row:
            if pd.notna(cell):
                cell_str = str(cell).lower()
                for keyword in header_keywords:
                    if keyword in cell_str:
                        score += 1
                        break  # Chỉ đếm 1 lần/cell
        
        # Cộng điểm cho số cột có dữ liệu
        score += non_nan_count * 0.1
        
        if score > best_score:
            best_score = score
            best_row = idx
    
    return best_row if best_score > 1 else 0


def guess_column_type(column_name, sample_values):
    """
    Dự đoán loại cột dựa vào tên cột và giá trị mẫu
    
    Args:
        column_name: Tên cột (có thể là NaN hoặc Unnamed)
        sample_values: List các giá trị mẫu từ cột
        
    Returns:
        str: Loại cột dự đoán (ten_phan_bon, ten_thuoc, hoat_chat, etc.)
    """
    col_str = str(column_name).lower() if pd.notna(column_name) else ''
    
    # Lọc bỏ giá trị NaN trong sample
    valid_samples = [str(v).lower() for v in sample_values if pd.notna(v)]
    if not valid_samples:
        return 'unknown'
    
    # Phân tích tên cột
    if 'tên phân bón' in col_str or 'ten phan bon' in col_str:
        return 'ten_phan_bon'
    if 'tên thuốc' in col_str or 'ten thuoc' in col_str or 'thương phẩm' in col_str:
        return 'ten_thuoc'
    if 'hoạt chất' in col_str or 'hoat chat' in col_str:
        return 'hoat_chat'
    if 'hàm lượng' in col_str or 'ham luong' in col_str:
        return 'ham_luong'
    if 'thành phần' in col_str or 'thanh phan' in col_str:
        return 'thanh_phan'
    if 'loại' in col_str or 'loai' in col_str or 'nhóm' in col_str:
        return 'loai'
    if 'đơn vị' in col_str or 'don vi' in col_str or 'unit' in col_str:
        return 'don_vi'
    if 'tổ chức' in col_str or 'to chuc' in col_str or 'cá nhân' in col_str or 'ca nhan' in col_str:
        return 'to_chuc'
    if 'mã' in col_str or 'ma' in col_str or 'code' in col_str or 'stt' in col_str:
        return 'ma_so'
    if 'đối tượng' in col_str or 'doi tuong' in col_str or 'pest' in col_str or 'crop' in col_str:
        return 'doi_tuong_su_dung'
    if 'ngày' in col_str or 'ngay' in col_str or 'date' in col_str:
        return 'ngay_thang'
    
    # Phân tích nội dung mẫu
    # Kiểm tra xem có phải là cột tên sản phẩm không
    avg_length = sum(len(str(v)) for v in valid_samples[:10]) / len(valid_samples[:10])
    
    # Cột tên sản phẩm thường có độ dài 15-100 ký tự
    if 15 <= avg_length <= 100:
        # Kiểm tra xem có chứa các từ đặc trưng không
        chemical_indicators = ['ec', 'wp', 'wg', 'sc', '%', 'kg', 'lít', 'lit']
        product_indicators = any(any(ind in sample for ind in chemical_indicators) 
                                for sample in valid_samples[:5])
        
        if product_indicators:
            # Phân biệt phân bón vs thuốc BVTV
            pesticide_words = ['sâu', 'sau', 'nấm', 'nam', 'cỏ', 'co', 'rệp', 'rep', 'bọ', 'bo']
            is_pesticide = any(any(word in sample for word in pesticide_words) 
                             for sample in valid_samples[:5])
            return 'ten_thuoc' if is_pesticide else 'ten_phan_bon'
    
    # Cột công ty/tổ chức
    company_indicators = ['công ty', 'cong ty', 'cp', 'tnhh', 'ltd', 'co.']
    if any(any(ind in sample for ind in company_indicators) for sample in valid_samples[:5]):
        return 'to_chuc'
    
    return 'unknown'


def smart_read_excel(file_path, sheet_name=0):
    """
    Đọc Excel file thông minh - tự động phát hiện dòng tiêu đề
    
    Args:
        file_path: Đường dẫn file Excel
        sheet_name: Tên sheet hoặc index
        
    Returns:
        tuple: (DataFrame, dict mapping column types)
    """
    # Đọc file không có header để phân tích
    df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # Phát hiện dòng tiêu đề
    header_row = detect_header_row(df_raw)
    
    # Đọc lại với header đúng
    if header_row > 0:
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
    else:
        df = df_raw
        # Đặt tên cột là row đầu tiên
        if len(df) > 0:
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
    
    # Dự đoán loại cột
    column_types = {}
    for col in df.columns:
        sample_values = df[col].head(20).tolist()
        col_type = guess_column_type(col, sample_values)
        column_types[col] = col_type
    
    return df, column_types


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
                # ma_cay: Mã loại cây (VD: LC001)
                ma_cay,
                row.get('TenLoaiCay', 'N/A'),       # ten_cay: Tên loại cây
                # ten_khoa_hoc: Tên khoa học
                row.get('TenKhoaHoc', None),
                # nhom_cay_id: Nhóm cây (chưa có data)
                None,
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
                # loai_to_chuc: Loại (Cá nhân/Doanh nghiệp)
                row.get('LoaiToChuc', 'Cá nhân'),
                # dien_thoai: Số điện thoại
                row.get('DienThoai', None),
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
    Import phân bón từ tất cả các file Excel trong thư mục phanbon/

    Database table: nongsan.phan_bon
    Columns: ma_phan_bon, ten_phan_bon, thanh_phan, don_vi, loai_phan_bon_id

    Chức năng:
    - Đọc tất cả file .xlsx và .xls trong thư mục phanbon/
    - Tự động phát hiện cột tên phân bón và thành phần
    - Import tất cả dữ liệu có tên phân bón hợp lệ
    """
    print("\n📥 Import Phân bón từ nhiều file...")

    phanbon_dir = 'phanbon/'
    if not os.path.exists(phanbon_dir):
        print(f"⚠️  Thư mục {phanbon_dir} không tồn tại")
        return

    # Lấy danh sách tất cả file Excel trong thư mục
    excel_files = [f for f in os.listdir(
        phanbon_dir) if f.endswith(('.xlsx', '.xls'))]

    if not excel_files:
        print(f"⚠️  Không tìm thấy file Excel nào trong thư mục {phanbon_dir}")
        return

    print(f"   Tìm thấy {len(excel_files)} file Excel:")
    for f in excel_files:
        print(f"      - {f}")

    total_imported = 0
    cursor = conn.cursor()
    phan_bon_counter = 1  # Để tạo mã phân bón duy nhất

    # Danh sách các tên cột có thể chứa tên phân bón
    potential_ten_phan_bon_cols = [
        'TenPhanBon', 'Tên phân bón', 'Ten phan bon',
        'Tên sản phẩm', 'Ten san pham', 'San pham',
        'Tên', 'Ten', 'Name', 'Product Name'
    ]

    # Danh sách các tên cột có thể chứa thành phần
    potential_thanh_phan_cols = [
        'ThanhPhan', 'Thành phần', 'Thanh phan',
        'Hàm lượng', 'Ham luong', 'Content',
        'Composition', 'Formula'
    ]

    for file_name in excel_files:
        file_path = os.path.join(phanbon_dir, file_name)
        print(f"\n   ➡️  Đọc file: {file_name}")

        try:
            # Đọc tất cả sheets trong file Excel
            df_dict = pd.read_excel(file_path, sheet_name=None)

            for sheet_name, sheet_df in df_dict.items():
                print(f"      📄 Sheet: '{sheet_name}' ({len(sheet_df)} rows)")

                # Debug: Hiển thị các cột có trong sheet
                # print(f"         Columns: {sheet_df.columns.tolist()}")

                rows_imported = 0

                for idx, row in sheet_df.iterrows():
                    # Tìm tên phân bón từ các cột có thể
                    ten_phan_bon = None
                    for col in potential_ten_phan_bon_cols:
                        if col in row and pd.notna(row[col]):
                            ten_phan_bon = str(row[col]).strip()
                            # Bỏ qua các giá trị không hợp lệ
                            if len(ten_phan_bon) > 3 and ten_phan_bon.lower() not in ['n/a', 'null', 'none']:
                                break
                            else:
                                ten_phan_bon = None

                    # Bỏ qua nếu không tìm được tên phân bón hợp lệ
                    if not ten_phan_bon:
                        continue

                    # Tìm thành phần từ các cột có thể
                    thanh_phan = None
                    for col in potential_thanh_phan_cols:
                        if col in row and pd.notna(row[col]):
                            thanh_phan = str(row[col]).strip()
                            break

                    # Tạo mã phân bón duy nhất
                    # PB00001, PB00002...
                    ma_phan_bon = f"PB{phan_bon_counter:05d}"
                    phan_bon_counter += 1

                    try:
                        cursor.execute("""
                            INSERT INTO nongsan.phan_bon 
                            (ma_phan_bon, ten_phan_bon, thanh_phan, don_vi, loai_phan_bon_id)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (ma_phan_bon) DO NOTHING
                        """, (
                            ma_phan_bon,      # ma_phan_bon: Mã phân bón duy nhất
                            ten_phan_bon,     # ten_phan_bon: Tên phân bón
                            thanh_phan,       # thanh_phan: Thành phần hóa học
                            'kg',             # don_vi: Đơn vị tính (default)
                            # loai_phan_bon_id: Default (Phân đạm)
                            1
                        ))
                        rows_imported += 1
                        total_imported += 1

                    except Exception as e:
                        # In lỗi nhưng tiếp tục với row tiếp theo
                        if idx < 5:  # Chỉ in lỗi cho 5 row đầu tiên để không spam
                            print(f"         ⚠️  Row {idx+1}: {str(e)[:80]}")
                        continue

                if rows_imported > 0:
                    print(
                        f"         ✅ Import {rows_imported} phân bón từ sheet này")

            conn.commit()  # Commit sau mỗi file thành công

        except Exception as e:
            print(f"      ❌ Lỗi đọc file {file_name}: {e}")
            conn.rollback()
            continue

    cursor.close()
    print(
        f"\n✅ HOÀN TẤT import phân bón. Tổng: {total_imported} phân bón từ {len(excel_files)} file.")


def import_thuoc_bvtv(conn):
    """
    Import thuốc bảo vệ thực vật từ tất cả các file Excel trong thư mục ThuocBaoVeThucVat/

    Database table: nongsan.thuoc_bvtv
    Columns: ma_thuoc, ten_thuoc, ten_hoat_chat, ham_luong, nhom_thuoc_id, trang_thai_su_dung, mo_ta
    """
    print("\n📥 Import Thuốc BVTV từ nhiều file...")

    tbvtv_dir = 'ThuocBaoVeThucVat/'
    excel_files = [f for f in os.listdir(
        tbvtv_dir) if f.endswith(('.xlsx', '.xls'))]

    if not excel_files:
        print(f"⚠️  Không tìm thấy file Excel nào trong thư mục {tbvtv_dir}")
        return

    total_imported = 0
    cursor = conn.cursor()
    thuoc_bvtv_counter = 1  # Để tạo mã thuốc duy nhất

    for file_name in excel_files:
        file_path = os.path.join(tbvtv_dir, file_name)
        print(f"   ➡️ Đọc file: {file_name}")

        try:
            df = pd.read_excel(file_path, sheet_name=None)  # Đọc tất cả sheets

            for sheet_name, sheet_df in df.items():
                print(f"      Đọc sheet: {sheet_name} ({len(sheet_df)} rows)")
                # print(f"      Columns: {sheet_df.columns.tolist()}") # Debug: show columns

                # Cố gắng tìm các cột liên quan đến tên thuốc, hoạt chất, hàm lượng
                potential_ten_thuoc_cols = [
                    'TenThuoc', 'Tên thuốc', 'Ten thuoc', 'Tên thương phẩm', 'Tên sản phẩm']
                potential_hoat_chat_cols = [
                    'HoatChat', 'Hoạt chất', 'Hoat chat', 'Thành phần hoạt chất', 'Thanh phan hoat chat']
                potential_ham_luong_cols = [
                    'HamLuong', 'Hàm lượng', 'Ham luong']

                for idx, row in sheet_df.iterrows():
                    ten_thuoc = None
                    for col in potential_ten_thuoc_cols:
                        if col in row and pd.notna(row[col]):
                            ten_thuoc = str(row[col]).strip()
                            break

                    if not ten_thuoc or ten_thuoc == 'N/A':
                        continue  # Bỏ qua nếu không tìm được tên thuốc

                    ten_hoat_chat = None
                    for col in potential_hoat_chat_cols:
                        if col in row and pd.notna(row[col]):
                            ten_hoat_chat = str(row[col]).strip()
                            break

                    ham_luong = None
                    for col in potential_ham_luong_cols:
                        if col in row and pd.notna(row[col]):
                            ham_luong = str(row[col]).strip()
                            break

                    # Tạo mã thuốc duy nhất
                    # TBVTV00001, TBVTV00002...
                    ma_thuoc = f"TBVTV{thuoc_bvtv_counter:05d}"
                    thuoc_bvtv_counter += 1

                    # Auto-detect nhom_thuoc_id based on ten_thuoc (cải thiện logic)
                    nhom_thuoc_id = 1  # Default: Trừ sâu
                    ten_lower = ten_thuoc.lower()
                    if 'nấm' in ten_lower or 'nam' in ten_lower or 'bệnh' in ten_lower or 'benh' in ten_lower:
                        nhom_thuoc_id = 2  # Diệt nấm
                    elif 'cỏ' in ten_lower or 'co' in ten_lower:
                        nhom_thuoc_id = 3  # Diệt cỏ
                    elif 'kiểm soát' in ten_lower or 'dịch hại' in ten_lower:  # Giả định
                        nhom_thuoc_id = 6  # Điều hòa sinh trưởng

                    try:
                        cursor.execute("""
                            INSERT INTO nongsan.thuoc_bvtv 
                            (ma_thuoc, ten_thuoc, ten_hoat_chat, ham_luong, nhom_thuoc_id, trang_thai_su_dung, mo_ta)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (ma_thuoc) DO NOTHING
                        """, (
                            ma_thuoc,
                            ten_thuoc,
                            ten_hoat_chat,
                            ham_luong,
                            nhom_thuoc_id,
                            'Được phép',  # Giả định: tất cả thuốc trong các file này là được phép
                            'Dữ liệu giả định từ Excel' if ma_thuoc.startswith('TBVTV') and not pd.notna(
                                # Mô tả
                                row.get('MoTa', None)) else row.get('MoTa', None)
                        ))
                        total_imported += 1
                    except Exception as e:
                        conn.rollback()  # Rollback nếu có lỗi ở một row
                        print(
                            f"      ⚠️  Lỗi import row {idx+1} trong {file_name} (sheet {sheet_name}): {str(e)[:100]}...")

            conn.commit()  # Commit sau mỗi file
        except Exception as e:
            print(f"   ❌ Lỗi đọc hoặc xử lý file {file_name}: {e}")
            conn.rollback()

    cursor.close()
    print(
        f"✅ HOÀN TẤT import thuốc BVTV. Tổng cộng đã import {total_imported} thuốc.")


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
