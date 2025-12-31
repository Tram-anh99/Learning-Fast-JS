"""
Models cho Chủ Vùng (Farm Owners)
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class ChuVung(Base):
    """Thông tin chủ vùng trồng"""
    __tablename__ = "chu_vung"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_chu = Column(String(50), unique=True, index=True)
    ten_chu = Column(String(255), nullable=False)
    loai_chu = Column(String(50))  # 'ca_nhan' hoặc 'to_chuc'
    cccd_mst = Column(String(50))  # CCCD hoặc MST
    dia_chi = Column(Text)
    dien_thoai = Column(String(20))
    email = Column(String(255))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    vung_trong_list = relationship("VungTrong", back_populates="chu_vung")
