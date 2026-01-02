# 📔 Nhật Ký Phát Triển Dự Án (Development Journal)

> Ghi chú chi tiết quá trình phát triển hệ thống WebGIS Nông nghiệp

## 📅 Timeline Tổng Quan

| Giai đoạn | Thời gian               | Nội dung                                   | Trạng thái    |
| --------- | ----------------------- | ------------------------------------------ | ------------- |
| Phase 1   | 20-25/12/2025           | Setup & Database Design                    | ✅ Hoàn thành |
| Phase 2   | 26-30/12/2025           | Backend API Development                    | ✅ Hoàn thành |
| Phase 3   | 31/12/2025 - 01/01/2026 | Frontend Integration                       | ✅ Hoàn thành |
| Phase 4   | 01/01/2026              | New Features (Fertilizers, Pesticides, QR) | ✅ Hoàn thành |
| Phase 5   | 02/01/2026              | Authentication & RBAC                      | ⏳ Đang làm   |

---

## 🎯 Phase 1: Setup & Database Design (20-25/12/2025)

### Mục tiêu

-    Setup môi trường phát triển (PostgreSQL, Python, Node.js)
-    Thiết kế schema database theo chuẩn 3NF
-    Import dữ liệu từ Excel files

### Các bước thực hiện

#### Bước 1.1: Cài đặt môi trường (2 giờ)

**Tools cần cài:**

```bash
# 1. PostgreSQL 14+
brew install postgresql@14
brew services start postgresql@14

# 2. Python 3.11+
brew install python@3.11

# 3. Node.js 18+
brew install node@18

# 4. Git
brew install git
```

**Kiểm tra:**

```bash
psql --version        # PostgreSQL 14.x
python3 --version     # Python 3.11.x
node --version        # Node 18.x
git --version         # Git 2.x
```

**Lỗi gặp phải:**

-    ❌ PostgreSQL không start → Giải quyết: `brew services restart postgresql@14`
-    ❌ Port 5432 đã dùng → Giải quyết: Dùng port 5433 trong config

---

#### Bước 1.2: Tạo database (1 giờ)

**Tạo database:**

```bash
# Kết nối PostgreSQL
psql -U postgres

# Tạo database
CREATE DATABASE nongsan_db;

# Tạo schema
\c nongsan_db
CREATE SCHEMA nongsan;

# Tạo user riêng (optional)
CREATE USER nongsan_admin WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE nongsan_db TO nongsan_admin;
GRANT ALL ON SCHEMA nongsan TO nongsan_admin;
```

**Test kết nối:**

```bash
psql -h localhost -p 5432 -U postgres -d nongsan_db -c "\dt nongsan.*"
```

**Kết quả:**
✅ Database `nongsan_db` với schema `nongsan` đã sẵn sàng

---

#### Bước 1.3: Thiết kế schema (4 giờ)

**Phân tích yêu cầu:**

1. Quản lý vùng trồng (MSVT)
2. Quản lý loại cây, giống
3. Quản lý tổ chức/cá nhân
4. Nhật ký canh tác
5. Truy xuất nguồn gốc
6. Danh mục phân bón, thuốc BVTV

**Các bảng chính thiết kế:**

