-- ========================================
-- DATABASE VIEWS CHO FRONTEND
-- Purpose: Tổng hợp data từ nhiều bảng, Frontend chỉ cần query views
-- Date: 2026-01-11
-- ========================================

-- ========== VIEW 1: Danh sách Vùng Trồng với Thông tin Đầy đủ ==========
-- Mix data từ: vung_trong, to_chuc, loai_cay_trong, tinh_thanh_pho, toa_do_vung
DROP VIEW IF EXISTS nongsan.v_vung_trong_full CASCADE;
CREATE VIEW nongsan.v_vung_trong_full AS
SELECT 
    vt.id,
    vt.ma_vung,
    vt.ten_vung,
    vt.dia_chi,
    vt.dien_tich,
    vt.ngay_tao,
    vt.ngay_cap_nhat,
    
    -- Thông tin chủ sở hữu
    tc.id as chu_so_huu_id,
    tc.ten_to_chuc as chu_so_huu,
    tc.dia_chi as dia_chi_chu_so_huu,
    tc.so_dien_thoai as sdt_chu_so_huu,
    tc.email as email_chu_so_huu,
    
    -- Thông tin cây trồng
    lct.id as loai_cay_id,
    lct.ten_loai as loai_cay,
    lct.ten_khoa_hoc as ten_khoa_hoc_cay,
    
    -- Địa điểm
    ttp.id as tinh_id,
    ttp.ten_tinh,
    qh.id as huyen_id,
    qh.ten_quan_huyen,
    pxa.id as xa_id,
    pxa.ten_phuong_xa,
    
    -- Tọa độ (lấy centroid từ polygon nếu có)
    CASE 
        WHEN COUNT(tdv.id) > 0 THEN ST_Y(ST_Centroid(ST_Collect(tdv.toa_do)))
        ELSE NULL 
    END as latitude,
    CASE 
        WHEN COUNT(tdv.id) > 0 THEN ST_X(ST_Centroid(ST_Collect(tdv.toa_do)))
        ELSE NULL 
    END as longitude,
    
    -- Số lượng tọa độ polygon
    COUNT(tdv.id) as so_diem_toa_do,
    
    -- Trạng thái (computed)
    CASE 
        WHEN EXISTS (
            SELECT 1 FROM nongsan.lich_su_canh_tac lsct 
            WHERE lsct.vung_trong_id = vt.id 
            AND lsct.ngay_thuc_hien >= CURRENT_DATE - INTERVAL '30 days'
        ) THEN 'active'
        ELSE 'inactive'
    END as trang_thai,
    
    -- Số hoạt động gần đây (30 ngày)
    (SELECT COUNT(*) 
     FROM nongsan.lich_su_canh_tac lsct 
     WHERE lsct.vung_trong_id = vt.id 
     AND lsct.ngay_thuc_hien >= CURRENT_DATE - INTERVAL '30 days'
    ) as so_hoat_dong_gan_day

FROM nongsan.vung_trong vt
LEFT JOIN nongsan.to_chuc tc ON vt.chu_so_huu_id = tc.id
LEFT JOIN nongsan.loai_cay_trong lct ON vt.loai_cay_trong_id = lct.id
LEFT JOIN nongsan.phuong_xa pxa ON vt.phuong_xa_id = pxa.id
LEFT JOIN nongsan.quan_huyen qh ON pxa.quan_huyen_id = qh.id
LEFT JOIN nongsan.tinh_thanh_pho ttp ON qh.tinh_thanh_pho_id = ttp.id
LEFT JOIN nongsan.toa_do_vung tdv ON vt.id = tdv.vung_trong_id
GROUP BY 
    vt.id, vt.ma_vung, vt.ten_vung, vt.dia_chi, vt.dien_tich, vt.ngay_tao, vt.ngay_cap_nhat,
    tc.id, tc.ten_to_chuc, tc.dia_chi, tc.so_dien_thoai, tc.email,
    lct.id, lct.ten_loai, lct.ten_khoa_hoc,
    ttp.id, ttp.ten_tinh, qh.id, qh.ten_quan_huyen, pxa.id, pxa.ten_phuong_xa;

