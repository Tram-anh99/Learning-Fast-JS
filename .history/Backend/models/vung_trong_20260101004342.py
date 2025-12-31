"""
========== Models cho Vùng Trồng (Farm Zones) ==========
File: models/vung_trong.py
Purpose: Định nghĩa SQLAlchemy ORM models cho bảng vung_trong và toa_do_vung

Module này định nghĩa:
1. VungTrong: Bảng chính chứa thông tin vùng trồng
2. ToaDoVung: Bảng tọa độ (coordinates) để vẽ polygon trên map
3. VungCayTrong: Bảng liên kết vùng trồng với cây trồng (n-n relationship)

Kết nối đến:
- database.py: Base class cho tất cả models
- models/chu_vung.py: Relationship với ChuVung (chủ vùng)
- models/trang_thai.py: Relationship với TrangThai (trạng thái)
- routes/farms.py: CRUD operations sử dụng models này
- schemas.py: VungTrongResponse, VungTrongCreate mapping từ models này

Database table: nongsan.vung_trong
"""

# Import SQLAlchemy column types và utilities
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, TIMESTAMP
# Column: Định nghĩa cột trong bảng
# Integer, String, Float, Date, Text, TIMESTAMP: Kiểu dữ liệu
# ForeignKey: Định nghĩa foreign key constraint
from sqlalchemy.orm import relationship  # Định nghĩa relationship giữa các models
from sqlalchemy.sql import func          # SQL functions (func.now() cho timestamps)
from database import Base                # Base class từ declarative_base()


class VungTrong(Base):
    """
    SQLAlchemy Model cho bảng vung_trong (Vùng Trồng)
    
    Bảng này chứa thông tin chính về vùng trồng:
    - Thông tin cơ bản: mã vùng, tên vùng, địa chỉ, diện tích
    - Thông tin mã vùng trồng: ngày cấp mã, ngày hết hạn
    - Foreign keys: chu_vung_id (chủ vùng), trang_thai_id (trạng thái)
    - Relationships: toa_do (list tọa độ), cay_trong (list cây trồng)
    
    Database: nongsan.vung_trong
    
    Kết nối đến:
    - routes/farms.py: get_farms(), create_farm(), update_farm(), delete_farm()
    - schemas.py: VungTrongResponse, VungTrongCreate, VungTrongDetail
    - Frontend: HomeView.vue, MapComponent.vue display farm data
    """
    __tablename__ = "vung_trong"                # Tên bảng trong database
    __table_args__ = {"schema": "nongsan"}      # Schema name (không dùng public schema)
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    # - primary_key=True: Đây là primary key (unique identifier)
    # - index=True: Tạo database index cho tốc độ query
    
    # ========== BASIC INFORMATION ==========
    ma_vung = Column(String(50), unique=True, nullable=False, index=True)
    # - String(50): VARCHAR(50) trong PostgreSQL
    # - unique=True: Giá trị phải unique trong toàn bộ bảng (database constraint)
    # - nullable=False: Không được NULL (required field)
    # - index=True: Tạo index vì thường query theo ma_vung
    # Example: "MSVT001", "MSVT002"
    
    ten_vung = Column(String(255), nullable=False)
    # - String(255): VARCHAR(255) - tên vùng trồng
    # - nullable=False: Bắt buộc phải có tên
    # Example: "Vườn A", "Vườn B"
    
    dia_chi = Column(Text)
    # - Text: Không giới hạn độ dài (khác String có max length)
    # - nullable=True (default): Có thể NULL
    # Example: "123 Đường ABC, Phường XYZ, Quận 1, TP.HCM"
    
    dien_tich_ha = Column(Float)
    # - Float: Số thập phân (REAL/DOUBLE PRECISION trong PostgreSQL)
    # - Diện tích tính bằng hecta (ha)
    # Example: 5.5, 10.25
    
    ngay_cap_ma = Column(Date)
    # - Date: Chỉ lưu ngày (YYYY-MM-DD), không có time
    # - Ngày cấp mã vùng trồng
    # Example: date(2024, 1, 1)
    
    ngay_het_han = Column(Date)
    # - Ngày hết hạn mã vùng trồng
    # - Dùng để tính trạng thái: còn hạn, sắp hết hạn, hết hạn
    # Example: date(2025, 12, 31)
    
    # ========== FOREIGN KEYS ==========
    chu_vung_id = Column(Integer, ForeignKey("nongsan.chu_vung.id"))
    # - ForeignKey: Liên kết đến bảng chu_vung (chủ vùng)
    # - Format: "schema.table.column"
    # - nullable=True (default): Vùng có thể chưa có chủ
    # - ondelete: Không set (default RESTRICT - không xóa được chu_vung nếu có vung_trong)
    
    trang_thai_id = Column(Integer, ForeignKey("nongsan.trang_thai.id"))
    # - ForeignKey: Liên kết đến bảng trang_thai
    # - Trạng thái: Còn hạn, Sắp hết hạn, Hết hạn, etc.
    
    # ========== TIMESTAMPS ==========
    created_at = Column(TIMESTAMP, server_default=func.now())
    # - TIMESTAMP: Date + time (YYYY-MM-DD HH:MM:SS)
    # - server_default=func.now(): Database tự động set = NOW() khi INSERT
    # - Không thể update sau khi tạo
    
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    # - server_default: Set = NOW() khi INSERT
    # - onupdate=func.now(): Tự động update = NOW() mỗi khi UPDATE record
    # - Tracking last modified time
    
    # ========== RELATIONSHIPS ==========
    # SQLAlchemy relationships để join với bảng khác (không lưu trong DB, chỉ là mapping)
    
    chu_vung = relationship("ChuVung", back_populates="vung_trong_list")
    # - Relationship với model ChuVung (many-to-one: nhiều vùng -> 1 chủ)
    # - back_populates="vung_trong_list": Tên attribute trong ChuVung model
    # - Usage: vung.chu_vung.ten_chu (access chủ vùng từ vùng trồng)
    # - Reverse: chu_vung.vung_trong_list (access list vùng từ chủ vùng)
    
    trang_thai = relationship("TrangThai", back_populates="vung_trong_list")
    # - Relationship với model TrangThai (many-to-one)
    # - Usage: vung.trang_thai.ten_trang_thai (get tên trạng thái)
    
    toa_do = relationship("ToaDoVung", back_populates="vung_trong", cascade="all, delete-orphan")
    # - Relationship với model ToaDoVung (one-to-many: 1 vùng -> nhiều tọa độ)
    # - cascade="all, delete-orphan": Xóa vùng -> tự động xóa tất cả tọa độ
    #   + "all": Propagate tất cả operations (save, update, delete, merge, refresh)
    #   + "delete-orphan": Xóa tọa độ nếu remove khỏi vung.toa_do list
    # - Usage: vung.toa_do = [ToaDoVung(...), ToaDoVung(...)]
    
    cay_trong = relationship("VungCayTrong", back_populates="vung_trong", cascade="all, delete-orphan")
    # - Relationship với model VungCayTrong (one-to-many: 1 vùng -> nhiều cây trồng)
    # - cascade="all, delete-orphan": Xóa vùng -> xóa tất cả cây trồng trong vùng


