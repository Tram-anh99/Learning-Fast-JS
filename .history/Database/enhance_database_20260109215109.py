#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cải tiến database:
1. Thêm cột tọa độ (latitude, longitude) cho bảng co_so
2. Cập nhật tinh_id cho co_so từ địa chỉ
3. Import dữ liệu vào vung_cay_trong
4. Tạo các views hữu ích
"""

import psycopg2
import re
import random

def get_connection():
    """Kết nối database"""
    return psycopg2.connect(
        host='localhost',
        port=5432,
        database='postgres',
        user='postgres',
        password='123456'
    )

def add_coordinates_to_co_so(conn):
    """
    Thêm cột tọa độ cho bảng co_so
    """
    cur = conn.cursor()
    
    print("="*80)
    print("📍 THÊM TỌA ĐỘ CHO CƠ SỞ")
    print("="*80)
    
    # Check if columns already exist
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'nongsan' 
        AND table_name = 'co_so' 
        AND column_name IN ('latitude', 'longitude')
    """)
    
    existing_cols = [row[0] for row in cur.fetchall()]
    
    if 'latitude' not in existing_cols:
        print("\n1️⃣  Thêm cột latitude...")
        cur.execute("""
            ALTER TABLE nongsan.co_so 
            ADD COLUMN latitude DECIMAL(10, 8)
        """)
        conn.commit()
        print("   ✅ Đã thêm cột latitude")
    else:
        print("\n1️⃣  Cột latitude đã tồn tại")
    
    if 'longitude' not in existing_cols:
        print("\n2️⃣  Thêm cột longitude...")
        cur.execute("""
            ALTER TABLE nongsan.co_so 
            ADD COLUMN longitude DECIMAL(11, 8)
        """)
        conn.commit()
        print("   ✅ Đã thêm cột longitude")
    else:
        print("\n2️⃣  Cột longitude đã tồn tại")
    
    # Generate random coordinates for facilities based on province
    print("\n3️⃣  Tạo tọa độ mẫu cho các cơ sở...")
    
    # Province coordinates (center points)
    province_coords = {
        'Gia Lai': {'lat': 13.9, 'lon': 108.0},
        'Đắk Lắk': {'lat': 12.7, 'lon': 108.2},
        'Bến Tre': {'lat': 10.2, 'lon': 106.4},
        'Tiền Giang': {'lat': 10.4, 'lon': 106.3},
        'Long An': {'lat': 10.7, 'lon': 106.4},
        'Vĩnh Long': {'lat': 10.3, 'lon': 105.9},
    }
    
    # Get all co_so with tinh_id
    cur.execute("""
        SELECT cs.id, t.ten_tinh
        FROM nongsan.co_so cs
        LEFT JOIN nongsan.tinh t ON cs.tinh_id = t.id
        WHERE cs.latitude IS NULL OR cs.longitude IS NULL
    """)
    
    facilities = cur.fetchall()
    updated = 0
    
    for fac_id, tinh_name in facilities:
        if tinh_name and tinh_name in province_coords:
            base_lat = province_coords[tinh_name]['lat']
            base_lon = province_coords[tinh_name]['lon']
            
            # Add random offset (±0.5 degrees)
            lat = base_lat + random.uniform(-0.5, 0.5)
            lon = base_lon + random.uniform(-0.5, 0.5)
            
            cur.execute("""
                UPDATE nongsan.co_so
                SET latitude = %s, longitude = %s
                WHERE id = %s
            """, (lat, lon, fac_id))
            
            updated += 1
    
    conn.commit()
    print(f"   ✅ Đã tạo tọa độ cho {updated} cơ sở")
    
    cur.close()

