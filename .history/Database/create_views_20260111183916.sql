/*
========== DATABASE VIEWS CHO FRONTEND ==========
Purpose: Tạo views kết hợp nhiều bảng để Frontend query dễ dàng
Date: 2026-01-11
*/

-- ========== VIEW 1: VÙNG TRỒNG CHI TIẾT ==========
-- Kết hợp: vung_trong + loai_cay_trong + toa_do_vung + lich_su_canh_tac
CREATE OR REPLACE VIEW nongsan.v_vung_trong_chi_tiet AS
SELECT 
    vt.id,
    vt.ma_vung,
    vt.ten_vung,
    vt.loai_cay_trong_id,
    lct.ten_cay AS ten_cay_trong,
    lct.ten_khoa_hoc,
    vt.dien_tich,
    vt.san_luong_du_kien,
    vt.ngay_gieo_trong,
    vt.ngay_thu_hoach_du_kien,
    vt.trang_thai,
    vt.ghi_chu,
    vt.ma_global_gap,
    vt.ma_vietgap,
    vt.ngay_cap_chung_nhan,
    vt.ngay_het_han_chung_nhan,
    -- Tọa độ vùng (JSON array)
    COALESCE(
        (SELECT json_agg(json_build_object(
            'lat', tdv.위도,
            'lng', tdv.경도,
            'thu_tu', tdv.thu_tu_diem
        ) ORDER BY tdv.thu_tu_diem)
        FROM nongsan.toa_do_vung tdv 
        WHERE tdv.vung_trong_id = vt.id),
        '[]'::json
    ) AS toa_do,
    -- Thống kê hoạt động
    (SELECT COUNT(*) 
     FROM nongsan.lich_su_canh_tac lsct 
     WHERE lsct.vung_trong_id = vt.id) AS tong_hoat_dong,
    -- Hoạt động gần nhất
    (SELECT MAX(lsct.ngay_thuc_hien) 
     FROM nongsan.lich_su_canh_tac lsct 
     WHERE lsct.vung_trong_id = vt.id) AS hoat_dong_gan_nhat,
    -- Timestamps
    vt.ngay_tao,
    vt.ngay_cap_nhat
FROM nongsan.vung_trong vt
LEFT JOIN nongsan.loai_cay_trong lct ON vt.loai_cay_trong_id = lct.id
WHERE vt.deleted_at IS NULL;

COMMENT ON VIEW nongsan.v_vung_trong_chi_tiet IS 
'View tổng hợp thông tin vùng trồng với tọa độ, thống kê hoạt động. Dùng cho Frontend HomeView, QuanLyView';


-- ========== VIEW 2: LỊCH SỬ CANH TÁC CHI TIẾT ==========  
-- Kết hợp: lich_su_canh_tac + vung_trong + loai_hoat_dong + phan_bon + thuoc_bvtv
CREATE OR REPLACE VIEW nongsan.v_lich_su_canh_tac_chi_tiet AS
SELECT 
    lsct.id,
    lsct.vung_trong_id,
    vt.ma_vung,
    vt.ten_vung,
    lsct.loai_hoat_dong_id,
    lhd.ten_loai AS ten_hoat_dong,
    lhd.ma_loai AS ma_hoat_dong,
    lhd.icon AS icon_hoat_dong,
    lsct.ngay_thuc_hien,
    lsct.tieu_de,
    lsct.noi_dung,
    lsct.nguoi_thuc_hien,
    lsct.thua_ruong,
    -- Phân bón
    lsct.phan_bon_id,
    pb.ten_phan_bon,
    pb.loai_phan_bon,
    lsct.lieu_luong_phan_bon,
    -- Thuốc BVTV
    lsct.thuoc_bvtv_id,
    tb.ten_thuoc,
    tb.hoat_chat,
    lsct.lieu_luong_thuoc,
    -- Ghi chú
    lsct.ghi_chu,
    -- Timestamps
    lsct.ngay_tao,
    lsct.ngay_cap_nhat
FROM nongsan.lich_su_canh_tac lsct
LEFT JOIN nongsan.vung_trong vt ON lsct.vung_trong_id = vt.id
LEFT JOIN nongsan.loai_hoat_dong lhd ON lsct.loai_hoat_dong_id = lhd.id
LEFT JOIN nongsan.phan_bon pb ON lsct.phan_bon_id = pb.id
LEFT JOIN nongsan.thuoc_bvtv tb ON lsct.thuoc_bvtv_id = tb.id;

COMMENT ON VIEW nongsan.v_lich_su_canh_tac_chi_tiet IS 
'View tổng hợp lịch sử canh tác với vùng trồng, loại hoạt động, phân bón, thuốc. Dùng cho DiaryPage';


