#!/usr/bin/env python3
"""
========== IMPORT THÔNG MINH VỚI CONTENT-BASED DETECTION ==========

Script này import dữ liệu từ file Excel vào PostgreSQL với khả năng:
- Tự động phát hiện dòng tiêu đề (header row detection)
- Dự đoán loại cột dựa vào nội dung (content-based column type guessing)
- Xử lý file Excel không có tiêu đề rõ ràng

Author: GitHub Copilot
Date: 09/01/2026
Version: 3.0 (Smart Detection)
"""

import pandas as pd
import psycopg2
import os
import re
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


def detect_header_row(df, max_rows=10):
    """
    Phát hiện dòng tiêu đề thông minh dựa vào:
    - Từ khóa đặc trưng trong cột
    - Số lượng giá trị không null
    - Pattern của dữ liệu
    """
    header_keywords = [
        'tên', 'ten', 'name', 'mã', 'ma', 'code', 'stt', 'số', 'so',
        'loại', 'loai', 'type', 'thành phần', 'thanh phan', 'composition',
        'hoạt chất', 'hoat chat', 'active', 'hàm lượng', 'ham luong',
        'đơn vị', 'don vi', 'unit', 'tổ chức', 'to chuc', 'organization',
        'địa chỉ', 'dia chi', 'address', 'quyết định', 'quyet dinh',
        'ngày', 'ngay', 'date', 'đối tượng', 'doi tuong', 'pest', 'crop',
        'common name', 'trade name', 'thương phẩm', 'thuong pham'
    ]
    
    best_score = 0
    best_row = 0
    
    for idx in range(min(max_rows, len(df))):
        row = df.iloc[idx]
        score = 0
        
        # Đếm giá trị không NaN
        non_nan_count = row.notna().sum()
        if non_nan_count < 2:
            continue
        
        # Kiểm tra từ khóa
        for cell in row:
            if pd.notna(cell):
                cell_str = str(cell).lower()
                # Chỉ tính điểm nếu cell ngắn (< 50 ký tự) → có thể là tiêu đề
                if len(cell_str) < 50:
                    for keyword in header_keywords:
                        if keyword in cell_str:
                            score += 2  # Điểm cao cho từ khóa tiêu đề
                            break
        
        # Cộng điểm cho số cột có dữ liệu
        score += non_nan_count * 0.5
        
        if score > best_score:
            best_score = score
            best_row = idx
    
    return best_row if best_score > 2 else 0


