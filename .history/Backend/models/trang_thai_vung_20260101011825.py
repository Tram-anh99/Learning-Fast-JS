"""
========== Models cho Trạng Thái Vùng (Farm Status) ==========
File: models/trang_thai_vung.py  
Purpose: Quản lý trạng thái vùng trồng

Database: nongsan.trang_thai_vung, nongsan.trang_thai_ma_vung
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class TrangThaiVung(Base):
    """
    Model cho bảng trang_thai_vung (Trạng Thái Vùng)
    
    Danh mục trạng thái:
    - Hoạt động
    - Tạm ngưng
    - Hết hạn
    - Chờ cấp phép
    
    Database: nongsan.trang_thai_vung
    """
    __tablename__ = "trang_thai_vung"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== THÔNG TIN TRẠNG THÁI ==========
    ma_trang_thai = Column(String, unique=True, nullable=False, index=True)
    # Mã trạng thái (unique)
    # Example: "HOAT_DONG", "TAM_NGUNG"
    
    ten_trang_thai = Column(String, nullable=False)
    # Tên trạng thái hiển thị
    # Example: "Đang hoạt động", "Tạm ngưng"
    
    mau_sac = Column(String)
    # Màu sắc hiển thị (HEX code)
    # Example: "#4CAF50", "#FF9800"
    
    css_class = Column(String)
    # CSS class cho styling
    # Example: "badge-success", "badge-warning"
    
    mo_ta = Column(Text)
    # Mô tả chi tiết
    
    # ========== TIMESTAMPS ==========
    ngay_tao = Column(TIMESTAMP, server_default=func.now())
    
    # ========== RELATIONSHIPS ==========
    # vung_trong_list = relationship("VungTrong", back_populates="trang_thai")


class TrangThaiMaVung(Base):
    """
    Model cho bảng trang_thai_ma_vung (Lịch Sử Trạng Thái Mã)
    
    Tracking lịch sử thay đổi trạng thái mã vùng trồng.
    
    Database: nongsan.trang_thai_ma_vung
    """
    __tablename__ = "trang_thai_ma_vung"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== THÔNG TIN ==========
    ma_vung = Column(String, nullable=False, index=True)
    # Mã vùng trồng
    
    trang_thai_id = Column(Integer, ForeignKey("nongsan.trang_thai_vung.id"), nullable=False)
    # FK → trang_thai_vung.id
    
    ngay_thay_doi = Column(TIMESTAMP, server_default=func.now())
    # Thời điểm thay đổi trạng thái
    
    ghi_chu = Column(Text)
    # Ghi chú về thay đổi
    
    # ========== RELATIONSHIPS ==========
    # trang_thai = relationship("TrangThaiVung", back_populates="lich_su_ma")
