"""
========== Models cho Trạng Thái (Status) ==========
File: models/trang_thai.py
Purpose: Định nghĩa SQLAlchemy ORM models cho trạng thái vùng trồng

Module này định nghĩa:
1. TrangThai: Danh mục trạng thái (Còn hạn, Sắp hết hạn, Hết hạn)
2. TrangThaiMa: Lịch sử thay đổi trạng thái mã vùng (status history tracking)

Database tables:
- nongsan.trang_thai
- nongsan.trang_thai_ma

Kết nối đến:
- models/vung_trong.py: VungTrong.trang_thai relationship
- routes/farms.py: Filter farms by status
- Frontend: Status indicators, color coding
"""

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class TrangThai(Base):
    """
    SQLAlchemy Model cho bảng trang_thai (Trạng Thái)
    
    Danh mục các trạng thái của vùng trồng:
    - Còn hạn: Mã vùng trồng còn hiệu lực
    - Sắp hết hạn: Mã sắp hết hạn (< 30 ngày)
    - Hết hạn: Mã đã hết hạn
    - Tạm ngưng: Vùng tạm ngưng hoạt động
    
    Mỗi trạng thái có màu sắc riêng để hiển thị trên UI
    
    Database: nongsan.trang_thai
    """
    __tablename__ = "trang_thai"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== STATUS INFORMATION ==========
    ma_trang_thai = Column(String(50), unique=True, nullable=False, index=True)
    # - Mã trạng thái (unique code)
    # - unique=True: Không trùng
    # - nullable=False: Bắt buộc
    # Example: "CON_HAN", "SAP_HET_HAN", "HET_HAN"
    
    ten_trang_thai = Column(String(100), nullable=False)
    # - Tên trạng thái hiển thị
    # - nullable=False: Bắt buộc
    # Example: "Còn hạn", "Sắp hết hạn", "Hết hạn"
    
    mau_sac = Column(String(20))
    # - Màu sắc HEX code để hiển thị trên UI
    # - nullable=True: Có thể NULL (dùng màu default)
    # Example: "#4CAF50" (green), "#FF9800" (orange), "#F44336" (red)
    # Usage: Frontend display status badge with this color
    
    mo_ta = Column(String(255))
    # - Mô tả chi tiết trạng thái
    # Example: "Mã vùng trồng còn hiệu lực"
    
    # ========== TIMESTAMPS ==========
    created_at = Column(TIMESTAMP, server_default=func.now())
    # - Ngày tạo record (master data, ít khi thay đổi)
    
    # ========== RELATIONSHIPS ==========
    vung_trong_list = relationship("VungTrong", back_populates="trang_thai")
    # - Relationship với VungTrong (one-to-many: 1 trạng thái -> nhiều vùng)
    # - Usage: trang_thai.vung_trong_list → tất cả vùng có trạng thái này
    
    trang_thai_ma = relationship("TrangThaiMa", back_populates="trang_thai")
    # - Relationship với TrangThaiMa (one-to-many: 1 trạng thái -> nhiều history records)
    # - Usage: trang_thai.trang_thai_ma → lịch sử tất cả mã có trạng thái này


class TrangThaiMa(Base):
    """
    SQLAlchemy Model cho bảng trang_thai_ma (Lịch Sử Trạng Thái Mã)
    
    Bảng này tracking lịch sử thay đổi trạng thái của mã vùng trồng:
    - Khi mã mới được cấp → ghi record với trạng thái "Còn hạn"
    - Khi mã sắp hết hạn → ghi record với trạng thái "Sắp hết hạn"
    - Khi mã hết hạn → ghi record với trạng thái "Hết hạn"
    - Khi gia hạn → ghi record với trạng thái "Còn hạn" mới
    
    Purpose: Audit trail, báo cáo, phân tích xu hướng
    
    Database: nongsan.trang_thai_ma
    """
    __tablename__ = "trang_thai_ma"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== STATUS HISTORY DATA ==========
    ma_vung = Column(String(50), nullable=False, index=True)
    # - Mã vùng trồng (KHÔNG phải FK, chỉ lưu string)
    # - nullable=False: Bắt buộc
    # - index=True: Query theo mã vùng
    # Example: "MSVT001"
    # Note: Không dùng FK vì có thể track cả mã đã bị xóa
    
    trang_thai_id = Column(Integer, ForeignKey("nongsan.trang_thai.id"), nullable=False)
    # - FK đến bảng trang_thai
    # - nullable=False: Bắt buộc phải có trạng thái
    # - Đã fix: Trước đó thiếu ForeignKey, gây lỗi relationship
    
    ngay_thay_doi = Column(TIMESTAMP, server_default=func.now())
    # - Thời điểm thay đổi trạng thái
    # - server_default=func.now(): Auto-set khi INSERT
    # - Dùng để track timeline: Khi nào mã chuyển từ Còn hạn → Hết hạn?
    
    ghi_chu = Column(String(500))
    # - Ghi chú về thay đổi
    # Example: "Mã mới được cấp", "Mã hết hạn do quá thời hạn", "Gia hạn mã"
    
    # ========== RELATIONSHIPS ==========
    trang_thai = relationship("TrangThai", back_populates="trang_thai_ma")
    # - Relationship với TrangThai (many-to-one: nhiều history -> 1 trạng thái)
    # - Usage: history.trang_thai.ten_trang_thai → get tên trạng thái từ history record
