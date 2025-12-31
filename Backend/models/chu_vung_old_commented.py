"""
========== Models cho Chủ Vùng (Farm Owners) ==========
File: models/chu_vung.py
Purpose: Định nghĩa SQLAlchemy ORM model cho bảng chu_vung

Bảng này chứa thông tin về chủ vùng trồng (farm owners):
- Có thể là cá nhân hoặc tổ chức
- Một chủ vùng có thể sở hữu nhiều vùng trồng (1-to-many)

Database table: nongsan.chu_vung

Kết nối đến:
- models/vung_trong.py: VungTrong.chu_vung relationship
- routes/owners.py: CRUD operations cho chủ vùng (nếu có)
- schemas.py: ChuVungResponse, ChuVungCreate
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class ChuVung(Base):
    """
    SQLAlchemy Model cho bảng chu_vung (Chủ Vùng Trồng)
    
    Thông tin chủ vùng trồng (cá nhân hoặc tổ chức):
    - Thông tin cơ bản: mã chủ, tên chủ, loại chủ
    - Thông tin liên hệ: địa chỉ, điện thoại, email
    - Thông tin định danh: CCCD (cá nhân) hoặc MST (doanh nghiệp)
    - Relationship: Một chủ có thể sở hữu nhiều vùng trồng
    
    Database: nongsan.chu_vung
    """
    __tablename__ = "chu_vung"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== BASIC INFORMATION ==========
    ma_chu = Column(String(50), unique=True, index=True)
    # - Mã chủ vùng (unique code)
    # - unique=True: Không trùng lặp
    # - nullable=True (default): Có thể NULL (auto-generate sau)
    # Example: "CHU001", "CHU002"
    
    ten_chu = Column(String(255), nullable=False)
    # - Tên chủ vùng (tên cá nhân hoặc tên công ty)
    # - nullable=False: Bắt buộc phải có tên
    # Example: "Nguyễn Văn A", "Công ty TNHH ABC"
    
    loai_chu = Column(String(50))
    # - Loại chủ vùng: "ca_nhan" hoặc "to_chuc"/"doanh_nghiep"
    # - nullable=True: Có thể NULL
    # - Default có thể set ở application level
    # Example: "ca_nhan", "doanh_nghiep", "hop_tac_xa"
    
    cccd_mst = Column(String(50))
    # - CCCD (Căn cước công dân) cho cá nhân
    # - MST (Mã số thuế) cho doanh nghiệp
    # - nullable=True: Có thể không có
    # Example: "001234567890" (CCCD), "0123456789" (MST)
    
    # ========== CONTACT INFORMATION ==========
    dia_chi = Column(Text)
    # - Địa chỉ chủ vùng
    # - Text: Không giới hạn độ dài
    # Example: "123 Đường ABC, Phường XYZ, Quận 1, TP.HCM"
    
    dien_thoai = Column(String(20))
    # - Số điện thoại
    # - String(20): Đủ cho số điện thoại quốc tế
    # Example: "0901234567", "+84901234567"
    
    email = Column(String(255))
    # - Email liên hệ
    # Example: "nguyenvana@example.com"
    
    # ========== TIMESTAMPS ==========
    created_at = Column(TIMESTAMP, server_default=func.now())
    # - Ngày tạo record (auto-set bởi database)
    
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    # - Ngày cập nhật cuối (auto-update mỗi khi UPDATE)
    
    # ========== RELATIONSHIPS ==========
    vung_trong_list = relationship("VungTrong", back_populates="chu_vung")
    # - Relationship với VungTrong (one-to-many: 1 chủ -> nhiều vùng)
    # - back_populates="chu_vung": Tên attribute trong VungTrong model
    # - Usage:
    #   + chu_vung.vung_trong_list → List[VungTrong] (tất cả vùng của chủ này)
    #   + vung.chu_vung → ChuVung (chủ sở hữu vùng)
    # - No cascade: Xóa chủ vùng KHÔNG tự động xóa vùng trồng (cần handle riêng)

