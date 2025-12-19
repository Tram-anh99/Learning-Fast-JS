-- =============================================================================
-- CƠ SỞ DỮ LIỆU QUẢN LÝ NÔNG SẢN - POSTGRESQL
-- Thiết kế theo 3 chuẩn cơ sở dữ liệu (3NF)
-- =============================================================================
-- Chuẩn 1 (1NF): Mỗi cột chỉ chứa giá trị nguyên tử, không có nhóm lặp
-- Chuẩn 2 (2NF): Mọi thuộc tính không khóa phụ thuộc hoàn toàn vào khóa chính
-- Chuẩn 3 (3NF): Không có phụ thuộc bắc cầu giữa các thuộc tính không khóa
-- =============================================================================

-- Xóa database cũ nếu tồn tại (chỉ dùng khi cần reset)
-- DROP SCHEMA IF EXISTS nongsan CASCADE;

-- Tạo schema
CREATE SCHEMA IF NOT EXISTS nongsan;
SET search_path TO nongsan;

-- =============================================================================
-- BẢNG THAM CHIẾU (REFERENCE TABLES)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Bảng Trạng thái Vùng trồng
-- Tách riêng để đảm bảo 3NF - không lặp lại text trạng thái
-- -----------------------------------------------------------------------------
CREATE TABLE trang_thai (
    id SERIAL PRIMARY KEY,
    ma_trang_thai VARCHAR(20) UNIQUE NOT NULL,       -- canh_tac, sau_benh, thu_hoach, da_thu_hoach
    ten_trang_thai VARCHAR(50) NOT NULL,             -- Đang canh tác, Cảnh báo dịch hại, ...
    mau_sac VARCHAR(10),                             -- #4caf50, #ef5350, ...
    css_class VARCHAR(30),                           -- bg-green-500, bg-red-500, ...
    mo_ta TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2. Bảng Trạng thái Mã vùng (hoat_dong, bi_thu_hoi)
-- -----------------------------------------------------------------------------
CREATE TABLE trang_thai_ma (
    id SERIAL PRIMARY KEY,
    ma_trang_thai VARCHAR(20) UNIQUE NOT NULL,       -- hoat_dong, bi_thu_hoi
    ten_trang_thai VARCHAR(50) NOT NULL,             -- Hoạt động, Bị thu hồi
    mo_ta TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 3. Bảng Chứng nhận (VietGAP, GlobalGAP, OCOP, ...)
-- -----------------------------------------------------------------------------
CREATE TABLE chung_nhan (
    id SERIAL PRIMARY KEY,
    ma_chung_nhan VARCHAR(20) UNIQUE NOT NULL,       -- VIETGAP, GLOBALGAP, OCOP4, OCOP5
    ten_chung_nhan VARCHAR(100) NOT NULL,            -- VietGAP, GlobalGAP, OCOP 4 Sao
    to_chuc_cap VARCHAR(100),                        -- Tổ chức cấp chứng nhận
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 4. Bảng Thị trường Xuất khẩu
-- Tách riêng để đảm bảo 1NF - không lưu mảng trong 1 cột
-- -----------------------------------------------------------------------------
CREATE TABLE thi_truong (
    id SERIAL PRIMARY KEY,
    ma_thi_truong VARCHAR(20) UNIQUE NOT NULL,       -- TQ, HK, EU, ASEAN, JP, ND
    ten_thi_truong VARCHAR(100) NOT NULL,            -- Trung Quốc, Hoa Kỳ, Châu Âu, ...
    vung_dia_ly VARCHAR(50),                         -- Châu Á, Bắc Mỹ, Châu Âu, ...
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 5. Bảng Loại Hoạt động Canh tác
-- Tách riêng để đảm bảo 3NF
-- -----------------------------------------------------------------------------
CREATE TABLE loai_hoat_dong (
    id SERIAL PRIMARY KEY,
    ma_loai VARCHAR(20) UNIQUE NOT NULL,             -- tillage, sow, fertilizer, spray, water, harvest
    ten_loai VARCHAR(50) NOT NULL,                   -- Cày ải, Gieo sạ, Bón phân, ...
    icon VARCHAR(10),                                -- 🚜, 🌱, 🌾, 💊, 💧, 💰
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- BẢNG THỰC THỂ CHÍNH (MAIN ENTITY TABLES)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 6. Bảng Chủ vùng / Hộ nông dân / HTX
-- -----------------------------------------------------------------------------
CREATE TABLE chu_vung (
    id SERIAL PRIMARY KEY,
    ma_chu VARCHAR(20) UNIQUE NOT NULL,              -- CV-001, CV-002, ...
    ten_chu VARCHAR(100) NOT NULL,                   -- Nguyễn Văn A, HTX Lúa Vàng, ...
    loai_chu VARCHAR(20) NOT NULL DEFAULT 'ca_nhan', -- ca_nhan, htx, doanh_nghiep
    so_dien_thoai VARCHAR(15),
    email VARCHAR(100),
    dia_chi TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 7. Bảng Vùng trồng (Main table)
-- -----------------------------------------------------------------------------
CREATE TABLE vung_trong (
    id SERIAL PRIMARY KEY,
    ma_vung VARCHAR(20) UNIQUE NOT NULL,             -- VT-001, VT-002, ...
    ten_vung VARCHAR(100) NOT NULL,                  -- HTX Xoài Mỹ Xương, Thanh Long VietGAP, ...
    chu_vung_id INTEGER REFERENCES chu_vung(id) ON DELETE SET NULL,
    trang_thai_id INTEGER REFERENCES trang_thai(id),
    trang_thai_ma_id INTEGER REFERENCES trang_thai_ma(id),
    chung_nhan_id INTEGER REFERENCES chung_nhan(id),
    ma_qr VARCHAR(50),                               -- Mã QR để truy xuất
    anh_dai_dien TEXT,                               -- URL ảnh đại diện
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 8. Bảng Tọa độ Polygon (Đa giác vùng trồng)
-- Tách riêng để đảm bảo 1NF - mỗi điểm là 1 dòng
-- -----------------------------------------------------------------------------
CREATE TABLE toa_do_vung (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER NOT NULL REFERENCES vung_trong(id) ON DELETE CASCADE,
    thu_tu INTEGER NOT NULL,                         -- Thứ tự điểm (1, 2, 3, 4 cho polygon)
    vi_do DECIMAL(10, 6) NOT NULL,                   -- Latitude (10.762)
    kinh_do DECIMAL(10, 6) NOT NULL,                 -- Longitude (106.66)
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vung_trong_id, thu_tu)
);

-- -----------------------------------------------------------------------------
-- 9. Bảng Loại cây trồng
-- -----------------------------------------------------------------------------
CREATE TABLE loai_cay (
    id SERIAL PRIMARY KEY,
    ma_cay VARCHAR(20) UNIQUE NOT NULL,              -- XOAI_MY, THANH_LONG_DO, LUA_JASMINE, ...
    ten_cay VARCHAR(100) NOT NULL,                   -- Xoài Mỹ Xương, Thanh Long Đỏ, ...
    nhom_cay VARCHAR(50),                            -- Cây ăn trái, Lúa, Rau củ, Cây công nghiệp
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 10. Bảng Chi tiết Cây trồng trong Vùng (Quan hệ N-N)
-- Một vùng có thể trồng nhiều loại cây, một loại cây có thể ở nhiều vùng
-- -----------------------------------------------------------------------------
CREATE TABLE vung_cay_trong (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER NOT NULL REFERENCES vung_trong(id) ON DELETE CASCADE,
    loai_cay_id INTEGER NOT NULL REFERENCES loai_cay(id) ON DELETE CASCADE,
    dien_tich DECIMAL(10, 2) NOT NULL,               -- Diện tích trồng (ha)
    nam_trong INTEGER,                               -- Năm trồng (2019, 2020, ...)
    nang_suat DECIMAL(10, 2),                        -- Năng suất (tạ/ha)
    gia_xuat_khau DECIMAL(10, 2),                    -- Giá xuất khẩu (USD/kg)
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vung_trong_id, loai_cay_id)
);

-- -----------------------------------------------------------------------------
-- 11. Bảng Thị trường Xuất khẩu của Cây trồng (Quan hệ N-N)
-- Một cây có thể xuất sang nhiều thị trường, một thị trường có nhiều loại cây
-- -----------------------------------------------------------------------------
CREATE TABLE cay_thi_truong (
    id SERIAL PRIMARY KEY,
    vung_cay_trong_id INTEGER NOT NULL REFERENCES vung_cay_trong(id) ON DELETE CASCADE,
    thi_truong_id INTEGER NOT NULL REFERENCES thi_truong(id) ON DELETE CASCADE,
    san_luong_xuat DECIMAL(12, 2),                   -- Sản lượng xuất khẩu (kg)
    gia_tri_xuat DECIMAL(15, 2),                     -- Giá trị xuất khẩu (USD)
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vung_cay_trong_id, thi_truong_id)
);

-- -----------------------------------------------------------------------------
-- 12. Bảng Lịch sử Canh tác / Nhật ký đồng ruộng
-- -----------------------------------------------------------------------------
CREATE TABLE lich_su_canh_tac (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER NOT NULL REFERENCES vung_trong(id) ON DELETE CASCADE,
    loai_hoat_dong_id INTEGER REFERENCES loai_hoat_dong(id),
    ngay_thuc_hien DATE NOT NULL,
    tieu_de VARCHAR(100),                            -- Bón thúc đợt 1, Phun thuốc trừ rầy, ...
    noi_dung TEXT,                                   -- Chi tiết hoạt động
    nguoi_thuc_hien VARCHAR(100),                    -- Người thực hiện
    thua_ruong VARCHAR(100),                         -- Thửa A (Gần nhà), Thửa B (Bãi bồi), ...
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 13. Bảng Điểm phát sinh Sâu bệnh
-- -----------------------------------------------------------------------------
CREATE TABLE diem_sau_benh (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER REFERENCES vung_trong(id) ON DELETE CASCADE,
    vi_do DECIMAL(10, 6) NOT NULL,
    kinh_do DECIMAL(10, 6) NOT NULL,
    loai_sau_benh VARCHAR(100),                      -- Rầy nâu, Nấm tắc kè, ...
    muc_do VARCHAR(20),                              -- nhe, trung_binh, nang
    ngay_phat_hien DATE NOT NULL,
    trang_thai VARCHAR(20) DEFAULT 'chua_xu_ly',     -- chua_xu_ly, dang_xu_ly, da_xu_ly
    bien_phap TEXT,                                  -- Biện pháp xử lý
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 14. Bảng Thống kê hệ thống (Lưu snapshot)
-- -----------------------------------------------------------------------------
CREATE TABLE thong_ke_he_thong (
    id SERIAL PRIMARY KEY,
    ngay_thong_ke DATE NOT NULL,
    tong_vung INTEGER DEFAULT 0,
    tong_dien_tich DECIMAL(12, 2) DEFAULT 0,         -- Tổng diện tích (ha)
    san_luong_du_kien DECIMAL(12, 2) DEFAULT 0,      -- Tấn
    so_canh_bao INTEGER DEFAULT 0,
    so_ma_thu_hoi INTEGER DEFAULT 0,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ngay_thong_ke)
);

-- =============================================================================
-- TẠO INDEX ĐỂ TỐI ƯU TRUY VẤN
-- =============================================================================

CREATE INDEX idx_vung_trong_ma ON vung_trong(ma_vung);
CREATE INDEX idx_vung_trong_trang_thai ON vung_trong(trang_thai_id);
CREATE INDEX idx_vung_trong_chu ON vung_trong(chu_vung_id);
CREATE INDEX idx_vung_cay_vung ON vung_cay_trong(vung_trong_id);
CREATE INDEX idx_vung_cay_cay ON vung_cay_trong(loai_cay_id);
CREATE INDEX idx_lich_su_vung ON lich_su_canh_tac(vung_trong_id);
CREATE INDEX idx_lich_su_ngay ON lich_su_canh_tac(ngay_thuc_hien);
CREATE INDEX idx_diem_sau_benh_vung ON diem_sau_benh(vung_trong_id);

-- =============================================================================
-- INSERT DỮ LIỆU MẪU
-- =============================================================================

-- 1. Trạng thái vùng trồng
INSERT INTO trang_thai (ma_trang_thai, ten_trang_thai, mau_sac, css_class, mo_ta) VALUES
('canh_tac', 'Đang canh tác', '#4caf50', 'bg-green-500', 'Vùng đang trong quá trình canh tác'),
('sau_benh', 'Cảnh báo dịch hại', '#ef5350', 'bg-red-500', 'Vùng có cảnh báo sâu bệnh, dịch hại'),
('thu_hoach', 'Đang thu hoạch', '#ffca28', 'bg-yellow-500', 'Vùng đang trong quá trình thu hoạch'),
('da_thu_hoach', 'Đã thu hoạch', '#2563eb', 'bg-blue-600', 'Vùng đã hoàn thành thu hoạch');

-- 2. Trạng thái mã vùng
INSERT INTO trang_thai_ma (ma_trang_thai, ten_trang_thai, mo_ta) VALUES
('hoat_dong', 'Hoạt động', 'Mã vùng đang hoạt động bình thường'),
('bi_thu_hoi', 'Bị thu hồi', 'Mã vùng bị thu hồi do vi phạm quy định');

-- 3. Chứng nhận
INSERT INTO chung_nhan (ma_chung_nhan, ten_chung_nhan, to_chuc_cap, mo_ta) VALUES
('VIETGAP', 'VietGAP', 'Bộ NN&PTNT Việt Nam', 'Thực hành nông nghiệp tốt Việt Nam'),
('GLOBALGAP', 'GlobalGAP', 'GLOBALG.A.P.', 'Tiêu chuẩn thực hành nông nghiệp tốt toàn cầu'),
('OCOP3', 'OCOP 3 Sao', 'Chương trình OCOP Việt Nam', 'Sản phẩm OCOP đạt 3 sao'),
('OCOP4', 'OCOP 4 Sao', 'Chương trình OCOP Việt Nam', 'Sản phẩm OCOP đạt 4 sao'),
('OCOP5', 'OCOP 5 Sao', 'Chương trình OCOP Việt Nam', 'Sản phẩm OCOP đạt 5 sao');

-- 4. Thị trường xuất khẩu
INSERT INTO thi_truong (ma_thi_truong, ten_thi_truong, vung_dia_ly, mo_ta) VALUES
('TQ', 'Trung Quốc', 'Châu Á', 'Thị trường xuất khẩu lớn nhất'),
('HK', 'Hoa Kỳ', 'Bắc Mỹ', 'Thị trường cao cấp Bắc Mỹ'),
('EU', 'Châu Âu', 'Châu Âu', 'Thị trường EU với tiêu chuẩn cao'),
('ASEAN', 'ASEAN', 'Châu Á', 'Cộng đồng kinh tế ASEAN'),
('JP', 'Nhật Bản', 'Châu Á', 'Thị trường cao cấp Nhật Bản'),
('ND', 'Nội địa', 'Việt Nam', 'Tiêu thụ trong nước');

-- 5. Loại hoạt động canh tác
INSERT INTO loai_hoat_dong (ma_loai, ten_loai, icon, mo_ta) VALUES
('tillage', 'Cày ải', '🚜', 'Làm đất, cày xới'),
('sow', 'Gieo sạ', '🌱', 'Gieo hạt, trồng cây'),
('fertilizer', 'Bón phân', '🌾', 'Bón phân hữu cơ, vô cơ'),
('spray', 'Phun thuốc', '💊', 'Phun thuốc bảo vệ thực vật'),
('water', 'Tưới nước', '💧', 'Tưới tiêu'),
('harvest', 'Thu hoạch', '💰', 'Thu hoạch nông sản'),
('prune', 'Tỉa cành', '✂️', 'Tỉa cành tạo tán'),
('inspect', 'Kiểm tra', '🔍', 'Kiểm tra, giám sát'),
('pack', 'Đóng gói', '📦', 'Đóng gói sản phẩm');

-- 6. Chủ vùng / Nông dân / HTX
INSERT INTO chu_vung (ma_chu, ten_chu, loai_chu, so_dien_thoai, email, dia_chi) VALUES
('CV-001', 'Nguyễn Văn A', 'ca_nhan', '0901234567', 'nguyenvana@gmail.com', 'Xã Mỹ Xương, Cao Lãnh, Đồng Tháp'),
('CV-002', 'Trần Thị B', 'ca_nhan', '0912345678', 'tranthib@gmail.com', 'Xã Long Trị, Long Hồ, Vĩnh Long'),
('CV-003', 'HTX Lúa Vàng', 'htx', '02773123456', 'htxluavang@gmail.com', 'Xã Tân Hưng, Tân Hiệp, Kiên Giang'),
('CV-004', 'Lê Văn C', 'ca_nhan', '0923456789', 'levanc@gmail.com', 'Xã Cai Lậy, Cai Lậy, Tiền Giang'),
('CV-005', 'Võ Văn D', 'ca_nhan', '0934567890', 'vovand@gmail.com', 'Xã Lộc Ninh, Bình Long, Bình Phước');

-- 7. Loại cây trồng
INSERT INTO loai_cay (ma_cay, ten_cay, nhom_cay, mo_ta) VALUES
('XOAI_MY', 'Xoài Mỹ Xương', 'Cây ăn trái', 'Giống xoài đặc sản Đồng Tháp'),
('NHAN', 'Nhãn', 'Cây ăn trái', 'Nhãn lồng'),
('THANH_LONG_DO', 'Thanh Long Đỏ', 'Cây ăn trái', 'Thanh long ruột đỏ'),
('THANH_LONG_TRANG', 'Thanh Long Trắng', 'Cây ăn trái', 'Thanh long ruột trắng'),
('LUA_JASMINE', 'Lúa Jasmine', 'Lúa', 'Giống lúa thơm Jasmine'),
('LUA_THOM', 'Lúa Thơm', 'Lúa', 'Giống lúa thơm đặc sản'),
('SAU_RIENG_RI6', 'Sầu Riêng Ri6', 'Cây ăn trái', 'Giống sầu riêng Ri6 Việt Nam'),
('SAU_RIENG_MUSANG', 'Sầu Riêng Musang King', 'Cây ăn trái', 'Giống sầu riêng Musang King'),
('TIEU_DEN', 'Tiêu đen', 'Cây công nghiệp', 'Hồ tiêu đen'),
('TIEU_TRANG', 'Tiêu trắng', 'Cây công nghiệp', 'Hồ tiêu trắng'),
('DUA', 'Dừa', 'Cây ăn trái', 'Dừa tươi'),
('CA_PHE_ROBUSTA', 'Cà phê Robusta', 'Cây công nghiệp', 'Giống cà phê Robusta'),
('CA_PHE_ARABICA', 'Cà phê Arabica', 'Cây công nghiệp', 'Giống cà phê Arabica'),
('RAU_AN_TOAN', 'Rau an toàn', 'Rau củ', 'Rau xanh an toàn'),
('BUOI_DA_XANH', 'Bưởi Da Xanh', 'Cây ăn trái', 'Giống bưởi da xanh Bến Tre'),
('CHANH_DAY', 'Chanh dây', 'Cây ăn trái', 'Chanh dây (Passion fruit)');

-- 8. Vùng trồng
INSERT INTO vung_trong (ma_vung, ten_vung, chu_vung_id, trang_thai_id, trang_thai_ma_id, chung_nhan_id, ma_qr, anh_dai_dien) VALUES
('VT-001', 'HTX Xoài Mỹ Xương', 1, 1, 1, 1, 'VT-001', 'https://images.unsplash.com/photo-1553279768-865429fa0078'),
('VT-002', 'Thanh Long VietGAP', 2, 2, 1, 2, 'VT-002', 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba'),
('VT-003', 'Lúa Chất lượng cao', 3, 3, 2, 4, 'VT-003', 'https://images.unsplash.com/photo-1536617621572-1d5f1e6269a0'),
('VT-004', 'Sầu Riêng Ri6', 4, 4, 1, 1, 'VT-004', 'https://images.unsplash.com/photo-1588611095757-5e53e8e87e91'),
('VT-005', 'Tiêu đen Chất lượng', 5, 1, 2, 1, 'VT-005', 'https://images.unsplash.com/photo-1596796930096-5c5e1e0f07d1');

-- 9. Tọa độ vùng trồng (Polygon 4 góc)
INSERT INTO toa_do_vung (vung_trong_id, thu_tu, vi_do, kinh_do) VALUES
-- VT-001
(1, 1, 10.759, 106.656), (1, 2, 10.759, 106.664), (1, 3, 10.765, 106.664), (1, 4, 10.765, 106.656),
-- VT-002
(2, 1, 10.768, 106.668), (2, 2, 10.768, 106.676), (2, 3, 10.772, 106.676), (2, 4, 10.772, 106.668),
-- VT-003
(3, 1, 10.747, 106.648), (3, 2, 10.747, 106.656), (3, 3, 10.753, 106.656), (3, 4, 10.753, 106.648),
-- VT-004
(4, 1, 10.777, 106.637), (4, 2, 10.777, 106.645), (4, 3, 10.781, 106.645), (4, 4, 10.781, 106.637),
-- VT-005
(5, 1, 10.758, 106.662), (5, 2, 10.758, 106.670), (5, 3, 10.762, 106.670), (5, 4, 10.762, 106.662);

-- 10. Chi tiết cây trồng trong vùng
INSERT INTO vung_cay_trong (vung_trong_id, loai_cay_id, dien_tich, nam_trong, nang_suat, gia_xuat_khau) VALUES
-- VT-001: Xoài, Nhãn, Dừa
(1, 1, 8.5, 2019, 42.3, 0.85),   -- Xoài Mỹ Xương
(1, 2, 3.2, 2021, 28.5, 0.65),   -- Nhãn
(1, 11, 5.0, 2020, 38.5, 0.75), -- Dừa
-- VT-002: Thanh Long Đỏ, Trắng, Cà phê
(2, 3, 12.0, 2020, 35.8, 1.20),  -- Thanh Long Đỏ
(2, 4, 6.5, 2021, 32.1, 1.00),   -- Thanh Long Trắng
(2, 12, 8.0, 2019, 45.2, 2.20),  -- Cà phê Robusta
(2, 13, 4.5, 2020, 40.8, 2.80),  -- Cà phê Arabica
-- VT-003: Lúa
(3, 5, 15.0, 2022, 58.5, 0.45),  -- Lúa Jasmine
(3, 6, 10.0, 2022, 55.2, 0.55),  -- Lúa Thơm
(3, 14, 6.5, 2023, 65.0, 0.35), -- Rau an toàn
-- VT-004: Sầu riêng, Bưởi
(4, 7, 7.0, 2018, 28.5, 2.50),   -- Sầu Riêng Ri6
(4, 8, 5.5, 2020, 30.2, 3.20),   -- Sầu Riêng Musang King
(4, 15, 3.8, 2021, 35.5, 0.95), -- Bưởi Da Xanh
-- VT-005: Tiêu, Chanh dây
(5, 9, 4.5, 2019, 22.5, 3.80),   -- Tiêu đen
(5, 10, 2.0, 2021, 18.5, 2.80),  -- Tiêu trắng
(5, 16, 3.2, 2022, 42.0, 1.50); -- Chanh dây

-- 11. Thị trường xuất khẩu của cây
INSERT INTO cay_thi_truong (vung_cay_trong_id, thi_truong_id) VALUES
-- Xoài Mỹ Xương: TQ, HK
(1, 1), (1, 2),
-- Nhãn: TQ
(2, 1),
-- Dừa: ASEAN, TQ
(3, 4), (3, 1),
-- Thanh Long Đỏ: TQ, HK, EU
(4, 1), (4, 2), (4, 3),
-- Thanh Long Trắng: TQ, EU
(5, 1), (5, 3),
-- Cà phê Robusta: EU, HK, JP
(6, 3), (6, 2), (6, 5),
-- Cà phê Arabica: EU, JP
(7, 3), (7, 5),
-- Lúa Jasmine: TQ, ASEAN
(8, 1), (8, 4),
-- Lúa Thơm: TQ, HK
(9, 1), (9, 2),
-- Rau an toàn: Nội địa, ASEAN
(10, 6), (10, 4),
-- Sầu Riêng Ri6: TQ
(11, 1),
-- Sầu Riêng Musang King: TQ, HK
(12, 1), (12, 2),
-- Bưởi Da Xanh: TQ, ASEAN
(13, 1), (13, 4),
-- Tiêu đen: TQ, EU, HK
(14, 1), (14, 3), (14, 2),
-- Tiêu trắng: EU, HK
(15, 3), (15, 2),
-- Chanh dây: EU, JP, HK
(16, 3), (16, 5), (16, 2);

-- 12. Lịch sử canh tác
INSERT INTO lich_su_canh_tac (vung_trong_id, loai_hoat_dong_id, ngay_thuc_hien, tieu_de, noi_dung, nguoi_thuc_hien, thua_ruong) VALUES
-- VT-001
(1, 3, '2024-12-01', 'Bón phân NPK', 'Bón lót 50kg phân vi sinh', 'Nguyễn Văn A', 'Thửa A'),
(1, 4, '2024-11-15', 'Phun thuốc trừ sâu', 'Phun thuốc sinh học định kỳ', 'Nguyễn Văn A', 'Thửa A'),
(1, 5, '2024-11-01', 'Tưới nước', 'Tưới nhỏ giọt 2 giờ', 'Nguyễn Văn A', 'Thửa A'),
-- VT-002
(2, 4, '2024-12-10', 'Xử lý sâu hại khẩn cấp', 'Phát hiện sâu hại - Xử lý khẩn cấp', 'Trần Thị B', 'Thửa B'),
(2, 3, '2024-12-05', 'Bón phân hữu cơ', 'Bón phân chuồng ủ hoai', 'Trần Thị B', 'Thửa B'),
(2, 7, '2024-11-20', 'Tỉa cành', 'Tỉa cành tạo tán sau thu hoạch', 'Trần Thị B', 'Thửa B'),
-- VT-003
(3, 6, '2024-12-14', 'Thu hoạch lúa', 'Thu hoạch lúa vụ Đông Xuân', 'HTX Lúa Vàng', 'Thửa C'),
(3, 8, '2024-11-30', 'Kiểm định chất lượng', 'Phát hiện dư lượng thuốc vượt ngưỡng', 'Thanh tra', 'Thửa C'),
(3, 4, '2024-11-25', 'Phun thuốc diệt cỏ', 'Sử dụng thuốc diệt cỏ tiền nảy mầm', 'HTX Lúa Vàng', 'Thửa C'),
-- VT-004
(4, 6, '2024-12-08', 'Hoàn thành thu hoạch', 'Thu hoạch xong 100% diện tích', 'Lê Văn C', 'Thửa D'),
(4, 9, '2024-11-28', 'Đóng gói vận chuyển', 'Đóng gói xuất khẩu đợt 1', 'Lê Văn C', 'Thửa D'),
(4, 8, '2024-11-15', 'Kiểm định chất lượng', 'Kiểm tra đạt tiêu chuẩn xuất khẩu', 'Chi cục NN', 'Thửa D'),
-- VT-005
(5, 8, '2024-12-12', 'Mã bị thu hồi', 'Mã bị thu hồi do vi phạm quy trình', 'Chi cục NN', 'Thửa E'),
(5, 4, '2024-12-01', 'Vi phạm BVTV', 'Sử dụng thuốc bảo vệ thực vật cấm', 'Võ Văn D', 'Thửa E'),
(5, 3, '2024-11-20', 'Bón phân', 'Bón phân NPK định kỳ', 'Võ Văn D', 'Thửa E');

-- 13. Điểm phát sinh sâu bệnh
INSERT INTO diem_sau_benh (vung_trong_id, vi_do, kinh_do, loai_sau_benh, muc_do, ngay_phat_hien, trang_thai, bien_phap) VALUES
(2, 10.770, 106.670, 'Nấm tắc kè', 'trung_binh', '2024-12-05', 'dang_xu_ly', 'Phun thuốc sinh học'),
(2, 10.771, 106.671, 'Rầy chổng cánh', 'nhe', '2024-12-08', 'da_xu_ly', 'Phun thuốc trừ sâu'),
(2, 10.769, 106.669, 'Sâu đục thân', 'nang', '2024-12-10', 'dang_xu_ly', 'Phun thuốc và cắt tỉa'),
(3, 10.750, 106.650, 'Rầy nâu', 'trung_binh', '2024-11-28', 'da_xu_ly', 'Phun thuốc diệt rầy');

-- 14. Thống kê hệ thống
INSERT INTO thong_ke_he_thong (ngay_thong_ke, tong_vung, tong_dien_tich, san_luong_du_kien, so_canh_bao, so_ma_thu_hoi) VALUES
('2024-12-18', 124, 450.00, 1200.00, 5, 2);

-- =============================================================================
-- TẠO VIEW ĐỂ TRUY VẤN DỮ LIỆU DỄ DÀNG
-- =============================================================================

-- View danh sách vùng trồng đầy đủ thông tin
CREATE OR REPLACE VIEW v_vung_trong_full AS
SELECT 
    vt.id,
    vt.ma_vung,
    vt.ten_vung,
    cv.ten_chu AS chu_vung,
    cv.loai_chu,
    tt.ten_trang_thai AS trang_thai,
    tt.mau_sac,
    ttm.ten_trang_thai AS trang_thai_ma,
    cn.ten_chung_nhan AS chung_nhan,
    vt.ma_qr,
    vt.anh_dai_dien,
    vt.ngay_tao
FROM vung_trong vt
LEFT JOIN chu_vung cv ON vt.chu_vung_id = cv.id
LEFT JOIN trang_thai tt ON vt.trang_thai_id = tt.id
LEFT JOIN trang_thai_ma ttm ON vt.trang_thai_ma_id = ttm.id
LEFT JOIN chung_nhan cn ON vt.chung_nhan_id = cn.id;

-- View chi tiết cây trồng với thông tin vùng
CREATE OR REPLACE VIEW v_cay_trong_chi_tiet AS
SELECT 
    vct.id,
    vt.ma_vung,
    vt.ten_vung,
    lc.ten_cay,
    lc.nhom_cay,
    vct.dien_tich,
    vct.nam_trong,
    vct.nang_suat,
    vct.gia_xuat_khau
FROM vung_cay_trong vct
JOIN vung_trong vt ON vct.vung_trong_id = vt.id
JOIN loai_cay lc ON vct.loai_cay_id = lc.id;

-- View thống kê năng suất theo loại cây
CREATE OR REPLACE VIEW v_thong_ke_nang_suat AS
SELECT 
    lc.ten_cay,
    lc.nhom_cay,
    COUNT(vct.id) AS so_vung,
    SUM(vct.dien_tich) AS tong_dien_tich,
    AVG(vct.nang_suat) AS nang_suat_tb,
    AVG(vct.gia_xuat_khau) AS gia_xuat_tb
FROM loai_cay lc
LEFT JOIN vung_cay_trong vct ON lc.id = vct.loai_cay_id
GROUP BY lc.id, lc.ten_cay, lc.nhom_cay
ORDER BY tong_dien_tich DESC;

-- View thống kê xuất khẩu theo thị trường
CREATE OR REPLACE VIEW v_thong_ke_xuat_khau AS
SELECT 
    tt.ten_thi_truong,
    tt.vung_dia_ly,
    COUNT(DISTINCT ctt.vung_cay_trong_id) AS so_loai_cay,
    SUM(vct.dien_tich * vct.nang_suat * vct.gia_xuat_khau) AS gia_tri_du_kien
FROM thi_truong tt
LEFT JOIN cay_thi_truong ctt ON tt.id = ctt.thi_truong_id
LEFT JOIN vung_cay_trong vct ON ctt.vung_cay_trong_id = vct.id
GROUP BY tt.id, tt.ten_thi_truong, tt.vung_dia_ly
ORDER BY gia_tri_du_kien DESC;

-- =============================================================================
-- KẾT THÚC SCRIPT
-- =============================================================================

COMMENT ON SCHEMA nongsan IS 'Schema quản lý nông sản - Thiết kế theo 3NF';
COMMENT ON TABLE vung_trong IS 'Bảng chính lưu thông tin vùng trồng';
COMMENT ON TABLE vung_cay_trong IS 'Bảng quan hệ N-N giữa vùng và cây trồng';
COMMENT ON TABLE cay_thi_truong IS 'Bảng quan hệ N-N giữa cây và thị trường xuất khẩu';
COMMENT ON TABLE lich_su_canh_tac IS 'Bảng lưu nhật ký đồng ruộng';
