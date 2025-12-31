#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script phân tích cấu trúc các file Excel để thiết kế CSDL
"""

import os
import pandas as pd
from pathlib import Path

def analyze_excel_file(file_path):
    """Phân tích một file Excel và in ra cấu trúc"""
    try:
        print(f"\n{'='*80}")
        print(f"FILE: {file_path.name}")
        print(f"{'='*80}")
        
        # Đọc tất cả các sheet
        excel_file = pd.ExcelFile(file_path)
        print(f"Số sheets: {len(excel_file.sheet_names)}")
        print(f"Tên sheets: {excel_file.sheet_names}\n")
        
        # Phân tích từng sheet
        for sheet_name in excel_file.sheet_names:
            print(f"\n--- SHEET: {sheet_name} ---")
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name, nrows=5)
                print(f"Số cột: {len(df.columns)}")
                print(f"Số dòng (sample): {len(df)}")
                print(f"\nCác cột:")
                for i, col in enumerate(df.columns, 1):
                    print(f"  {i}. {col}")
                
                # In 2 dòng đầu tiên
                print(f"\nDữ liệu mẫu (2 dòng đầu):")
                print(df.head(2).to_string())
                
            except Exception as e:
                print(f"Lỗi đọc sheet: {e}")
        
    except Exception as e:
        print(f"Lỗi đọc file: {e}")

def main():
    """Main function"""
    base_path = Path(__file__).parent
    
    # Danh sách thư mục cần phân tích
    folders = [
        'giong',
        'msvt', 
        'phanbon',
        'ThuocBaoVeThucVat',
        'CoSo/cs_donggoi',
        'CoSo/cs_giong',
        'CoSo/cs_pb',
        'CoSo/cs_tbvtv'
    ]
    
    print("BẮT ĐẦU PHÂN TÍCH CẤU TRÚC FILE EXCEL")
    print("="*80)
    
    for folder in folders:
        folder_path = base_path / folder
        if not folder_path.exists():
            print(f"\nThư mục không tồn tại: {folder}")
            continue
            
        print(f"\n\n{'#'*80}")
        print(f"# THƯ MỤC: {folder}")
        print(f"{'#'*80}")
        
        # Tìm tất cả file Excel
        excel_files = list(folder_path.glob('*.xlsx')) + list(folder_path.glob('*.xls'))
        
        if not excel_files:
            print(f"Không có file Excel trong thư mục này")
            continue
            
        print(f"Tìm thấy {len(excel_files)} file Excel")
        
        # Phân tích từng file
        for excel_file in excel_files:
            if '~$' in excel_file.name:  # Bỏ qua file tạm
                continue
            analyze_excel_file(excel_file)
    
    print("\n\nHOÀN THÀNH PHÂN TÍCH!")

if __name__ == '__main__':
    main()