-- ========== VIEW 3: THỐNG KÊ DASHBOARD ==========
-- Tổng hợp số liệu cho dashboard
CREATE OR REPLACE VIEW nongsan.v_thong_ke_dashboard AS
SELECT 
    -- Tổng số vùng
    (SELECT COUNT(*) FROM nongsan.vung_trong WHERE deleted_at IS NULL) AS tong_vung,
    -- Vùng hoạt động
    (SELECT COUNT(*) FROM nongsan.vung_trong 
     WHERE trang_thai = 'active' AND deleted_at IS NULL) AS vung_hoat_dong,
    -- Tổng diện tích
    (SELECT COALESCE(SUM(dien_tich), 0) FROM nongsan.vung_trong 
     WHERE deleted_at IS NULL) AS tong_dien_tich,
    -- Tổng hoạt động
    (SELECT COUNT(*) FROM nongsan.lich_su_canh_tac) AS tong_hoat_dong,
    -- Hoạt động tháng này
    (SELECT COUNT(*) FROM nongsan.lich_su_canh_tac 
     WHERE ngay_thuc_hien >= date_trunc('month', CURRENT_DATE)) AS hoat_dong_thang_nay,
    -- Sản lượng dự kiến
    (SELECT COALESCE(SUM(san_luong_du_kien), 0) FROM nongsan.vung_trong 
     WHERE deleted_at IS NULL) AS san_luong_du_kien_tong;

COMMENT ON VIEW nongsan.v_thong_ke_dashboard IS 
'View thống kê tổng quan cho Dashboard. Dùng cho QuanLyView, StatsBarComponent';


-- ========== VIEW 4: TRACEABILITY (TRUY XUẤT NGUỒN GỐC) ==========
-- Thông tin đầy đủ cho QR code traceability
CREATE OR REPLACE VIEW nongsan.v_traceability AS
SELECT 
    vt.id,
    vt.ma_vung,
    vt.ten_vung,
    lct.ten_cay AS ten_cay_trong,
    vt.dien_tich,
    vt.ngay_gieo_trong,
    vt.ngay_thu_hoach_du_kien,
    vt.ma_global_gap,
    vt.ma_vietgap,
    vt.ngay_cap_chung_nhan,
    vt.ngay_het_han_chung_nhan,
    -- Lịch sử hoạt động (JSON array)
    COALESCE(
        (SELECT json_agg(json_build_object(
            'ngay', lsct.ngay_thuc_hien,
            'hoat_dong', lhd.ten_loai,
            'noi_dung', lsct.noi_dung,
            'nguoi_thuc_hien', lsct.nguoi_thuc_hien
        ) ORDER BY lsct.ngay_thuc_hien DESC)
        FROM nongsan.lich_su_canh_tac lsct
        LEFT JOIN nongsan.loai_hoat_dong lhd ON lsct.loai_hoat_dong_id = lhd.id
        WHERE lsct.vung_trong_id = vt.id
        LIMIT 20),
        '[]'::json
    ) AS lich_su_hoat_dong,
    -- Tọa độ
    (SELECT json_agg(json_build_object(
        'lat', tdv.위도,
        'lng', tdv.경도
    ) ORDER BY tdv.thu_tu_diem)
    FROM nongsan.toa_do_vung tdv 
    WHERE tdv.vung_trong_id = vt.id) AS toa_do
FROM nongsan.vung_trong vt
LEFT JOIN nongsan.loai_cay_trong lct ON vt.loai_cay_trong_id = lct.id
WHERE vt.deleted_at IS NULL;

COMMENT ON VIEW nongsan.v_traceability IS 
'View truy xuất nguồn gốc đầy đủ cho QR code. Dùng cho TraceabilityPage';


-- ========== GRANT PERMISSIONS ==========
-- Cho phép Backend user query các views
GRANT SELECT ON nongsan.v_vung_trong_chi_tiet TO postgres;
GRANT SELECT ON nongsan.v_lich_su_canh_tac_chi_tiet TO postgres;
GRANT SELECT ON nongsan.v_thong_ke_dashboard TO postgres;
GRANT SELECT ON nongsan.v_traceability TO postgres;

-- ========== TEST VIEWS ==========
SELECT 'View v_vung_trong_chi_tiet:' AS info, COUNT(*) AS count FROM nongsan.v_vung_trong_chi_tiet
UNION ALL
SELECT 'View v_lich_su_canh_tac_chi_tiet:', COUNT(*) FROM nongsan.v_lich_su_canh_tac_chi_tiet
UNION ALL
SELECT 'View v_thong_ke_dashboard:', 1 FROM nongsan.v_thong_ke_dashboard
UNION ALL
SELECT 'View v_traceability:', COUNT(*) FROM nongsan.v_traceability;
