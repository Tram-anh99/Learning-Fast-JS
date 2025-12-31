"""
Models cho Trạng Thái
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class TrangThai(Base):
    """Danh mục trạng thái vùng trồng"""
    __tablename__ = "trang_thai"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_trang_thai = Column(String(50), unique=True, nullable=False, index=True)
    ten_trang_thai = Column(String(100), nullable=False)
    mau_sac = Column(String(20))  # HEX color code
    mo_ta = Column(String(255))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    vung_trong_list = relationship("VungTrong", back_populates="trang_thai")
    trang_thai_ma = relationship("TrangThaiMa", back_populates="trang_thai")


class TrangThaiMa(Base):
    """Lịch sử trạng thái mã vùng"""
    __tablename__ = "trang_thai_ma"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_vung = Column(String(50), nullable=False, index=True)
    trang_thai_id = Column(Integer, ForeignKey("nongsan.trang_thai.id"), nullable=False)
    ngay_thay_doi = Column(TIMESTAMP, server_default=func.now())
    ghi_chu = Column(String(500))
    
    # Relationships
    trang_thai = relationship("TrangThai", back_populates="trang_thai_ma")
