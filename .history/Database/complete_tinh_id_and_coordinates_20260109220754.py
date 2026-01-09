#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to complete tinh_id and coordinates for all facilities
Improvements over enhance_database.py:
- Better province name mapping (English/Vietnamese variations)
- More aggressive address parsing
- Coordinate generation for all facilities with tinh_id
"""

import psycopg2
import re
import random
from datetime import datetime

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': '123456'
}

# Comprehensive province name mapping - AUTO-LOADED FROM DATABASE
# Will be populated dynamically from nongsan.tinh table
PROVINCE_MAPPING = {}

# Province coordinates (center points) - expanded list
PROVINCE_COORDINATES = {
    'Gia Lai': (13.9, 108.0),
    'Đắk Lắk': (12.7, 108.2),
    'Bến Tre': (10.2, 106.4),
    'Tiền Giang': (10.4, 106.3),
    'Long An': (10.7, 106.4),
    'Vĩnh Long': (10.3, 105.9),
    'Đồng Nai': (10.9, 107.2),
    'Đồng Tháp': (10.5, 105.6),
    'Cần Thơ': (10.0, 105.8),
    'Cà Mau': (9.2, 105.2),
    'Hà Nội': (21.0, 105.8),
    'Lâm Đồng': (11.6, 108.3),
    'Bình Phước': (11.7, 106.7),
    'Kon Tum': (14.4, 108.0),
    'Khánh Hòa': (12.2, 109.0),
    'Bình Thuận': (10.9, 108.1),
    'Tây Ninh': (11.3, 106.1),
    'An Giang': (10.5, 105.1),
}

def build_province_mapping(provinces_dict):
    """
    Build comprehensive province mapping from database provinces
    Includes: original name, lowercase, without accents, common variations
    """
    import unicodedata
    
    mapping = {}
    
    # Manual additions for common English/variant names
    province_variants = {
        'Đắk Lắk': ['dak lak', 'daklak', 'dac lac', 'buon ma thuot', 'buon me thuot'],
        'Gia Lai': ['gia lai', 'gialai', 'pleiku'],
        'Bến Tre': ['ben tre', 'bentre'],
        'Tiền Giang': ['tien giang', 'tiengiang', 'my tho'],
        'Long An': ['long an', 'longan', 'tan an'],
        'Vĩnh Long': ['vinh long', 'vinhlong'],
        'Đồng Nai': ['dong nai', 'dongnai', 'bien hoa'],
        'Đồng Tháp': ['dong thap', 'dongthap', 'cao lanh'],
        'Cần Thơ': ['can tho', 'cantho'],
        'Cà Mau': ['ca mau', 'camau'],
        'Hà Nội': ['ha noi', 'hanoi'],
        'Lâm Đồng': ['lam dong', 'lamdong', 'da lat', 'dalat'],
        'Bình Phước': ['binh phuoc', 'binhphuoc', 'bu dop', 'bu gia map'],
        'Kon Tum': ['kon tum', 'kontum'],
        'Khánh Hòa': ['khanh hoa', 'khanhhoa', 'nha trang'],
        'Bình Thuận': ['binh thuan', 'binhthuan', 'phan thiet'],
        'Tây Ninh': ['tay ninh', 'tayninh'],
        'An Giang': ['an giang', 'angiang', 'long xuyen', 'chau doc'],
    }
    
    for province_name in provinces_dict.keys():
        # Original name (with accents)
        key_original = province_name.lower().strip()
        mapping[key_original] = province_name
        
        # Without accents (ASCII-fold)
        key_ascii = ''.join(
            c for c in unicodedata.normalize('NFD', key_original)
            if unicodedata.category(c) != 'Mn'
        )
        # Replace đ/Đ manually
        key_ascii = key_ascii.replace('đ', 'd').replace('Đ', 'D')
        mapping[key_ascii] = province_name
        
        # Without spaces
        mapping[key_original.replace(' ', '')] = province_name
        mapping[key_ascii.replace(' ', '')] = province_name
        
        # With hyphens
        mapping[key_original.replace(' ', '-')] = province_name
        mapping[key_ascii.replace(' ', '-')] = province_name
        
        # Add manual variants
        if province_name in province_variants:
            for variant in province_variants[province_name]:
                mapping[variant] = province_name
                mapping[variant.replace(' ', '')] = province_name
                mapping[variant.replace(' ', '-')] = province_name
    
    return mapping

def extract_province_advanced(address: str, ten_co_so: str = None, province_mapping: dict = None) -> str:
def extract_province_advanced(address: str, ten_co_so: str = None, province_mapping: dict = None) -> str:
    """
    Advanced province extraction from address and facility name
    """
    if not province_mapping:
        province_mapping = PROVINCE_MAPPING
        
    if not address:
        address = ""
    if not ten_co_so:
        ten_co_so = ""
    
    # Combine address and facility name for better matching
    combined_text = f"{address} {ten_co_so}".lower()
    
    # Remove common Vietnamese words that interfere
    combined_text = re.sub(r'\b(tinh|tỉnh|province|city|tp|thanh pho|thành phố|huyen|huyện|district|xa|xã|commune|ward)\b', ' ', combined_text)
    
    # Try exact match first (longest keys first to match "dong thap" before "dong")
    sorted_keys = sorted(province_mapping.keys(), key=len, reverse=True)
    for key in sorted_keys:
        if key in combined_text:
            return province_mapping[key]
    
    # Try word-boundary match (more strict)
    for key in sorted_keys:
        pattern = r'\b' + re.escape(key) + r'\b'
        if re.search(pattern, combined_text):
            return province_mapping[key]
    
    return None

def update_tinh_id_comprehensive(conn):
    """
    Update tinh_id for all facilities using comprehensive matching
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("📍 CẬP NHẬT TINH_ID CHO CƠ SỞ (COMPREHENSIVE)")
    print("="*80)
    
    # Get all provinces
    cur.execute("SELECT id, ten_tinh FROM nongsan.tinh ORDER BY id")
    provinces = {row[1]: row[0] for row in cur.fetchall()}
    print(f"\n✅ Loaded {len(provinces)} provinces from database")
    for ten_tinh, tinh_id in provinces.items():
        print(f"   - {ten_tinh} (id={tinh_id})")
    
    # Build comprehensive mapping
    print(f"\n🔧 Building province mapping...")
    province_mapping = build_province_mapping(provinces)
    print(f"✅ Created {len(province_mapping)} mapping entries")
    
    # Get all facilities without tinh_id
    cur.execute("""
        SELECT id, ma_co_so, ten_co_so, dia_chi, tinh_id
        FROM nongsan.co_so
        ORDER BY id
    """)
    facilities = cur.fetchall()
    
    total = len(facilities)
    has_tinh_id = sum(1 for f in facilities if f[4] is not None)
    needs_update = total - has_tinh_id
    
    print(f"\n📊 THỐNG KÊ:")
    print(f"   Tổng số cơ sở:          {total:,}")
    print(f"   Đã có tinh_id:          {has_tinh_id:,} ({has_tinh_id/total*100:.1f}%)")
    print(f"   Cần cập nhật:           {needs_update:,} ({needs_update/total*100:.1f}%)")
    
    # Update facilities
    updated = 0
    skipped = 0
    failed = 0
    
    print(f"\n🔄 Bắt đầu cập nhật...")
    
    for fid, ma_co_so, ten_co_so, dia_chi, current_tinh_id in facilities:
        if current_tinh_id is not None:
            skipped += 1
            continue
        
        # Try to extract province
        province_name = extract_province_advanced(dia_chi, ten_co_so, province_mapping)
        
        if province_name and province_name in provinces:
            tinh_id = provinces[province_name]
            cur.execute("""
                UPDATE nongsan.co_so
                SET tinh_id = %s
                WHERE id = %s
            """, (tinh_id, fid))
            updated += 1
            
            if updated <= 10 or updated % 1000 == 0:
                print(f"   ✅ [{updated:,}] {ma_co_so}: {ten_co_so[:40] if ten_co_so else 'N/A'}")
                print(f"      Address: {dia_chi[:60] if dia_chi else 'N/A'}")
                print(f"      → {province_name} (id={tinh_id})")
        else:
            failed += 1
            if failed <= 5:
                print(f"   ❌ Failed: {ma_co_so}: {ten_co_so[:40] if ten_co_so else 'N/A'}")
                print(f"      Address: {dia_chi[:60] if dia_chi else 'N/A'}")
    
    conn.commit()
    
    print(f"\n" + "="*80)
    print(f"✅ HOÀN THÀNH CẬP NHẬT TINH_ID")
    print(f"="*80)
    print(f"   Updated:    {updated:,} facilities")
    print(f"   Skipped:    {skipped:,} (already have tinh_id)")
    print(f"   Failed:     {failed:,} (could not determine province)")
    print(f"   Success:    {(updated/(updated+failed)*100):.1f}%")
    
    # Final stats
    cur.execute("SELECT COUNT(*) FROM nongsan.co_so WHERE tinh_id IS NOT NULL")
    final_count = cur.fetchone()[0]
    print(f"\n📊 TỔNG KẾT:")
    print(f"   Cơ sở có tinh_id:  {final_count:,}/{total:,} ({final_count/total*100:.1f}%)")
    
    return updated