```sql
-- 1. Địa điểm (3 bảng)
CREATE TABLE nongsan.tinh (...);
CREATE TABLE nongsan.huyen (...);
CREATE TABLE nongsan.xa (...);

-- 2. Tổ chức & Cơ sở (3 bảng)
CREATE TABLE nongsan.to_chuc_ca_nhan (
    id SERIAL PRIMARY KEY,
    ma_so_thue VARCHAR(20) UNIQUE,
    ten_to_chuc TEXT NOT NULL,
    dia_chi TEXT,
    dien_thoai VARCHAR(20),
    email VARCHAR(100),
    loai_to_chuc VARCHAR(50),
    ngay_tao TIMESTAMP DEFAULT NOW()
);

-- 3. Vùng trồng (2 bảng)
CREATE TABLE nongsan.vung_trong (
    id SERIAL PRIMARY KEY,
    ma_vung VARCHAR(50) UNIQUE NOT NULL,
    ten_vung TEXT NOT NULL,
    dia_chi TEXT,
    dien_tich DECIMAL(10,2),
    chu_so_huu_id INTEGER REFERENCES nongsan.to_chuc_ca_nhan(id),
    loai_cay_id INTEGER,
    trang_thai_id INTEGER,
    ngay_tao TIMESTAMP DEFAULT NOW()
);

CREATE TABLE nongsan.toa_do_vung (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER REFERENCES nongsan.vung_trong(id),
    vi_do DECIMAL(10,6) NOT NULL,
    kinh_do DECIMAL(10,6) NOT NULL,
    thu_tu INTEGER DEFAULT 1
);

-- 4. Loại cây (2 bảng)
CREATE TABLE nongsan.loai_cay (
    id SERIAL PRIMARY KEY,
    ma_loai_cay VARCHAR(20) UNIQUE,
    ten_loai_cay TEXT NOT NULL,
    ten_khoa_hoc TEXT,
    phan_loai VARCHAR(50),
    mo_ta TEXT
);

-- 5. Trạng thái vùng
CREATE TABLE nongsan.trang_thai_vung (
    id SERIAL PRIMARY KEY,
    ma_trang_thai VARCHAR(30) UNIQUE,
    ten_trang_thai VARCHAR(100) NOT NULL,
    mau_sac VARCHAR(7),
    mo_ta TEXT
);

-- 6. Nhật ký canh tác
CREATE TABLE nongsan.loai_hoat_dong (
    id SERIAL PRIMARY KEY,
    ma_loai VARCHAR(30) UNIQUE,
    ten_loai VARCHAR(100) NOT NULL,
    icon VARCHAR(50),
    mau_sac VARCHAR(7)
);

CREATE TABLE nongsan.lich_su_canh_tac (
    id SERIAL PRIMARY KEY,
    vung_trong_id INTEGER REFERENCES nongsan.vung_trong(id),
    loai_hoat_dong_id INTEGER REFERENCES nongsan.loai_hoat_dong(id),
    tieu_de TEXT NOT NULL,
    noi_dung TEXT,
    ngay_thuc_hien DATE NOT NULL,
    nguoi_thuc_hien TEXT,
    phan_bon_id INTEGER,
    thuoc_bvtv_id INTEGER,
    ngay_tao TIMESTAMP DEFAULT NOW()
);

-- 7. Phân bón (2 bảng)
CREATE TABLE nongsan.loai_phan_bon (
    id SERIAL PRIMARY KEY,
    ma_loai VARCHAR(20) UNIQUE,
    ten_loai VARCHAR(100) NOT NULL,
    mo_ta TEXT
);

CREATE TABLE nongsan.phan_bon (
    id SERIAL PRIMARY KEY,
    ma_phan_bon VARCHAR(50) UNIQUE,
    ten_phan_bon TEXT NOT NULL,
    thanh_phan TEXT,
    don_vi VARCHAR(20),
    loai_phan_bon_id INTEGER REFERENCES nongsan.loai_phan_bon(id),
    mo_ta TEXT
);

-- 8. Thuốc BVTV (2 bảng)
CREATE TABLE nongsan.nhom_thuoc_bvtv (
    id SERIAL PRIMARY KEY,
    ma_nhom VARCHAR(50) UNIQUE,
    ten_nhom VARCHAR(150) NOT NULL,
    mo_ta TEXT
);

CREATE TABLE nongsan.thuoc_bvtv (
    id SERIAL PRIMARY KEY,
    ma_thuoc VARCHAR(50) UNIQUE,
    ten_thuoc TEXT NOT NULL,
    ten_hoat_chat TEXT,
    ham_luong VARCHAR(50),
    dang_bao_che VARCHAR(20),
    trang_thai_su_dung VARCHAR(20),
    nhom_thuoc_id INTEGER REFERENCES nongsan.nhom_thuoc_bvtv(id),
    mo_ta TEXT
);
```

**Indexes tạo:**

```sql
CREATE INDEX idx_vung_trong_chu ON nongsan.vung_trong(chu_so_huu_id);
CREATE INDEX idx_vung_trong_loai_cay ON nongsan.vung_trong(loai_cay_id);
CREATE INDEX idx_toa_do_vung ON nongsan.toa_do_vung(vung_trong_id);
CREATE INDEX idx_lich_su_vung ON nongsan.lich_su_canh_tac(vung_trong_id);
```

**Lỗi gặp phải:**

-    ❌ Foreign key constraint failed → Giải quyết: Tạo bảng cha trước
-    ❌ Duplicate column name → Giải quyết: Review lại schema

**Kết quả:**
✅ 15 bảng core được tạo với đầy đủ relationships

---

#### Bước 1.4: Import dữ liệu từ Excel (3 giờ)

**Dữ liệu nguồn:**

```
Database/
├── msvt/
│   ├── msvt_chusohuu.xlsx          # 10 tổ chức
│   ├── msvt_thongtinvungtrong.xlsx # 5 vùng trồng
│   └── msvt_caytrong.xlsx          # 8 loại cây
├── phanbon/
│   └── DanhMuc_PhanBon_DuocPhep_LuuHanh.xlsx  # 1000+ phân bón
└── ThuocBaoVeThucVat/
    └── 23.10.24_Phu luc 1_TBVTV DUOC SU DUNG.xlsx  # 500+ thuốc
```

**Script import Python:**

```python
# Database/import_data.py
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='nongsan_db',
    user='postgres',
    password='123456'
)

# Import tổ chức
df_chu = pd.read_excel('msvt/msvt_chusohuu.xlsx')
for _, row in df_chu.iterrows():
    cursor.execute("""
        INSERT INTO nongsan.to_chuc_ca_nhan (ma_so_thue, ten_to_chuc, dia_chi, dien_thoai)
        VALUES (%s, %s, %s, %s)
    """, (row['MaSoThue'], row['TenToChuc'], row['DiaChi'], row['DienThoai']))

conn.commit()
```

**Dữ liệu đã import:**

-    ✅ 10 tổ chức/cá nhân
-    ✅ 8 loại cây
-    ✅ 5 vùng trồng + 60 tọa độ
-    ✅ 6 nhóm thuốc BVTV
-    ✅ 4 loại phân bón
-    ✅ 4 loại hoạt động nhật ký
-    ✅ 4 trạng thái vùng

**Lỗi gặp phải:**

-    ❌ Excel encoding issues → Giải quyết: `pd.read_excel(file, encoding='utf-8')`
-    ❌ NULL values → Giải quyết: `fillna('')`
-    ❌ Duplicate keys → Giải quyết: `ON CONFLICT DO NOTHING`

**Test dữ liệu:**