def guess_column_type(column_name, sample_values):
    """
    Dự đoán loại cột dựa vào TÊN CỘT và NỘI DUNG THỰC TẾ
    """
    col_str = str(column_name).lower() if pd.notna(column_name) else ''
    
    # Lọc giá trị hợp lệ
    valid_samples = [str(v) for v in sample_values if pd.notna(v) and str(v).strip() != '']
    if len(valid_samples) < 2:
        return 'unknown'
    
    # === PHÂN TÍCH TÊN CỘT ===
    # Phân bón
    if any(word in col_str for word in ['tên phân bón', 'ten phan bon', 'tên sản phẩm phân']):
        return 'ten_phan_bon'
    
    # Thuốc BVTV
    if any(word in col_str for word in ['tên thuốc', 'ten thuoc', 'thương phẩm', 'thuong pham', 'trade name']):
        return 'ten_thuoc'
    
    # Hoạt chất
    if any(word in col_str for word in ['hoạt chất', 'hoat chat', 'active', 'common name']):
        return 'hoat_chat'
    
    # Thành phần / Hàm lượng
    if any(word in col_str for word in ['thành phần', 'thanh phan', 'hàm lượng', 'ham luong', 'composition']):
        return 'thanh_phan'
    
    # Đối tượng sử dụng
    if any(word in col_str for word in ['đối tượng', 'doi tuong', 'pest', 'crop', 'phòng trừ', 'phong tru']):
        return 'doi_tuong_su_dung'
    
    # Tổ chức / Công ty
    if any(word in col_str for word in ['tổ chức', 'to chuc', 'công ty', 'cong ty', 'cá nhân', 'ca nhan']):
        return 'to_chuc'
    
    # === PHÂN TÍCH NỘI DUNG ===
    first_samples = valid_samples[:10]
    avg_length = sum(len(s) for s in first_samples) / len(first_samples)
    
    # Dấu hiệu của TÊN SẢN PHẨM (15-100 ký tự, có ký hiệu công thức)
    if 15 <= avg_length <= 100:
        product_indicators = ['ec', 'wp', 'wg', 'sc', '%', 'g/l', 'kg', 'lít']
        has_product_indicators = any(
            any(ind.lower() in sample.lower() for ind in product_indicators)
            for sample in first_samples[:5]
        )
        
        if has_product_indicators:
            # Phân biệt phân bón vs thuốc BVTV
            pesticide_words = ['sâu', 'sau', 'nấm', 'nam', 'cỏ', 'co', 'rệp', 'rep', 'bọ', 'bo', 'lúa', 'lua', 'cải', 'cai']
            is_pesticide = any(
                any(word in sample.lower() for word in pesticide_words)
                for sample in first_samples[:5]
            )
            
            return 'ten_thuoc' if is_pesticide else 'ten_phan_bon'
    
    # Dấu hiệu của TỔ CHỨC (có từ "công ty", "TNHH", "CP")
    company_indicators = ['công ty', 'cong ty', 'cp', 'tnhh', 'ltd', 'co.', 'corp']
    if any(any(ind.lower() in sample.lower() for ind in company_indicators) for sample in first_samples):
        return 'to_chuc'
    
    # Dấu hiệu của HOẠT CHẤT / THÀNH PHẦN (có tên hóa chất, %, min, max)
    chemical_indicators = ['min', 'max', '%', 'acid', 'oxide', '-', 'ium', 'ate']
    if any(any(ind in sample.lower() for ind in chemical_indicators) for sample in first_samples):
        return 'hoat_chat'
    
    return 'unknown'