def update_tinh_id_for_co_so(conn):
    """
    Cập nhật tinh_id cho các cơ sở từ địa chỉ
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🗺️  CẬP NHẬT TINH_ID CHO CƠ SỞ")
    print("="*80)
    
    # Get province mapping
    cur.execute("SELECT id, ten_tinh FROM nongsan.tinh")
    tinh_map = {name.lower(): id for id, name in cur.fetchall()}
    
    # Also add English province names
    province_name_map = {
        'ben tre': 'Bến Tre',
        'dak lak': 'Đắk Lắk',
        'gia lai': 'Gia Lai',
        'tien giang': 'Tiền Giang',
        'long an': 'Long An',
        'vinh long': 'Vĩnh Long',
    }
    
    # Get facilities without tinh_id
    cur.execute("""
        SELECT id, dia_chi 
        FROM nongsan.co_so 
        WHERE tinh_id IS NULL AND dia_chi IS NOT NULL
    """)
    
    facilities = cur.fetchall()
    updated = 0
    
    print(f"\n   Tìm thấy {len(facilities)} cơ sở chưa có tinh_id")
    
    for fac_id, dia_chi in facilities:
        if not dia_chi:
            continue
        
        # Try to extract province from address
        dia_chi_lower = dia_chi.lower()
        
        found_tinh_id = None
        
        # Check Vietnamese province names
        for vn_name, tinh_id in tinh_map.items():
            if vn_name in dia_chi_lower:
                found_tinh_id = tinh_id
                break
        
        # Check English province names
        if not found_tinh_id:
            for en_name, vn_name in province_name_map.items():
                if en_name in dia_chi_lower:
                    found_tinh_id = tinh_map.get(vn_name.lower())
                    break
        
        if found_tinh_id:
            cur.execute("""
                UPDATE nongsan.co_so
                SET tinh_id = %s
                WHERE id = %s
            """, (found_tinh_id, fac_id))
            updated += 1
    
    conn.commit()
    print(f"   ✅ Đã cập nhật tinh_id cho {updated} cơ sở")
    
    cur.close()

def import_vung_cay_trong(conn):
    """
    Import dữ liệu vào bảng vung_cay_trong
    Link vùng trồng với loại cây
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🌱 IMPORT DỮ LIỆU VÙNG CÂY TRỒNG")
    print("="*80)
    
    # Get vung_trong
    cur.execute("SELECT id FROM nongsan.vung_trong")
    vung_trong_ids = [row[0] for row in cur.fetchall()]
    
    if not vung_trong_ids:
        print("   ⚠️  Không có dữ liệu vùng trồng, bỏ qua bước này")
        cur.close()
        return
    
    # Get loai_cay
    cur.execute("SELECT id, ten_cay FROM nongsan.loai_cay")
    loai_cay_list = cur.fetchall()
    
    if not loai_cay_list:
        print("   ⚠️  Không có dữ liệu loại cây, bỏ qua bước này")
        cur.close()
        return
    
    # For each vung_trong, assign 1-2 random loai_cay
    imported = 0
    
    for vung_id in vung_trong_ids:
        # Random 1-2 crops per farm
        num_crops = random.randint(1, 2)
        selected_crops = random.sample(loai_cay_list, min(num_crops, len(loai_cay_list)))
        
        for loai_cay_id, loai_cay_name in selected_crops:
            # Random area (5-50 ha)
            dien_tich = round(random.uniform(5.0, 50.0), 2)
            
            # Check if already exists
            cur.execute("""
                SELECT id FROM nongsan.vung_cay_trong
                WHERE vung_trong_id = %s AND loai_cay_id = %s
            """, (vung_id, loai_cay_id))
            
            if cur.fetchone():
                continue
            
            # Insert
            cur.execute("""
                INSERT INTO nongsan.vung_cay_trong (
                    vung_trong_id, loai_cay_id, dien_tich, nam_trong
                )
                VALUES (%s, %s, %s, EXTRACT(YEAR FROM NOW()))
            """, (vung_id, loai_cay_id, dien_tich))
            
            imported += 1
    
    conn.commit()
    print(f"   ✅ Đã import {imported} records vào vung_cay_trong")
    
    cur.close()

