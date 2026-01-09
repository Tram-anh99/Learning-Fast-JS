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

# Comprehensive province name mapping
PROVINCE_MAPPING = {
    # Gia Lai
    'gia lai': 'Gia Lai',
    'gialai': 'Gia Lai',
    'gia-lai': 'Gia Lai',
    'pleiku': 'Gia Lai',
    
    # Đắk Lắk
    'dak lak': 'Đắk Lắk',
    'daklak': 'Đắk Lắk',
    'dak-lak': 'Đắk Lắk',
    'đak lak': 'Đắk Lắk',
    'đăk lăk': 'Đắk Lắk',
    'dac lac': 'Đắk Lắk',
    'buon ma thuot': 'Đắk Lắk',
    'buon me thuot': 'Đắk Lắk',
    
    # Bến Tre
    'ben tre': 'Bến Tre',
    'bentre': 'Bến Tre',
    'ben-tre': 'Bến Tre',
    
    # Tiền Giang
    'tien giang': 'Tiền Giang',
    'tiengiang': 'Tiền Giang',
    'tien-giang': 'Tiền Giang',
    'my tho': 'Tiền Giang',
    
    # Long An
    'long an': 'Long An',
    'longan': 'Long An',
    'long-an': 'Long An',
    'tan an': 'Long An',
    
    # Vĩnh Long
    'vinh long': 'Vĩnh Long',
    'vinhlong': 'Vĩnh Long',
    'vinh-long': 'Vĩnh Long',
    'vinhlong city': 'Vĩnh Long',
    
    # Đồng Nai
    'dong nai': 'Đồng Nai',
    'dongnai': 'Đồng Nai',
    'dong-nai': 'Đồng Nai',
    'bien hoa': 'Đồng Nai',
}

# Province coordinates (center points)
PROVINCE_COORDINATES = {
    'Gia Lai': (13.9, 108.0),
    'Đắk Lắk': (12.7, 108.2),
    'Bến Tre': (10.2, 106.4),
    'Tiền Giang': (10.4, 106.3),
    'Long An': (10.7, 106.4),
    'Vĩnh Long': (10.3, 105.9),
    'Đồng Nai': (10.9, 107.2),
}

def extract_province_advanced(address: str, ten_co_so: str = None) -> str:
    """
    Advanced province extraction from address and facility name
    """
    if not address:
        address = ""
    if not ten_co_so:
        ten_co_so = ""
    
    # Combine address and facility name for better matching
    combined_text = f"{address} {ten_co_so}".lower()
    
    # Remove common Vietnamese words
    combined_text = re.sub(r'\b(tinh|tinh|province|city|tp|thanh pho)\b', '', combined_text)
    
    # Try exact match first
    for key, value in PROVINCE_MAPPING.items():
        if key in combined_text:
            return value
    
    # Try partial match for multi-word provinces
    for key, value in PROVINCE_MAPPING.items():
        words = key.split()
        if len(words) > 1:
            # Check if all words present (in any order)
            if all(word in combined_text for word in words):
                return value
    
    # Try fuzzy match (at least 80% of characters match)
    for key, value in PROVINCE_MAPPING.items():
        if len(key) > 4:  # Only for longer names
            # Count matching characters
            match_count = sum(1 for c in key if c in combined_text)
            if match_count / len(key) >= 0.8:
                return value
    
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
        province_name = extract_province_advanced(dia_chi, ten_co_so)
        
        if province_name and province_name in provinces:
            tinh_id = provinces[province_name]
            cur.execute("""
                UPDATE nongsan.co_so
                SET tinh_id = %s
                WHERE id = %s
            """, (tinh_id, fid))
            updated += 1
            
            if updated <= 10 or updated % 500 == 0:
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
