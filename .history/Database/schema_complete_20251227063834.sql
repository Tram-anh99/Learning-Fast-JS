-- =============================================================================
-- CƠ SỞ DỮ LIỆU QUẢN LÝ NÔNG SẢN - POSTGRESQL (HOÀN CHỈNH)
-- Thiết kế theo 3 chuẩn cơ sở dữ liệu (3NF)
-- =============================================================================
-- Tích hợp:
-- - Hệ thống truy xuất nguồn gốc (MSVT)
-- - Quản lý giống cây trồng & nguồn gen
-- - Quản lý phân bón
-- - Quản lý thuốc bảo vệ thực vật (TBVTV)
-- - Quản lý cơ sở sản xuất kinh doanh
-- - Vùng trồng và nhật ký canh tác
-- =============================================================================

-- Xóa schema cũ nếu cần (CẢNH BÁO: Xóa toàn bộ dữ liệu)
-- DROP SCHEMA IF EXISTS nongsan CASCADE;

-- Tạo schema
CREATE SCHEMA IF NOT EXISTS nongsan;
SET search_path TO nongsan;

-- =============================================================================
-- PHẦN 1: BẢNG DANH MỤC CƠ BẢN (REFERENCE TABLES)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1.1. Đơn vị hành chính
-- -----------------------------------------------------------------------------
CREATE TABLE tinh (
    id SERIAL PRIMARY KEY,
    ma_tinh VARCHAR(10) UNIQUE NOT NULL,
    ten_tinh VARCHAR(100) NOT NULL,
    vung_dia_ly VARCHAR(50),                         -- Đồng bằng sông Cửu Long, Đông Nam Bộ, ...
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE huyen (
    id SERIAL PRIMARY KEY,
    ma_huyen VARCHAR(10) UNIQUE NOT NULL,
    ten_huyen VARCHAR(100) NOT NULL,
    tinh_id INTEGER REFERENCES tinh(id),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE xa (
    id SERIAL PRIMARY KEY,
    ma_xa VARCHAR(10) UNIQUE NOT NULL,
    ten_xa VARCHAR(100) NOT NULL,
    huyen_id INTEGER REFERENCES huyen(id),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 1.2. Trạng thái
-- -----------------------------------------------------------------------------
CREATE TABLE trang_thai_vung (
    id SERIAL PRIMARY KEY,
    ma_trang_thai VARCHAR(20) UNIQUE NOT NULL,       -- canh_tac, sau_benh, thu_hoach, da_thu_hoach
    ten_trang_thai VARCHAR(50) NOT NULL,
    mau_sac VARCHAR(10),
    css_class VARCHAR(30),
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trang_thai_ma_vung (
    id SERIAL PRIMARY KEY,
    ma_trang_thai VARCHAR(20) UNIQUE NOT NULL,       -- hoat_dong, bi_thu_hoi
    ten_trang_thai VARCHAR(50) NOT NULL,
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 1.3. Chứng nhận & Tiêu chuẩn
-- -----------------------------------------------------------------------------
CREATE TABLE chung_nhan (
    id SERIAL PRIMARY KEY,
    ma_chung_nhan VARCHAR(20) UNIQUE NOT NULL,       -- VIETGAP, GLOBALGAP, OCOP4, OCOP5
    ten_chung_nhan VARCHAR(100) NOT NULL,
    to_chuc_cap VARCHAR(100),
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 1.4. Thị trường
-- -----------------------------------------------------------------------------
CREATE TABLE thi_truong (
    id SERIAL PRIMARY KEY,
    ma_thi_truong VARCHAR(20) UNIQUE NOT NULL,       -- TQ, HK, EU, ASEAN, JP, ND
    ten_thi_truong VARCHAR(100) NOT NULL,
    vung_dia_ly VARCHAR(50),                         -- Châu Á, Bắc Mỹ, Châu Âu
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 1.5. Loại hoạt động canh tác
-- -----------------------------------------------------------------------------
CREATE TABLE loai_hoat_dong (
    id SERIAL PRIMARY KEY,
    ma_loai VARCHAR(20) UNIQUE NOT NULL,             -- tillage, sow, fertilizer, spray, water, harvest
    ten_loai VARCHAR(50) NOT NULL,
    icon VARCHAR(10),                                -- 🚜, 🌱, 🌾, 💊, 💧, 💰
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- PHẦN 2: QUẢN LÝ GIỐNG CÂY TRỒNG & NGUỒN GEN
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 2.1. Nhóm cây trồng
-- -----------------------------------------------------------------------------
CREATE TABLE nhom_cay (
    id SERIAL PRIMARY KEY,
    ma_nhom VARCHAR(20) UNIQUE NOT NULL,
    ten_nhom VARCHAR(100) NOT NULL,                  -- Cây ăn quả, Lúa, Rau củ, Cây công nghiệp
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2.2. Loại cây trồng (Thống nhất từ cả 2 nguồn: giong và msvt)
-- -----------------------------------------------------------------------------
CREATE TABLE loai_cay (
    id SERIAL PRIMARY KEY,
    ma_cay VARCHAR(20) UNIQUE NOT NULL,              -- XOAI_MY, THANH_LONG_DO, LUA_JASMINE
    ten_cay VARCHAR(100) NOT NULL,
    ten_khoa_hoc VARCHAR(200),                       -- Tên khoa học (Latin)
    nhom_cay_id INTEGER REFERENCES nhom_cay(id),
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2.3. Cơ quan lưu trữ nguồn gen
-- -----------------------------------------------------------------------------
CREATE TABLE co_quan_luu_tru_gen (
    id SERIAL PRIMARY KEY,
    ma_co_quan VARCHAR(20) UNIQUE NOT NULL,
    ten_co_quan VARCHAR(200) NOT NULL,               -- Viện nghiên cứu cây ăn quả Miền Nam
    dia_chi TEXT,
    dien_thoai VARCHAR(20),
    email VARCHAR(100),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2.4. Nơi thu thập nguồn gen
-- -----------------------------------------------------------------------------
CREATE TABLE noi_thu_thap_gen (
    id SERIAL PRIMARY KEY,
    ten_noi VARCHAR(200) NOT NULL,                   -- Đồng bằng sông Cửu Long, Tây Nguyên
    tinh_id INTEGER REFERENCES tinh(id),
    vung_dia_ly VARCHAR(100),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2.5. Nguồn thu thập
-- -----------------------------------------------------------------------------
CREATE TABLE nguon_thu_thap (
    id SERIAL PRIMARY KEY,
    ten_nguon TEXT NOT NULL,                         -- Đề tài Bảo tồn và Lưu giữ nguồn gen...
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2.6. Nguồn gen cây trồng
-- -----------------------------------------------------------------------------
CREATE TABLE nguon_gen (
    id SERIAL PRIMARY KEY,
    ma_gbvn VARCHAR(50) UNIQUE NOT NULL,             -- GBVNML18.351
    loai_cay_id INTEGER NOT NULL REFERENCES loai_cay(id),
    nhom_cay_id INTEGER REFERENCES nhom_cay(id),
    co_quan_luu_tru_id INTEGER REFERENCES co_quan_luu_tru_gen(id),
    noi_thu_thap_id INTEGER REFERENCES noi_thu_thap_gen(id),
    nguon_thu_thap_id INTEGER REFERENCES nguon_thu_thap(id),
    nam_thu_thap INTEGER,
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2.7. Giống bảo hộ (PVPO)
-- -----------------------------------------------------------------------------
CREATE TABLE giong_bao_ho (
    id SERIAL PRIMARY KEY,
    so_bang VARCHAR(50) UNIQUE NOT NULL,             -- 47.VN.2022
    ma_giong VARCHAR(50) UNIQUE NOT NULL,            -- PVPO001910
    ten_giong VARCHAR(200) NOT NULL,                 -- HP6, LCT1
    loai_cay_id INTEGER REFERENCES loai_cay(id),
    ten_chu_so_huu VARCHAR(300),                     -- Viên Nghiên Cứu Rau Quả
    ngay_bat_dau_hieu_luc DATE,
    tinh_trang VARCHAR(50),                          -- Còn hiệu lực, Hết hiệu lực
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- PHẦN 3: QUẢN LÝ TỔ CHỨC, CÁ NHÂN
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 3.1. Tổ chức/Cá nhân (Chủ vùng, Cơ sở SX/KD)
-- -----------------------------------------------------------------------------
CREATE TABLE to_chuc_ca_nhan (
    id SERIAL PRIMARY KEY,
    ma_to_chuc VARCHAR(50) UNIQUE NOT NULL,          -- TC-001, TC-002
    ten_to_chuc VARCHAR(300) NOT NULL,
    loai_to_chuc VARCHAR(50) NOT NULL,               -- ca_nhan, htx, doanh_nghiep, co_quan_nha_nuoc
    nguoi_dai_dien VARCHAR(200),
    dien_thoai VARCHAR(20),
    email VARCHAR(100),
    dia_chi TEXT,
    xa_id INTEGER REFERENCES xa(id),
    huyen_id INTEGER REFERENCES huyen(id),
    tinh_id INTEGER REFERENCES tinh(id),
    trang_thai VARCHAR(20) DEFAULT 'hoat_dong',      -- hoat_dong, tam_ngung, thu_hoi
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- PHẦN 4: QUẢN LÝ CƠ SỞ SẢN XUẤT KINH DOANH
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 4.1. Loại hình cơ sở
-- -----------------------------------------------------------------------------
CREATE TABLE loai_hinh_co_so (
    id SERIAL PRIMARY KEY,
    ma_loai VARCHAR(50) UNIQUE NOT NULL,             -- CS_GIONG, CS_PB, CS_TBVTV, CS_DONG_GOI
    ten_loai VARCHAR(200) NOT NULL,                  -- Cơ sở giống, Cơ sở phân bón, ...
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 4.2. Cơ sở sản xuất kinh doanh
-- -----------------------------------------------------------------------------
CREATE TABLE co_so (
    id SERIAL PRIMARY KEY,
    ma_co_so VARCHAR(50) UNIQUE NOT NULL,
    ten_co_so VARCHAR(300) NOT NULL,
    bien_hieu VARCHAR(300),                          -- Biển hiệu
    loai_hinh_id INTEGER REFERENCES loai_hinh_co_so(id),
    to_chuc_id INTEGER NOT NULL REFERENCES to_chuc_ca_nhan(id),
    so_giay_phep VARCHAR(100),                       -- Số giấy chứng nhận
    ngay_cap_phep DATE,
    ngay_het_han DATE,
    tinh_trang VARCHAR(50) DEFAULT 'con_hieu_luc',   -- con_hieu_luc, het_hieu_luc, bi_thu_hoi
    dia_chi TEXT,
    xa_id INTEGER REFERENCES xa(id),
    huyen_id INTEGER REFERENCES huyen(id),
    tinh_id INTEGER REFERENCES tinh(id),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- PHẦN 5: QUẢN LÝ PHÂN BÓN
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 5.1. Loại phân bón
-- -----------------------------------------------------------------------------
CREATE TABLE loai_phan_bon (
    id SERIAL PRIMARY KEY,
    ma_loai VARCHAR(50) UNIQUE NOT NULL,
    ten_loai VARCHAR(200) NOT NULL,                  -- Phân hữu cơ, Phân NPK, Phân vi lượng
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 5.2. Phân bón
-- -----------------------------------------------------------------------------
CREATE TABLE phan_bon (
    id SERIAL PRIMARY KEY,
    ma_phan_bon VARCHAR(100) UNIQUE NOT NULL,
    ten_phan_bon VARCHAR(300) NOT NULL,
    loai_phan_bon_id INTEGER REFERENCES loai_phan_bon(id),
    thanh_phan TEXT,                                 -- Thành phần, hàm lượng
    don_vi VARCHAR(50),                              -- %, kg/bao
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 5.3. Phân bón được phép lưu hành
-- -----------------------------------------------------------------------------
CREATE TABLE phan_bon_luu_hanh (
    id SERIAL PRIMARY KEY,
    phan_bon_id INTEGER NOT NULL REFERENCES phan_bon(id),
    to_chuc_cong_bo_id INTEGER REFERENCES to_chuc_ca_nhan(id),
    so_tiep_nhan VARCHAR(100),
    so_chung_nhan VARCHAR(100),
    to_chuc_chung_nhan_id INTEGER REFERENCES to_chuc_ca_nhan(id),
    quyet_dinh_cong_nhan VARCHAR(100),
    ngay_cong_nhan DATE,
    loai_hinh_danh_gia VARCHAR(100),                 -- Bên thứ nhất, Bên thứ ba
    trang_thai VARCHAR(50) DEFAULT 'con_hieu_luc',
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 5.4. Cơ sở sản xuất/kinh doanh phân bón
-- -----------------------------------------------------------------------------
CREATE TABLE co_so_phan_bon (
    id SERIAL PRIMARY KEY,
    co_so_id INTEGER NOT NULL REFERENCES co_so(id),
    phan_bon_id INTEGER NOT NULL REFERENCES phan_bon(id),
    hoat_dong VARCHAR(50),                           -- san_xuat, nhap_khau, mua_ban
    ngay_bat_dau DATE,
    ngay_ket_thuc DATE,
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(co_so_id, phan_bon_id, hoat_dong)
);

-- =============================================================================
-- PHẦN 6: QUẢN LÝ THUỐC BẢO VỆ THỰC VẬT (TBVTV)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 6.1. Nhóm thuốc BVTV
-- -----------------------------------------------------------------------------
CREATE TABLE nhom_thuoc_bvtv (
    id SERIAL PRIMARY KEY,
    ma_nhom VARCHAR(50) UNIQUE NOT NULL,
    ten_nhom VARCHAR(200) NOT NULL,                  -- Thuốc trừ sâu, Thuốc diệt nấm, ...
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 6.2. Thuốc bảo vệ thực vật
-- -----------------------------------------------------------------------------
CREATE TABLE thuoc_bvtv (
    id SERIAL PRIMARY KEY,
    ma_thuoc VARCHAR(100) UNIQUE NOT NULL,
    ten_thuoc VARCHAR(300) NOT NULL,
    ten_hoat_chat VARCHAR(300),                      -- Hoạt chất chính
    ham_luong VARCHAR(200),                          -- Hàm lượng hoạt chất
    nhom_thuoc_id INTEGER REFERENCES nhom_thuoc_bvtv(id),
    dang_bao_che VARCHAR(100),                       -- EC, WP, SC, ...
    trang_thai_su_dung VARCHAR(50) DEFAULT 'duoc_su_dung', -- duoc_su_dung, cam_su_dung
    mo_ta TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 6.3. Thuốc BVTV được phép lưu hành
-- -----------------------------------------------------------------------------
CREATE TABLE thuoc_bvtv_luu_hanh (
    id SERIAL PRIMARY KEY,
    thuoc_bvtv_id INTEGER NOT NULL REFERENCES thuoc_bvtv(id),
    to_chuc_cong_bo_id INTEGER REFERENCES to_chuc_ca_nhan(id),
    so_dang_ky VARCHAR(100),
    ngay_dang_ky DATE,
    ngay_het_han DATE,
    trang_thai VARCHAR(50) DEFAULT 'con_hieu_luc',
    doi_tuong_su_dung TEXT,                          -- Cây trồng áp dụng
    lieu_luong_khuyen_cao TEXT,                      -- Liều lượng khuyến cáo
    thoi_gian_cach_ly INTEGER,                       -- Ngày cách ly trước thu hoạch
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 6.4. Cơ sở kinh doanh thuốc BVTV
-- -----------------------------------------------------------------------------
CREATE TABLE co_so_thuoc_bvtv (
    id SERIAL PRIMARY KEY,
    co_so_id INTEGER NOT NULL REFERENCES co_so(id),
    thuoc_bvtv_id INTEGER NOT NULL REFERENCES thuoc_bvtv(id),
    hoat_dong VARCHAR(50),                           -- san_xuat, nhap_khau, buon_ban
    ngay_bat_dau DATE,
    ngay_ket_thuc DATE,
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(co_so_id, thuoc_bvtv_id, hoat_dong)
);

-- =============================================================================
-- PHẦN 7: QUẢN LÝ VÙNG TRỒNG (MSVT)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 7.1. Vùng trồng
-- -----------------------------------------------------------------------------
CREATE TABLE vung_trong (
    id SERIAL PRIMARY KEY,
    ma_vung VARCHAR(50) UNIQUE NOT NULL,             -- VT-001, VN-GLOR-0064 (PUC)
    ma_vung_puc VARCHAR(50),                         -- Mã vùng theo PUC (nếu có)
    ten_vung VARCHAR(300) NOT NULL,
    chu_so_huu_id INTEGER REFERENCES to_chuc_ca_nhan(id),
    trang_thai_id INTEGER REFERENCES trang_thai_vung(id),
    trang_thai_ma_id INTEGER REFERENCES trang_thai_ma_vung(id),
    chung_nhan_id INTEGER REFERENCES chung_nhan(id),
    dien_tich DECIMAL(12, 2),                        -- Diện tích (ha)
    ma_qr VARCHAR(100),                              -- Mã QR truy xuất
    anh_dai_dien TEXT,
    dia_chi TEXT,
    xa_id INTEGER REFERENCES xa(id),
    huyen_id INTEGER REFERENCES huyen(id),
    tinh_id INTEGER REFERENCES tinh(id),
    thoi_gian_bat_dau_thu_hoach DATE,
    thoi_gian_ket_thuc_thu_hoach DATE,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 7.2. Tọa độ polygon vùng trồng
-- -----------------------------------------------------------------------------
CREATE TABLE toa_do_vung (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER NOT NULL REFERENCES vung_trong(id) ON DELETE CASCADE,
    thu_tu INTEGER NOT NULL,                         -- Thứ tự điểm
    vi_do DECIMAL(10, 6) NOT NULL,
    kinh_do DECIMAL(10, 6) NOT NULL,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vung_trong_id, thu_tu)
);

-- -----------------------------------------------------------------------------
-- 7.3. Cây trồng trong vùng (N-N)
-- -----------------------------------------------------------------------------
CREATE TABLE vung_cay_trong (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER NOT NULL REFERENCES vung_trong(id) ON DELETE CASCADE,
    loai_cay_id INTEGER NOT NULL REFERENCES loai_cay(id),
    giong_id INTEGER REFERENCES giong_bao_ho(id),    -- Giống cụ thể (nếu có)
    dien_tich DECIMAL(12, 2),                        -- Diện tích (ha)
    nam_trong INTEGER,
    nang_suat DECIMAL(12, 2),                        -- Năng suất (tạ/ha)
    gia_xuat_khau DECIMAL(12, 2),                    -- USD/kg
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vung_trong_id, loai_cay_id)
);

-- -----------------------------------------------------------------------------
-- 7.4. Thị trường xuất khẩu của cây trồng (N-N)
-- -----------------------------------------------------------------------------
CREATE TABLE vung_thi_truong (
    id SERIAL PRIMARY KEY,
    vung_cay_trong_id INTEGER NOT NULL REFERENCES vung_cay_trong(id) ON DELETE CASCADE,
    thi_truong_id INTEGER NOT NULL REFERENCES thi_truong(id),
    san_luong_xuat DECIMAL(12, 2),                   -- Sản lượng dự kiến (tấn)
    gia_tri_xuat DECIMAL(15, 2),                     -- Giá trị dự kiến (USD)
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vung_cay_trong_id, thi_truong_id)
);

-- -----------------------------------------------------------------------------
-- 7.5. Cơ sở đóng gói phục vụ vùng
-- -----------------------------------------------------------------------------
CREATE TABLE vung_co_so_dong_goi (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER NOT NULL REFERENCES vung_trong(id),
    co_so_id INTEGER NOT NULL REFERENCES co_so(id),
    ngay_bat_dau DATE,
    ngay_ket_thuc DATE,
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(vung_trong_id, co_so_id)
);

-- =============================================================================
-- PHẦN 8: NHẬT KÝ CANH TÁC & QUẢN LÝ SẢU BỆNH
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 8.1. Nhật ký canh tác/Lịch sử canh tác
-- -----------------------------------------------------------------------------
CREATE TABLE lich_su_canh_tac (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER NOT NULL REFERENCES vung_trong(id) ON DELETE CASCADE,
    loai_hoat_dong_id INTEGER REFERENCES loai_hoat_dong(id),
    ngay_thuc_hien DATE NOT NULL,
    tieu_de VARCHAR(300),
    noi_dung TEXT,
    nguoi_thuc_hien VARCHAR(200),
    thua_ruong VARCHAR(200),                         -- Thửa A, Thửa B, ...
    
    -- Thông tin vật tư sử dụng
    phan_bon_id INTEGER REFERENCES phan_bon(id),
    lieu_luong_phan_bon VARCHAR(100),
    thuoc_bvtv_id INTEGER REFERENCES thuoc_bvtv(id),
    lieu_luong_thuoc VARCHAR(100),
    
    ghi_chu TEXT,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 8.2. Điểm phát sinh sâu bệnh
-- -----------------------------------------------------------------------------
CREATE TABLE diem_sau_benh (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER REFERENCES vung_trong(id) ON DELETE CASCADE,
    vi_do DECIMAL(10, 6) NOT NULL,
    kinh_do DECIMAL(10, 6) NOT NULL,
    loai_sau_benh VARCHAR(200),
    muc_do VARCHAR(50),                              -- nhe, trung_binh, nang
    ngay_phat_hien DATE NOT NULL,
    trang_thai VARCHAR(50) DEFAULT 'chua_xu_ly',     -- chua_xu_ly, dang_xu_ly, da_xu_ly
    bien_phap TEXT,
    thuoc_bvtv_su_dung_id INTEGER REFERENCES thuoc_bvtv(id),
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ngay_cap_nhat TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- PHẦN 9: THỐNG KÊ & BÁO CÁO
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 9.1. Thống kê hệ thống
-- -----------------------------------------------------------------------------
CREATE TABLE thong_ke_he_thong (
    id SERIAL PRIMARY KEY,
    ngay_thong_ke DATE NOT NULL UNIQUE,
    tong_vung INTEGER DEFAULT 0,
    tong_dien_tich DECIMAL(12, 2) DEFAULT 0,
    san_luong_du_kien DECIMAL(12, 2) DEFAULT 0,
    so_canh_bao INTEGER DEFAULT 0,
    so_ma_thu_hoi INTEGER DEFAULT 0,
    tong_co_so_hoat_dong INTEGER DEFAULT 0,
    ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- TẠO INDEX ĐỂ TỐI ƯU TRUY VẤN
-- =============================================================================

-- Index cho vùng trồng
CREATE INDEX idx_vung_trong_ma ON vung_trong(ma_vung);
CREATE INDEX idx_vung_trong_trang_thai ON vung_trong(trang_thai_id);
CREATE INDEX idx_vung_trong_chu ON vung_trong(chu_so_huu_id);
CREATE INDEX idx_vung_trong_tinh ON vung_trong(tinh_id);

-- Index cho cây trồng
CREATE INDEX idx_vung_cay_vung ON vung_cay_trong(vung_trong_id);
CREATE INDEX idx_vung_cay_cay ON vung_cay_trong(loai_cay_id);
CREATE INDEX idx_loai_cay_nhom ON loai_cay(nhom_cay_id);

-- Index cho lịch sử
CREATE INDEX idx_lich_su_vung ON lich_su_canh_tac(vung_trong_id);
CREATE INDEX idx_lich_su_ngay ON lich_su_canh_tac(ngay_thuc_hien);

-- Index cho cơ sở
CREATE INDEX idx_co_so_loai_hinh ON co_so(loai_hinh_id);
CREATE INDEX idx_co_so_to_chuc ON co_so(to_chuc_id);
CREATE INDEX idx_co_so_tinh ON co_so(tinh_id);

-- Index cho phân bón & thuốc
CREATE INDEX idx_phan_bon_loai ON phan_bon(loai_phan_bon_id);
CREATE INDEX idx_thuoc_bvtv_nhom ON thuoc_bvtv(nhom_thuoc_id);
CREATE INDEX idx_phan_bon_luu_hanh_pb ON phan_bon_luu_hanh(phan_bon_id);
CREATE INDEX idx_thuoc_luu_hanh_thuoc ON thuoc_bvtv_luu_hanh(thuoc_bvtv_id);

-- =============================================================================
-- INSERT DỮ LIỆU MẪU CƠ BẢN
-- =============================================================================

-- 1. Tỉnh/Thành phố
INSERT INTO tinh (ma_tinh, ten_tinh, vung_dia_ly) VALUES
('92', 'Cần Thơ', 'Đồng bằng sông Cửu Long'),
('87', 'Đồng Tháp', 'Đồng bằng sông Cửu Long'),
('86', 'Vĩnh Long', 'Đồng bằng sông Cửu Long'),
('82', 'Tiền Giang', 'Đồng bằng sông Cửu Long'),
('96', 'Cà Mau', 'Đồng bằng sông Cửu Long'),
('64', 'Gia Lai', 'Tây Nguyên'),
('01', 'Hà Nội', 'Đồng bằng sông Hồng');

-- 2. Trạng thái vùng
INSERT INTO trang_thai_vung (ma_trang_thai, ten_trang_thai, mau_sac, css_class) VALUES
('canh_tac', 'Đang canh tác', '#4caf50', 'bg-green-500'),
('sau_benh', 'Cảnh báo dịch hại', '#ef5350', 'bg-red-500'),
('thu_hoach', 'Đang thu hoạch', '#ffca28', 'bg-yellow-500'),
('da_thu_hoach', 'Đã thu hoạch', '#2563eb', 'bg-blue-600');

INSERT INTO trang_thai_ma_vung (ma_trang_thai, ten_trang_thai) VALUES
('hoat_dong', 'Hoạt động'),
('bi_thu_hoi', 'Bị thu hồi');

-- 3. Chứng nhận
INSERT INTO chung_nhan (ma_chung_nhan, ten_chung_nhan, to_chuc_cap) VALUES
('VIETGAP', 'VietGAP', 'Bộ NN&PTNT Việt Nam'),
('GLOBALGAP', 'GlobalGAP', 'GLOBALG.A.P.'),
('OCOP3', 'OCOP 3 Sao', 'Chương trình OCOP'),
('OCOP4', 'OCOP 4 Sao', 'Chương trình OCOP'),
('OCOP5', 'OCOP 5 Sao', 'Chương trình OCOP');

-- 4. Thị trường
INSERT INTO thi_truong (ma_thi_truong, ten_thi_truong, vung_dia_ly) VALUES
('TQ', 'Trung Quốc', 'Châu Á'),
('HK', 'Hoa Kỳ', 'Bắc Mỹ'),
('EU', 'Châu Âu', 'Châu Âu'),
('ASEAN', 'ASEAN', 'Châu Á'),
('JP', 'Nhật Bản', 'Châu Á'),
('ND', 'Nội địa', 'Việt Nam');

-- 5. Loại hoạt động canh tác
INSERT INTO loai_hoat_dong (ma_loai, ten_loai, icon) VALUES
('tillage', 'Cày ải', '🚜'),
('sow', 'Gieo sạ', '🌱'),
('fertilizer', 'Bón phân', '🌾'),
('spray', 'Phun thuốc', '💊'),
('water', 'Tưới nước', '💧'),
('harvest', 'Thu hoạch', '💰'),
('prune', 'Tỉa cành', '✂️'),
('inspect', 'Kiểm tra', '🔍'),
('pack', 'Đóng gói', '📦');

-- 6. Nhóm cây trồng
INSERT INTO nhom_cay (ma_nhom, ten_nhom) VALUES
('CAY_AN_QUA', 'Cây ăn quả'),
('LUA', 'Lúa'),
('RAU_CU', 'Rau củ'),
('CAY_CONG_NGHIEP', 'Cây công nghiệp'),
('HOA', 'Cây hoa'),
('DUOC_LIEU', 'Cây dược liệu');

-- 7. Loại cây (Kết hợp từ nhiều nguồn)
INSERT INTO loai_cay (ma_cay, ten_cay, ten_khoa_hoc, nhom_cay_id) VALUES
('XOAI_MY', 'Xoài Mỹ Xương', 'Mangifera indica', 1),
('THANH_LONG_DO', 'Thanh Long Đỏ', 'Hylocereus undatus', 1),
('LUA_JASMINE', 'Lúa Jasmine', 'Oryza sativa', 2),
('SAU_RIENG_RI6', 'Sầu Riêng Ri6', 'Durio zibethinus', 1),
('TIEU_DEN', 'Tiêu đen', 'Piper nigrum', 4),
('CHANH_LEO', 'Chanh leo', 'Passiflora edulis', 1),
('CHUOI', 'Chuối', 'Musa', 1),
('QUE', 'Quế', 'Cinnamomum verum', 4);

-- 8. Loại hình cơ sở
INSERT INTO loai_hinh_co_so (ma_loai, ten_loai) VALUES
('CS_GIONG', 'Cơ sở giống cây trồng'),
('CS_PB', 'Cơ sở phân bón'),
('CS_TBVTV', 'Cơ sở thuốc BVTV'),
('CS_DONG_GOI', 'Cơ sở đóng gói'),
('CS_CHE_BIEN', 'Cơ sở chế biến');

-- 9. Loại phân bón
INSERT INTO loai_phan_bon (ma_loai, ten_loai) VALUES
('HUU_CO', 'Phân hữu cơ'),
('NPK', 'Phân NPK'),
('DAM', 'Phân đạm'),
('LAN', 'Phân lân'),
('KALI', 'Phân kali'),
('VI_LUONG', 'Phân vi lượng'),
('SINH_HOC', 'Phân sinh học');

-- 10. Nhóm thuốc BVTV
INSERT INTO nhom_thuoc_bvtv (ma_nhom, ten_nhom) VALUES
('TRU_SAU', 'Thuốc trừ sâu'),
('DIET_NAM', 'Thuốc diệt nấm'),
('DIET_CO', 'Thuốc diệt cỏ'),
('TRU_BO_KEN', 'Thuốc trừ bọ kẹn'),
('DIET_CHUOT', 'Thuốc diệt chuột'),
('DIEU_HOA_SINH_TRUONG', 'Chất điều hòa sinh trưởng');

-- =============================================================================
-- TẠO VIEW TRUY VẤN
-- =============================================================================

-- View vùng trồng đầy đủ
CREATE OR REPLACE VIEW v_vung_trong_full AS
SELECT 
    vt.id,
    vt.ma_vung,
    vt.ma_vung_puc,
    vt.ten_vung,
    tcn.ten_to_chuc AS chu_so_huu,
    tcn.nguoi_dai_dien,
    ttv.ten_trang_thai AS trang_thai,
    ttm.ten_trang_thai AS trang_thai_ma,
    cn.ten_chung_nhan AS chung_nhan,
    vt.dien_tich,
    vt.ma_qr,
    x.ten_xa,
    h.ten_huyen,
    t.ten_tinh,
    vt.ngay_tao
FROM vung_trong vt
LEFT JOIN to_chuc_ca_nhan tcn ON vt.chu_so_huu_id = tcn.id
LEFT JOIN trang_thai_vung ttv ON vt.trang_thai_id = ttv.id
LEFT JOIN trang_thai_ma_vung ttm ON vt.trang_thai_ma_id = ttm.id
LEFT JOIN chung_nhan cn ON vt.chung_nhan_id = cn.id
LEFT JOIN xa x ON vt.xa_id = x.id
LEFT JOIN huyen h ON vt.huyen_id = h.id
LEFT JOIN tinh t ON vt.tinh_id = t.id;

-- View cây trồng trong vùng
CREATE OR REPLACE VIEW v_vung_cay_trong AS
SELECT 
    vct.id,
    vt.ma_vung,
    vt.ten_vung,
    lc.ten_cay,
    lc.ten_khoa_hoc,
    nc.ten_nhom AS nhom_cay,
    vct.dien_tich,
    vct.nam_trong,
    vct.nang_suat,
    vct.gia_xuat_khau,
    gb.ten_giong AS giong_bao_ho
FROM vung_cay_trong vct
JOIN vung_trong vt ON vct.vung_trong_id = vt.id
JOIN loai_cay lc ON vct.loai_cay_id = lc.id
LEFT JOIN nhom_cay nc ON lc.nhom_cay_id = nc.id
LEFT JOIN giong_bao_ho gb ON vct.giong_id = gb.id;

-- View cơ sở đầy đủ
CREATE OR REPLACE VIEW v_co_so_full AS
SELECT 
    cs.id,
    cs.ma_co_so,
    cs.ten_co_so,
    cs.bien_hieu,
    lh.ten_loai AS loai_hinh,
    tcn.ten_to_chuc AS to_chuc_chu_quan,
    cs.so_giay_phep,
    cs.ngay_cap_phep,
    cs.ngay_het_han,
    cs.tinh_trang,
    x.ten_xa,
    h.ten_huyen,
    t.ten_tinh
FROM co_so cs
JOIN loai_hinh_co_so lh ON cs.loai_hinh_id = lh.id
JOIN to_chuc_ca_nhan tcn ON cs.to_chuc_id = tcn.id
LEFT JOIN xa x ON cs.xa_id = x.id
LEFT JOIN huyen h ON cs.huyen_id = h.id
LEFT JOIN tinh t ON cs.tinh_id = t.id;

-- =============================================================================
-- COMMENT
-- =============================================================================

COMMENT ON SCHEMA nongsan IS 'Hệ thống quản lý nông sản tích hợp - Thiết kế 3NF';
COMMENT ON TABLE vung_trong IS 'Vùng trồng với mã số vùng trồng (MSVT)';
COMMENT ON TABLE loai_cay IS 'Loại cây trồng (thống nhất từ nhiều nguồn)';
COMMENT ON TABLE phan_bon IS 'Phân bón được phép sử dụng';
COMMENT ON TABLE thuoc_bvtv IS 'Thuốc bảo vệ thực vật';
COMMENT ON TABLE co_so IS 'Cơ sở sản xuất kinh doanh (giống, phân bón, TBVTV, đóng gói)';
COMMENT ON TABLE lich_su_canh_tac IS 'Nhật ký đồng ruộng - lịch sử canh tác';

-- =============================================================================
-- KẾT THÚC
-- =============================================================================