COMMENT ON VIEW nongsan.v_vung_trong_full IS 'View tổng hợp thông tin vùng trồng với tọa độ, chủ sở hữu, cây trồng, địa điểm';


-- ========== VIEW 2: Lịch Sử Canh Tác với Thông tin Chi tiết ==========
DROP VIEW IF EXISTS nongsan.v_lich_su_canh_tac_full CASCADE;
CREATE VIEW nongsan.v_lich_su_canh_tac_full AS
SELECT 
    lsct.id,
    lsct.ngay_thuc_hien,
    lsct.tieu_de,
    lsct.noi_dung,
    lsct.nguoi_thuc_hien,
    lsct.thua_ruong,
    lsct.ghi_chu,
    lsct.ngay_tao,
    lsct.ngay_cap_nhat,
    
    -- Vùng trồng
    vt.id as vung_trong_id,
    vt.ma_vung,
    vt.ten_vung,
    vt.dia_chi as dia_chi_vung,
    
    -- Loại hoạt động
    lhd.id as loai_hoat_dong_id,
    lhd.ma_loai as ma_loai_hoat_dong,
    lhd.ten_loai as ten_loai_hoat_dong,
    lhd.icon as icon_hoat_dong,
    
    -- Phân bón (nếu có)
    pb.id as phan_bon_id,
    pb.ten_phan_bon,
    lsct.lieu_luong_phan_bon,
    
    -- Thuốc BVTV (nếu có)
    tb.id as thuoc_bvtv_id,
    tb.ten_thuoc,
    lsct.lieu_luong_thuoc,
    
    -- Chủ sở hữu vùng
    tc.ten_to_chuc as chu_so_huu
    
FROM nongsan.lich_su_canh_tac lsct
INNER JOIN nongsan.vung_trong vt ON lsct.vung_trong_id = vt.id
LEFT JOIN nongsan.loai_hoat_dong lhd ON lsct.loai_hoat_dong_id = lhd.id
LEFT JOIN nongsan.phan_bon pb ON lsct.phan_bon_id = pb.id
LEFT JOIN nongsan.thuoc_bvtv tb ON lsct.thuoc_bvtv_id = tb.id
LEFT JOIN nongsan.to_chuc tc ON vt.chu_so_huu_id = tc.id
ORDER BY lsct.ngay_thuc_hien DESC, lsct.id DESC;

COMMENT ON VIEW nongsan.v_lich_su_canh_tac_full IS 'View nhật ký canh tác với thông tin vùng, loại hoạt động, vật tư';


-- ========== VIEW 3: Dashboard Statistics ==========
DROP VIEW IF EXISTS nongsan.v_dashboard_stats CASCADE;
CREATE VIEW nongsan.v_dashboard_stats AS
SELECT 
    (SELECT COUNT(*) FROM nongsan.vung_trong) as total_farms,
    (SELECT COUNT(*) FROM nongsan.vung_trong vt
     WHERE EXISTS (
        SELECT 1 FROM nongsan.lich_su_canh_tac lsct 
        WHERE lsct.vung_trong_id = vt.id 
        AND lsct.ngay_thuc_hien >= CURRENT_DATE - INTERVAL '30 days'
     )) as active_farms,
    (SELECT COALESCE(SUM(CAST(dien_tich AS DECIMAL)), 0) FROM nongsan.vung_trong) as total_area,
    (SELECT COUNT(*) FROM nongsan.lich_su_canh_tac) as total_activities,
    (SELECT COUNT(*) FROM nongsan.lich_su_canh_tac 
     WHERE ngay_thuc_hien >= CURRENT_DATE - INTERVAL '30 days') as activities_last_30_days,
    (SELECT COUNT(DISTINCT vung_trong_id) FROM nongsan.lich_su_canh_tac) as farms_with_activities;

