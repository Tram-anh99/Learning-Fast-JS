"""
========== MODELS: THUỐC BẢO VỆ THỰC VẬT (Pesticides) ==========

Mục đích:
Models cho quản lý thuốc BVTV và nhóm thuốc

Models:
1. NhomThuocBVTV: Phân nhóm thuốc (Diệt côn trùng, Diệt nấm, Diệt cỏ)
2. ThuocBVTV: Thông tin chi tiết thuốc BVTV

Database tables:
- nongsan.nhom_thuoc_bvtv (4 columns)
- nongsan.thuoc_bvtv (9 columns)

Relationships:
- ThuocBVTV.nhom_thuoc_id → NhomThuocBVTV.id (many-to-one)
- LichSuCanhTac.thuoc_bvtv_id → ThuocBVTV.id (many-to-one)

Usage:
- Admin quản lý danh mục thuốc BVTV
- Nha nông chọn thuốc khi ghi nhật ký phun thuốc
"""

# ========== IMPORTS ==========
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# ========== NHÓM THUỐC BVTV MODEL ==========
class NhomThuocBVTV(Base):
    """
    ========== Nhóm thuốc BVTV (Pesticide Group) ==========
    
    Phân nhóm thuốc bảo vệ thực vật theo công dụng
    
    Columns:
    - id: Primary key
    - ma_nhom: Mã nhóm (unique) - DIETCONTRUONG, DIETNAMBENHHAI, DIETCO, etc.
    - ten_nhom: Tên nhóm hiển thị
    - mo_ta: Mô tả chi tiết
    - ngay_tao: Timestamp tạo record (auto)
    
    Relationships:
    - thuoc_bvtv: List thuốc thuộc nhóm (one-to-many)
    
    Examples:
    - NhomThuocBVTV(ma_nhom="DIETCONTRUONG", ten_nhom="Thuốc trừ sâu")
    - NhomThuocBVTV(ma_nhom="DIETNAMBENHHAI", ten_nhom="Thuốc trừ nấm bệnh")
    - NhomThuocBVTV(ma_nhom="DIETCO", ten_nhom="Thuốc diệt cỏ")
    """
    __tablename__ = "nhom_thuoc_bvtv"
    __table_args__ = {'schema': 'nongsan'}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== FIELDS ==========
    ma_nhom = Column(String(50), unique=True, nullable=False, index=True)
    # Mã nhóm thuốc (unique)
    # Examples: "DIETCONTRUONG", "DIETNAMBENHHAI", "DIETCO", "KICHTHOAT"
    
    ten_nhom = Column(String(200), nullable=False)
    # Tên nhóm hiển thị
    # Examples: "Thuốc trừ sâu", "Thuốc trừ nấm bệnh", "Thuốc diệt cỏ"
    
    mo_ta = Column(Text)
    # Mô tả công dụng nhóm thuốc
    # Giải thích đối tượng tác dụng, cách sử dụng
    
    # ========== TIMESTAMP ==========
    ngay_tao = Column(DateTime(timezone=False), server_default=func.now())
    # Auto timestamp
    
    # ========== RELATIONSHIPS ==========
    thuoc_bvtv = relationship("ThuocBVTV", back_populates="nhom_thuoc", lazy="select")
    # One-to-many: Một nhóm có nhiều thuốc
    
    def __repr__(self):
        return f"<NhomThuocBVTV(id={self.id}, ma_nhom={self.ma_nhom}, ten_nhom={self.ten_nhom})>"


# ========== THUỐC BVTV MODEL ==========
class ThuocBVTV(Base):
    """
    ========== Thuốc bảo vệ thực vật (Pesticide) ==========
    
    Thông tin chi tiết thuốc BVTV
    
    Columns:
    - id: Primary key
    - ma_thuoc: Mã thuốc (unique)
    - ten_thuoc: Tên thương mại
    - ten_hoat_chat: Tên hoạt chất chính
    - ham_luong: Hàm lượng hoạt chất (%)
    - nhom_thuoc_id: FK → nhom_thuoc_bvtv.id
    - dang_bao_che: Dạng bào chế (EC, WP, SC, etc.)
    - trang_thai_su_dung: Trạng thái (Được phép, Hạn chế, Cấm)
    - mo_ta: Mô tả, hướng dẫn
    - ngay_tao: Timestamp (auto)
    
    Relationships:
    - nhom_thuoc: Nhóm thuốc (many-to-one)
    - lich_su_canh_tac: Lịch sử sử dụng (one-to-many)
    
    Examples:
    - ThuocBVTV(ma_thuoc="ABAMEC18", ten_thuoc="Abamectin 1.8% EC",
                ten_hoat_chat="Abamectin", ham_luong="1.8%",
                dang_bao_che="EC", trang_thai_su_dung="Được phép")
    """
    __tablename__ = "thuoc_bvtv"
    __table_args__ = {'schema': 'nongsan'}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== FIELDS ==========
    ma_thuoc = Column(String(50), unique=True, nullable=False, index=True)
    # Mã thuốc (unique)
    # Examples: "ABAMEC18", "IMIDA25", "GLYPHO41"
    
    ten_thuoc = Column(String(200), nullable=False)
    # Tên thương mại
    # Examples: "Abamectin 1.8% EC", "Imidacloprid 25% WP"
    
    ten_hoat_chat = Column(String(200))
    # Tên hoạt chất chính
    # Examples: "Abamectin", "Imidacloprid", "Glyphosate"
    
    ham_luong = Column(String(50))
    # Hàm lượng hoạt chất
    # Examples: "1.8%", "25%", "41% SL"
    
    nhom_thuoc_id = Column(Integer, ForeignKey('nongsan.nhom_thuoc_bvtv.id', ondelete="SET NULL"))
    # FK → nhom_thuoc_bvtv
    # ondelete="SET NULL": Xóa nhóm không xóa thuốc
    
    dang_bao_che = Column(String(50))
    # Dạng bào chế
    # Examples: "EC" (Nhũ dầu), "WP" (Bột), "SC" (Huyền phù)
    
    trang_thai_su_dung = Column(String(50))
    # Trạng thái cho phép sử dụng
    # Values: "Được phép", "Hạn chế", "Cấm sử dụng"
    # Theo quy định của Bộ NN & PTNT
    
    mo_ta = Column(Text)
    # Mô tả chi tiết
    # Hướng dẫn sử dụng, liều lượng, thời gian cách ly
    
    # ========== TIMESTAMP ==========
    ngay_tao = Column(DateTime(timezone=False), server_default=func.now())
    
    # ========== RELATIONSHIPS ==========
    nhom_thuoc = relationship("NhomThuocBVTV", back_populates="thuoc_bvtv")
    # Many-to-one: Nhiều thuốc thuộc 1 nhóm
    
    lich_su_canh_tac = relationship("LichSuCanhTac", back_populates="thuoc_bvtv", foreign_keys="LichSuCanhTac.thuoc_bvtv_id")
    # One-to-many: 1 thuốc dùng trong nhiều lần phun
    
    def __repr__(self):
        return f"<ThuocBVTV(id={self.id}, ma_thuoc={self.ma_thuoc}, ten_thuoc={self.ten_thuoc})>"