class ToaDoVung(Base):
    """
    SQLAlchemy Model cho bảng toa_do_vung (Tọa độ Vùng Trồng)
    
    Bảng này chứa các điểm tọa độ (latitude, longitude) để vẽ polygon ranh giới vùng trồng trên bản đồ.
    
    Cách hoạt động:
    1. Mỗi vùng trồng có nhiều tọa độ (1-to-many relationship)
    2. Các tọa độ được sắp xếp theo thu_tu (1, 2, 3, ...) để vẽ polygon theo thứ tự
    3. Polygon được tạo bằng cách nối các điểm theo thu_tu, điểm cuối nối về điểm đầu
    
    Example:
    Vùng trồng ID=1 có 4 tọa độ:
    - (thu_tu=1, lat=10.7626, lng=106.6821)
    - (thu_tu=2, lat=10.7627, lng=106.6822)
    - (thu_tu=3, lat=10.7628, lng=106.6821)
    - (thu_tu=4, lat=10.7627, lng=106.6820)
    → Vẽ polygon 4 cạnh trên map
    
    Database: nongsan.toa_do_vung
    
    Kết nối đến:
    - models/vung_trong.py: VungTrong.toa_do relationship
    - routes/farms.py: create_farm() tạo vùng + tọa độ cùng lúc
    - schemas.py: ToaDoResponse, ToaDoBase
    - Frontend: MapComponent.vue draw polygon from coordinates
    """
    __tablename__ = "toa_do_vung"              # Tên bảng trong database
    __table_args__ = {"schema": "nongsan"}      # Schema name
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    # - primary_key: Unique identifier cho mỗi tọa độ
    # - index: Index cho performance
    
    # ========== FOREIGN KEY ==========
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), nullable=False)
    # - ForeignKey: Liên kết đến vung_trong.id
    # - ondelete="CASCADE": Xóa vùng trồng -> tự động xóa tất cả tọa độ
    #   (không cần tọa độ nếu vùng trồng không còn)
    # - nullable=False: Bắt buộc phải có vung_trong_id (tọa độ không thể độc lập)
    
    # ========== COORDINATE DATA ==========
    thu_tu = Column(Integer, nullable=False)
    # - Thứ tự điểm trong polygon (1, 2, 3, 4, ...)
    # - nullable=False: Bắt buộc (để vẽ polygon đúng thứ tự)
    # - Dùng để ORDER BY khi query: ORDER BY thu_tu ASC
    
    latitude = Column(Float, nullable=False)
    # - Vĩ độ (latitude): -90 đến +90
    # - nullable=False: Bắt buộc phải có
    # - Example: 10.7626 (Việt Nam nằm trong khoảng 8°-24°N)
    
    longitude = Column(Float, nullable=False)
    # - Kinh độ (longitude): -180 đến +180
    # - nullable=False: Bắt buộc phải có
    # - Example: 106.6821 (Việt Nam nằm trong khoảng 102°-110°E)
    
    # ========== RELATIONSHIPS ==========
    vung_trong = relationship("VungTrong", back_populates="toa_do")
    # - Relationship với model VungTrong (many-to-one: nhiều tọa độ -> 1 vùng)
    # - back_populates="toa_do": Tên attribute trong VungTrong model
    # - Usage: 
    #   + toa_do.vung_trong.ten_vung (access vùng từ tọa độ)
    #   + vung.toa_do (access list tọa độ từ vùng)
    # - Note: Không set cascade ở đây (đã set ở VungTrong.toa_do)
