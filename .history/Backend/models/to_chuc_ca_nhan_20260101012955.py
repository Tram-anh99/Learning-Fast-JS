"""
========== Models cho Tổ Chức/Cá Nhân (Organizations/Individuals) ==========
File: models/to_chuc_ca_nhan.py
Purpose: Định nghĩa model cho chủ sở hữu vùng trồng

Model này thay thế chu_vung cũ, quản lý:
- Tổ chức (công ty, hợp tác xã, trang trại)
- Cá nhân (nông dân)

Database: nongsan.to_chuc_ca_nhan
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class ToChucCaNhan(Base):
    """
    Model cho bảng to_chuc_ca_nhan (Tổ Chức/Cá Nhân)
    
    Thông tin chủ sở hữu vùng trồng:
    - Loại: Cá nhân, Công ty, Hợp tác xã, Trang trại
    - Thông tin liên hệ: điện thoại, email, địa chỉ
    - Hành chính: tỉnh/huyện/xã
    
    Database: nongsan.to_chuc_ca_nhan
    """
    __tablename__ = "to_chuc_ca_nhan"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== THÔNG TIN CƠ BẢN ==========
    ma_to_chuc = Column(String, unique=True, nullable=False, index=True)
    # Mã tổ chức/cá nhân (unique)
    # Example: "TC001", "CN001"
    
    ten_to_chuc = Column(String, nullable=False)
    # Tên tổ chức hoặc tên cá nhân
    # Example: "Công ty TNHH ABC", "Nguyễn Văn A"
    
    loai_to_chuc = Column(String, nullable=False)
    # Loại: "ca_nhan", "cong_ty", "hop_tac_xa", "trang_trai"
    
    nguoi_dai_dien = Column(String)
    # Người đại diện (với tổ chức)
    # Example: "Ông Nguyễn Văn B"
    
    # ========== LIÊN HỆ ==========
    dien_thoai = Column(String)
    # Số điện thoại liên hệ
    
    email = Column(String)
    # Email liên hệ
    
    dia_chi = Column(Text)
    # Địa chỉ chi tiết
    
    # ========== HÀNH CHÍNH ==========
    xa_id = Column(Integer, ForeignKey("nongsan.xa.id"))
    # FK → xa.id
    
    huyen_id = Column(Integer, ForeignKey("nongsan.huyen.id"))
    # FK → huyen.id
    
    tinh_id = Column(Integer, ForeignKey("nongsan.tinh.id"))
    # FK → tinh.id
    
    # ========== TRẠNG THÁI ==========
    trang_thai = Column(String)
    # Trạng thái: "hoat_dong", "tam_ngung", etc.
    
    # ========== TIMESTAMPS ==========
    ngay_tao = Column(TIMESTAMP, server_default=func.now())
    ngay_cap_nhat = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # ========== RELATIONSHIPS ==========
    vung_trong_list = relationship("VungTrong", back_populates="chu_so_huu")