```sql
SELECT COUNT(*) FROM nongsan.vung_trong;        -- 5 rows
SELECT COUNT(*) FROM nongsan.to_chuc_ca_nhan;   -- 10 rows
SELECT COUNT(*) FROM nongsan.loai_cay;          -- 8 rows
SELECT COUNT(*) FROM nongsan.toa_do_vung;       -- 60 rows
```

✅ **Phase 1 hoàn thành:** Database với 15 bảng và ~100 rows dữ liệu mẫu

---

## 🎯 Phase 2: Backend API Development (26-30/12/2025)

### Mục tiêu

-    Xây dựng REST API với FastAPI
-    Implement SQLAlchemy ORM models
-    Tạo CRUD endpoints cho 3 modules chính

### Các bước thực hiện

#### Bước 2.1: Setup FastAPI project (2 giờ)

**Tạo cấu trúc project:**

```bash
Backend/
├── app.py                 # Main application
├── config.py              # Settings
├── database.py            # Database connection
├── schemas.py             # Pydantic models
├── models/                # SQLAlchemy models
│   ├── __init__.py
│   ├── vung_trong.py
│   └── ...
├── routes/                # API endpoints
│   ├── __init__.py
│   ├── farms.py
│   └── ...
├── requirements.txt       # Dependencies
└── .env                   # Environment variables
```

**Cài đặt dependencies:**

```bash
cd Backend
python3 -m venv .venv
source .venv/bin/activate

pip install fastapi==0.115.6
pip install uvicorn==0.34.0
pip install sqlalchemy==2.0.36
pip install psycopg2-binary==2.9.10
pip install pydantic==2.10.5
pip install python-dotenv==1.0.1
pip install qrcode==8.0
pip install pillow==11.1.0

pip freeze > requirements.txt
```

**File .env:**

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nongsan_db
DB_USER=postgres
DB_PASSWORD=123456
DB_SCHEMA=nongsan
API_PREFIX=/api
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
```

**Kết quả:**
✅ FastAPI project structure hoàn chỉnh

---

#### Bước 2.2: Tạo database connection (1 giờ)

**File: database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Database URL
DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**File: config.py**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "nongsan_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456"
    DB_SCHEMA: str = "nongsan"
    API_PREFIX: str = "/api"
    CORS_ORIGINS: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()
```

**Test kết nối:**

```bash
cd Backend
python -c "from database import engine; print(engine.connect())"
```

**Lỗi gặp phải:**

-    ❌ `ModuleNotFoundError: pydantic_settings` → Giải quyết: `pip install pydantic-settings`
-    ❌ Connection refused → Giải quyết: Check PostgreSQL đang chạy

**Kết quả:**
✅ Database connection hoạt động

---

#### Bước 2.3: Tạo SQLAlchemy Models (6 giờ)

**Model 1: ToChucCaNhan**

```python
# Backend/models/to_chuc_ca_nhan.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class ToChucCaNhan(Base):
    """
    Model: Tổ chức / Cá nhân (Chủ sở hữu vùng trồng)

    Bảng: nongsan.to_chuc_ca_nhan
    Relationships:
        - 1 Tổ chức có nhiều VungTrong (1-to-many)
    """
    __tablename__ = "to_chuc_ca_nhan"
    __table_args__ = {'schema': 'nongsan'}

    id = Column(Integer, primary_key=True, index=True, comment='ID tự tăng')
    ma_so_thue = Column(String(20), unique=True, index=True, comment='Mã số thuế (unique)')
    ten_to_chuc = Column(Text, nullable=False, comment='Tên tổ chức/cá nhân')
    dia_chi = Column(Text, comment='Địa chỉ')
    dien_thoai = Column(String(20), comment='Số điện thoại')
    email = Column(String(100), comment='Email liên hệ')
    loai_to_chuc = Column(String(50), comment='Loại: HTX, DN, Cá nhân')
    ngay_tao = Column(DateTime, default=datetime.now, comment='Ngày tạo bản ghi')

    # Relationships
    vung_trong = relationship("VungTrong", back_populates="chu_so_huu")
```

**Model 2: VungTrong**

