#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script xuất toàn bộ schema và data thành file SQL backup
"""

import psycopg2
from datetime import datetime

def export_schema_and_data():
    """Export schema và data thành file SQL"""
    
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='postgres',
        user='postgres',
        password='123456'
    )
    
    cur = conn.cursor()
    
    # Create filename với timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'nongsan_backup_{timestamp}.sql'
    
    print("="*80)
    print(f"📦 XUẤT DATABASE THÀNH FILE SQL: {filename}")
    print("="*80)
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Header
        f.write("-- =====================================================\n")
        f.write("-- NONGSAN DATABASE BACKUP\n")
        f.write(f"-- Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- Schema: nongsan\n")
        f.write("-- =====================================================\n\n")
        
        f.write("-- Create schema if not exists\n")
        f.write("CREATE SCHEMA IF NOT EXISTS nongsan;\n")
        f.write("SET search_path TO nongsan;\n\n")
        
        # Get all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'nongsan' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cur.fetchall()]
        
        print(f"\n📋 Xuất {len(tables)} bảng...")
        
        # Export each table
        for table in tables:
            print(f"   - {table:40} ", end='', flush=True)
            
            # Get table structure
            f.write(f"\n-- =====================================================\n")
            f.write(f"-- Table: {table}\n")
            f.write(f"-- =====================================================\n\n")
            
            # Get row count
            cur.execute(f"SELECT COUNT(*) FROM nongsan.{table}")
            row_count = cur.fetchone()[0]
            
            # Get CREATE TABLE statement (simplified)
            cur.execute(f"""
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    numeric_precision,
                    numeric_scale,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'nongsan' AND table_name = '{table}'
                ORDER BY ordinal_position
            """)
            
            columns = cur.fetchall()
            
            # Export data if any
            if row_count > 0:
                # Get all data
                cur.execute(f"SELECT * FROM nongsan.{table}")
                rows = cur.fetchall()
                
                # Get column names
                col_names = [desc[0] for desc in cur.description]
                
                # Write INSERT statements
                f.write(f"-- Data: {row_count} records\n")
                f.write(f"TRUNCATE TABLE nongsan.{table} CASCADE;\n")
                
                for row in rows:
                    # Format values
                    values = []
                    for val in row:
                        if val is None:
                            values.append('NULL')
                        elif isinstance(val, str):
                            # Escape single quotes
                            escaped = val.replace("'", "''")
                            values.append(f"'{escaped}'")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, bool):
                            values.append('TRUE' if val else 'FALSE')
                        else:
                            # Handle dates, timestamps, etc.
                            values.append(f"'{val}'")
                    
                    f.write(f"INSERT INTO nongsan.{table} ({', '.join(col_names)}) VALUES ({', '.join(values)});\n")
                
                f.write("\n")
                print(f"✅ {row_count:>8,} records")
            else:
                f.write(f"-- Empty table\n\n")
                print("   (trống)")
        
        # Export views
        print(f"\n👁️  Xuất views...")
        
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'nongsan' 
            AND table_type = 'VIEW'
            ORDER BY table_name
        """)
        
        views = [row[0] for row in cur.fetchall()]
        
        for view in views:
            print(f"   - {view:40} ", end='', flush=True)
            
            # Get view definition
            cur.execute(f"""
                SELECT definition 
                FROM pg_views 
                WHERE schemaname = 'nongsan' AND viewname = '{view}'
            """)
            
            definition = cur.fetchone()
            if definition:
                f.write(f"\n-- View: {view}\n")
                f.write(f"DROP VIEW IF EXISTS nongsan.{view} CASCADE;\n")
                f.write(f"CREATE VIEW nongsan.{view} AS\n{definition[0]};\n\n")
                print("✅")
        
        # Add sequences reset
        f.write("\n-- =====================================================\n")
        f.write("-- Reset sequences\n")
        f.write("-- =====================================================\n\n")
        
        for table in tables:
            f.write(f"SELECT setval('nongsan.{table}_id_seq', (SELECT MAX(id) FROM nongsan.{table}));\n")
        
        f.write("\n-- =====================================================\n")
        f.write("-- END OF BACKUP\n")
        f.write("-- =====================================================\n")
    
    conn.close()
    
    # Get file size
    import os
    file_size = os.path.getsize(filename)
    
    print(f"\n✅ Đã xuất thành công!")
    print(f"   File: {filename}")
    print(f"   Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    print("\n" + "="*80)

if __name__ == '__main__':
    export_schema_and_data()
