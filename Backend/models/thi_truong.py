"""
Models cho Thị Trường Xuất Khẩu
"""

from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class ThiTruong(Base):
    """Danh mục thị trường xuất khẩu"""
    __tablename__ = "thi_truong"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_thi_truong = Column(String(50), unique=True, nullable=False, index=True)
    ten_thi_truong = Column(String(255), nullable=False)
    ma_quoc_gia = Column(String(10))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    cay_thi_truong = relationship("CayThiTruong", back_populates="thi_truong")


class CayThiTruong(Base):
    """Bảng trung gian: Vùng cây trồng - Thị trường (N-N)"""
    __tablename__ = "cay_thi_truong"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    vung_cay_trong_id = Column(Integer, ForeignKey("nongsan.vung_cay_trong.id", ondelete="CASCADE"), nullable=False)
    thi_truong_id = Column(Integer, ForeignKey("nongsan.thi_truong.id", ondelete="CASCADE"), nullable=False)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    # vung_cay_trong = relationship("VungCayTrong", back_populates="thi_truong")
    thi_truong = relationship("ThiTruong", back_populates="cay_thi_truong")