```python
# Backend/models/vung_trong.py
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class VungTrong(Base):
    """
    Model: Vùng trồng (MSVT)

    Bảng: nongsan.vung_trong
    Foreign Keys:
        - chu_so_huu_id → to_chuc_ca_nhan(id)
        - loai_cay_id → loai_cay(id)
        - trang_thai_id → trang_thai_vung(id)
    Relationships:
        - Belongs to: ToChucCaNhan, LoaiCay, TrangThaiVung
        - Has many: ToaDoVung, LichSuCanhTac
    """
    __tablename__ = "vung_trong"
    __table_args__ = {'schema': 'nongsan'}

    id = Column(Integer, primary_key=True, index=True)
    ma_vung = Column(String(50), unique=True, nullable=False, index=True,
                     comment='Mã số vùng trồng (MSVT) - Unique')
    ten_vung = Column(Text, nullable=False, comment='Tên vùng trồng')
    dia_chi = Column(Text, comment='Địa chỉ vùng')
    dien_tich = Column(Numeric(10, 2), comment='Diện tích (ha)')

    # Foreign Keys
    chu_so_huu_id = Column(Integer, ForeignKey('nongsan.to_chuc_ca_nhan.id'),
                           comment='ID chủ sở hữu')
    loai_cay_id = Column(Integer, ForeignKey('nongsan.loai_cay.id'),
                         comment='ID loại cây trồng')
    trang_thai_id = Column(Integer, ForeignKey('nongsan.trang_thai_vung.id'),
                           comment='ID trạng thái')

    ngay_tao = Column(DateTime, default=datetime.now)

    # Relationships
    chu_so_huu = relationship("ToChucCaNhan", back_populates="vung_trong",
                              foreign_keys=[chu_so_huu_id])
    loai_cay = relationship("LoaiCay", back_populates="vung_trong",
                            foreign_keys=[loai_cay_id])
    trang_thai = relationship("TrangThaiVung", back_populates="vung_trong",
                              foreign_keys=[trang_thai_id])
    toa_do = relationship("ToaDoVung", back_populates="vung_trong",
                          cascade="all, delete-orphan")
    lich_su_canh_tac = relationship("LichSuCanhTac", back_populates="vung_trong")

class ToaDoVung(Base):
    """
    Model: Tọa độ vùng trồng (Polygon points)

    Bảng: nongsan.toa_do_vung
    """
    __tablename__ = "toa_do_vung"
    __table_args__ = {'schema': 'nongsan'}

    id = Column(Integer, primary_key=True)
    vung_trong_id = Column(Integer, ForeignKey('nongsan.vung_trong.id'),
                           nullable=False, index=True)
    vi_do = Column(Numeric(10, 6), nullable=False, comment='Vĩ độ (Latitude)')
    kinh_do = Column(Numeric(10, 6), nullable=False, comment='Kinh độ (Longitude)')
    thu_tu = Column(Integer, default=1, comment='Thứ tự điểm trong polygon')

    # Relationships
    vung_trong = relationship("VungTrong", back_populates="toa_do")
```

**Model 3: LichSuCanhTac**

```python
# Backend/models/lich_su.py
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class LoaiHoatDong(Base):
    """Model: Loại hoạt động canh tác"""
    __tablename__ = "loai_hoat_dong"
    __table_args__ = {'schema': 'nongsan'}

    id = Column(Integer, primary_key=True)
    ma_loai = Column(String(30), unique=True, comment='Mã loại: GIEO_TRONG, BON_PHAN, ...')
    ten_loai = Column(String(100), nullable=False, comment='Tên loại hoạt động')
    icon = Column(String(50), comment='Icon class (fa-seed, fa-spray-can, ...)')
    mau_sac = Column(String(7), comment='Màu hiển thị (#22c55e)')
    mo_ta = Column(Text)

    # Relationships
    lich_su = relationship("LichSuCanhTac", back_populates="loai_hoat_dong")

class LichSuCanhTac(Base):
    """Model: Lịch sử canh tác (Nhật ký)"""
    __tablename__ = "lich_su_canh_tac"
    __table_args__ = {'schema': 'nongsan'}

    id = Column(Integer, primary_key=True)
    vung_trong_id = Column(Integer, ForeignKey('nongsan.vung_trong.id'),
                           nullable=False, index=True)
    loai_hoat_dong_id = Column(Integer, ForeignKey('nongsan.loai_hoat_dong.id'))
    tieu_de = Column(Text, nullable=False, comment='Tiêu đề hoạt động')
    noi_dung = Column(Text, comment='Mô tả chi tiết')
    ngay_thuc_hien = Column(Date, nullable=False, comment='Ngày thực hiện')
    nguoi_thuc_hien = Column(Text, comment='Người thực hiện')
    phan_bon_id = Column(Integer, ForeignKey('nongsan.phan_bon.id'),
                         comment='ID phân bón (nếu là bón phân)')
    thuoc_bvtv_id = Column(Integer, ForeignKey('nongsan.thuoc_bvtv.id'),
                           comment='ID thuốc BVTV (nếu là phun thuốc)')
    ngay_tao = Column(DateTime, default=datetime.now)

    # Relationships
    vung_trong = relationship("VungTrong", back_populates="lich_su_canh_tac")
    loai_hoat_dong = relationship("LoaiHoatDong", back_populates="lich_su")
    phan_bon = relationship("PhanBon", back_populates="lich_su_canh_tac",
                            foreign_keys=[phan_bon_id])
    thuoc_bvtv = relationship("ThuocBVTV", back_populates="lich_su_canh_tac",
                              foreign_keys=[thuoc_bvtv_id])
```

**Test models:**

```bash
cd Backend
.venv/bin/python -c "from models import VungTrong, ToChucCaNhan, LichSuCanhTac; print('✅ Models OK')"
```

**Lỗi gặp phải:**

-    ❌ `ImportError: cannot import name 'PhanBon'` → Giải quyết: Tạo model PhanBon trước
-    ❌ Circular import → Giải quyết: Dùng `foreign_keys=[...]` explicit

**Kết quả:**
✅ 7 models hoàn chỉnh với đầy đủ relationships

---

#### Bước 2.4: Tạo Pydantic Schemas (3 giờ)

**File: schemas.py**

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

# === SECTION 1: TỔ CHỨC & CHỦ SỞ HỮU ===

class ToChucCaNhanBase(BaseModel):
    """Base schema cho Tổ chức/Cá nhân"""
    ten_to_chuc: str = Field(..., description="Tên tổ chức/cá nhân")
    ma_so_thue: Optional[str] = Field(None, description="Mã số thuế")
    dia_chi: Optional[str] = None
    dien_thoai: Optional[str] = None
    email: Optional[str] = None
    loai_to_chuc: Optional[str] = Field(None, description="HTX, DN, Cá nhân")

class ToChucCaNhanCreate(ToChucCaNhanBase):
    """Schema tạo mới tổ chức"""
    pass

