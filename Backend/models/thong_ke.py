"""
Models cho Thống Kê Hệ Thống
"""

from sqlalchemy import Column, Integer, Float, Date, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class ThongKeHeThong(Base):
    """Thống kê tổng hợp theo ngày"""
    __tablename__ = "thong_ke_he_thong"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ngay = Column(Date, unique=True, nullable=False, index=True)
    
    # Số lượng
    tong_vung_trong = Column(Integer, default=0)
    vung_con_han = Column(Integer, default=0)
    vung_sap_het_han = Column(Integer, default=0)
    vung_het_han = Column(Integer, default=0)
    
    # Diện tích
    tong_dien_tich = Column(Float, default=0)
    
    # Sản lượng
    tong_san_luong = Column(Float, default=0)
    
    # Hoạt động
    so_hoat_dong = Column(Integer, default=0)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
