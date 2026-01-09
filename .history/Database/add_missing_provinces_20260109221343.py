#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add missing provinces to nongsan.tinh table
Based on addresses found in co_so table
"""

import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': '123456'
}

# All provinces mentioned in addresses
ADDITIONAL_PROVINCES = [
    'Đắk Lắk',
    'Bến Tre',
    'Long An',
    'Lâm Đồng',
    'Bình Phước',
    'Kon Tum',
    'Đồng Nai',
    'Khánh Hòa',
    'Bình Thuận',
    'Tây Ninh',
    'An Giang',
    'Bà Rịa - Vũng Tàu',
    'Bình Dương',
    'Bạc Liêu',
    'Sóc Trăng',
    'Trà Vinh',
    'Kiên Giang',
    'Hậu Giang',
    'Bình Định',
    'Phú Yên',
    'Nghệ An',
    'Thanh Hóa',
    'Quảng Nam',
    'Quảng Ngãi',
]

def add_provinces(conn):
    """
    Add provinces to nongsan.tinh table
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("📍 THÊM CÁC TỈNH VÀO DATABASE")
    print("="*80)
    
    # Get existing provinces
    cur.execute("SELECT ten_tinh FROM nongsan.tinh")
    existing = {row[0] for row in cur.fetchall()}
    
    print(f"\n✅ Hiện có {len(existing)} tỉnh trong database:")
    for p in sorted(existing):
        print(f"   - {p}")
    
    # Add new provinces
    added = 0
    skipped = 0
    
    print(f"\n🔄 Đang thêm tỉnh mới...")
    
    for province_name in sorted(ADDITIONAL_PROVINCES):
        if province_name in existing:
            skipped += 1
            print(f"   ⏭️  {province_name} (đã tồn tại)")
            continue
        
        # Generate ma_tinh from name
        ma_tinh = province_name.replace(' ', '').replace('-', '')[:10].upper()
        
        # Insert province
        cur.execute("""
            INSERT INTO nongsan.tinh (ma_tinh, ten_tinh)
            VALUES (%s, %s)
        """, (ma_tinh, province_name))
        added += 1
        print(f"   ✅ {province_name} (ma={ma_tinh})")
    
    conn.commit()
    
    # Final count
    cur.execute("SELECT COUNT(*) FROM nongsan.tinh")
    total = cur.fetchone()[0]
    
    print(f"\n" + "="*80)
    print(f"✅ HOÀN THÀNH!")
    print(f"="*80)
    print(f"   Đã thêm:     {added} tỉnh")
    print(f"   Bỏ qua:      {skipped} tỉnh (đã tồn tại)")
    print(f"   Tổng cộng:   {total} tỉnh trong database")
    print("="*80 + "\n")
    
    return added

def main():
    try:
        print("\n📡 Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected!")
        
        added = add_provinces(conn)
        
        conn.close()
        
        print(f"✅ Thêm thành công {added} tỉnh mới vào database!\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