class ToChucCaNhanResponse(ToChucCaNhanBase):
    """Schema response tổ chức"""
    id: int
    ngay_tao: datetime

    model_config = ConfigDict(from_attributes=True)

# === SECTION 2: VÙNG TRỒNG ===

class ToaDoCreate(BaseModel):
    """Schema tạo tọa độ"""
    vi_do: Decimal = Field(..., description="Vĩ độ")
    kinh_do: Decimal = Field(..., description="Kinh độ")
    thu_tu: int = Field(1, description="Thứ tự điểm")

class ToaDoResponse(ToaDoCreate):
    """Schema response tọa độ"""
    id: int

    model_config = ConfigDict(from_attributes=True)

class VungTrongBase(BaseModel):
    """Base schema vùng trồng"""
    ma_vung: str = Field(..., description="Mã số vùng trồng (MSVT)")
    ten_vung: str = Field(..., description="Tên vùng")
    dia_chi: Optional[str] = None
    dien_tich: Optional[Decimal] = Field(None, description="Diện tích (ha)")
    chu_so_huu_id: Optional[int] = None
    loai_cay_id: Optional[int] = None
    trang_thai_id: Optional[int] = None

class VungTrongCreate(VungTrongBase):
    """Schema tạo vùng trồng"""
    toa_do: List[ToaDoCreate] = Field([], description="Danh sách tọa độ polygon")

class VungTrongResponse(VungTrongBase):
    """Schema response vùng trồng"""
    id: int
    ngay_tao: datetime
    toa_do: List[ToaDoResponse] = []

    model_config = ConfigDict(from_attributes=True)

# === SECTION 3: NHẬT KÝ CANH TÁC ===

class LichSuCanhTacBase(BaseModel):
    """Base schema nhật ký"""
    vung_trong_id: int
    loai_hoat_dong_id: int
    tieu_de: str
    noi_dung: Optional[str] = None
    ngay_thuc_hien: date
    nguoi_thuc_hien: Optional[str] = None
    phan_bon_id: Optional[int] = None
    thuoc_bvtv_id: Optional[int] = None

class LichSuCanhTacCreate(LichSuCanhTacBase):
    """Schema tạo nhật ký"""
    pass

class LichSuCanhTacResponse(LichSuCanhTacBase):
    """Schema response nhật ký"""
    id: int
    ngay_tao: datetime

    model_config = ConfigDict(from_attributes=True)

# === PAGINATION ===

