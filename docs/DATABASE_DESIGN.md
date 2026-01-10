# Database Design Documentation

## Hệ Thống Quản Lý Nông Nghiệp & Truy Xuất Nguồn Gốc

**Version:** 2.0  
**Last Updated:** January 10, 2026  
**Database:** PostgreSQL 16  
**Schema:** nongsan

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Entity Relationship Diagram](#entity-relationship-diagram)
3. [Table Specifications](#table-specifications)
4. [Relationships](#relationships)
5. [Indexes & Constraints](#indexes--constraints)
6. [Views](#views)
7. [Data Dictionary](#data-dictionary)

---

## 🎯 Overview

### Purpose

Hệ thống quản lý toàn diện các vùng trồng trọt, nhật ký canh tác, cơ sở sản xuất, và truy xuất nguồn gốc nông sản tại Việt Nam.

### Key Features

-    ✅ Quản lý vùng trồng và cây trồng
-    ✅ Nhật ký hoạt động canh tác (gieo trồng, tưới nước, bón phân, thu hoạch)
-    ✅ Quản lý cơ sở sản xuất (đóng gói, phân bón, thuốc BVTV, giống)
-    ✅ Truy xuất nguồn gốc qua QR code
-    ✅ Tích hợp tọa độ địa lý (GIS)
-    ✅ Quản lý chứng nhận & tiêu chuẩn

### Database Statistics

-    **Total Tables:** 31 (26 data tables + 5 views)
-    **Total Records:** ~45,000+
-    **Schema:** nongsan
-    **Encoding:** UTF8
-    **Collation:** vi_VN.UTF-8

---

## 📊 Entity Relationship Diagram

### Core Entities

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOCATION HIERARCHY                            │
│                                                                   │
│  ┌──────┐      ┌───────┐      ┌──────┐                          │
│  │ tinh │──────│ huyen │──────│  xa  │                          │
│  └──────┘      └───────┘      └──────┘                          │
│     │              │              │                               │
│     │              │              │                               │
│     └──────────────┴──────────────┘                              │
│                    │                                              │
│                    ▼                                              │
│              ┌──────────┐                                         │
│              │ vung_trong│◄──────┐                               │
│              └──────────┘        │                               │
│                    │              │                               │
│                    │              │                               │
│     ┌──────────────┼──────────────┼──────────┐                  │
│     │              │              │           │                   │
│     ▼              ▼              ▼           ▼                   │
│ ┌────────┐  ┌──────────┐  ┌─────────┐  ┌─────────┐             │
│ │ loai_  │  │  vung_   │  │  toa_do_│  │lich_su_ │             │
│ │  cay   │  │cay_trong │  │  vung   │  │canh_tac │             │
│ └────────┘  └──────────┘  └─────────┘  └─────────┘             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    FACILITY MANAGEMENT                           │
│                                                                   │
│              ┌──────────────┐                                    │
│              │   co_so      │                                    │
│              │  (Base)      │                                    │
│              └──────────────┘                                    │
│                    │                                              │
│     ┌──────────────┼──────────────┬──────────────┐              │
│     │              │              │               │              │
│     ▼              ▼              ▼               ▼              │
│ ┌────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│ │co_so_  │  │  co_so_  │  │  co_so_  │  │  co_so_  │          │
│ │dong_goi│  │ phan_bon │  │thuoc_bvtv│  │  giong   │          │
│ └────────┘  └──────────┘  └──────────┘  └──────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  PRODUCT CATALOGUES                              │
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │phan_bon  │    │thuoc_bvtv│    │giong_cay │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│       │               │                │                          │
│       ▼               ▼                ▼                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │loai_phan_│    │nhom_thuoc│    │giong_bao │                  │
│  │   bon    │    │  _bvtv   │    │   _ho    │                  │
│  └──────────┘    └──────────┘    └──────────┘                  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    TRACEABILITY                                  │
│                                                                   │
│  ┌──────────┐                                                    │
│  │vung_trong│                                                    │
│  └──────────┘                                                    │
│       │                                                           │
│       │ ma_vung (QR Code)                                        │
│       │                                                           │
│       ▼                                                           │
│  ┌──────────┐                                                    │
│  │lich_su_  │                                                    │
│  │canh_tac  │  ───► Truy xuất nguồn gốc                         │
│  └──────────┘                                                    │
│       │                                                           │
│       └─► Show: Giống cây, Hoạt động, Phân bón, Thuốc BVTV     │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📐 Table Specifications

### 1. Location Tables (Địa danh)

#### `tinh` (Provinces)

Quản lý 63 tỉnh/thành phố Việt Nam.

| Column   | Type          | Constraints      | Description                |
| -------- | ------------- | ---------------- | -------------------------- |
| id       | SERIAL        | PRIMARY KEY      | ID tự tăng                 |
| ten_tinh | VARCHAR(100)  | NOT NULL, UNIQUE | Tên tỉnh                   |
| x        | DECIMAL(11,8) | NULL             | Longitude (tọa độ kinh độ) |
| y        | DECIMAL(10,8) | NULL             | Latitude (tọa độ vĩ độ)    |
| ngay_tao | TIMESTAMP     | DEFAULT NOW()    | Ngày tạo record            |

**Sample Data:**

```sql
INSERT INTO nongsan.tinh (ten_tinh, x, y) VALUES
('Đắk Lắk', 108.2, 12.7),
('Gia Lai', 108.0, 13.9);
```

**Notes:**

-    Dropped column `ma_tinh` (Jan 10, 2026)
-    Added `x, y` coordinates for GeoJSON support

#### `huyen` (Districts)

Quản lý huyện/quận thuộc các tỉnh.

| Column    | Type          | Constraints            | Description    |
| --------- | ------------- | ---------------------- | -------------- |
| id        | SERIAL        | PRIMARY KEY            | ID tự tăng     |
| ten_huyen | VARCHAR(100)  | NOT NULL               | Tên huyện      |
| tinh_id   | INTEGER       | FOREIGN KEY → tinh(id) | Thuộc tỉnh nào |
| x         | DECIMAL(11,8) | NULL                   | Longitude      |
| y         | DECIMAL(10,8) | NULL                   | Latitude       |
| ngay_tao  | TIMESTAMP     | DEFAULT NOW()          | Ngày tạo       |

**Relationships:**

-    `tinh_id` → `tinh.id` (ON DELETE CASCADE)

#### `xa` (Communes)

Quản lý xã/phường thuộc các huyện.

| Column   | Type          | Constraints             | Description   |
| -------- | ------------- | ----------------------- | ------------- |
| id       | SERIAL        | PRIMARY KEY             | ID tự tăng    |
| ten_xa   | VARCHAR(100)  | NOT NULL                | Tên xã/phường |
| huyen_id | INTEGER       | FOREIGN KEY → huyen(id) | Thuộc huyện   |
| x        | DECIMAL(11,8) | NULL                    | Longitude     |
| y        | DECIMAL(10,8) | NULL                    | Latitude      |
| ngay_tao | TIMESTAMP     | DEFAULT NOW()           | Ngày tạo      |

---

### 2. Farm Management (Quản lý vùng trồng)

#### `vung_trong` (Farming Zones)

Bảng trung tâm - quản lý các vùng trồng trọt.

| Column        | Type          | Constraints              | Description          |
| ------------- | ------------- | ------------------------ | -------------------- |
| id            | SERIAL        | PRIMARY KEY              | ID tự tăng           |
| ma_vung       | VARCHAR(50)   | UNIQUE, NOT NULL         | Mã vùng (QR code)    |
| ten_vung      | VARCHAR(200)  | NOT NULL                 | Tên vùng trồng       |
| dien_tich     | DECIMAL(10,2) | NULL                     | Diện tích (hectares) |
| tinh_id       | INTEGER       | FK → tinh(id)            | Thuộc tỉnh           |
| huyen_id      | INTEGER       | FK → huyen(id)           | Thuộc huyện          |
| xa_id         | INTEGER       | FK → xa(id)              | Thuộc xã             |
| chu_so_huu_id | INTEGER       | FK → to_chuc_ca_nhan(id) | Chủ sở hữu           |
| trang_thai_id | INTEGER       | FK → trang_thai_vung(id) | Trạng thái           |
| ngay_tao      | TIMESTAMP     | DEFAULT NOW()            | Ngày tạo             |

**Indexes:**

```sql
CREATE INDEX idx_vung_trong_ma_vung ON vung_trong(ma_vung);
CREATE INDEX idx_vung_trong_tinh ON vung_trong(tinh_id);
CREATE INDEX idx_vung_trong_chu_so_huu ON vung_trong(chu_so_huu_id);
```

**Business Rules:**

-    `ma_vung` must be unique (used for QR code traceability)
-    `dien_tich` must be > 0 if provided
-    Default `trang_thai_id` = 1 (Đang canh tác)

#### `vung_cay_trong` (Crop-Farm Junction)

Many-to-many relationship giữa vùng trồng và loại cây.

| Column        | Type          | Constraints         | Description       |
| ------------- | ------------- | ------------------- | ----------------- |
| id            | SERIAL        | PRIMARY KEY         | ID                |
| vung_trong_id | INTEGER       | FK → vung_trong(id) | Vùng trồng        |
| loai_cay_id   | INTEGER       | FK → loai_cay(id)   | Loại cây trồng    |
| dien_tich     | DECIMAL(10,2) | NULL                | Diện tích cây này |
| ngay_trong    | DATE          | NULL                | Ngày gieo trồng   |

**Composite Unique:**

```sql
ALTER TABLE vung_cay_trong
ADD CONSTRAINT uk_vung_cay UNIQUE (vung_trong_id, loai_cay_id);
```

#### `toa_do_vung` (Farm Coordinates)

Lưu tọa độ các điểm ranh giới vùng trồng (polygon).

| Column        | Type          | Constraints         | Description              |
| ------------- | ------------- | ------------------- | ------------------------ |
| id            | SERIAL        | PRIMARY KEY         | ID                       |
| vung_trong_id | INTEGER       | FK → vung_trong(id) | Vùng trồng               |
| latitude      | DECIMAL(10,8) | NOT NULL            | Vĩ độ                    |
| longitude     | DECIMAL(11,8) | NOT NULL            | Kinh độ                  |
| thu_tu        | INTEGER       | NULL                | Thứ tự điểm (1, 2, 3...) |

**Usage:**

```sql
-- Get polygon coordinates
SELECT latitude, longitude
FROM toa_do_vung
WHERE vung_trong_id = 1
ORDER BY thu_tu;
```

---

### 3. Crop Catalog (Danh mục cây trồng)

#### `loai_cay` (Crop Types)

Danh mục các loại cây trồng.

| Column                | Type         | Constraints       | Description                 |
| --------------------- | ------------ | ----------------- | --------------------------- |
| id                    | SERIAL       | PRIMARY KEY       | ID                          |
| ten_cay               | VARCHAR(100) | NOT NULL          | Tên cây (Lúa, Cà phê, Tiêu) |
| ten_khoa_hoc          | VARCHAR(200) | NULL              | Tên khoa học                |
| nhom_cay_id           | INTEGER      | FK → nhom_cay(id) | Thuộc nhóm                  |
| mo_ta                 | TEXT         | NULL              | Mô tả                       |
| thoi_gian_sinh_truong | INTEGER      | NULL              | Số ngày sinh trưởng         |
| ngay_tao              | TIMESTAMP    | DEFAULT NOW()     | Ngày tạo                    |

**Sample Data:**

```sql
INSERT INTO nongsan.loai_cay (ten_cay, nhom_cay_id, thoi_gian_sinh_truong) VALUES
('Lúa Jasmine', 1, 120),
('Cà phê Arabica', 2, 1825),
('Tiêu', 3, 1460);
```

#### `nhom_cay` (Crop Categories)

Phân nhóm cây trồng.

| Column   | Type         | Constraints | Description                            |
| -------- | ------------ | ----------- | -------------------------------------- |
| id       | SERIAL       | PRIMARY KEY | ID                                     |
| ten_nhom | VARCHAR(100) | NOT NULL    | Tên nhóm (Lương thực, Cây công nghiệp) |
| mo_ta    | TEXT         | NULL        | Mô tả                                  |

---

### 4. Activity Logs (Nhật ký canh tác)

#### `lich_su_canh_tac` (Farming Activity History)

Nhật ký tất cả hoạt động canh tác.

| Column            | Type         | Constraints             | Description               |
| ----------------- | ------------ | ----------------------- | ------------------------- |
| id                | SERIAL       | PRIMARY KEY             | ID                        |
| vung_trong_id     | INTEGER      | FK → vung_trong(id)     | Vùng trồng                |
| loai_hoat_dong_id | INTEGER      | FK → loai_hoat_dong(id) | Loại hoạt động            |
| ngay_thuc_hien    | DATE         | NOT NULL                | Ngày thực hiện            |
| chi_tiet          | TEXT         | NULL                    | Chi tiết hoạt động        |
| nguoi_thuc_hien   | VARCHAR(200) | NULL                    | Người thực hiện           |
| phan_bon_id       | INTEGER      | FK → phan_bon(id)       | Phân bón sử dụng (nếu có) |
| thuoc_bvtv_id     | INTEGER      | FK → thuoc_bvtv(id)     | Thuốc BVTV (nếu có)       |
| giong_id          | INTEGER      | FK → giong_cay(id)      | Giống sử dụng (nếu có)    |
| lieu_luong        | VARCHAR(100) | NULL                    | Liều lượng                |
| don_vi            | VARCHAR(50)  | NULL                    | Đơn vị (kg, lít)          |
| ngay_tao          | TIMESTAMP    | DEFAULT NOW()           | Ngày tạo record           |

**Indexes:**

```sql
CREATE INDEX idx_lich_su_vung ON lich_su_canh_tac(vung_trong_id);
CREATE INDEX idx_lich_su_ngay ON lich_su_canh_tac(ngay_thuc_hien);
CREATE INDEX idx_lich_su_loai ON lich_su_canh_tac(loai_hoat_dong_id);
```

**Business Logic:**

```sql
-- Get activity timeline for farm
SELECT
    lh.ngay_thuc_hien,
    lh.loai_hoat_dong_id,
    lh.chi_tiet,
    pb.ten_phan_bon,
    tb.ten_thuoc
FROM lich_su_canh_tac lh
LEFT JOIN phan_bon pb ON lh.phan_bon_id = pb.id
LEFT JOIN thuoc_bvtv tb ON lh.thuoc_bvtv_id = tb.id
WHERE lh.vung_trong_id = 1
ORDER BY lh.ngay_thuc_hien DESC;
```

#### `loai_hoat_dong` (Activity Types)

Danh mục các loại hoạt động canh tác.

| Column   | Type         | Constraints | Description   |
| -------- | ------------ | ----------- | ------------- |
| id       | SERIAL       | PRIMARY KEY | ID            |
| ten_loai | VARCHAR(100) | NOT NULL    | Tên hoạt động |
| mo_ta    | TEXT         | NULL        | Mô tả         |
| icon     | VARCHAR(50)  | NULL        | Icon name     |

**Sample Data:**

```sql
INSERT INTO nongsan.loai_hoat_dong (id, ten_loai) VALUES
(1, 'Gieo trồng'),
(2, 'Làm đất'),
(3, 'Bón phân'),
(4, 'Phun thuốc BVTV'),
(5, 'Tưới nước'),
(6, 'Thu hoạch');
```

**Note:** Cleaned duplicates on Jan 10, 2026 (removed 3 duplicate entries)

---

### 5. Facilities (Cơ sở sản xuất)

#### `co_so` (Base Facilities)

Bảng cha cho tất cả các cơ sở.

| Column         | Type         | Constraints              | Description     |
| -------------- | ------------ | ------------------------ | --------------- |
| id             | SERIAL       | PRIMARY KEY              | ID              |
| ma_co_so       | VARCHAR(50)  | UNIQUE                   | Mã cơ sở        |
| ten_co_so      | VARCHAR(200) | NOT NULL                 | Tên cơ sở       |
| dia_chi        | TEXT         | NULL                     | Địa chỉ         |
| tinh_id        | INTEGER      | FK → tinh(id)            | Thuộc tỉnh      |
| huyen_id       | INTEGER      | FK → huyen(id)           | Thuộc huyện     |
| xa_id          | INTEGER      | FK → xa(id)              | Thuộc xã        |
| loai_hinh_id   | INTEGER      | FK → loai_hinh_co_so(id) | Loại hình       |
| dien_thoai     | VARCHAR(20)  | NULL                     | Số điện thoại   |
| email          | VARCHAR(100) | NULL                     | Email           |
| chu_so_huu_id  | INTEGER      | FK → to_chuc_ca_nhan(id) | Chủ sở hữu      |
| ngay_thanh_lap | DATE         | NULL                     | Ngày thành lập  |
| ngay_tao       | TIMESTAMP    | DEFAULT NOW()            | Ngày tạo record |

**Data Cleanup (Jan 10, 2026):**

-    Removed 127 invalid records (single-char names, numeric-only patterns)
-    Before: 7,856 records
-    After: 7,729 records

#### `co_so_dong_goi` (Packaging Facilities)

Cơ sở đóng gói sản phẩm.

| Column              | Type          | Constraints    | Description          |
| ------------------- | ------------- | -------------- | -------------------- |
| id                  | SERIAL        | PRIMARY KEY    | ID                   |
| co_so_id            | INTEGER       | FK → co_so(id) | Tham chiếu co_so     |
| cong_suat           | VARCHAR(100)  | NULL           | Công suất (tấn/ngày) |
| dien_tich_nha_xuong | DECIMAL(10,2) | NULL           | Diện tích (m²)       |
| so_day_chuyen       | INTEGER       | NULL           | Số dây chuyền        |

#### `co_so_phan_bon` (Fertilizer Facilities)

#### `co_so_thuoc_bvtv` (Pesticide Facilities)

#### `co_so_giong` (Seed Facilities)

---

### 6. Product Catalogs

#### `phan_bon` (Fertilizers)

| Column                 | Type         | Constraints            | Description    |
| ---------------------- | ------------ | ---------------------- | -------------- |
| id                     | SERIAL       | PRIMARY KEY            | ID             |
| ma_phan_bon            | VARCHAR(50)  | UNIQUE                 | Mã phân bón    |
| ten_phan_bon           | VARCHAR(200) | NOT NULL               | Tên phân bón   |
| loai_phan_bon_id       | INTEGER      | FK → loai_phan_bon(id) | Loại phân      |
| thanh_phan             | TEXT         | NULL                   | Thành phần NPK |
| ham_luong              | VARCHAR(100) | NULL                   | Hàm lượng      |
| cong_dung              | TEXT         | NULL                   | Công dụng      |
| lieu_luong_khuyen_nghi | VARCHAR(200) | NULL                   | Liều lượng     |
| nha_san_xuat           | VARCHAR(200) | NULL                   | Nhà sản xuất   |
| nuoc_san_xuat          | VARCHAR(100) | NULL                   | Nước sản xuất  |
| ghi_chu                | TEXT         | NULL                   | Ghi chú        |

#### `thuoc_bvtv` (Pesticides)

| Column        | Type         | Constraints              | Description         |
| ------------- | ------------ | ------------------------ | ------------------- |
| id            | SERIAL       | PRIMARY KEY              | ID                  |
| ma_thuoc      | VARCHAR(50)  | UNIQUE                   | Mã thuốc            |
| ten_thuoc     | VARCHAR(200) | NOT NULL                 | Tên thuốc BVTV      |
| nhom_thuoc_id | INTEGER      | FK → nhom_thuoc_bvtv(id) | Nhóm thuốc          |
| mo_ta         | TEXT         | NULL                     | Mô tả               |
| ghi_chu       | TEXT         | NULL                     | Ghi chú + Hoạt chất |
| cong_dung     | TEXT         | NULL                     | Công dụng           |
| lieu_luong    | VARCHAR(200) | NULL                     | Liều lượng          |
| nha_san_xuat  | VARCHAR(200) | NULL                     | Nhà sản xuất        |

**Data Migration (Jan 10, 2026):**

-    Moved `ten_hoat_chat` → `ghi_chu` (4,922 records)
-    Dropped column `ten_hoat_chat`
-    Format: `CONCAT(ghi_chu, ' | Hoạt chất: ', ten_hoat_chat)`

#### `giong_cay` (Crop Varieties)

| Column                | Type         | Constraints           | Description   |
| --------------------- | ------------ | --------------------- | ------------- |
| id                    | SERIAL       | PRIMARY KEY           | ID            |
| ma_giong              | VARCHAR(50)  | UNIQUE                | Mã giống      |
| ten_giong             | VARCHAR(200) | NOT NULL              | Tên giống     |
| loai_cay_id           | INTEGER      | FK → loai_cay(id)     | Loại cây      |
| giong_bao_ho_id       | INTEGER      | FK → giong_bao_ho(id) | Giống bảo hộ  |
| dac_tinh              | TEXT         | NULL                  | Đặc tính      |
| nang_suat             | VARCHAR(100) | NULL                  | Năng suất     |
| thoi_gian_sinh_truong | INTEGER      | NULL                  | Số ngày       |
| nha_tao_giong         | VARCHAR(200) | NULL                  | Nhà tạo giống |

---

### 7. Supporting Tables

#### `to_chuc_ca_nhan` (Organizations/Individuals)

Chủ sở hữu vùng trồng và cơ sở.

| Column      | Type         | Constraints    | Description             |
| ----------- | ------------ | -------------- | ----------------------- |
| id          | SERIAL       | PRIMARY KEY    | ID                      |
| ma_to_chuc  | VARCHAR(50)  | UNIQUE         | Mã tổ chức              |
| ten_to_chuc | VARCHAR(200) | NOT NULL       | Tên tổ chức/cá nhân     |
| loai        | VARCHAR(50)  | NULL           | Loại (Cá nhân, HTX, DN) |
| dia_chi     | TEXT         | NULL           | Địa chỉ                 |
| tinh_id     | INTEGER      | FK → tinh(id)  | Thuộc tỉnh              |
| huyen_id    | INTEGER      | FK → huyen(id) | Thuộc huyện             |
| xa_id       | INTEGER      | FK → xa(id)    | Thuộc xã                |
| dien_thoai  | VARCHAR(20)  | NULL           | Điện thoại              |
| email       | VARCHAR(100) | NULL           | Email                   |
| ma_so_thue  | VARCHAR(50)  | NULL           | Mã số thuế              |

**Added (Jan 10, 2026):**

-    Added `tinh_id`, `huyen_id`, `xa_id` columns with FK constraints

#### `chung_nhan` (Certifications)

Các chứng nhận VietGAP, GlobalGAP, Organic...

| Column          | Type         | Constraints         | Description             |
| --------------- | ------------ | ------------------- | ----------------------- |
| id              | SERIAL       | PRIMARY KEY         | ID                      |
| vung_trong_id   | INTEGER      | FK → vung_trong(id) | Vùng được cấp           |
| loai_chung_nhan | VARCHAR(100) | NOT NULL            | Loại (VietGAP, Organic) |
| so_chung_nhan   | VARCHAR(100) | UNIQUE              | Số chứng nhận           |
| ngay_cap        | DATE         | NULL                | Ngày cấp                |
| ngay_het_han    | DATE         | NULL                | Ngày hết hạn            |
| to_chuc_cap     | VARCHAR(200) | NULL                | Tổ chức cấp             |
| file_url        | TEXT         | NULL                | Link file scan          |

#### `thi_truong` (Markets)

Thị trường tiêu thụ sản phẩm.

| Column         | Type         | Constraints   | Description    |
| -------------- | ------------ | ------------- | -------------- |
| id             | SERIAL       | PRIMARY KEY   | ID             |
| ma_thi_truong  | VARCHAR(50)  | UNIQUE        | Mã thị trường  |
| ten_thi_truong | VARCHAR(200) | NOT NULL      | Tên thị trường |
| vung_dia_ly    | VARCHAR(200) | NULL          | Vùng địa lý    |
| mo_ta          | TEXT         | NULL          | Mô tả          |
| ngay_tao       | TIMESTAMP    | DEFAULT NOW() | Ngày tạo       |

#### `vung_trong_thi_truong` (Farm-Market Junction)

Many-to-many relationship.

---

## 🔗 Relationships

### Key Foreign Keys

```sql
-- Location Hierarchy
ALTER TABLE huyen ADD CONSTRAINT fk_huyen_tinh
    FOREIGN KEY (tinh_id) REFERENCES tinh(id) ON DELETE CASCADE;

ALTER TABLE xa ADD CONSTRAINT fk_xa_huyen
    FOREIGN KEY (huyen_id) REFERENCES huyen(id) ON DELETE CASCADE;

-- Farm to Location
ALTER TABLE vung_trong ADD CONSTRAINT fk_vung_tinh
    FOREIGN KEY (tinh_id) REFERENCES tinh(id) ON DELETE SET NULL;

ALTER TABLE vung_trong ADD CONSTRAINT fk_vung_huyen
    FOREIGN KEY (huyen_id) REFERENCES huyen(id) ON DELETE SET NULL;

ALTER TABLE vung_trong ADD CONSTRAINT fk_vung_xa
    FOREIGN KEY (xa_id) REFERENCES xa(id) ON DELETE SET NULL;

-- Farm to Owner
ALTER TABLE vung_trong ADD CONSTRAINT fk_vung_chu_so_huu
    FOREIGN KEY (chu_so_huu_id) REFERENCES to_chuc_ca_nhan(id) ON DELETE SET NULL;

-- Activity Log
ALTER TABLE lich_su_canh_tac ADD CONSTRAINT fk_lich_su_vung
    FOREIGN KEY (vung_trong_id) REFERENCES vung_trong(id) ON DELETE CASCADE;

ALTER TABLE lich_su_canh_tac ADD CONSTRAINT fk_lich_su_loai
    FOREIGN KEY (loai_hoat_dong_id) REFERENCES loai_hoat_dong(id);

-- Products
ALTER TABLE lich_su_canh_tac ADD CONSTRAINT fk_lich_su_phan_bon
    FOREIGN KEY (phan_bon_id) REFERENCES phan_bon(id) ON DELETE SET NULL;

ALTER TABLE lich_su_canh_tac ADD CONSTRAINT fk_lich_su_thuoc
    FOREIGN KEY (thuoc_bvtv_id) REFERENCES thuoc_bvtv(id) ON DELETE SET NULL;

-- Organization Location
ALTER TABLE to_chuc_ca_nhan ADD CONSTRAINT fk_to_chuc_tinh
    FOREIGN KEY (tinh_id) REFERENCES tinh(id) ON DELETE SET NULL;

ALTER TABLE to_chuc_ca_nhan ADD CONSTRAINT fk_to_chuc_huyen
    FOREIGN KEY (huyen_id) REFERENCES huyen(id) ON DELETE SET NULL;

ALTER TABLE to_chuc_ca_nhan ADD CONSTRAINT fk_to_chuc_xa
    FOREIGN KEY (xa_id) REFERENCES xa(id) ON DELETE SET NULL;
```

### Cardinality

```
tinh (1) ──< (N) huyen (1) ──< (N) xa
  │                                │
  └────────────────────────────────┴──< (N) vung_trong

vung_trong (1) ──< (N) vung_cay_trong >── (N) loai_cay
vung_trong (1) ──< (N) toa_do_vung
vung_trong (1) ──< (N) lich_su_canh_tac
vung_trong (N) ──< (N) thi_truong (via vung_trong_thi_truong)

to_chuc_ca_nhan (1) ──< (N) vung_trong
to_chuc_ca_nhan (1) ──< (N) co_so
```

---

## 🗂️ Views

### `v_vung_trong_full` (Full Farm View)

Tổng hợp toàn bộ thông tin vùng trồng.

```sql
CREATE VIEW v_vung_trong_full AS
SELECT
    vt.id,
    vt.ma_vung,
    vt.ten_vung,
    vt.dien_tich,
    t.ten_tinh,
    h.ten_huyen,
    x.ten_xa,
    tch.ten_to_chuc as chu_so_huu,
    tt.ten_trang_thai,
    STRING_AGG(DISTINCT lc.ten_cay, ', ') as cay_trong
FROM vung_trong vt
LEFT JOIN tinh t ON vt.tinh_id = t.id
LEFT JOIN huyen h ON vt.huyen_id = h.id
LEFT JOIN xa x ON vt.xa_id = x.id
LEFT JOIN to_chuc_ca_nhan tch ON vt.chu_so_huu_id = tch.id
LEFT JOIN trang_thai_vung tt ON vt.trang_thai_id = tt.id
LEFT JOIN vung_cay_trong vct ON vt.id = vct.vung_trong_id
LEFT JOIN loai_cay lc ON vct.loai_cay_id = lc.id
GROUP BY vt.id, t.ten_tinh, h.ten_huyen, x.ten_xa, tch.ten_to_chuc, tt.ten_trang_thai;
```

### `v_co_so_full` (Full Facility View)

```sql
CREATE VIEW v_co_so_full AS
SELECT
    cs.id,
    cs.ma_co_so,
    cs.ten_co_so,
    cs.dia_chi,
    t.ten_tinh,
    h.ten_huyen,
    lh.ten_loai_hinh,
    tch.ten_to_chuc as chu_so_huu
FROM co_so cs
LEFT JOIN tinh t ON cs.tinh_id = t.id
LEFT JOIN huyen h ON cs.huyen_id = h.id
LEFT JOIN loai_hinh_co_so lh ON cs.loai_hinh_id = lh.id
LEFT JOIN to_chuc_ca_nhan tch ON cs.chu_so_huu_id = tch.id;
```

### `v_vung_cay_trong` (Farm-Crop View)

---

## 📊 Data Dictionary

### Status Codes

#### `trang_thai_vung` (Farm Status)

-    `1` - Đang canh tác
-    `2` - Thu hoạch
-    `3` - Ngưng hoạt động
-    `4` - Chuẩn bị

#### `trang_thai_ma_vung` (QR Code Status)

-    `active` - Đang hoạt động
-    `inactive` - Ngưng sử dụng
-    `expired` - Hết hạn

### Enums

#### Activity Types (`loai_hoat_dong`)

1. Làm đất
2. Gieo trồng
3. Bón phân
4. Phun thuốc BVTV
5. Tưới nước
6. Thu hoạch
7. Khác

#### Organization Types (`to_chuc_ca_nhan.loai`)

-    `Cá nhân` - Individual farmer
-    `Hợp tác xã` - Cooperative
-    `Doanh nghiệp` - Enterprise
-    `Tập đoàn` - Corporation

---

## 📈 Indexes & Performance

### Primary Indexes

```sql
-- Most queried columns
CREATE INDEX idx_vung_trong_ma_vung ON vung_trong(ma_vung);
CREATE INDEX idx_vung_trong_tinh ON vung_trong(tinh_id);
CREATE INDEX idx_co_so_ma ON co_so(ma_co_so);
CREATE INDEX idx_lich_su_vung_ngay ON lich_su_canh_tac(vung_trong_id, ngay_thuc_hien);

-- GeoJSON support
CREATE INDEX idx_tinh_coords ON tinh(x, y) WHERE x IS NOT NULL;
CREATE INDEX idx_huyen_coords ON huyen(x, y) WHERE x IS NOT NULL;
```

### Query Optimization

**Slow Query Example:**

```sql
-- Before (Full scan)
SELECT * FROM vung_trong WHERE ma_vung = 'VT001';
-- Execution time: 250ms

-- After (Index scan)
CREATE INDEX idx_ma_vung ON vung_trong(ma_vung);
-- Execution time: 2ms
```

---

## 🔒 Data Integrity

### Constraints

```sql
-- Business rules
ALTER TABLE vung_trong
ADD CONSTRAINT chk_dien_tich
CHECK (dien_tich > 0);

ALTER TABLE lich_su_canh_tac
ADD CONSTRAINT chk_ngay_thuc_hien
CHECK (ngay_thuc_hien <= CURRENT_DATE);

ALTER TABLE chung_nhan
ADD CONSTRAINT chk_ngay_het_han
CHECK (ngay_het_han > ngay_cap);
```

### Triggers

```sql
-- Auto-generate ma_vung if not provided
CREATE OR REPLACE FUNCTION generate_ma_vung()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ma_vung IS NULL THEN
        NEW.ma_vung := 'VT' || LPAD(NEW.id::TEXT, 6, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_generate_ma_vung
BEFORE INSERT ON vung_trong
FOR EACH ROW
EXECUTE FUNCTION generate_ma_vung();
```

---

## 📝 Change Log

### Version 2.0 (January 10, 2026)

**Schema Changes:**

-    ✅ Dropped 10 unused tables (co_quan_luu_tru_gen, diem_sau_benh, etc.)
-    ✅ Dropped column `tinh.ma_tinh`
-    ✅ Added `tinh.x`, `tinh.y` (coordinates)
-    ✅ Added `huyen.x`, `huyen.y`
-    ✅ Added `xa.x`, `xa.y`
-    ✅ Added `to_chuc_ca_nhan.tinh_id`, `huyen_id`, `xa_id`
-    ✅ Migrated `thuoc_bvtv.ten_hoat_chat` → `ghi_chu`
-    ✅ Dropped column `thuoc_bvtv.ten_hoat_chat`

**Data Cleanup:**

-    ✅ Removed 127 invalid records from `co_so` (single-char, numeric patterns)
-    ✅ Removed 127 invalid records from `co_so_dong_goi`
-    ✅ Removed 3 duplicates from `loai_hoat_dong`
-    ✅ Migrated 4,922 records in `thuoc_bvtv`

**Total Changes:**

-    Tables: 41 → 31 (-24.4%)
-    Invalid records removed: 254
-    Duplicates removed: 3
-    Records migrated: 4,922

---

## 📚 References

-    PostgreSQL Documentation: https://www.postgresql.org/docs/
-    GeoJSON Specification: https://geojson.org/
-    Vietnam Administrative Units: https://danhmuchanhchinh.gso.gov.vn/

---

**Document Owner:** Development Team  
**Review Cycle:** Quarterly  
**Next Review:** April 10, 2026
