"""
Models cho Loại Cây và Vùng Cây Trồng
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class LoaiCay(Base):
    """Danh mục loại cây trồng"""
    __tablename__ = "loai_cay"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_cay = Column(String(50), unique=True, nullable=False, index=True)
    ten_cay = Column(String(255), nullable=False)
    ten_khoa_hoc = Column(String(255))
    mo_ta = Column(Text)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    vung_cay_trong = relationship("VungCayTrong", back_populates="loai_cay")


class VungCayTrong(Base):
    """Bảng trung gian: Vùng trồng - Loại cây (N-N)"""
    __tablename__ = "vung_cay_trong"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), nullable=False)
    loai_cay_id = Column(Integer, ForeignKey("nongsan.loai_cay.id", ondelete="CASCADE"), nullable=False)
    dien_tich_ha = Column(Float)
    san_luong_du_kien = Column(Float)
    nam_trong = Column(Integer)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    vung_trong = relationship("VungTrong", back_populates="cay_trong")
    loai_cay = relationship("LoaiCay", back_populates="vung_cay_trong")
    thi_truong = relationship("CayThiTruong", back_populates="vung_cay_trong", cascade="all, delete-orphan")
