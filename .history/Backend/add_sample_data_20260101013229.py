"""
Script để thêm dữ liệu mẫu vào database
Chạy: python add_sample_data.py
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import (
    VungTrong, ToaDoVung, LoaiCay, 
    ToChucCaNhan, TrangThaiVung,
    LichSuCanhTac, LoaiHoatDong
)
from datetime import date, datetime


def add_sample_data():
    """
    Thêm dữ liệu mẫu vào database
    """
    db = SessionLocal()
    
    try:
        print("🚀 Bắt đầu thêm dữ liệu mẫu...")
        
        # ========== 1. TRẠNG THÁI VÙNG (Master Data) ==========
        print("\n📋 1. Kiểm tra Trạng Thái Vùng...")
        trang_thai_count = db.query(TrangThaiVung).count()
        if trang_thai_count == 0:
            print("   ⏳ Thêm trạng thái...")
            trang_thai_list = [
                TrangThaiVung(
                    ma_trang_thai="HOAT_DONG",
                    ten_trang_thai="Đang hoạt động",
                    mau_sac="#4CAF50",
                    css_class="badge-success",
                    mo_ta="Vùng đang hoạt động bình thường"
                ),
                TrangThaiVung(
                    ma_trang_thai="TAM_NGUNG",
                    ten_trang_thai="Tạm ngưng",
                    mau_sac="#FF9800",
                    css_class="badge-warning",
                    mo_ta="Vùng tạm ngưng hoạt động"
                ),
                TrangThaiVung(
                    ma_trang_thai="HET_HAN",
                    ten_trang_thai="Hết hạn",
                    mau_sac="#F44336",
                    css_class="badge-danger",
                    mo_ta="Vùng đã hết hạn chứng nhận"
                ),
                TrangThaiVung(
                    ma_trang_thai="CHO_CAP_PHEP",
                    ten_trang_thai="Chờ cấp phép",
                    mau_sac="#2196F3",
                    css_class="badge-info",
                    mo_ta="Vùng đang chờ cấp phép"
                ),
            ]
            db.add_all(trang_thai_list)
            db.commit()
            print(f"   ✅ Đã thêm {len(trang_thai_list)} trạng thái")
        else:
            print(f"   ✅ Đã có {trang_thai_count} trạng thái")
        
        # Get trạng thái để dùng sau
        trang_thai_hoat_dong = db.query(TrangThaiVung).filter_by(ma_trang_thai="HOAT_DONG").first()
        
        # ========== 2. LOẠI CÂY (Master Data) ==========
        print("\n🌱 2. Kiểm tra Loại Cây...")
        loai_cay_count = db.query(LoaiCay).count()
        if loai_cay_count == 0:
            print("   ⏳ Thêm loại cây...")
            loai_cay_list = [
                LoaiCay(ma_cay="LUA01", ten_cay="Lúa", ten_khoa_hoc="Oryza sativa", mo_ta="Cây lương thực chính"),
                LoaiCay(ma_cay="CAPHE01", ten_cay="Cà phê Robusta", ten_khoa_hoc="Coffea canephora", mo_ta="Cà phê chất lượng cao"),
                LoaiCay(ma_cay="TIEU01", ten_cay="Tiêu đen", ten_khoa_hoc="Piper nigrum", mo_ta="Gia vị xuất khẩu"),
                LoaiCay(ma_cay="XOAI01", ten_cay="Xoài", ten_khoa_hoc="Mangifera indica", mo_ta="Trái cây nhiệt đới"),
                LoaiCay(ma_cay="CAU01", ten_cay="Cau", ten_khoa_hoc="Areca catechu", mo_ta="Cây công nghiệp"),
            ]
            db.add_all(loai_cay_list)
            db.commit()
            print(f"   ✅ Đã thêm {len(loai_cay_list)} loại cây")
        else:
            print(f"   ✅ Đã có {loai_cay_count} loại cây")
        
        # ========== 3. TỔ CHỨC/CÁ NHÂN ==========
        print("\n👥 3. Thêm Tổ Chức/Cá Nhân...")
        to_chuc_count = db.query(ToChucCaNhan).count()
        if to_chuc_count == 0:
            to_chuc_list = [
                ToChucCaNhan(
                    ma_to_chuc="TC001",
                    ten_to_chuc="Công ty TNHH Nông Sản Xanh",
                    loai_to_chuc="cong_ty",
                    nguoi_dai_dien="Ông Nguyễn Văn A",
                    dien_thoai="0909123456",
                    email="contact@nongsanxanh.vn",
                    dia_chi="123 Đường ABC, Quận 1",
                    trang_thai="hoat_dong"
                ),
                ToChucCaNhan(
                    ma_to_chuc="CN001",
                    ten_to_chuc="Trần Thị Bình",
                    loai_to_chuc="ca_nhan",
                    nguoi_dai_dien="Trần Thị Bình",
                    dien_thoai="0912345678",
                    email="ttbinh@gmail.com",
                    dia_chi="45 Xã An Lộc, Huyện Cần Giuộc",
                    trang_thai="hoat_dong"
                ),
                ToChucCaNhan(
                    ma_to_chuc="HTX001",
                    ten_to_chuc="Hợp tác xã Nông nghiệp Đắk Lắk",
                    loai_to_chuc="hop_tac_xa",
                    nguoi_dai_dien="Ông Lê Văn C",
                    dien_thoai="0987654321",
                    email="htx@daklak.vn",
                    dia_chi="Xã Ea Kao, Huyện Buôn Ma Thuột",
                    trang_thai="hoat_dong"
                ),
            ]
            db.add_all(to_chuc_list)
            db.commit()
            print(f"   ✅ Đã thêm {len(to_chuc_list)} tổ chức/cá nhân")
        else:
            print(f"   ✅ Đã có {to_chuc_count} tổ chức/cá nhân")
        
        # Get tổ chức để dùng sau
        chu_so_huu_1 = db.query(ToChucCaNhan).filter_by(ma_to_chuc="TC001").first()
        chu_so_huu_2 = db.query(ToChucCaNhan).filter_by(ma_to_chuc="CN001").first()
        chu_so_huu_3 = db.query(ToChucCaNhan).filter_by(ma_to_chuc="HTX001").first()
        
        # ========== 4. VÙNG TRỒNG ==========
        print("\n🌾 4. Thêm Vùng Trồng...")
        vung_trong_count = db.query(VungTrong).count()
        if vung_trong_count == 0:
            vung_trong_list = [
                VungTrong(
                    ma_vung="MSVT001",
                    ten_vung="Vùng Lúa An Lộc 1",
                    dia_chi="Xã An Lộc, Huyện Cần Giuộc, Long An",
                    dien_tich=5.5,
                    chu_so_huu_id=chu_so_huu_1.id if chu_so_huu_1 else None,
                    trang_thai_id=trang_thai_hoat_dong.id if trang_thai_hoat_dong else None,
                    ma_qr="QR001",
                    thoi_gian_bat_dau_thu_hoach=date(2026, 3, 15),
                    thoi_gian_ket_thuc_thu_hoach=date(2026, 4, 30),
                ),
                VungTrong(
                    ma_vung="MSVT002",
                    ten_vung="Vùng Cà Phê Đắk Lắk",
                    dia_chi="Xã Ea Kao, Huyện Buôn Ma Thuột, Đắk Lắk",
                    dien_tich=12.3,
                    chu_so_huu_id=chu_so_huu_3.id if chu_so_huu_3 else None,
                    trang_thai_id=trang_thai_hoat_dong.id if trang_thai_hoat_dong else None,
                    ma_qr="QR002",
                    thoi_gian_bat_dau_thu_hoach=date(2026, 2, 1),
                    thoi_gian_ket_thuc_thu_hoach=date(2026, 5, 31),
                ),
                VungTrong(
                    ma_vung="MSVT003",
                    ten_vung="Vườn Tiêu Gia Lai",
                    dia_chi="Xã Ia Kha, Huyện Ia Grai, Gia Lai",
                    dien_tich=8.7,
                    chu_so_huu_id=chu_so_huu_2.id if chu_so_huu_2 else None,
                    trang_thai_id=trang_thai_hoat_dong.id if trang_thai_hoat_dong else None,
                    ma_qr="QR003",
                    thoi_gian_bat_dau_thu_hoach=date(2026, 6, 1),
                    thoi_gian_ket_thuc_thu_hoach=date(2026, 8, 15),
                ),
            ]
            db.add_all(vung_trong_list)
            db.commit()
            print(f"   ✅ Đã thêm {len(vung_trong_list)} vùng trồng")
            
            # Refresh để lấy ID
            for vung in vung_trong_list:
                db.refresh(vung)
            
            # ========== 5. TỌA ĐỘ VÙNG (Polygons) ==========
            print("\n📍 5. Thêm tọa độ vùng...")
            toa_do_list = [
                # Vùng 1: Polygon nhỏ ở Long An
                ToaDoVung(vung_trong_id=vung_trong_list[0].id, thu_tu=1, latitude=10.5234, longitude=106.4567),
                ToaDoVung(vung_trong_id=vung_trong_list[0].id, thu_tu=2, latitude=10.5245, longitude=106.4589),
                ToaDoVung(vung_trong_id=vung_trong_list[0].id, thu_tu=3, latitude=10.5221, longitude=106.4601),
                ToaDoVung(vung_trong_id=vung_trong_list[0].id, thu_tu=4, latitude=10.5210, longitude=106.4579),
                
                # Vùng 2: Polygon ở Đắk Lắk
                ToaDoVung(vung_trong_id=vung_trong_list[1].id, thu_tu=1, latitude=12.6667, longitude=108.0500),
                ToaDoVung(vung_trong_id=vung_trong_list[1].id, thu_tu=2, latitude=12.6689, longitude=108.0534),
                ToaDoVung(vung_trong_id=vung_trong_list[1].id, thu_tu=3, latitude=12.6656, longitude=108.0567),
                ToaDoVung(vung_trong_id=vung_trong_list[1].id, thu_tu=4, latitude=12.6634, longitude=108.0523),
                
                # Vùng 3: Polygon ở Gia Lai
                ToaDoVung(vung_trong_id=vung_trong_list[2].id, thu_tu=1, latitude=13.9787, longitude=108.0045),
                ToaDoVung(vung_trong_id=vung_trong_list[2].id, thu_tu=2, latitude=13.9801, longitude=108.0078),
                ToaDoVung(vung_trong_id=vung_trong_list[2].id, thu_tu=3, latitude=13.9776, longitude=108.0089),
                ToaDoVung(vung_trong_id=vung_trong_list[2].id, thu_tu=4, latitude=13.9765, longitude=108.0056),
            ]
            db.add_all(toa_do_list)
            db.commit()
            print(f"   ✅ Đã thêm {len(toa_do_list)} tọa độ")
        else:
            print(f"   ✅ Đã có {vung_trong_count} vùng trồng")
        
        # ========== TỔNG KẾT ==========
        print("\n" + "="*50)
        print("📊 TỔNG KẾT DỮ LIỆU:")
        print(f"   - Trạng thái vùng: {db.query(TrangThaiVung).count()}")
        print(f"   - Loại cây: {db.query(LoaiCay).count()}")
        print(f"   - Tổ chức/Cá nhân: {db.query(ToChucCaNhan).count()}")
        print(f"   - Vùng trồng: {db.query(VungTrong).count()}")
        print(f"   - Tọa độ vùng: {db.query(ToaDoVung).count()}")
        print("="*50)
        print("✅ HOÀN TẤT!")
        
    except Exception as e:
        print(f"❌ LỖI: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    add_sample_data()
