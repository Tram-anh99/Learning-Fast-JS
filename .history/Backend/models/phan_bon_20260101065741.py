"""
========== MODELS: PHÂN BÓN (Fertilizers) ==========

Mục đích:
Models cho quản lý phân bón và loại phân bón

Models:
1. LoaiPhanBon: Phân loại phân bón (Đạm, Lân, Kali, Hữu cơ, etc.)
2. PhanBon: Thông tin chi tiết phân bón

Database tables:
- nongsan.loai_phan_bon (4 columns)
- nongsan.phan_bon (7 columns)

Relationships:
- PhanBon.loai_phan_bon_id → LoaiPhanBon.id (many-to-one)
- LichSuCanhTac.phan_bon_id → PhanBon.id (many-to-one)

Usage:
- Admin quản lý danh mục phân bón
- Nha nông chọn phân bón khi ghi nhật ký
"""

# ========== IMPORTS ==========
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# ========== LOẠI PHÂN BÓN MODEL ==========
class LoaiPhanBon(Base):
    """
    ========== Loại phân bón (Fertilizer Category) ==========
    
    Phân loại phân bón theo thành phần chính
    
    Columns:
    - id: Primary key
    - ma_loai: Mã loại (unique) - NPKDAM, NPKLAN, NPKKALI, HUUCO, etc.
    - ten_loai: Tên loại hiển thị - "Phân đạm", "Phân lân", "Phân hữu cơ"
    - mo_ta: Mô tả chi tiết loại phân bón
    - ngay_tao: Timestamp tạo record (auto)
    
    Relationships:
    - phan_bon: List các phân bón thuộc loại này (one-to-many)
    
    Examples:
    - LoaiPhanBon(ma_loai="NPKDAM", ten_loai="Phân đạm (N)")
    - LoaiPhanBon(ma_loai="HUUCO", ten_loai="Phân hữu cơ")
    """
    __tablename__ = "loai_phan_bon"
    __table_args__ = {'schema': 'nongsan'}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    # Auto increment ID
    
    # ========== FIELDS ==========
    ma_loai = Column(String(50), unique=True, nullable=False, index=True)
    # Mã loại phân bón (unique constraint)
    # Index cho lookup nhanh
    # Examples: "NPKDAM", "NPKLAN", "HUUCO"
    
    ten_loai = Column(String(200), nullable=False)
    # Tên loại hiển thị
    # Examples: "Phân đạm (N)", "Phân lân (P)", "Phân hữu cơ"
    
    mo_ta = Column(Text)
    # Mô tả chi tiết
    # Giải thích công dụng, đặc điểm loại phân bón
    
    # ========== TIMESTAMP ==========
    ngay_tao = Column(DateTime(timezone=False), server_default=func.now())
    # Auto set khi INSERT
    # Không có timezone (local time)
    
    # ========== RELATIONSHIPS ==========
    phan_bon = relationship("PhanBon", back_populates="loai_phan_bon", lazy="select")
    # One-to-many: Một loại có nhiều phân bón
    # lazy="select": Load khi access (default)
    # back_populates: Two-way relationship
    
    def __repr__(self):
        return f"<LoaiPhanBon(id={self.id}, ma_loai={self.ma_loai}, ten_loai={self.ten_loai})>"


# ========== PHÂN BÓN MODEL ==========
class PhanBon(Base):
    """
    ========== Phân bón (Fertilizer) ==========
    
    Thông tin chi tiết từng loại phân bón
    
    Columns:
    - id: Primary key
    - ma_phan_bon: Mã phân bón (unique)
    - ten_phan_bon: Tên thương mại
    - loai_phan_bon_id: FK → loai_phan_bon.id
    - thanh_phan: Thành phần hóa học (NPK 16-16-8, etc.)
    - don_vi: Đơn vị đo (kg, tấn, bao)
    - mo_ta: Mô tả chi tiết
    - ngay_tao: Timestamp tạo record (auto)
    
    Relationships:
    - loai_phan_bon: Loại phân bón (many-to-one)
    - lich_su_canh_tac: Lịch sử sử dụng (one-to-many)
    
    Examples:
    - PhanBon(ma_phan_bon="NPK168", ten_phan_bon="Phân NPK 16-16-8", 
              thanh_phan="N:16%, P:16%, K:8%", don_vi="kg")
    """
    __tablename__ = "phan_bon"
    __table_args__ = {'schema': 'nongsan'}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== FIELDS ==========
    ma_phan_bon = Column(String(50), unique=True, nullable=False, index=True)
    # Mã phân bón (unique)
    # Examples: "NPK168", "URIEM46", "DAP", "SA"
    
    ten_phan_bon = Column(String(200), nullable=False)
    # Tên thương mại
    # Examples: "Phân NPK 16-16-8", "Phân Urê 46%", "Phân DAP"
    
    loai_phan_bon_id = Column(Integer, ForeignKey('nongsan.loai_phan_bon.id', ondelete="SET NULL"))
    # FK → loai_phan_bon
    # ondelete="SET NULL": Khi xóa loại → set NULL (không xóa phân bón)
    
    thanh_phan = Column(Text)
    # Thành phần hóa học chi tiết
    # Examples: "N: 16%, P2O5: 16%, K2O: 8%"
    # Text type cho nội dung dài
    
    don_vi = Column(String(50))
    # Đơn vị đo lường
    # Examples: "kg", "tấn", "bao", "lít"
    
    mo_ta = Column(Text)
    # Mô tả, hướng dẫn sử dụng
    # Liều lượng khuyến cáo, cách sử dụng
    
    # ========== TIMESTAMP ==========
    ngay_tao = Column(DateTime(timezone=False), server_default=func.now())
    # Auto timestamp khi tạo
    
    # ========== RELATIONSHIPS ==========
    loai_phan_bon = relationship("LoaiPhanBon", back_populates="phan_bon")
    # Many-to-one: Nhiều phân bón thuộc 1 loại
    
    lich_su_canh_tac = relationship("LichSuCanhTac", back_populates="phan_bon", foreign_keys="LichSuCanhTac.phan_bon_id")
    # One-to-many: 1 phân bón dùng trong nhiều lần ghi nhật ký
    # foreign_keys: Specify FK column trong LichSuCanhTac
    
    def __repr__(self):
        return f"<PhanBon(id={self.id}, ma_phan_bon={self.ma_phan_bon}, ten_phan_bon={self.ten_phan_bon})>"