def import_phan_bon_smart(conn):
    """
    Import phân bón với SMART DETECTION
    Tự động phát hiện tiêu đề và dự đoán cột
    """
    print("\n📥 IMPORT PHÂN BÓN - SMART DETECTION")
    print("="*70)
    
    phanbon_dir = 'phanbon/'
    if not os.path.exists(phanbon_dir):
        print(f"⚠️ Thư mục {phanbon_dir} không tồn tại")
        return
    
    excel_files = [f for f in os.listdir(phanbon_dir) if f.endswith(('.xlsx', '.xls'))]
    if not excel_files:
        print(f"⚠️ Không tìm thấy file Excel nào")
        return
    
    print(f"📁 Tìm thấy {len(excel_files)} file:")
    for f in excel_files:
        print(f"   - {f}")
    
    cursor = conn.cursor()
    total_imported = 0
    counter = 1
    
    for file_name in excel_files:
        file_path = os.path.join(phanbon_dir, file_name)
        print(f"\n➡️ File: {file_name}")
        
        try:
            # Đọc file để lấy danh sách sheets
            xls = pd.ExcelFile(file_path)
            
            for sheet_name in xls.sheet_names:
                print(f"\n   📄 Sheet: '{sheet_name}'")
                
                # Đọc sheet không có header
                df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                
                if len(df_raw) == 0:
                    print(f"      ⚠️ Sheet rỗng, bỏ qua")
                    continue
                
                # Phát hiện dòng tiêu đề
                header_row = detect_header_row(df_raw)
                print(f"      🔍 Phát hiện tiêu đề ở dòng {header_row}")
                
                # Đọc lại với header đúng
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
                print(f"      📊 Đọc được {len(df)} dòng dữ liệu")
                
                # Dự đoán loại cột
                column_map = {}
                for col in df.columns:
                    sample_values = df[col].head(20).tolist()
                    col_type = guess_column_type(col, sample_values)
                    if col_type != 'unknown':
                        column_map[col_type] = col
                
                print(f"      📋 Phát hiện cột: {list(column_map.keys())}")
                
                # Tìm cột tên phân bón
                ten_pb_col = column_map.get('ten_phan_bon')
                thanh_phan_col = column_map.get('thanh_phan') or column_map.get('hoat_chat')
                
                if not ten_pb_col:
                    print(f"      ⚠️ Không tìm thấy cột tên phân bón → Bỏ qua sheet")
                    continue
                
                # Import dữ liệu
                imported_count = 0
                for idx, row in df.iterrows():
                    ten_phan_bon = row.get(ten_pb_col)
                    
                    # Kiểm tra giá trị hợp lệ
                    if not pd.notna(ten_phan_bon):
                        continue
                    
                    ten_phan_bon = str(ten_phan_bon).strip()
                    
                    # Bỏ qua giá trị không hợp lệ
                    if len(ten_phan_bon) < 3 or ten_phan_bon.lower() in ['n/a', 'nan', 'null', 'none']:
                        continue
                    
                    # Lấy thành phần (nếu có)
                    thanh_phan = None
                    if thanh_phan_col and pd.notna(row.get(thanh_phan_col)):
                        thanh_phan = str(row.get(thanh_phan_col)).strip()[:500]  # Giới hạn 500 ký tự
                    
                    # Tạo mã phân bón
                    ma_phan_bon = f"PB{counter:05d}"
                    counter += 1
                    
                    try:
                        cursor.execute("""
                            INSERT INTO nongsan.phan_bon 
                            (ma_phan_bon, ten_phan_bon, thanh_phan, don_vi, loai_phan_bon_id)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (ma_phan_bon) DO NOTHING
                        """, (ma_phan_bon, ten_phan_bon, thanh_phan, 'kg', 1))
                        
                        imported_count += 1
                        total_imported += 1
                        
                    except Exception as e:
                        conn.rollback()
                        if idx < 3:
                            print(f"         ⚠️ Row {idx+1} lỗi: {str(e)[:60]}...")
                
                if imported_count > 0:
                    conn.commit()
                    print(f"      ✅ Import {imported_count} phân bón từ sheet này")
        
        except Exception as e:
            print(f"   ❌ Lỗi đọc file: {str(e)[:100]}")
            conn.rollback()
    
    cursor.close()
    print(f"\n{'='*70}")
    print(f"✅ HOÀN TẤT: Import {total_imported} phân bón từ {len(excel_files)} file")


