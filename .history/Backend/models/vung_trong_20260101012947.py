"""
========== Models cho Vùng Trồng (Farm Zones) ==========
File: models/vung_trong.py
Purpose: Định nghĩa SQLAlchemy ORM models cho bảng vung_trong và toa_do_vung

Module này định nghĩa:
1. VungTrong: Bảng chính chứa thông tin vùng trồng
2. ToaDoVung: Bảng tọa độ (coordinates) để vẽ polygon trên map

Database tables: nongsan.vung_trong, nongsan.toa_do_vung

Kết nối đến:
- models/to_chuc_ca_nhan.py: Relationship với ToChucCaNhan (chủ sở hữu)
- models/trang_thai.py: Relationship với TrangThaiVung (trạng thái)
- routes/farms.py: CRUD operations
- Frontend: HomeView.vue, MapComponent.vue
"""

from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class VungTrong(Base):
    """
    Model cho bảng vung_trong (Vùng Trồng)
    
    Thông tin vùng trồng nông sản:
    - Mã vùng, tên vùng, địa chỉ, diện tích
    - Liên kết: chủ sở hữu, trạng thái, hành chính (tỉnh/huyện/xã)
    - Tọa độ polygon, ảnh đại diện, QR code
    
    Database: nongsan.vung_trong
    """
    __tablename__ = "vung_trong"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== MÃ VÙNG ==========
    ma_vung = Column(String, unique=True, nullable=False, index=True)
    # Mã vùng trồng VietGAP (unique)
    # Example: "MSVT001", "MSVT002"
    
    ma_vung_puc = Column(String)
    # Mã vùng PUC (Product Use Certificate) - nếu có
    # Example: "PUC2024001"
    
    # ========== THÔNG TIN CƠ BẢN ==========
    ten_vung = Column(String, nullable=False)
    # Tên vùng trồng
    # Example: "Vườn Lúa An Lộc", "Vùng Cà Phê Đắk Lắk"
    
    dia_chi = Column(Text)
    # Địa chỉ chi tiết
    
    dien_tich = Column(Numeric)
    # Diện tích (hecta) - NOTE: DB dùng Numeric, không phải Float
    # Example: 5.5, 10.25
    
    # ========== FOREIGN KEYS ==========
    chu_so_huu_id = Column(Integer, ForeignKey("nongsan.to_chuc_ca_nhan.id"))
    # FK → to_chuc_ca_nhan.id (chủ sở hữu vùng)
    # NOTE: DB table name là "to_chuc_ca_nhan" không phải "chu_vung"
    
    trang_thai_id = Column(Integer, ForeignKey("nongsan.trang_thai_vung.id"))
    # FK → trang_thai_vung.id (trạng thái hiện tại)
    # NOTE: DB table name là "trang_thai_vung" không phải "trang_thai"
    
    trang_thai_ma_id = Column(Integer)
    # FK → trang_thai_ma_vung.id (lịch sử trạng thái mã)
    
    chung_nhan_id = Column(Integer, ForeignKey("nongsan.chung_nhan.id"))
    # FK → chung_nhan.id (chứng nhận: VietGAP, GlobalGAP, etc.)
    
    # ========== HÀNH CHÍNH ==========
    xa_id = Column(Integer, ForeignKey("nongsan.xa.id"))
    # FK → xa.id (xã/phường)
    
    huyen_id = Column(Integer, ForeignKey("nongsan.huyen.id"))
    # FK → huyen.id (quận/huyện)
    
    tinh_id = Column(Integer, ForeignKey("nongsan.tinh.id"))
    # FK → tinh.id (tỉnh/thành phố)
    
    # ========== MEDIA & QR ==========
    ma_qr = Column(String)
    # Mã QR code cho truy xuất nguồn gốc
    
    anh_dai_dien = Column(Text)
    # URL/path ảnh đại diện vùng trồng
    
    # ========== THU HOẠCH ==========
    thoi_gian_bat_dau_thu_hoach = Column(Date)
    # Ngày bắt đầu thu hoạch
    
    thoi_gian_ket_thuc_thu_hoach = Column(Date)
    # Ngày kết thúc thu hoạch
    
    # ========== TIMESTAMPS ==========
    ngay_tao = Column(TIMESTAMP, server_default=func.now())
    # Ngày tạo record (auto-set)
    
    ngay_cap_nhat = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    # Ngày cập nhật cuối (auto-update)
    
    # ========== RELATIONSHIPS ==========
    chu_so_huu = relationship("ToChucCaNhan", back_populates="vung_trong_list")
    trang_thai = relationship("TrangThaiVung", back_populates="vung_trong_list")
    toa_do = relationship("ToaDoVung", back_populates="vung_trong", cascade="all, delete-orphan")
    cay_trong = relationship("VungCayTrong", back_populates="vung_trong", cascade="all, delete-orphan")


class ToaDoVung(Base):
    """
    Model cho bảng toa_do_vung (Tọa độ Vùng Trồng)
    
    Lưu trữ các điểm tọa độ (lat, lng) để vẽ polygon ranh giới vùng trồng trên bản đồ.
    Các điểm được sắp xếp theo thứ tự để tạo thành polygon khép kín.
    
    Database: nongsan.toa_do_vung
    """
    __tablename__ = "toa_do_vung"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== FOREIGN KEY ==========
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), nullable=False)
    # FK → vung_trong.id
    # ondelete="CASCADE": Xóa vùng → xóa tất cả tọa độ
    
    # ========== COORDINATE DATA ==========
    thu_tu = Column(Integer, nullable=False)
    # Thứ tự điểm trong polygon (1, 2, 3, ...)
    # Dùng để vẽ polygon đúng thứ tự
    
    latitude = Column(Numeric, nullable=False)
    # Vĩ độ (latitude)
    # Example: 10.762622 (TP.HCM)
    
    longitude = Column(Numeric, nullable=False)
    # Kinh độ (longitude)
    # Example: 106.660172 (TP.HCM)
    
    # ========== RELATIONSHIPS ==========
    vung_trong = relationship("VungTrong", back_populates="toa_do")
