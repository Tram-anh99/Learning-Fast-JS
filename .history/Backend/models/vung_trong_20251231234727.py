"""
Models cho Vùng Trồng (Farm Zones)
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class VungTrong(Base):
    """Bảng vùng trồng chính"""
    __tablename__ = "vung_trong"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_vung = Column(String(50), unique=True, nullable=False, index=True)
    ten_vung = Column(String(255), nullable=False)
    dia_chi = Column(Text)
    dien_tich_ha = Column(Float)
    ngay_cap_ma = Column(Date)
    ngay_het_han = Column(Date)
    
    # Foreign Keys
    chu_vung_id = Column(Integer, ForeignKey("nongsan.chu_vung.id"))
    trang_thai_id = Column(Integer, ForeignKey("nongsan.trang_thai.id"))
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    chu_vung = relationship("ChuVung", back_populates="vung_trong_list")
    trang_thai = relationship("TrangThai", back_populates="vung_trong_list")
    toa_do = relationship("ToaDoVung", back_populates="vung_trong", cascade="all, delete-orphan")
    cay_trong = relationship("VungCayTrong", back_populates="vung_trong", cascade="all, delete-orphan")


class ToaDoVung(Base):
    """Tọa độ polygon của vùng trồng"""
    __tablename__ = "toa_do_vung"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), nullable=False)
    thu_tu = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Relationships
    vung_trong = relationship("VungTrong", back_populates="toa_do")