COMMENT ON VIEW nongsan.v_dashboard_stats IS 'View thống kê tổng quan cho dashboard';


-- ========== VIEW 4: QR Traceability Info ==========
DROP VIEW IF EXISTS nongsan.v_qr_traceability CASCADE;
CREATE VIEW nongsan.v_qr_traceability AS
SELECT 
    vt.ma_vung as qr_code,
    vt.ten_vung,
    vt.dia_chi,
    vt.dien_tich,
    
    -- Chủ sở hữu
    tc.ten_to_chuc as chu_so_huu,
    tc.so_dien_thoai as sdt_lien_he,
    tc.email,
    
    -- Cây trồng
    lct.ten_loai as loai_cay,
    
    -- Địa điểm
    ttp.ten_tinh || ', ' || qh.ten_quan_huyen || ', ' || pxa.ten_phuong_xa as dia_diem_day_du,
    
    -- Số hoạt động
    (SELECT COUNT(*) FROM nongsan.lich_su_canh_tac lsct 
     WHERE lsct.vung_trong_id = vt.id) as tong_hoat_dong,
     
    -- Hoạt động gần nhất
    (SELECT MAX(ngay_thuc_hien) FROM nongsan.lich_su_canh_tac lsct 
     WHERE lsct.vung_trong_id = vt.id) as hoat_dong_gan_nhat,
     
    -- Lịch sử canh tác (JSON array)
    (SELECT json_agg(
        json_build_object(
            'ngay', lsct.ngay_thuc_hien,
            'hoat_dong', lhd.ten_loai,
            'noi_dung', lsct.noi_dung,
            'nguoi_thuc_hien', lsct.nguoi_thuc_hien
        ) ORDER BY lsct.ngay_thuc_hien DESC
    )
    FROM nongsan.lich_su_canh_tac lsct
    LEFT JOIN nongsan.loai_hoat_dong lhd ON lsct.loai_hoat_dong_id = lhd.id
    WHERE lsct.vung_trong_id = vt.id
    LIMIT 10
    ) as lich_su_json
    
FROM nongsan.vung_trong vt
LEFT JOIN nongsan.to_chuc tc ON vt.chu_so_huu_id = tc.id
LEFT JOIN nongsan.loai_cay_trong lct ON vt.loai_cay_trong_id = lct.id
LEFT JOIN nongsan.phuong_xa pxa ON vt.phuong_xa_id = pxa.id
LEFT JOIN nongsan.quan_huyen qh ON pxa.quan_huyen_id = qh.id
LEFT JOIN nongsan.tinh_thanh_pho ttp ON qh.tinh_thanh_pho_id = ttp.id;

COMMENT ON VIEW nongsan.v_qr_traceability IS 'View thông tin truy xuất nguồn gốc qua QR code';


-- ========== GRANT PERMISSIONS ==========
GRANT SELECT ON nongsan.v_vung_trong_full TO PUBLIC;
GRANT SELECT ON nongsan.v_lich_su_canh_tac_full TO PUBLIC;
GRANT SELECT ON nongsan.v_dashboard_stats TO PUBLIC;
GRANT SELECT ON nongsan.v_qr_traceability TO PUBLIC;

-- ========== SUCCESS MESSAGE ==========
DO $$
BEGIN
    RAISE NOTICE '✅ Successfully created 4 database views:';
    RAISE NOTICE '  1. v_vung_trong_full - Danh sách vùng trồng đầy đủ';
    RAISE NOTICE '  2. v_lich_su_canh_tac_full - Lịch sử canh tác chi tiết';
    RAISE NOTICE '  3. v_dashboard_stats - Thống kê dashboard';
    RAISE NOTICE '  4. v_qr_traceability - Thông tin QR traceability';
END $$;
