#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script chuẩn hóa và import dữ liệu vào các bảng trống
- Chuẩn hóa tên địa danh (tỉnh, huyện, xã) - viết hoa đúng chuẩn
- Import dữ liệu vào bảng tinh, huyen, xa
- Import dữ liệu vào bảng co_so từ các bảng co_so_*
- Đảm bảo tuân thủ chuẩn 3NF
"""

import psycopg2
import re
from datetime import datetime

def get_connection():
    """Kết nối database"""
    return psycopg2.connect(
        host='localhost',
        port=5432,
        database='postgres',
        user='postgres',
        password='123456'
    )

def standardize_location_name(name):
    """
    Chuẩn hóa tên địa danh:
    - Xóa khoảng trắng thừa
    - Viết hoa chữ cái đầu mỗi từ
    - Xử lý các trường hợp đặc biệt
    """
    if not name:
        return None
    
    # Trim whitespace
    name = name.strip()
    
    # Lowercase everything first
    name = name.lower()
    
    # Capitalize first letter of each word
    words = name.split()
    result = []
    
    for word in words:
        # Skip empty words
        if not word:
            continue
            
        # Các từ nên viết thường (giữa câu)
        lowercase_words = ['và', 'của', 'các', 'hoặc']
        
        if word in lowercase_words and len(result) > 0:
            result.append(word)
        else:
            # Viết hoa chữ cái đầu
            result.append(word.capitalize())
    
    return ' '.join(result)

def extract_province_from_address(address):
    """Trích xuất tên tỉnh từ địa chỉ"""
    if not address:
        return None
    
    # Common patterns: "..., <Province> province" or "tỉnh <Province>"
    patterns = [
        r',\s*([^,]+)\s+[Pp]rovince',
        r'[Tt]ỉnh\s+([^,]+)',
        r'[Tt][.]?[Pp]\s+([^,]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, address)
        if match:
            province = match.group(1).strip()
            return standardize_location_name(province)
    
    return None

def import_location_data(conn):
    """
    Import dữ liệu địa danh từ vung_trong_thi_truong vào bảng tinh, huyen, xa
    """
    cur = conn.cursor()
    
    print("="*80)
    print("🗺️  IMPORT DỮ LIỆU ĐỊA DANH")
    print("="*80)
    
    # 1. Import TỈNH
    print("\n1️⃣  Import dữ liệu TỈNH...")
    
    # Get distinct provinces
    cur.execute("""
        SELECT DISTINCT TRIM(tinh) as tinh
        FROM nongsan.vung_trong_thi_truong
        WHERE tinh IS NOT NULL AND TRIM(tinh) != ''
    """)
    
    provinces = cur.fetchall()
    imported_provinces = 0
    
    for (province,) in provinces:
        std_province = standardize_location_name(province)
        
        # Generate ma_tinh (GL for Gia Lai, etc.)
        words = std_province.split()
        ma_tinh = ''.join([w[0].upper() for w in words])
        
        # Check if already exists
        cur.execute("SELECT id FROM nongsan.tinh WHERE ten_tinh = %s", (std_province,))
        if cur.fetchone():
            continue
        
        # Insert
        cur.execute("""
            INSERT INTO nongsan.tinh (ma_tinh, ten_tinh, ngay_tao)
            VALUES (%s, %s, NOW())
            ON CONFLICT (ma_tinh) DO NOTHING
        """, (ma_tinh, std_province))
        
        imported_provinces += 1
    
    conn.commit()
    print(f"   ✅ Import {imported_provinces} tỉnh mới")
    
    # Get tinh mapping
    cur.execute("SELECT id, ten_tinh FROM nongsan.tinh")
    tinh_map = {name: id for id, name in cur.fetchall()}
    
    # 2. Import HUYỆN
    print("\n2️⃣  Import dữ liệu HUYỆN...")
    
    cur.execute("""
        SELECT DISTINCT TRIM(huyen) as huyen, TRIM(tinh) as tinh
        FROM nongsan.vung_trong_thi_truong
        WHERE huyen IS NOT NULL AND TRIM(huyen) != ''
        AND tinh IS NOT NULL AND TRIM(tinh) != ''
    """)
    
    districts = cur.fetchall()
    imported_districts = 0
    
    for huyen, tinh in districts:
        std_huyen = standardize_location_name(huyen)
        std_tinh = standardize_location_name(tinh)
        
        if std_tinh not in tinh_map:
            continue
        
        tinh_id = tinh_map[std_tinh]
        
        # Generate ma_huyen
        words = std_huyen.split()
        ma_huyen = ''.join([w[0].upper() for w in words[:3]])  # Max 3 words
        
        # Check if already exists
        cur.execute("""
            SELECT id FROM nongsan.huyen 
            WHERE ten_huyen = %s AND tinh_id = %s
        """, (std_huyen, tinh_id))
        
        if cur.fetchone():
            continue
        
        # Insert
        cur.execute("""
            INSERT INTO nongsan.huyen (ma_huyen, ten_huyen, tinh_id, ngay_tao)
            VALUES (%s, %s, %s, NOW())
            ON CONFLICT DO NOTHING
        """, (ma_huyen, std_huyen, tinh_id))
        
        imported_districts += 1
    
    conn.commit()
    print(f"   ✅ Import {imported_districts} huyện mới")
    
    # Get huyen mapping
    cur.execute("""
        SELECT h.id, h.ten_huyen, t.ten_tinh 
        FROM nongsan.huyen h
        JOIN nongsan.tinh t ON h.tinh_id = t.id
    """)
    huyen_map = {}
    for id, ten_huyen, ten_tinh in cur.fetchall():
        key = (ten_huyen, ten_tinh)
        huyen_map[key] = id
    
    # 3. Import XÃ
    print("\n3️⃣  Import dữ liệu XÃ...")
    
    cur.execute("""
        SELECT DISTINCT TRIM(xa) as xa, TRIM(huyen) as huyen, TRIM(tinh) as tinh
        FROM nongsan.vung_trong_thi_truong
        WHERE xa IS NOT NULL AND TRIM(xa) != ''
        AND huyen IS NOT NULL AND TRIM(huyen) != ''
        AND tinh IS NOT NULL AND TRIM(tinh) != ''
    """)
    
    communes = cur.fetchall()
    imported_communes = 0
    skipped_communes = 0
    
    for xa, huyen, tinh in communes:
        # Handle multiple communes in one field (separated by comma or "và")
        xa_list = re.split(r'[,và]', xa)
        
        for xa_single in xa_list:
            std_xa = standardize_location_name(xa_single.strip())
            if not std_xa:
                continue
                
            std_huyen = standardize_location_name(huyen)
            std_tinh = standardize_location_name(tinh)
            
            key = (std_huyen, std_tinh)
            if key not in huyen_map:
                skipped_communes += 1
                continue
            
            huyen_id = huyen_map[key]
            
            # Generate ma_xa
            words = std_xa.split()
            ma_xa = ''.join([w[0].upper() for w in words[:3]])
            
            # Check if already exists
            cur.execute("""
                SELECT id FROM nongsan.xa 
                WHERE ten_xa = %s AND huyen_id = %s
            """, (std_xa, huyen_id))
            
            if cur.fetchone():
                continue
            
            # Insert
            cur.execute("""
                INSERT INTO nongsan.xa (ma_xa, ten_xa, huyen_id, ngay_tao)
                VALUES (%s, %s, %s, NOW())
                ON CONFLICT DO NOTHING
            """, (ma_xa, std_xa, huyen_id))
            
            imported_communes += 1
    
    conn.commit()
    print(f"   ✅ Import {imported_communes} xã mới")
    if skipped_communes > 0:
        print(f"   ⚠️  Bỏ qua {skipped_communes} xã (không tìm thấy huyện tương ứng)")
    
    # 4. Update vung_trong_thi_truong với địa danh chuẩn hóa
    print("\n4️⃣  Chuẩn hóa địa danh trong bảng vung_trong_thi_truong...")
    
    cur.execute("""
        SELECT id, tinh, huyen, xa 
        FROM nongsan.vung_trong_thi_truong
    """)
    
    updated = 0
    for id, tinh, huyen, xa in cur.fetchall():
        std_tinh = standardize_location_name(tinh) if tinh else None
        std_huyen = standardize_location_name(huyen) if huyen else None
        std_xa = standardize_location_name(xa) if xa else None
        
        if std_tinh != tinh or std_huyen != huyen or std_xa != xa:
            cur.execute("""
                UPDATE nongsan.vung_trong_thi_truong
                SET tinh = %s, huyen = %s, xa = %s
                WHERE id = %s
            """, (std_tinh, std_huyen, std_xa, id))
            updated += 1
    
    conn.commit()
    print(f"   ✅ Chuẩn hóa {updated} records")
    
    cur.close()

def import_co_so_data(conn):
    """
    Import dữ liệu từ các bảng co_so_* vào bảng co_so chính
    Đảm bảo 3NF: co_so là bảng trung tâm, các bảng con chỉ lưu thông tin bổ sung
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🏢 IMPORT DỮ LIỆU CƠ SỞ")
    print("="*80)
    
    # Map loai_hinh to loai_hinh_id
    loai_hinh_map = {
        'Đóng gói': 1,
        'Giống': 2,
        'Phân bón': 3,
        'Thuốc BVTV': 4,
    }
    
    # Default to_chuc_id (we need to create a default organization first)
    cur.execute("""
        SELECT id FROM nongsan.to_chuc_ca_nhan 
        WHERE ma_to_chuc = 'DEFAULT'
    """)
    result = cur.fetchone()
    
    if result:
        default_to_chuc_id = result[0]
    else:
        cur.execute("""
            INSERT INTO nongsan.to_chuc_ca_nhan (
                ma_to_chuc, ten_to_chuc, loai_to_chuc, ngay_tao
            )
            VALUES ('DEFAULT', 'Chưa xác định', 'khac', NOW())
            RETURNING id
        """)
        result = cur.fetchone()
        default_to_chuc_id = result[0]
        conn.commit()
    
    total_imported = 0
    
    # 1. Import from co_so_dong_goi
    print("\n1️⃣  Import từ co_so_dong_goi...")
    
    cur.execute("""
        SELECT ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh
        FROM nongsan.co_so_dong_goi
    """)
    
    imported = 0
    for row in cur.fetchall():
        ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh = row
        
        # Check if already exists
        cur.execute("SELECT id FROM nongsan.co_so WHERE ma_co_so = %s", (ma_co_so,))
        if cur.fetchone():
            continue
        
        # Extract province from address
        province = extract_province_from_address(dia_chi)
        tinh_id = None
        
        if province:
            cur.execute("SELECT id FROM nongsan.tinh WHERE ten_tinh = %s", (province,))
            result = cur.fetchone()
            if result:
                tinh_id = result[0]
        
        # Insert
        cur.execute("""
            INSERT INTO nongsan.co_so (
                ma_co_so, ten_co_so, loai_hinh_id, to_chuc_id, 
                dia_chi, tinh_id, ngay_tao
            )
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            ON CONFLICT (ma_co_so) DO NOTHING
        """, (ma_co_so, ten_co_so, loai_hinh_map['Đóng gói'], 
              default_to_chuc_id, dia_chi, tinh_id))
        
        imported += 1
    
    conn.commit()
    print(f"   ✅ Import {imported} cơ sở đóng gói")
    total_imported += imported
    
    # 2. Import from co_so_giong
    print("\n2️⃣  Import từ co_so_giong...")
    
    cur.execute("""
        SELECT ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh
        FROM nongsan.co_so_giong
    """)
    
    imported = 0
    for row in cur.fetchall():
        ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh = row
        
        cur.execute("SELECT id FROM nongsan.co_so WHERE ma_co_so = %s", (ma_co_so,))
        if cur.fetchone():
            continue
        
        cur.execute("""
            INSERT INTO nongsan.co_so (
                ma_co_so, ten_co_so, loai_hinh_id, to_chuc_id, 
                dia_chi, ngay_tao
            )
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON CONFLICT (ma_co_so) DO NOTHING
        """, (ma_co_so, ten_co_so, loai_hinh_map['Giống'], 
              default_to_chuc_id, dia_chi))
        
        imported += 1
    
    conn.commit()
    print(f"   ✅ Import {imported} cơ sở giống")
    total_imported += imported
    
    # 3. Import from co_so_phan_bon
    print("\n3️⃣  Import từ co_so_phan_bon...")
    
    cur.execute("""
        SELECT ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh
        FROM nongsan.co_so_phan_bon
    """)
    
    imported = 0
    for row in cur.fetchall():
        ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh = row
        
        cur.execute("SELECT id FROM nongsan.co_so WHERE ma_co_so = %s", (ma_co_so,))
        if cur.fetchone():
            continue
        
        cur.execute("""
            INSERT INTO nongsan.co_so (
                ma_co_so, ten_co_so, loai_hinh_id, to_chuc_id, 
                dia_chi, ngay_tao
            )
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON CONFLICT (ma_co_so) DO NOTHING
        """, (ma_co_so, ten_co_so, loai_hinh_map['Phân bón'], 
              default_to_chuc_id, dia_chi))
        
        imported += 1
    
    conn.commit()
    print(f"   ✅ Import {imported} cơ sở phân bón")
    total_imported += imported
    
    # 4. Import from co_so_thuoc_bvtv
    print("\n4️⃣  Import từ co_so_thuoc_bvtv...")
    
    cur.execute("""
        SELECT ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh
        FROM nongsan.co_so_thuoc_bvtv
    """)
    
    imported = 0
    for row in cur.fetchall():
        ma_co_so, ten_co_so, dia_chi, dien_thoai, email, loai_hinh = row
        
        cur.execute("SELECT id FROM nongsan.co_so WHERE ma_co_so = %s", (ma_co_so,))
        if cur.fetchone():
            continue
        
        cur.execute("""
            INSERT INTO nongsan.co_so (
                ma_co_so, ten_co_so, loai_hinh_id, to_chuc_id, 
                dia_chi, ngay_tao
            )
            VALUES (%s, %s, %s, %s, %s, NOW())
            ON CONFLICT (ma_co_so) DO NOTHING
        """, (ma_co_so, ten_co_so, loai_hinh_map['Thuốc BVTV'], 
              default_to_chuc_id, dia_chi))
        
        imported += 1
    
    conn.commit()
    print(f"   ✅ Import {imported} cơ sở thuốc BVTV")
    total_imported += imported
    
    print(f"\n   🎉 TỔNG: Import {total_imported} cơ sở vào bảng co_so")
    
    cur.close()

def main():
    """Main function"""
    conn = get_connection()
    
    try:
        print("🚀 BẮT ĐẦU QUÁ TRÌNH CHUẨN HÓA VÀ IMPORT DỮ LIỆU")
        print("="*80)
        
        # 1. Import location data
        import_location_data(conn)
        
        # 2. Import co_so data
        import_co_so_data(conn)
        
        print("\n" + "="*80)
        print("✅ HOÀN THÀNH CHUẨN HÓA VÀ IMPORT DỮ LIỆU")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