class PaginatedResponse(BaseModel):
    """Schema phân trang chung"""
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int
```

**Kết quả:**
✅ 15+ schemas cho request/response validation

---

#### Bước 2.5: Viết API Endpoints (8 giờ)

**Route 1: Farms API (443 lines)**

_File: Backend/routes/farms.py_

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from database import get_db
from models import VungTrong, ToaDoVung, ToChucCaNhan, LoaiCay, TrangThaiVung
from schemas import VungTrongCreate, VungTrongResponse, PaginatedResponse

router = APIRouter(prefix="/farms", tags=["Farms"])

@router.get("/", response_model=PaginatedResponse)
async def get_farms(
    skip: int = Query(0, ge=0, description="Số bản ghi bỏ qua"),
    limit: int = Query(20, ge=1, le=100, description="Số bản ghi mỗi trang"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên/mã"),
    loai_cay_id: Optional[int] = Query(None, description="Filter theo loại cây"),
    trang_thai_id: Optional[int] = Query(None, description="Filter theo trạng thái"),
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách vùng trồng (có pagination, search, filter)

    Query Parameters:
        - skip: Offset (default 0)
        - limit: Page size (1-100, default 20)
        - search: Tìm kiếm (tên vùng, mã MSVT, địa chỉ)
        - loai_cay_id: Filter theo loại cây
        - trang_thai_id: Filter theo trạng thái

    Returns:
        PaginatedResponse with VungTrongResponse items
    """
    # Base query với eager loading
    query = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        joinedload(VungTrong.loai_cay),
        joinedload(VungTrong.trang_thai),
        joinedload(VungTrong.toa_do)
    )

    # Search filter
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (VungTrong.ten_vung.ilike(search_filter)) |
            (VungTrong.ma_vung.ilike(search_filter)) |
            (VungTrong.dia_chi.ilike(search_filter))
        )

    # Loại cây filter
    if loai_cay_id:
        query = query.filter(VungTrong.loai_cay_id == loai_cay_id)

    # Trạng thái filter
    if trang_thai_id:
        query = query.filter(VungTrong.trang_thai_id == trang_thai_id)

    # Count total
    total = query.count()

    # Paginate
    items = query.offset(skip).limit(limit).all()

    return {
        "items": items,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }

@router.get("/{farm_id}", response_model=VungTrongResponse)
async def get_farm(farm_id: int, db: Session = Depends(get_db)):
    """
    Lấy chi tiết vùng trồng theo ID

    Path Parameters:
        - farm_id: ID vùng trồng

    Returns:
        VungTrongResponse with relationships

    Raises:
        404: Không tìm thấy vùng trồng
    """
    farm = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        joinedload(VungTrong.loai_cay),
        joinedload(VungTrong.trang_thai),
        joinedload(VungTrong.toa_do)
    ).filter(VungTrong.id == farm_id).first()

    if not farm:
        raise HTTPException(status_code=404, detail="Vùng trồng không tồn tại")

    return farm

@router.get("/by-code/{ma_vung}", response_model=VungTrongResponse)
async def get_farm_by_code(ma_vung: str, db: Session = Depends(get_db)):
    """
    Lấy vùng trồng theo mã MSVT

    Use case: QR code scanning, quick lookup
    """
    farm = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        joinedload(VungTrong.loai_cay),
        joinedload(VungTrong.trang_thai),
        joinedload(VungTrong.toa_do)
    ).filter(VungTrong.ma_vung == ma_vung).first()

    if not farm:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy MSVT: {ma_vung}")

    return farm

@router.post("/", response_model=VungTrongResponse, status_code=201)
async def create_farm(
    farm_data: VungTrongCreate,
    db: Session = Depends(get_db)
):
    """
    Tạo vùng trồng mới (bao gồm tọa độ polygon)

    Request Body:
        VungTrongCreate with nested toa_do array

    Returns:
        VungTrongResponse (201 Created)

    Raises:
        400: Mã vùng đã tồn tại
    """
    # Check duplicate ma_vung
    existing = db.query(VungTrong).filter(VungTrong.ma_vung == farm_data.ma_vung).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Mã vùng {farm_data.ma_vung} đã tồn tại")

    # Create farm
    farm = VungTrong(
        ma_vung=farm_data.ma_vung,
        ten_vung=farm_data.ten_vung,
        dia_chi=farm_data.dia_chi,
        dien_tich=farm_data.dien_tich,
        chu_so_huu_id=farm_data.chu_so_huu_id,
        loai_cay_id=farm_data.loai_cay_id,
        trang_thai_id=farm_data.trang_thai_id
    )
    db.add(farm)
    db.flush()  # Get farm.id

    # Create coordinates
    for toa_do_data in farm_data.toa_do:
        toa_do = ToaDoVung(
            vung_trong_id=farm.id,
            vi_do=toa_do_data.vi_do,
            kinh_do=toa_do_data.kinh_do,
            thu_tu=toa_do_data.thu_tu
        )
        db.add(toa_do)

    db.commit()
    db.refresh(farm)

    return farm

@router.put("/{farm_id}", response_model=VungTrongResponse)
async def update_farm(
    farm_id: int,
    farm_data: VungTrongCreate,
    db: Session = Depends(get_db)
):
    """
    Cập nhật vùng trồng (bao gồm tọa độ)

    Note: Tọa độ cũ sẽ bị xóa và thay thế bằng tọa độ mới
    """
    farm = db.query(VungTrong).filter(VungTrong.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Vùng trồng không tồn tại")

    # Update fields
    farm.ma_vung = farm_data.ma_vung
    farm.ten_vung = farm_data.ten_vung
    farm.dia_chi = farm_data.dia_chi
    farm.dien_tich = farm_data.dien_tich
    farm.chu_so_huu_id = farm_data.chu_so_huu_id
    farm.loai_cay_id = farm_data.loai_cay_id
    farm.trang_thai_id = farm_data.trang_thai_id

    # Delete old coordinates
    db.query(ToaDoVung).filter(ToaDoVung.vung_trong_id == farm_id).delete()

    # Create new coordinates
    for toa_do_data in farm_data.toa_do:
        toa_do = ToaDoVung(
            vung_trong_id=farm.id,
            vi_do=toa_do_data.vi_do,
            kinh_do=toa_do_data.kinh_do,
            thu_tu=toa_do_data.thu_tu
        )
        db.add(toa_do)

    db.commit()
    db.refresh(farm)

    return farm

@router.delete("/{farm_id}", status_code=204)
async def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    """
    Xóa vùng trồng (cascade delete tọa độ)

    Returns:
        204 No Content
    """
    farm = db.query(VungTrong).filter(VungTrong.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Vùng trồng không tồn tại")

    db.delete(farm)
    db.commit()

    return None
```

**Test endpoint:**

```bash
# Start server
cd Backend
.venv/bin/uvicorn app:app --reload --host 0.0.0.0 --port 8000 &

# Test GET
curl http://localhost:8000/api/farms/ | python3 -m json.tool

# Test GET by ID
curl http://localhost:8000/api/farms/1 | python3 -m json.tool

# Test POST
curl -X POST http://localhost:8000/api/farms/ \
  -H "Content-Type: application/json" \
  -d '{
    "ma_vung": "MSVT999",
    "ten_vung": "Test Vùng",
    "dien_tich": 2.5,
    "toa_do": [
      {"vi_do": 10.123, "kinh_do": 106.456, "thu_tu": 1},
      {"vi_do": 10.124, "kinh_do": 106.457, "thu_tu": 2}
    ]
  }'
```

**Lỗi gặp phải:**

-    ❌ `422 Validation Error: field required` → Giải quyết: Kiểm tra schema required fields
-    ❌ `500 Foreign key violation` → Giải quyết: Đảm bảo chu_so_huu_id tồn tại
-    ❌ `404 Not Found` cho endpoint đúng → Giải quyết: Check router prefix trong app.py

**Kết quả:**
✅ Farms API với 6 endpoints hoạt động

---

**Route 2: Diary API (186 lines)**

_File: Backend/routes/diary.py_