def create_useful_views(conn):
    """
    Tạo các views hữu ích để query dễ dàng
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("👁️  TẠO VIEWS HỮU ÍCH")
    print("="*80)
    
    # View 1: Full farm information
    print("\n1️⃣  Tạo view v_vung_trong_full (đầy đủ thông tin vùng trồng)...")
    
    cur.execute("""
        DROP VIEW IF EXISTS nongsan.v_vung_trong_full CASCADE
    """)
    
    cur.execute("""
        CREATE VIEW nongsan.v_vung_trong_full AS
        SELECT 
            vt.id,
            vt.ma_vung,
            vt.ten_vung,
            vt.dien_tich,
            vt.so_nha,
            vt.duong,
            vt.mo_ta,
            x.ten_xa,
            h.ten_huyen,
            t.ten_tinh,
            tc.ten_to_chuc as chu_so_huu,
            tv.ten_trang_thai as trang_thai,
            vt.ngay_tao,
            vt.ngay_cap_nhat
        FROM nongsan.vung_trong vt
        LEFT JOIN nongsan.xa x ON vt.xa_id = x.id
        LEFT JOIN nongsan.huyen h ON vt.huyen_id = h.id
        LEFT JOIN nongsan.tinh t ON vt.tinh_id = t.id
        LEFT JOIN nongsan.to_chuc_ca_nhan tc ON vt.chu_so_huu_id = tc.id
        LEFT JOIN nongsan.trang_thai_vung tv ON vt.trang_thai_id = tv.id
    """)
    
    print("   ✅ Đã tạo view v_vung_trong_full")
    
    # View 2: Full facility information
    print("\n2️⃣  Tạo view v_co_so_full (đầy đủ thông tin cơ sở)...")
    
    cur.execute("""
        DROP VIEW IF EXISTS nongsan.v_co_so_full CASCADE
    """)
    
    cur.execute("""
        CREATE VIEW nongsan.v_co_so_full AS
        SELECT 
            cs.id,
            cs.ma_co_so,
            cs.ten_co_so,
            cs.bien_hieu,
            lh.ten_loai_hinh as loai_hinh,
            tc.ten_to_chuc as to_chuc,
            cs.so_giay_phep,
            cs.ngay_cap_phep,
            cs.ngay_het_han,
            cs.tinh_trang,
            cs.dia_chi,
            cs.latitude,
            cs.longitude,
            x.ten_xa,
            h.ten_huyen,
            t.ten_tinh,
            cs.ngay_tao,
            cs.ngay_cap_nhat
        FROM nongsan.co_so cs
        LEFT JOIN nongsan.loai_hinh_co_so lh ON cs.loai_hinh_id = lh.id
        LEFT JOIN nongsan.to_chuc_ca_nhan tc ON cs.to_chuc_id = tc.id
        LEFT JOIN nongsan.xa x ON cs.xa_id = x.id
        LEFT JOIN nongsan.huyen h ON cs.huyen_id = h.id
        LEFT JOIN nongsan.tinh t ON cs.tinh_id = t.id
    """)
    
    print("   ✅ Đã tạo view v_co_so_full")
    
    # View 3: Farm with crops
    print("\n3️⃣  Tạo view v_vung_cay_trong (vùng trồng cây gì)...")
    
    cur.execute("""
        DROP VIEW IF EXISTS nongsan.v_vung_cay_trong CASCADE
    """)
    
    cur.execute("""
        CREATE VIEW nongsan.v_vung_cay_trong AS
        SELECT 
            vct.id,
            vt.ma_vung,
            vt.ten_vung,
            lc.ten_cay,
            vct.dien_tich,
            vct.nam_trong,
            vct.nang_suat,
            t.ten_tinh
        FROM nongsan.vung_cay_trong vct
        JOIN nongsan.vung_trong vt ON vct.vung_trong_id = vt.id
        JOIN nongsan.loai_cay lc ON vct.loai_cay_id = lc.id
        LEFT JOIN nongsan.tinh t ON vt.tinh_id = t.id
    """)
    
    print("   ✅ Đã tạo view v_vung_cay_trong")
    
    conn.commit()
    cur.close()

def verify_enhancements(conn):
    """
    Kiểm tra kết quả sau khi cải tiến
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("✅ KIỂM TRA KẾT QUẢ SAU CẢI TIẾN")
    print("="*80)
    
    # Check coordinates
    print("\n📍 TỌA ĐỘ CƠ SỞ:")
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(latitude) as has_lat,
            COUNT(longitude) as has_lon
        FROM nongsan.co_so
    """)
    
    total, has_lat, has_lon = cur.fetchone()
    print(f"   Tổng số cơ sở:           {total:>6}")
    print(f"   Có latitude:             {has_lat:>6} ({100*has_lat/total if total > 0 else 0:.1f}%)")
    print(f"   Có longitude:            {has_lon:>6} ({100*has_lon/total if total > 0 else 0:.1f}%)")
    
    # Check tinh_id
    print("\n🗺️  TINH_ID CƠ SỞ:")
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(tinh_id) as has_tinh_id
        FROM nongsan.co_so
    """)
    
    total, has_tinh_id = cur.fetchone()
    print(f"   Tổng số cơ sở:           {total:>6}")
    print(f"   Có tinh_id:              {has_tinh_id:>6} ({100*has_tinh_id/total if total > 0 else 0:.1f}%)")
    
    # Check vung_cay_trong
    print("\n🌱 VÙNG CÂY TRỒNG:")
    cur.execute("SELECT COUNT(*) FROM nongsan.vung_cay_trong")
    vct_count = cur.fetchone()[0]
    print(f"   Số lượng records:        {vct_count:>6}")
    
    # Check views
    print("\n👁️  VIEWS:")
    views = ['v_vung_trong_full', 'v_co_so_full', 'v_vung_cay_trong']
    for view in views:
        cur.execute(f"SELECT COUNT(*) FROM nongsan.{view}")
        count = cur.fetchone()[0]
        print(f"   {view:30} {count:>6} records")
    
    print("\n" + "="*80)
    
    cur.close()

def main():
    """Main function"""
    conn = get_connection()
    
    try:
        print("🚀 BẮT ĐẦU CẢI TIẾN DATABASE")
        print("="*80)
        
        # 1. Add coordinates
        add_coordinates_to_co_so(conn)
        
        # 2. Update tinh_id
        update_tinh_id_for_co_so(conn)
        
        # 3. Import vung_cay_trong
        import_vung_cay_trong(conn)
        
        # 4. Create views
        create_useful_views(conn)
        
        # 5. Verify
        verify_enhancements(conn)
        
        print("\n" + "="*80)
        print("✅ HOÀN THÀNH CẢI TIẾN DATABASE")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ LỖI: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    main()
