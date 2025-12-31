"""
========== Models: Chứng Nhận và Giấy Phép ==========
File: models/chung_nhan.py
Purpose: Quản lý chứng nhận (VietGAP, GlobalGAP, Hữu cơ, ...)

Models:
1. ChungNhan: Thông tin chứng nhận của vùng trồng

Database: nongsan.chung_nhan
Kết nối: routes/farms.py -> Farm certificates
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class ChungNhan(Base):
    """Danh mục chứng nhận chất lượng"""
    __tablename__ = "chung_nhan"
    __table_args__ = {"schema": "nongsan"}
    
    id = Column(Integer, primary_key=True, index=True)
    ma_chung_nhan = Column(String(50), unique=True, nullable=False, index=True)
    ten_chung_nhan = Column(String(255), nullable=False)
    to_chuc_cap = Column(String(255))
    mo_ta = Column(Text)
    icon = Column(String(100))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
