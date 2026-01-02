"""
========== Models: Lịch Sử Canh Tác (Diary/Activity History) ==========
File: models/lich_su.py
Purpose: Tracking hoạt động canh tác hàng ngày trong vùng trồng

Models này định nghĩa:
1. LoaiHoatDong: Danh mục loại hoạt động (bón phân, phun thuốc, tưới nước, thu hoạch)
2. LichSuCanhTac: Nhật ký chi tiết hoạt động canh tác

Database tables: nongsan.loai_hoat_dong, nongsan.lich_su_canh_tac

Kết nối đến:
- models/vung_trong.py: Relationship với VungTrong
- routes/diary.py: CRUD operations cho nhật ký
- Frontend: DiaryPage.vue, DiaryActivityHistory.vue
"""

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class LoaiHoatDong(Base):
    """
    Model cho bảng loai_hoat_dong (Loại Hoạt Động Canh Tác)
    
    Danh mục các loại hoạt động:
    - Bón phân (fertilizing)
    - Phun thuốc BVTV (spraying pesticides)
    - Tưới nước (watering)
    - Thu hoạch (harvesting)
    - Làm đất (land preparation)
    - Gieo trồng (planting)
    
    Master data - ít thay đổi
    
    Database: nongsan.loai_hoat_dong
    """
    __tablename__ = "loai_hoat_dong"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== THÔNG TIN LOẠI HOẠT ĐỘNG ==========
    ma_loai = Column(String(50), unique=True, nullable=False, index=True)
    # Mã loại hoạt động (unique code)
    # Example: "BON_PHAN", "PHUN_THUOC", "TUOI_NUOC"
    
    ten_loai = Column(String(100), nullable=False)
    # Tên loại hoạt động
    # Example: "Bón phân", "Phun thuốc BVTV", "Tưới nước"
    
    nhom = Column(String(50))
    # Nhóm hoạt động để phân loại
    # Example: "cham_soc", "bao_ve_thuc_vat", "thu_hoach"
    # Usage: Filter, group by trong UI
    
    icon = Column(String(50))
    # Icon class cho hiển thị UI
    # Example: "fa-leaf", "fa-spray-can", "fa-droplet"
    
    mo_ta = Column(Text)
    # Mô tả chi tiết loại hoạt động
    
    # ========== TIMESTAMPS ==========
    ngay_tao = Column(TIMESTAMP, server_default=func.now())
    # Ngày tạo record
    
    # ========== RELATIONSHIPS ==========
    lich_su = relationship("LichSuCanhTac", back_populates="loai_hoat_dong")
    # Relationship với LichSuCanhTac (one-to-many)
    # Usage: loai_hoat_dong.lich_su → list tất cả activities của loại này


class LichSuCanhTac(Base):
    """
    Model cho bảng lich_su_canh_tac (Lịch Sử Canh Tác)
    
    Nhật ký hoạt động canh tác hàng ngày:
    - Ghi nhận công việc: ngày thực hiện, loại hoạt động, tiêu đề, nội dung
    - Tracking vật tư sử dụng: phân bón, thuốc BVTV với liều lượng
    - Thông tin người thực hiện, thửa ruộng
    - Ghi chú kết quả
    
    Example usage:
    - "01/01/2026 - Bón phân NPK cho vùng MSVT001, liều lượng 50kg, thửa A1"
    - "05/01/2026 - Phun thuốc trừ sâu, thuốc ABC, 200ml/20L nước"
    
    Database: nongsan.lich_su_canh_tac
    """
    __tablename__ = "lich_su_canh_tac"
    __table_args__ = {"schema": "nongsan"}
    
    # ========== PRIMARY KEY ==========
    id = Column(Integer, primary_key=True, index=True)
    
    # ========== FOREIGN KEYS ==========
    vung_trong_id = Column(Integer, ForeignKey("nongsan.vung_trong.id", ondelete="CASCADE"), nullable=False, index=True)
    # FK → vung_trong.id
    # ondelete="CASCADE": Xóa vùng → xóa tất cả lịch sử
    # index=True: Optimize queries filter by vung_trong_id
    
    loai_hoat_dong_id = Column(Integer, ForeignKey("nongsan.loai_hoat_dong.id"))
    # FK → loai_hoat_dong.id
    # nullable=True: Có thể có hoạt động không thuộc danh mục chuẩn
    
    # ========== THÔNG TIN HOẠT ĐỘNG ==========
    ngay_thuc_hien = Column(Date, nullable=False, index=True)
    # Ngày thực hiện hoạt động
    # index=True: Optimize queries order by date, filter by date range
    
    tieu_de = Column(String)
    # Tiêu đề ngắn gọn của hoạt động
    # Example: "Bón phân NPK lần 2", "Phun thuốc trừ rầy"
    
    noi_dung = Column(Text)
    # Nội dung chi tiết mô tả công việc
    # Example: "Bón phân NPK 16-16-8, phân bố đều quanh gốc cây, khoảng cách 20cm"
    
    nguoi_thuc_hien = Column(String)
    # Tên người/nhóm thực hiện
    # Example: "Nguyễn Văn A", "Đội 1"
    
    thua_ruong = Column(String)
    # Mã/tên thửa ruộng trong vùng
    # Example: "A1", "B2", "Thửa Đông"
    # Usage: Tracking chi tiết theo từng thửa
    
    # ========== VẬT TƯ SỬ DỤNG ==========
    phan_bon_id = Column(Integer, ForeignKey("nongsan.phan_bon.id"))
    # FK → phan_bon.id (nếu có sử dụng phân bón)
    # nullable=True: Chỉ áp dụng với hoạt động bón phân
    
    lieu_luong_phan_bon = Column(String)
    # Liều lượng phân bón sử dụng
    # Example: "50kg", "2 bao", "100kg/ha"
    # String để linh hoạt đơn vị
    
    thuoc_bvtv_id = Column(Integer, ForeignKey("nongsan.thuoc_bvtv.id"))
    # FK → thuoc_bvtv.id (nếu có sử dụng thuốc BVTV)
    # nullable=True: Chỉ áp dụng với hoạt động phun thuốc
    
    lieu_luong_thuoc = Column(String)
    # Liều lượng thuốc BVTV sử dụng
    # Example: "200ml/20L nước", "50g/bình 16L"
    # String để ghi linh hoạt
    
    ghi_chu = Column(Text)
    # Ghi chú thêm: thời tiết, kết quả quan sát, vấn đề phát sinh
    # Example: "Trời mưa nhẹ buổi chiều, cần theo dõi hiệu quả"
    
    # ========== TIMESTAMPS ==========
    ngay_tao = Column(TIMESTAMP, server_default=func.now())
    # Ngày tạo record (thời điểm ghi nhật ký)
    
    ngay_cap_nhat = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    # Ngày cập nhật cuối (khi chỉnh sửa)
    
    # ========== RELATIONSHIPS ==========
    loai_hoat_dong = relationship("LoaiHoatDong", back_populates="lich_su")
    # Relationship với LoaiHoatDong (many-to-one)
    # Usage: lich_su.loai_hoat_dong.ten_loai → get tên loại hoạt động

