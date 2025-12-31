"""
Models cho Điểm Sâu Bệnh
"""

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class DiemSauBenh(Base):
    """Điểm phát sinh sâu bệnh trên bản đồ"""
    __tablename__ = "diem_sau_benh"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), index=True)
    
    ten_sau_benh = Column(String(255), nullable=False)
    loai = Column(String(50))  # 'sau' hoặc 'benh'
    muc_do = Column(String(50))  # 'nhe', 'trung_binh', 'nang'
    
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    ngay_phat_hien = Column(Date, nullable=False)
    ngay_xu_ly = Column(Date)
    bien_phap = Column(Text)
    ket_qua = Column(Text)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
