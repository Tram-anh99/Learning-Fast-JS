#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Cleanup Script
- Drop unused empty tables
- Clean invalid data in co_so tables
- Remove duplicate entries
- Schema optimizations
"""

import psycopg2
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': '123456'
}

# Tables to drop (empty + not used in API/Frontend)
TABLES_TO_DROP = [
    'co_quan_luu_tru_gen',
    'diem_sau_benh',
    # 'lich_su_canh_tac',  # Keep - used in API (even if empty)
    'nguon_gen',
    'nguon_thu_thap',
    'noi_thu_thap_gen',
    'phan_bon_luu_hanh',
    'thong_ke_he_thong',
    'thuoc_bvtv_luu_hanh',
    'vung_co_so_dong_goi',
    'vung_thi_truong'
]

def drop_unused_tables(conn):
    """Drop unused empty tables"""
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🗑️  DROPPING UNUSED EMPTY TABLES")
    print("="*80)
    
    dropped = 0
    for table in TABLES_TO_DROP:
        try:
            cur.execute(f"DROP TABLE IF EXISTS nongsan.{table} CASCADE")
            print(f"   ✅ Dropped: {table}")
            dropped += 1
        except Exception as e:
            print(f"   ❌ Failed to drop {table}: {e}")
    
    conn.commit()
    print(f"\n📊 Total dropped: {dropped}/{len(TABLES_TO_DROP)} tables")
    return dropped


def clean_co_so_invalid_data(conn):
    """
    Clean co_so tables: Remove records with:
    - ten_co_so is 1 character OR
    - ten_co_so matches pattern like "9039/SNN" AND all other important columns are NULL
    """
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🧹 CLEANING INVALID DATA IN CO_SO TABLES")
    print("="*80)
    
    co_so_tables = ['co_so', 'co_so_dong_goi', 'co_so_phan_bon', 'co_so_thuoc_bvtv']
    total_deleted = 0
    
    for table in co_so_tables:
        try:
            # Check if table exists
            cur.execute(f"""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema='nongsan' AND table_name='{table}'
            """)
            if cur.fetchone()[0] == 0:
                print(f"   ⏭️  {table} doesn't exist, skipping")
                continue
            
            # Count before
            cur.execute(f"SELECT COUNT(*) FROM nongsan.{table}")
            count_before = cur.fetchone()[0]
            
            # Delete invalid records
            # Pattern 1: Single character names
            cur.execute(f"""
                DELETE FROM nongsan.{table}
                WHERE LENGTH(TRIM(ten_co_so)) <= 1
            """)
            deleted_1 = cur.rowcount
            
            # Pattern 2: Code-like names with all NULL important fields
            # (co_so has tinh_id, others don't)
            if table == 'co_so':
                cur.execute(f"""
                    DELETE FROM nongsan.{table}
                    WHERE ten_co_so ~ '^[0-9]+/[A-Z]+$'
                    AND dia_chi IS NULL
                    AND (tinh_id IS NULL OR tinh_id = 0)
                """)
            else:
                cur.execute(f"""
                    DELETE FROM nongsan.{table}
                    WHERE ten_co_so ~ '^[0-9]+/[A-Z]+$'
                    AND dia_chi IS NULL
                """)
            deleted_2 = cur.rowcount
            
            # Pattern 3: Numeric-only names
            cur.execute(f"""
                DELETE FROM nongsan.{table}
                WHERE ten_co_so ~ '^[0-9]+$'
                AND LENGTH(ten_co_so) <= 3
            """)
            deleted_3 = cur.rowcount
            
            deleted = deleted_1 + deleted_2 + deleted_3
            total_deleted += deleted
            
            # Count after
            cur.execute(f"SELECT COUNT(*) FROM nongsan.{table}")
            count_after = cur.fetchone()[0]
            
            print(f"\n   📋 {table}:")
            print(f"      Before: {count_before:,} records")
            print(f"      Deleted: {deleted:,} invalid records")
            print(f"        - Single char: {deleted_1}")
            print(f"        - Code pattern: {deleted_2}")
            print(f"        - Numeric only: {deleted_3}")
            print(f"      After: {count_after:,} records")
            
        except Exception as e:
            print(f"   ❌ Error cleaning {table}: {e}")
    
    conn.commit()
    print(f"\n📊 Total deleted across all co_so tables: {total_deleted:,} records")
    return total_deleted


def drop_column_ma_tinh(conn):
    """Drop ma_tinh column from tinh table"""
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🗑️  DROPPING COLUMN ma_tinh FROM tinh TABLE")
    print("="*80)
    
    try:
        cur.execute("ALTER TABLE nongsan.tinh DROP COLUMN IF EXISTS ma_tinh CASCADE")
        print("   ✅ Dropped column ma_tinh from tinh table")
        conn.commit()
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return False


def check_loai_hoat_dong_duplicates(conn):
    """Check and report duplicates in loai_hoat_dong table"""
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("🔍 CHECKING DUPLICATES IN loai_hoat_dong TABLE")
    print("="*80)
    
    try:
        # Find duplicates based on ten_loai (not ten_hoat_dong)
        cur.execute("""
            SELECT ten_loai, mo_ta, COUNT(*) as count
            FROM nongsan.loai_hoat_dong
            GROUP BY ten_loai, mo_ta
            HAVING COUNT(*) > 1
            ORDER BY count DESC
        """)
        
        duplicates = cur.fetchall()
        
        if duplicates:
            print(f"\n⚠️  Found {len(duplicates)} duplicate groups:\n")
            for ten, mo_ta, count in duplicates:
                print(f"   '{ten}' - '{mo_ta}': {count} times")
                
                # Get IDs of duplicates
                cur.execute("""
                    SELECT id FROM nongsan.loai_hoat_dong
                    WHERE ten_loai = %s AND (mo_ta = %s OR (mo_ta IS NULL AND %s IS NULL))
                    ORDER BY id
                """, (ten, mo_ta, mo_ta))
                ids = [row[0] for row in cur.fetchall()]
                print(f"      IDs: {ids}")
            
            # Auto-delete duplicates (keep first ID)
            total_deleted = 0
            for ten, mo_ta, count in duplicates:
                cur.execute("""
                    DELETE FROM nongsan.loai_hoat_dong
                    WHERE id NOT IN (
                        SELECT MIN(id) FROM nongsan.loai_hoat_dong
                        WHERE ten_loai = %s AND (mo_ta = %s OR (mo_ta IS NULL AND %s IS NULL))
                    )
                    AND ten_loai = %s AND (mo_ta = %s OR (mo_ta IS NULL AND %s IS NULL))
                """, (ten, mo_ta, mo_ta, ten, mo_ta, mo_ta))
                deleted = cur.rowcount
                total_deleted += deleted
                print(f"   ✅ Deleted {deleted} duplicates of '{ten}'")
            
            conn.commit()
            print(f"\n📊 Total deleted: {total_deleted} duplicate records")
            return total_deleted
        else:
            print("   ✅ No duplicates found")
            return 0
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return 0


def move_hoat_chat_to_ghi_chu(conn):
    """Move ten_hoat_chat content to ghi_chu in thuoc_bvtv table"""
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("📝 MOVING ten_hoat_chat TO ghi_chu IN thuoc_bvtv TABLE")
    print("="*80)
    
    try:
        # Update ghi_chu with ten_hoat_chat content
        cur.execute("""
            UPDATE nongsan.thuoc_bvtv
            SET ghi_chu = CASE 
                WHEN ghi_chu IS NULL THEN ten_hoat_chat
                WHEN ten_hoat_chat IS NULL THEN ghi_chu
                ELSE CONCAT(ghi_chu, ' | Hoạt chất: ', ten_hoat_chat)
            END
            WHERE ten_hoat_chat IS NOT NULL
        """)
        updated = cur.rowcount
        
        print(f"   ✅ Updated {updated:,} records")
        
        # Now drop the column
        cur.execute("ALTER TABLE nongsan.thuoc_bvtv DROP COLUMN IF EXISTS ten_hoat_chat")
        print(f"   ✅ Dropped column ten_hoat_chat")
        
        conn.commit()
        return updated
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return 0


def add_location_fk_to_to_chuc(conn):
    """Add tinh_id, huyen_id, xa_id to to_chuc_ca_nhan table"""
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("➕ ADDING LOCATION FKs TO to_chuc_ca_nhan TABLE")
    print("="*80)
    
    try:
        # Add columns
        columns_to_add = [
            ('tinh_id', 'INTEGER'),
            ('huyen_id', 'INTEGER'),
            ('xa_id', 'INTEGER')
        ]
        
        for col_name, col_type in columns_to_add:
            cur.execute(f"""
                ALTER TABLE nongsan.to_chuc_ca_nhan 
                ADD COLUMN IF NOT EXISTS {col_name} {col_type}
            """)
            print(f"   ✅ Added column: {col_name} ({col_type})")
        
        # Add foreign keys
        fk_constraints = [
            ('fk_to_chuc_tinh', 'tinh_id', 'tinh'),
            ('fk_to_chuc_huyen', 'huyen_id', 'huyen'),
            ('fk_to_chuc_xa', 'xa_id', 'xa')
        ]
        
        for fk_name, col_name, ref_table in fk_constraints:
            try:
                cur.execute(f"""
                    ALTER TABLE nongsan.to_chuc_ca_nhan
                    ADD CONSTRAINT {fk_name} FOREIGN KEY ({col_name})
                    REFERENCES nongsan.{ref_table}(id) ON DELETE SET NULL
                """)
                print(f"   ✅ Added FK: {fk_name} → {ref_table}")
            except Exception as e:
                if 'already exists' in str(e):
                    print(f"   ⏭️  FK {fk_name} already exists")
                else:
                    raise
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return False


def add_coordinates_to_locations(conn):
    """Add x, y coordinate columns to tinh, huyen, xa tables"""
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("📍 ADDING COORDINATE COLUMNS TO LOCATION TABLES")
    print("="*80)
    
    try:
        location_tables = ['tinh', 'huyen', 'xa']
        
        for table in location_tables:
            # Add x (longitude) and y (latitude) columns
            cur.execute(f"""
                ALTER TABLE nongsan.{table}
                ADD COLUMN IF NOT EXISTS x DECIMAL(11,8),
                ADD COLUMN IF NOT EXISTS y DECIMAL(10,8)
            """)
            print(f"   ✅ Added x, y columns to {table}")
        
        conn.commit()
        
        # Now populate with sample coordinates (can be updated later)
        print("\n   📊 Populating sample coordinates...")
        
        # Sample coordinates for provinces (from previous work)
        province_coords = {
            'Gia Lai': (108.0, 13.9),
            'Đắk Lắk': (108.2, 12.7),
            'Đắk Nông': (107.7, 12.2),
            'Bến Tre': (106.4, 10.2),
            'Tiền Giang': (106.3, 10.4),
            'Long An': (106.4, 10.7),
            'Vĩnh Long': (105.9, 10.3),
        }
        
        for ten_tinh, (x, y) in province_coords.items():
            cur.execute("""
                UPDATE nongsan.tinh
                SET x = %s, y = %s
                WHERE ten_tinh = %s
            """, (x, y, ten_tinh))
        
        updated = cur.rowcount
        print(f"   ✅ Updated {updated} provinces with coordinates")
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.rollback()
        return False


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🔧 DATABASE CLEANUP & OPTIMIZATION")
    print("="*80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("\n✅ Connected to database")
        
        # 1. Drop unused empty tables
        drop_unused_tables(conn)
        
        # 2. Clean invalid data in co_so tables
        clean_co_so_invalid_data(conn)
        
        # 3. Drop ma_tinh column
        drop_column_ma_tinh(conn)
        
        # 4. Check and remove duplicates in loai_hoat_dong
        check_loai_hoat_dong_duplicates(conn)
        
        # 5. Move ten_hoat_chat to ghi_chu in thuoc_bvtv
        move_hoat_chat_to_ghi_chu(conn)
        
        # 6. Add location FKs to to_chuc_ca_nhan
        add_location_fk_to_to_chuc(conn)
        
        # 7. Add coordinates to location tables
        add_coordinates_to_locations(conn)
        
        conn.close()
        
        print("\n" + "="*80)
        print("✅ DATABASE CLEANUP COMPLETED!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
