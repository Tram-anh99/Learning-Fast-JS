#!/bin/bash
# =============================================================================
# Script tự động tạo database và import schema
# =============================================================================

set -e  # Exit on error

# Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Thông tin database
DB_NAME="nongsan_db"
DB_USER="postgres"
DB_SCHEMA="nongsan"

echo -e "${BLUE}================================================================================================${NC}"
echo -e "${BLUE}  SCRIPT TỰ ĐỘNG TẠO DATABASE VÀ IMPORT SCHEMA - HỆ THỐNG QUẢN LÝ NÔNG SẢN${NC}"
echo -e "${BLUE}================================================================================================${NC}\n"

# Kiểm tra PostgreSQL đã cài đặt chưa
echo -e "${YELLOW}[1/5] Kiểm tra PostgreSQL...${NC}"
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL chưa được cài đặt!${NC}"
    echo -e "${YELLOW}Hướng dẫn cài đặt:${NC}"
    echo -e "  macOS:   ${GREEN}brew install postgresql@15 && brew services start postgresql@15${NC}"
    echo -e "  Ubuntu:  ${GREEN}sudo apt install postgresql-15${NC}"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL đã cài đặt${NC}\n"

# Kiểm tra PostgreSQL đang chạy
echo -e "${YELLOW}[2/5] Kiểm tra PostgreSQL service...${NC}"
if ! pg_isready -q; then
    echo -e "${RED}❌ PostgreSQL service chưa chạy!${NC}"
    echo -e "${YELLOW}Khởi động service:${NC}"
    echo -e "  macOS:   ${GREEN}brew services start postgresql@15${NC}"
    echo -e "  Ubuntu:  ${GREEN}sudo systemctl start postgresql${NC}"
    exit 1
fi
echo -e "${GREEN}✅ PostgreSQL service đang chạy${NC}\n"

# Kiểm tra file schema có tồn tại không
echo -e "${YELLOW}[3/5] Kiểm tra file schema...${NC}"
if [ ! -f "schema_complete.sql" ]; then
    echo -e "${RED}❌ Không tìm thấy file schema_complete.sql${NC}"
    echo -e "${YELLOW}Vui lòng chạy script từ thư mục Database${NC}"
    exit 1
fi
echo -e "${GREEN}✅ File schema_complete.sql tồn tại${NC}\n"

# Hỏi có muốn xóa database cũ không (nếu tồn tại)
echo -e "${YELLOW}[4/5] Kiểm tra database tồn tại...${NC}"
if psql -U "$DB_USER" -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
    echo -e "${YELLOW}⚠️  Database '$DB_NAME' đã tồn tại!${NC}"
    read -p "Bạn có muốn XÓA và TẠO LẠI database? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Đang xóa database cũ...${NC}"
        dropdb -U "$DB_USER" "$DB_NAME" --if-exists
        echo -e "${GREEN}✅ Đã xóa database cũ${NC}"
    else
        echo -e "${YELLOW}❌ Hủy bỏ. Database cũ được giữ lại.${NC}"
        echo -e "${YELLOW}Nếu muốn import vào database hiện tại, chạy:${NC}"
        echo -e "  ${GREEN}psql -U $DB_USER -d $DB_NAME -f schema_complete.sql${NC}"
        exit 0
    fi
fi

# Tạo database mới
echo -e "\n${YELLOW}[5/5] Tạo database và import schema...${NC}"
echo -e "${BLUE}Creating database '$DB_NAME'...${NC}"
createdb -U "$DB_USER" "$DB_NAME" || {
    echo -e "${RED}❌ Không thể tạo database!${NC}"
    exit 1
}
echo -e "${GREEN}✅ Đã tạo database '$DB_NAME'${NC}\n"

# Import schema
echo -e "${BLUE}Importing schema from schema_complete.sql...${NC}"
psql -U "$DB_USER" -d "$DB_NAME" -f schema_complete.sql -v ON_ERROR_STOP=1 || {
    echo -e "${RED}❌ Lỗi khi import schema!${NC}"
    exit 1
}

echo -e "\n${GREEN}================================================================================================${NC}"
echo -e "${GREEN}  ✅ HOÀN THÀNH! Database đã được tạo và import thành công${NC}"
echo -e "${GREEN}================================================================================================${NC}\n"

# Thống kê database
echo -e "${BLUE}📊 THỐNG KÊ DATABASE:${NC}\n"

echo -e "${YELLOW}Số lượng bảng:${NC}"
psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT COUNT(*) as \"Tổng số bảng\" 
    FROM information_schema.tables 
    WHERE table_schema = '$DB_SCHEMA' AND table_type = 'BASE TABLE';
" -t

echo -e "\n${YELLOW}Số lượng views:${NC}"
psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT COUNT(*) as \"Tổng số views\" 
    FROM information_schema.views 
    WHERE table_schema = '$DB_SCHEMA';
" -t

echo -e "\n${YELLOW}Danh sách bảng:${NC}"
psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT 
        table_name as \"Tên bảng\",
        pg_size_pretty(pg_total_relation_size('$DB_SCHEMA.' || table_name)) as \"Kích thước\"
    FROM information_schema.tables 
    WHERE table_schema = '$DB_SCHEMA' AND table_type = 'BASE TABLE'
    ORDER BY table_name;
"

echo -e "\n${YELLOW}Danh sách views:${NC}"
psql -U "$DB_USER" -d "$DB_NAME" -c "
    SELECT table_name as \"Tên view\"
    FROM information_schema.views 
    WHERE table_schema = '$DB_SCHEMA'
    ORDER BY table_name;
"

# Hướng dẫn sử dụng
echo -e "\n${GREEN}================================================================================================${NC}"
echo -e "${GREEN}  📖 HƯỚNG DẪN SỬ DỤNG${NC}"
echo -e "${GREEN}================================================================================================${NC}\n"

echo -e "${YELLOW}1. Kết nối vào database:${NC}"
echo -e "   ${GREEN}psql -U $DB_USER -d $DB_NAME${NC}\n"

echo -e "${YELLOW}2. Xem danh sách bảng:${NC}"
echo -e "   ${GREEN}\\dt $DB_SCHEMA.*${NC}\n"

echo -e "${YELLOW}3. Xem danh sách views:${NC}"
echo -e "   ${GREEN}\\dv $DB_SCHEMA.*${NC}\n"

echo -e "${YELLOW}4. Truy vấn dữ liệu mẫu:${NC}"
echo -e "   ${GREEN}SELECT * FROM $DB_SCHEMA.v_vung_trong_full;${NC}\n"

echo -e "${YELLOW}5. Xem cấu trúc bảng:${NC}"
echo -e "   ${GREEN}\\d $DB_SCHEMA.vung_trong${NC}\n"

echo -e "${YELLOW}6. Backup database:${NC}"
echo -e "   ${GREEN}pg_dump -U $DB_USER -d $DB_NAME > backup_\$(date +%Y%m%d).sql${NC}\n"

echo -e "${GREEN}================================================================================================${NC}"
echo -e "${GREEN}  🚀 SẴN SÀNG SỬ DỤNG!${NC}"
echo -e "${GREEN}================================================================================================${NC}\n"

echo -e "${BLUE}📚 Tài liệu chi tiết:${NC}"
echo -e "   - README_COMPLETE.md  - Hướng dẫn đầy đủ"
echo -e "   - ERD_DIAGRAM.md      - Sơ đồ ERD"
echo -e "   - SUMMARY.md          - Tóm tắt thiết kế"
echo -e ""