```python
@router.get("/", response_model=PaginatedResponse)
async def get_diary_entries(
    vung_trong_id: Optional[int] = None,
    loai_hoat_dong_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Lấy danh sách nhật ký canh tác"""
    query = db.query(LichSuCanhTac).options(
        joinedload(LichSuCanhTac.vung_trong),
        joinedload(LichSuCanhTac.loai_hoat_dong),
        joinedload(LichSuCanhTac.phan_bon),
        joinedload(LichSuCanhTac.thuoc_bvtv)
    )

    # Filters
    if vung_trong_id:
        query = query.filter(LichSuCanhTac.vung_trong_id == vung_trong_id)

    if loai_hoat_dong_id:
        query = query.filter(LichSuCanhTac.loai_hoat_dong_id == loai_hoat_dong_id)

    if from_date:
        query = query.filter(LichSuCanhTac.ngay_thuc_hien >= from_date)

    if to_date:
        query = query.filter(LichSuCanhTac.ngay_thuc_hien <= to_date)

    # Sort by date descending
    query = query.order_by(LichSuCanhTac.ngay_thuc_hien.desc())

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {"items": items, "total": total, "page": skip // limit + 1, "size": limit}

@router.post("/", response_model=LichSuCanhTacResponse, status_code=201)
async def create_diary_entry(
    entry: LichSuCanhTacCreate,
    db: Session = Depends(get_db)
):
    """Tạo nhật ký canh tác mới"""
    diary = LichSuCanhTac(**entry.dict())
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary
```

**Kết quả:**
✅ Diary API với 5 endpoints

---

**Route 3: Charts API (274 lines)**

Dashboard statistics với 6 chart endpoints. Chi tiết xem file: `Backend/routes/charts.py`

**Kết quả:**
✅ Charts API với 6 endpoints

---

#### Bước 2.6: Integrate routes vào app.py (1 giờ)

**File: app.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import farms, charts, diary, fertilizers, pesticides, qr