def import_thuoc_bvtv_smart(conn):
    """
    Import thuốc BVTV với SMART DETECTION
    """
    print("\n📥 IMPORT THUỐC BVTV - SMART DETECTION")
    print("="*70)
    
    tbvtv_dir = 'ThuocBaoVeThucVat/'
    excel_files = [f for f in os.listdir(tbvtv_dir) if f.endswith(('.xlsx', '.xls'))]
    
    if not excel_files:
        print(f"⚠️ Không tìm thấy file Excel nào")
        return
    
    print(f"📁 Tìm thấy {len(excel_files)} file")
    
    cursor = conn.cursor()
    total_imported = 0
    counter = 1
    
    for file_name in excel_files:
        file_path = os.path.join(tbvtv_dir, file_name)
        print(f"\n➡️ File: {file_name}")
        
        try:
            xls = pd.ExcelFile(file_path)
            
            for sheet_name in xls.sheet_names:
                print(f"\n   📄 Sheet: '{sheet_name}'")
                
                # Đọc sheet không có header
                df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
                
                if len(df_raw) < 2:
                    print(f"      ⚠️ Sheet quá ít dữ liệu, bỏ qua")
                    continue
                
                # Phát hiện dòng tiêu đề
                header_row = detect_header_row(df_raw)
                print(f"      🔍 Phát hiện tiêu đề ở dòng {header_row}")
                
                # Đọc lại với header đúng
                df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
                print(f"      📊 Đọc được {len(df)} dòng dữ liệu")
                
                # Dự đoán loại cột
                column_map = {}
                for col in df.columns:
                    sample_values = df[col].head(20).tolist()
                    col_type = guess_column_type(col, sample_values)
                    if col_type != 'unknown':
                        column_map[col_type] = col
                
                print(f"      📋 Phát hiện cột: {list(column_map.keys())}")
                
                # Tìm cột thuốc BVTV
                ten_thuoc_col = column_map.get('ten_thuoc')
                hoat_chat_col = column_map.get('hoat_chat')
                
                if not ten_thuoc_col:
                    print(f"      ⚠️ Không tìm thấy cột tên thuốc → Bỏ qua sheet")
                    continue
                
                # Import dữ liệu
                imported_count = 0
                for idx, row in df.iterrows():
                    ten_thuoc = row.get(ten_thuoc_col)
                    
                    if not pd.notna(ten_thuoc):
                        continue
                    
                    ten_thuoc = str(ten_thuoc).strip()
                    
                    if len(ten_thuoc) < 3 or ten_thuoc.lower() in ['n/a', 'nan', 'null', 'none']:
                        continue
                    
                    # Lấy hoạt chất
                    hoat_chat = None
                    if hoat_chat_col and pd.notna(row.get(hoat_chat_col)):
                        hoat_chat = str(row.get(hoat_chat_col)).strip()[:500]
                    
                    # Tạo mã thuốc
                    ma_thuoc = f"TBVTV{counter:05d}"
                    counter += 1
                    
                    # Auto-detect nhóm thuốc
                    ten_lower = ten_thuoc.lower()
                    if 'nấm' in ten_lower or 'bệnh' in ten_lower:
                        nhom_thuoc_id = 2  # Diệt nấm
                    elif 'cỏ' in ten_lower:
                        nhom_thuoc_id = 3  # Diệt cỏ
                    else:
                        nhom_thuoc_id = 1  # Trừ sâu (default)
                    
                    try:
                        cursor.execute("""
                            INSERT INTO nongsan.thuoc_bvtv 
                            (ma_thuoc, ten_thuoc, ten_hoat_chat, ham_luong, nhom_thuoc_id, trang_thai_su_dung, mo_ta)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (ma_thuoc) DO NOTHING
                        """, (ma_thuoc, ten_thuoc, hoat_chat, None, nhom_thuoc_id, 'Được phép', 
                              'Dữ liệu import tự động từ Excel (Smart Detection)'))
                        
                        imported_count += 1
                        total_imported += 1
                        
                    except Exception as e:
                        conn.rollback()
                        if idx < 3:
                            print(f"         ⚠️ Row {idx+1} lỗi: {str(e)[:60]}...")
                
                if imported_count > 0:
                    conn.commit()
                    print(f"      ✅ Import {imported_count} thuốc từ sheet này")
        
        except Exception as e:
            print(f"   ❌ Lỗi đọc file: {str(e)[:100]}")
            conn.rollback()
    
    cursor.close()
    print(f"\n{'='*70}")
    print(f"✅ HOÀN TẤT: Import {total_imported} thuốc BVTV từ {len(excel_files)} file")


# ========== MAIN ==========
if __name__ == "__main__":
    print("="*70)
    print("🚀 IMPORT DỮ LIỆU THÔNG MINH (SMART DETECTION)")
    print("="*70)
    
    conn = connect_db()
    if not conn:
        exit(1)
    
    try:
        # Import phân bón
        import_phan_bon_smart(conn)
        
        # Import thuốc BVTV
        import_thuoc_bvtv_smart(conn)
        
        # Kiểm tra kết quả
        print("\n" + "="*70)
        print("📊 KIỂM TRA DỮ LIỆU SAU IMPORT")
        print("="*70)
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM nongsan.phan_bon")
        pb_count = cursor.fetchone()[0]
        print(f"✅ Phân bón: {pb_count:,} records")
        
        cursor.execute("SELECT COUNT(*) FROM nongsan.thuoc_bvtv")
        thuoc_count = cursor.fetchone()[0]
        print(f"✅ Thuốc BVTV: {thuoc_count:,} records")
        
        cursor.close()
        print("\n" + "="*70)
        print("🎉 HOÀN TẤT IMPORT!")
        print("="*70)
        
    finally:
        conn.close()
        print("\n🔒 Đã đóng kết nối database")
