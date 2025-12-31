"""
Models cho Lịch Sử Canh Tác (Diary)
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class LoaiHoatDong(Base):
    """Danh mục loại hoạt động canh tác"""
    __tablename__ = "loai_hoat_dong"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_loai = Column(String(50), unique=True, nullable=False, index=True)
    ten_loai = Column(String(100), nullable=False)
    nhom = Column(String(50))  # 'bon_phan', 'phun_thuoc', 'tuoi_nuoc', 'thu_hoach'
    icon = Column(String(50))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    lich_su = relationship("LichSuCanhTac", back_populates="loai_hoat_dong")


class LichSuCanhTac(Base):
    """Nhật ký canh tác"""
    __tablename__ = "lich_su_canh_tac"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), nullable=False, index=True)
    loai_hoat_dong_id = Column(Integer, ForeignKey("nongsan.loai_hoat_dong.id"))
    
    ngay_thuc_hien = Column(Date, nullable=False, index=True)
    mo_ta = Column(Text)
    
    # Vật tư sử dụng (nullable - tùy loại hoạt động)
    phan_bon_id = Column(Integer)
    thuoc_bvtv_id = Column(Integer)
    luong_su_dung = Column(Float)
    don_vi = Column(String(20))
    
    # Kết quả
    ket_qua = Column(Text)
    nguoi_thuc_hien = Column(String(255))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    loai_hoat_dong = relationship("LoaiHoatDong", back_populates="lich_su")