def generate_coordinates_for_all(conn):
    """
    Generate coordinates for all facilities with tinh_id
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🗺️  TẠO TỌA ĐỘ CHO TẤT CẢ CƠ SỞ")
    print("="*80)
    
    # Get provinces
    cur.execute("SELECT id, ten_tinh FROM nongsan.tinh")
    provinces = {row[0]: row[1] for row in cur.fetchall()}
    
    # Get facilities with tinh_id but no coordinates
    cur.execute("""
        SELECT id, ma_co_so, ten_co_so, tinh_id
        FROM nongsan.co_so
        WHERE tinh_id IS NOT NULL
        AND (latitude IS NULL OR longitude IS NULL)
    """)
    facilities = cur.fetchall()
    
    print(f"\n📊 Facilities cần tọa độ: {len(facilities):,}")
    
    updated = 0
    skipped = 0
    
    for fid, ma_co_so, ten_co_so, tinh_id in facilities:
        province_name = provinces.get(tinh_id)
        
        if not province_name or province_name not in PROVINCE_COORDINATES:
            skipped += 1
            continue
        
        # Get province center
        base_lat, base_lon = PROVINCE_COORDINATES[province_name]
        
        # Random offset ±0.5 degrees (roughly ±55 km)
        lat = base_lat + random.uniform(-0.5, 0.5)
        lon = base_lon + random.uniform(-0.5, 0.5)
        
        # Update coordinates
        cur.execute("""
            UPDATE nongsan.co_so
            SET latitude = %s, longitude = %s
            WHERE id = %s
        """, (lat, lon, fid))
        updated += 1
        
        if updated <= 10 or updated % 1000 == 0:
            print(f"   ✅ [{updated:,}] {ma_co_so}: {province_name}")
            print(f"      → ({lat:.6f}, {lon:.6f})")
    
    conn.commit()
    
    print(f"\n" + "="*80)
    print(f"✅ HOÀN THÀNH TẠO TỌA ĐỘ")
    print(f"="*80)
    print(f"   Updated:    {updated:,} facilities")
    print(f"   Skipped:    {skipped:,} (no province mapping)")
    
    # Final stats
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(latitude) as has_coords,
            COUNT(tinh_id) as has_province
        FROM nongsan.co_so
    """)
    total, has_coords, has_province = cur.fetchone()
    
    print(f"\n📊 TỔNG KẾT:")
    print(f"   Tổng cơ sở:       {total:,}")
    print(f"   Có tọa độ:        {has_coords:,} ({has_coords/total*100:.1f}%)")
    print(f"   Có tinh_id:       {has_province:,} ({has_province/total*100:.1f}%)")
    
    return updated