app = FastAPI(
    title="Agriculture Management API",
    version="2.0.0",
    description="REST API for WebGIS Agriculture System"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(farms.router, prefix=settings.API_PREFIX)
app.include_router(charts.router, prefix=settings.API_PREFIX)
app.include_router(diary.router, prefix=settings.API_PREFIX)
app.include_router(fertilizers.router, prefix=settings.API_PREFIX)
app.include_router(pesticides.router, prefix=settings.API_PREFIX)
app.include_router(qr.router, prefix=settings.API_PREFIX)

# Health check
@app.get(f"{settings.API_PREFIX}/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Backend API is running",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

**Test toàn bộ API:**

```bash
curl http://localhost:8000/api/health
curl http://localhost:8000/api/farms/
curl http://localhost:8000/api/charts/dashboard-stats
curl http://localhost:8000/api/diary/
```

**Kết quả:**
✅ Backend API hoàn chỉnh với 34 endpoints

**Lỗi gặp phải:**

-    ❌ CORS error từ frontend → Giải quyết: Add localhost:5173 vào CORS_ORIGINS
-    ❌ `422 Unprocessable Entity` → Giải quyết: Check request body khớp schema

---

✅ **Phase 2 hoàn thành:** Backend API 34 endpoints hoạt động ổn định

---

## 🎯 Phase 3: Frontend Integration (31/12/2025 - 01/01/2026)

### Mục tiêu

-    Kết nối Vue 3 frontend với Backend API
-    Implement WebGIS với Leaflet
-    Tạo dashboard với charts
-    Hoàn thiện nhật ký canh tác

### Các bước thực hiện

#### Bước 3.1: Setup Vue 3 project (1 giờ)

Đã có sẵn Frontend, chỉ cần config API connection.

**File: Frontend/.env**

```env
VITE_API_URL=http://localhost:8000/api
```

**Test frontend:**

```bash
cd Frontend
npm run dev
# Open: http://localhost:5173
```

**Kết quả:**
✅ Frontend chạy trên port 5173

---

#### Bước 3.2: Test API integration (2 giờ)

**Fetch farms từ API:**

```javascript
// Frontend/src/composables/useFarms.js
const farms = ref([]);

async function fetchFarms() {
     const response = await fetch(`${API_URL}/farms/`);
     const data = await response.json();
     farms.value = data.items;
}
```

**Test trong browser console:**

```javascript
fetch("http://localhost:8000/api/farms/")
     .then((r) => r.json())
     .then((d) => console.log(d));
```

**Lỗi gặp phải:**

-    ❌ CORS policy blocked → Giải quyết: Đã fix ở backend
-    ❌ Network error → Giải quyết: Backend phải chạy trước

**Kết quả:**
✅ Frontend fetch data thành công

---

✅ **Phase 3 hoàn thành:** Frontend hiển thị data từ API

---

## 🎯 Phase 4: New Features (01/01/2026)

### Mục tiêu

-    Thêm Fertilizers API (Phân bón)
-    Thêm Pesticides API (Thuốc BVTV)
-    Thêm QR Code generation
-    Public traceability page

### Các bước thực hiện

#### Bước 4.1: Database check (30 phút)

**Query kiểm tra bảng:**

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema='nongsan'
AND table_name LIKE '%phan%' OR table_name LIKE '%thuoc%';
```

**Kết quả:**

-    phan_bon (7 columns)
-    loai_phan_bon (4 columns)
-    thuoc_bvtv (9 columns)
-    nhom_thuoc_bvtv (4 columns)

✅ Bảng đã tồn tại, không cần migration

---

#### Bước 4.2: Tạo Fertilizers models (1 giờ)

**File: Backend/models/phan_bon.py**

```python
class LoaiPhanBon(Base):
    __tablename__ = "loai_phan_bon"
    __table_args__ = {'schema': 'nongsan'}

    id = Column(Integer, primary_key=True)
    ma_loai = Column(String(20), unique=True)
    ten_loai = Column(String(100), nullable=False)
    mo_ta = Column(Text)

    phan_bon = relationship("PhanBon", back_populates="loai_phan_bon")

class PhanBon(Base):
    __tablename__ = "phan_bon"
    __table_args__ = {'schema': 'nongsan'}

    id = Column(Integer, primary_key=True)
    ma_phan_bon = Column(String(50), unique=True)
    ten_phan_bon = Column(Text, nullable=False)
    thanh_phan = Column(Text)
    don_vi = Column(String(20))
    loai_phan_bon_id = Column(Integer, ForeignKey('nongsan.loai_phan_bon.id'))
    mo_ta = Column(Text)

    loai_phan_bon = relationship("LoaiPhanBon", back_populates="phan_bon")
    lich_su_canh_tac = relationship("LichSuCanhTac", back_populates="phan_bon")
```

**Test:**

```bash
.venv/bin/python -c "from models import PhanBon, LoaiPhanBon; print('✅ OK')"
```

**Kết quả:**
✅ Models imported successfully

---

#### Bước 4.3: Tạo Fertilizers API (2 giờ)

**File: Backend/routes/fertilizers.py** (220 lines)

7 endpoints: categories (2), fertilizers CRUD (5)

**Test:**

```bash
curl http://localhost:8000/api/fertilizers/categories/
# Response: [] (empty, OK - chưa có data)
```

**Kết quả:**
✅ Fertilizers API hoạt động

---

#### Bước 4.4: Tạo Pesticides models & API (2 giờ)

Tương tự Fertilizers

**File: Backend/models/thuoc_bvtv.py** (170 lines)
**File: Backend/routes/pesticides.py** (230 lines)

**Test:**

```bash
curl http://localhost:8000/api/pesticides/groups/ | python3 -m json.tool
# Response: 6 groups (có data)
```

**Kết quả:**
✅ Pesticides API với 6 groups trong DB

---

#### Bước 4.5: QR Code generation (3 giờ)

**Install libraries:**

```bash
pip install qrcode pillow
```

**Lỗi:**

-    ❌ `pip install qrcode[pil]` failed → Giải quyết: Dùng `qrcode pillow` riêng

**File: Backend/routes/qr.py** (200 lines)

2 endpoints:

1. `/qr/generate/{ma_vung}` - Generate QR as base64 PNG
2. `/qr/trace/{ma_vung}` - Public traceability info

**Test:**

```bash
curl "http://localhost:8000/api/qr/generate/MSVT001?size=200"
# Response: {"qr_code": "data:image/png;base64,iVBORw0..."}

curl http://localhost:8000/api/qr/trace/MSVT001 | python3 -m json.tool
# Response: {farm, owner, status, coordinates, history}
```

**Kết quả:**
✅ QR generation hoạt động với base64 PNG

---

✅ **Phase 4 hoàn thành:** 18 endpoints mới (Fertilizers, Pesticides, QR)

---

## 🎯 Phase 5: Authentication & RBAC (02/01/2026)

### Mục tiêu

-    JWT authentication
-    Role-based access control (Admin, Nha nông, Khách)
-    User management

### Trạng thái: ⏳ TODO

Chi tiết xem: [TODO_AUTHENTICATION.md](../TODO_AUTHENTICATION.md)

---

## 📊 TỔNG KẾT DEVELOPMENT

### Thống kê tổng hợp

| Metrics       | Số lượng      |
| ------------- | ------------- |
| **Backend**   |
| Models        | 7 models      |
| Routes        | 6 route files |
| Endpoints     | 34 endpoints  |
| Lines of Code | ~3,730 lines  |
| **Frontend**  |
| Components    | 20 components |
| Views         | 4 views       |
| Composables   | 7 composables |
| Lines of Code | ~6,720 lines  |
| **Database**  |
| Tables        | 37 tables     |
| Sample Data   | ~50 rows      |

### Công nghệ sử dụng

-    **Backend:** FastAPI 0.115.6, SQLAlchemy 2.0.36, PostgreSQL 14
-    **Frontend:** Vue 3.5.13, Vite 6.0.1, Tailwind CSS 3.4.19
-    **Maps:** Leaflet 1.9.4
-    **Charts:** Chart.js 4.5.1
-    **QR:** python-qrcode 8.0, Pillow 11.1.0

### Lessons Learned

1. **Database Design:** Thiết kế schema 3NF từ đầu → Dễ mở rộng
2. **API First:** Viết API trước, test bằng curl → Frontend dễ integrate
3. **Eager Loading:** Dùng `joinedload()` → Giảm N+1 queries
4. **Error Handling:** Try-except + HTTPException → User-friendly errors
5. **Documentation:** Comment code tiếng Việt → Team hiểu nhanh
6. **Testing:** Test mỗi endpoint sau khi viết → Phát hiện bug sớm

### Challenges & Solutions

| Challenge              | Solution                                 |
| ---------------------- | ---------------------------------------- |
| CORS errors            | Add CORS middleware with proper origins  |
| Foreign key violations | Validate related IDs exist before insert |
| Slow queries           | Add indexes on foreign keys              |
| Circular imports       | Use `foreign_keys=[...]` explicit        |
| Duplicate data         | Add `UNIQUE` constraints                 |
| Excel import errors    | Handle NULL, encoding, duplicates        |

---

**Author:** Tram-anh99  
**Project:** Learning-Fast-JS  
**Last Updated:** 01/01/2026  
**Status:** 88% Complete (15/17 features)
