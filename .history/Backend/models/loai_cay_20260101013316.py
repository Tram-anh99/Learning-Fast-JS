"""
========== Models cho Loại Cây (Crop Types) và Vùng Cây Trồng ==========
File: models/loai_cay.py
Purpose: Định nghĩa SQLAlchemy ORM models cho loại cây và relationship với vùng trồng

Module này định nghĩa:
1. LoaiCay: Danh mục các loại cây trồng (Lúa, Cà phê, Tiêu, ...)
2. VungCayTrong: Bảng trung gian (junction table) cho many-to-many relationship
   giữa Vùng Trồng và Loại Cây

Relationship: VungTrong <--> VungCayTrong <--> LoaiCay (N-N)
Một vùng trồng có thể trồng nhiều loại cây
Một loại cây có thể được trồng ở nhiều vùng

Database tables:
- nongsan.loai_cay
- nongsan.vung_cay_trong

Kết nối đến:
- models/vung_trong.py: VungTrong.cay_trong relationship
- routes/crops.py: CRUD operations cho loại cây
- Frontend: Product selection, crop management
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class LoaiCay(Base):
    """
    SQLAlchemy Model cho bảng loai_cay (Loại Cây Trồng)
    
    Danh mục các loại cây trồng:
    - Thông tin cơ bản: mã cây, tên cây, tên khoa học
    - Mô tả đặc điểm cây
    - Master data (ít thay đổi)
    
    Example records:
    - Lúa (Oryza sativa)
    - Cà phê (Coffea)
    - Tiêu (Piper nigrum)
    
    Database: nongsan.loai_cay
    """
    __tablename__ = "loai_cay"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== CROP INFORMATION ==========
    ma_cay = Column(String(50), unique=True, nullable=False, index=True)
    # - Mã loại cây (unique code)
    # Example: "LUA01", "CAPHE01", "TIEU01"
    
    ten_cay = Column(String(255), nullable=False)
    # - Tên loại cây (Vietnamese name)
    # Example: "Lúa", "Cà phê Robusta", "Tiêu đen"
    
    ten_khoa_hoc = Column(String(255))
    # - Tên khoa học (Scientific name - Latin)
    # Example: "Oryza sativa", "Coffea canephora"
    
    mo_ta = Column(Text)
    # - Mô tả đặc điểm, công dụng, cách trồng
    # Example: "Cây lương thực chính, chu kỳ 3-4 tháng"
    
    # ========== TIMESTAMPS ==========
    ngay_tao = Column(TIMESTAMP, server_default=func.now())
    
    # ========== RELATIONSHIPS ==========
    vung_cay_trong = relationship("VungCayTrong", back_populates="loai_cay")
    # - Relationship với VungCayTrong (one-to-many)
    # - Usage: loai_cay.vung_cay_trong → list tất cả vùng trồng loại cây này


class VungCayTrong(Base):
    """
    SQLAlchemy Model cho bảng vung_cay_trong (Junction Table)
    
    Bảng trung gian (bridge table) cho many-to-many relationship:
    VungTrong <--N-N--> LoaiCay
    
    Thông tin chi tiết về việc trồng cây trong vùng:
    - Diện tích trồng (hecta)
    - Sản lượng dự kiến (tấn)
    - Năm bắt đầu trồng
    
    Example:
    - Vùng A (5ha) trồng Lúa (2ha, 4 tấn/vụ, từ 2020)
    - Vùng A (5ha) trồng Cà phê (3ha, 6 tấn/năm, từ 2018)
    
    Database: nongsan.vung_cay_trong
    """
    __tablename__ = "vung_cay_trong"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== FOREIGN KEYS (Junction) ==========
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), nullable=False)
    # - FK đến vung_trong.id
    # - ondelete="CASCADE": Xóa vùng → xóa tất cả records này
    # - nullable=False: Bắt buộc phải có vùng trồng
    
    loai_cay_id = Column(Integer, ForeignKey("nongsan.loai_cay.id", ondelete="CASCADE"), nullable=False)
    # - FK đến loai_cay.id
    # - ondelete="CASCADE": Xóa loại cây → xóa tất cả records này
    # - nullable=False: Bắt buộc phải có loại cây
    
    # ========== CROP DETAILS ==========
    dien_tich_ha = Column(Float)
    # - Diện tích trồng loại cây này trong vùng (hecta)
    # - nullable=True: Có thể chưa có dữ liệu
    # Example: 2.5 (2.5 hecta)
    # Note: Sum(dien_tich_ha) <= vung_trong.dien_tich_ha
    
    san_luong_du_kien = Column(Float)
    # - Sản lượng dự kiến (tấn/vụ hoặc tấn/năm)
    # Example: 4.5 (4.5 tấn)
    # Usage: Tính toán cho planning, forecasting
    
    nam_trong = Column(Integer)
    # - Năm bắt đầu trồng loại cây này
    # Example: 2020
    # Usage: Tính tuổi cây, chu kỳ thu hoạch
    
    # ========== TIMESTAMPS ==========
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # ========== RELATIONSHIPS ==========
    vung_trong = relationship("VungTrong", back_populates="cay_trong")
    # - Relationship với VungTrong (many-to-one)
    # - Usage: record.vung_trong.ten_vung → get tên vùng
    
    loai_cay = relationship("LoaiCay", back_populates="vung_cay_trong")
    # - Relationship với LoaiCay (many-to-one)
    # - Usage: record.loai_cay.ten_cay → get tên cây
    
    # thi_truong = relationship("CayThiTruong", back_populates="vung_cay_trong", cascade="all, delete-orphan")
    # - Relationship với CayThiTruong (one-to-many)
    # - Tracking thông tin xuất khẩu, thị trường cho cây trồng này
    # - cascade: Xóa vung_cay_trong → xóa tất cả thị trường liên quan