def analyze_failed_extractions(conn):
    """
    Analyze facilities that still don't have tinh_id
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🔍 PHÂN TÍCH CÁC CƠ SỞ CHƯA CÓ TINH_ID")
    print("="*80)
    
    cur.execute("""
        SELECT ma_co_so, ten_co_so, dia_chi
        FROM nongsan.co_so
        WHERE tinh_id IS NULL
        LIMIT 50
    """)
    
    failed = cur.fetchall()
    
    print(f"\nTop 50 cơ sở chưa xác định được tỉnh:\n")
    
    for i, (ma, ten, dia_chi) in enumerate(failed, 1):
        print(f"{i}. {ma}: {ten[:50]}")
        print(f"   Address: {dia_chi[:80] if dia_chi else 'N/A'}")
        print()

def main():
    """
    Main execution
    """
    print("\n" + "="*80)
    print("🚀 COMPLETE TINH_ID AND COORDINATES FOR ALL FACILITIES")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Connect to database
        print("\n📡 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected successfully!")
        
        # Step 1: Update tinh_id
        tinh_updated = update_tinh_id_comprehensive(conn)
        
        # Step 2: Generate coordinates
        coords_updated = generate_coordinates_for_all(conn)
        
        # Step 3: Analyze failures
        analyze_failed_extractions(conn)
        
        # Close connection
        conn.close()
        
        print("\n" + "="*80)
        print("🎉 HOÀN THÀNH TẤT CẢ!")
        print("="*80)
        print(f"✅ Cập nhật tinh_id:     {tinh_updated:,} facilities")
        print(f"✅ Tạo tọa độ:           {coords_updated:,} facilities")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
