# Tổng Hợp Thiết Kế Cơ Sở Dữ Liệu - Hệ Thống Quản Lý Nông Sản

## ✅ Hoàn Thành

Đã thiết kế lại cơ sở dữ liệu hoàn chỉnh theo 3 chuẩn (3NF) tích hợp:

### 📁 Files Đã Tạo

| File                  | Mô tả                                            | Dung lượng |
| --------------------- | ------------------------------------------------ | ---------- |
| `schema_complete.sql` | **Script SQL chính** - Import vào PostgreSQL     | ~500 dòng  |
| `README_COMPLETE.md`  | Hướng dẫn đầy đủ về CSDL, cách sử dụng, truy vấn | Chi tiết   |
| `ERD_DIAGRAM.md`      | Sơ đồ ERD ASCII với tất cả quan hệ               | Trực quan  |
| `analyze_excel.py`    | Script phân tích cấu trúc file Excel             | Tiện ích   |
| `schema.sql`          | Version cũ (giữ lại để tham khảo)                | Backup     |

## 📊 Cấu Trúc Database

### Tổng Số: 40 Bảng + 3 Views

#### Module 1️⃣: Địa Điểm & Tham Chiếu (10 bảng)

-    ✅ `tinh` - Tỉnh/Thành phố
-    ✅ `huyen` - Quận/Huyện
-    ✅ `xa` - Phường/Xã
-    ✅ `trang_thai_vung` - Trạng thái vùng trồng
-    ✅ `trang_thai_ma_vung` - Trạng thái mã vùng
-    ✅ `chung_nhan` - Chứng nhận (VietGAP, GlobalGAP...)
-    ✅ `thi_truong` - Thị trường xuất khẩu
-    ✅ `loai_hoat_dong` - Loại hoạt động canh tác
-    ✅ `nhom_cay` - Nhóm cây trồng
-    ✅ `loai_hinh_co_so` - Loại hình cơ sở

#### Module 2️⃣: Giống Cây Trồng & Nguồn Gen (7 bảng)

-    ✅ `loai_cay` - Loại cây trồng (thống nhất)
-    ✅ `nguon_gen` - Nguồn gen GBVN
-    ✅ `giong_bao_ho` - Giống bảo hộ PVPO
-    ✅ `co_quan_luu_tru_gen` - Cơ quan lưu trữ
-    ✅ `noi_thu_thap_gen` - Nơi thu thập
-    ✅ `nguon_thu_thap` - Nguồn thu thập
-    ✅ `nam_thu_thap` (trong nguon_gen)

**Tích hợp dữ liệu từ:**

-    ✅ Thư mục `giong/` (9 files Excel)
-    ✅ Thư mục `msvt/` (5 files Excel)

#### Module 3️⃣: Tổ Chức & Cơ Sở (3 bảng)

-    ✅ `to_chuc_ca_nhan` - Tổ chức/Cá nhân/HTX/DN
-    ✅ `co_so` - Cơ sở SX/KD (đa năng)
-    ✅ `loai_hinh_co_so` - Loại hình cơ sở

**Tích hợp dữ liệu từ:**

-    ✅ Thư mục `CoSo/cs_giong/`
-    ✅ Thư mục `CoSo/cs_pb/`
-    ✅ Thư mục `CoSo/cs_tbvtv/`
-    ✅ Thư mục `CoSo/cs_donggoi/`

#### Module 4️⃣: Phân Bón (4 bảng)

-    ✅ `loai_phan_bon` - Loại phân bón
-    ✅ `phan_bon` - Danh mục phân bón
-    ✅ `phan_bon_luu_hanh` - Công bố hợp quy
-    ✅ `co_so_phan_bon` - Cơ sở SX/KD phân bón (N-N)

**Tích hợp dữ liệu từ:**

-    ✅ Thư mục `phanbon/` (5 files Excel)
-    ✅ Danh mục phân bón được phép lưu hành
-    ✅ Đơn vị sản xuất, nhập khẩu, mua bán

#### Module 5️⃣: Thuốc BVTV (4 bảng)

-    ✅ `nhom_thuoc_bvtv` - Nhóm thuốc
-    ✅ `thuoc_bvtv` - Danh mục thuốc
-    ✅ `thuoc_bvtv_luu_hanh` - Đăng ký lưu hành
-    ✅ `co_so_thuoc_bvtv` - Cơ sở SX/KD thuốc (N-N)

**Tích hợp dữ liệu từ:**

-    ✅ Thư mục `ThuocBaoVeThucVat/` (6 files Excel)
-    ✅ Thuốc được sử dụng & cấm sử dụng
-    ✅ Đơn vị sản xuất, nhập khẩu, buôn bán

#### Module 6️⃣: Vùng Trồng - MSVT (6 bảng)

-    ✅ `vung_trong` - Vùng trồng (MSVT)
-    ✅ `toa_do_vung` - Tọa độ polygon
-    ✅ `vung_cay_trong` - Cây trồng trong vùng (N-N)
-    ✅ `vung_thi_truong` - Thị trường xuất khẩu (N-N)
-    ✅ `vung_co_so_dong_goi` - Cơ sở đóng gói (N-N)

**Tích hợp dữ liệu từ:**

-    ✅ Thư mục `msvt/` - Mã số vùng trồng
-    ✅ Mock data từ Frontend
-    ✅ Liên kết với cơ sở đóng gói

#### Module 7️⃣: Nhật Ký & Sâu Bệnh (3 bảng)

-    ✅ `lich_su_canh_tac` - Nhật ký đồng ruộng
     -    Liên kết với `phan_bon` (FK)
     -    Liên kết với `thuoc_bvtv` (FK)
     -    Ghi lại liều lượng sử dụng
-    ✅ `diem_sau_benh` - Điểm phát sinh sâu bệnh
-    ✅ `thong_ke_he_thong` - Thống kê hệ thống

#### Views (3 views)

-    ✅ `v_vung_trong_full` - Vùng trồng đầy đủ thông tin
-    ✅ `v_vung_cay_trong` - Cây trồng với thông tin vùng
-    ✅ `v_co_so_full` - Cơ sở đầy đủ thông tin

## 🎯 Điểm Nổi Bật

### ✅ Chuẩn Hóa 3NF

```
✅ 1NF: Tách mảng thành bảng riêng
   - toa_do_vung (từ toaDo array)
   - vung_thi_truong (từ thiBruongXuatKhau array)

✅ 2NF: Tách thông tin lặp lại thành bảng độc lập
   - loai_cay (thay vì lặp tên cây trong mỗi vùng)
   - phan_bon, thuoc_bvtv (thay vì lặp thông tin)

✅ 3NF: Loại bỏ phụ thuộc bắc cầu
   - trang_thai_vung (tách tên, màu sắc, CSS)
   - loai_phan_bon, nhom_thuoc_bvtv (tách nhóm riêng)
```

### ✅ Tích Hợp Dữ Liệu

```
✅ MSVT (msvt/) - Mã số vùng trồng
   ├─ msvt_caytrong.xlsx → loai_cay
   ├─ msvt_chusohuu.xlsx → to_chuc_ca_nhan
   ├─ msvt_thitruong.xlsx → thi_truong
   ├─ msvt_thitruongvungtrong.xlsx → vung_thi_truong
   └─ msvt_thongtinvungtrong.xlsx → vung_trong

✅ Giống (giong/) - Nguồn gen & giống bảo hộ
   ├─ gen_caygiong.xlsx → loai_cay
   ├─ gen_goc.xlsx → nguon_gen
   ├─ giong_baoho.xlsx → giong_bao_ho
   ├─ gen_coquanluutru.xlsx → co_quan_luu_tru_gen
   ├─ gen_noithuthap.xlsx → noi_thu_thap_gen
   └─ gen_nguonthuthap.xlsx → nguon_thu_thap

✅ Phân Bón (phanbon/)
   ├─ DanhMuc_PhanBon_DuocPhep_LuuHanh.xlsx → phan_bon + phan_bon_luu_hanh
   └─ DanhMuc_DonVi_SanXuat_NhapKhau_MuaBan_PhanBon.xlsx → co_so_phan_bon

✅ Thuốc BVTV (ThuocBaoVeThucVat/)
   ├─ DanhMuc_TongHop_ThuocBaoVeThucVat_DuocPhep_LuuHanh.xlsx → thuoc_bvtv_luu_hanh
   └─ DonVi_BuonBan_TBVTV.xlsx → co_so_thuoc_bvtv

✅ Cơ Sở (CoSo/)
   ├─ cs_giong/ → co_so (loai_hinh: CS_GIONG)
   ├─ cs_pb/ → co_so (loai_hinh: CS_PB)
   ├─ cs_tbvtv/ → co_so (loai_hinh: CS_TBVTV)
   └─ cs_donggoi/ → co_so (loai_hinh: CS_DONG_GOI)

✅ Frontend Data
   └─ composables/*.js → vung_trong, lich_su_canh_tac, diem_sau_benh
```

### ✅ Quan Hệ N-N Được Xử Lý

```
✅ Vùng ←→ Cây trồng (vung_cay_trong)
✅ Cây trồng ←→ Thị trường (vung_thi_truong)
✅ Vùng ←→ Cơ sở đóng gói (vung_co_so_dong_goi)
✅ Cơ sở ←→ Phân bón (co_so_phan_bon)
✅ Cơ sở ←→ Thuốc BVTV (co_so_thuoc_bvtv)
```

### ✅ Tính Năng Truy Xuất

```
✅ Mã QR cho từng vùng trồng
✅ Lịch sử canh tác đầy đủ với vật tư sử dụng
✅ Điểm phát sinh sâu bệnh trên bản đồ
✅ Liên kết giữa vùng và cơ sở đóng gói
✅ Thống kê xuất khẩu theo thị trường
✅ Theo dõi phân bón & thuốc BVTV sử dụng
```

## 🚀 Cách Sử Dụng

### Bước 1: Cài đặt PostgreSQL

```bash
# macOS
brew install postgresql@15
brew services start postgresql@15

# Ubuntu/Debian
sudo apt install postgresql-15
```

### Bước 2: Tạo Database

```bash
# Tạo database
createdb nongsan_db

# Hoặc trong psql
psql -U postgres
CREATE DATABASE nongsan_db;
\q
```

### Bước 3: Import Schema

```bash
cd /Users/anllen/LapTrinh/Learning-Fast-JS/Database

# Import schema hoàn chỉnh
psql -U postgres -d nongsan_db -f schema_complete.sql

# Kiểm tra kết quả
psql -U postgres -d nongsan_db
\dt nongsan.*
\dv nongsan.*
```

### Bước 4: Kiểm Tra Dữ Liệu

```sql
-- Xem danh sách vùng trồng
SELECT * FROM nongsan.v_vung_trong_full;

-- Xem cây trồng trong vùng
SELECT * FROM nongsan.v_vung_cay_trong;

-- Xem cơ sở
SELECT * FROM nongsan.v_co_so_full;

-- Đếm số bảng
SELECT COUNT(*) FROM information_schema.tables
WHERE table_schema = 'nongsan';
```

## 📝 Truy Vấn Thường Dùng

### 1. Lấy vùng trồng với tọa độ

```sql
SELECT
    vt.ma_vung,
    vt.ten_vung,
    array_agg(
        json_build_object(
            'lat', tdv.vi_do,
            'lng', tdv.kinh_do
        ) ORDER BY tdv.thu_tu
    ) AS toa_do
FROM nongsan.vung_trong vt
JOIN nongsan.toa_do_vung tdv ON vt.id = tdv.vung_trong_id
GROUP BY vt.id, vt.ma_vung, vt.ten_vung;
```

### 2. Lấy cây & thị trường xuất khẩu

```sql
SELECT
    vt.ma_vung,
    lc.ten_cay,
    tt.ten_thi_truong,
    vtt.san_luong_xuat,
    vtt.gia_tri_xuat
FROM nongsan.vung_thi_truong vtt
JOIN nongsan.vung_cay_trong vct ON vtt.vung_cay_trong_id = vct.id
JOIN nongsan.vung_trong vt ON vct.vung_trong_id = vt.id
JOIN nongsan.loai_cay lc ON vct.loai_cay_id = lc.id
JOIN nongsan.thi_truong tt ON vtt.thi_truong_id = tt.id;
```

### 3. Lịch sử sử dụng phân bón & thuốc

```sql
SELECT
    lsc.ngay_thuc_hien,
    lhd.ten_loai,
    lsc.tieu_de,
    pb.ten_phan_bon,
    lsc.lieu_luong_phan_bon,
    tb.ten_thuoc,
    lsc.lieu_luong_thuoc
FROM nongsan.lich_su_canh_tac lsc
JOIN nongsan.vung_trong vt ON lsc.vung_trong_id = vt.id
LEFT JOIN nongsan.loai_hoat_dong lhd ON lsc.loai_hoat_dong_id = lhd.id
LEFT JOIN nongsan.phan_bon pb ON lsc.phan_bon_id = pb.id
LEFT JOIN nongsan.thuoc_bvtv tb ON lsc.thuoc_bvtv_id = tb.id
WHERE vt.ma_vung = 'VT-001';
```

## 📖 Tài Liệu Đầy Đủ

-    📄 `schema_complete.sql` - Script SQL để import
-    📘 `README_COMPLETE.md` - Hướng dẫn chi tiết
-    📊 `ERD_DIAGRAM.md` - Sơ đồ ERD trực quan
-    🔍 `analyze_excel.py` - Tool phân tích Excel

## 🎨 Sơ Đồ Tổng Quan

```
          ┌────────────────────────────────────┐
          │    GIỐNG & NGUỒN GEN              │
          │  • Loại cây (thống nhất)          │
          │  • Nguồn gen GBVN                 │
          │  • Giống bảo hộ PVPO              │
          └─────────────┬──────────────────────┘
                        │
                        ▼
          ┌────────────────────────────────────┐
          │      VÙNG TRỒNG (MSVT)            │
          │  • Mã vùng, tọa độ                │
          │  • Cây trồng & thị trường         │
          │  • Cơ sở đóng gói                 │
          └──────┬────────────┬────────────────┘
                 │            │
        ┌────────▼───┐   ┌────▼──────────┐
        │ NHẬT KÝ    │   │  PHÂN BÓN &   │
        │ CANH TÁC   │   │  THUỐC BVTV   │
        │            │   │  • Danh mục   │
        │ • Hoạt động│   │  • Cơ sở SX/KD│
        │ • Phân bón │   │  • Lưu hành   │
        │ • Thuốc    │   │               │
        └────────────┘   └───────────────┘
```

## ✨ Tính Năng Nổi Bật

✅ **Chuẩn hóa 3NF** - Không dư thừa dữ liệu
✅ **Tích hợp đầy đủ** - Giống, phân bón, thuốc, vùng trồng
✅ **Truy xuất nguồn gốc** - MSVT, QR code
✅ **Nhật ký đầy đủ** - Theo dõi vật tư sử dụng
✅ **Quản lý cơ sở** - Đa năng (giống, PB, TBVTV, đóng gói)
✅ **Views tối ưu** - Truy vấn nhanh
✅ **Index đầy đủ** - Performance cao

## 🎯 Sẵn Sàng Import

Tất cả đã được thiết kế và sẵn sàng để import vào PostgreSQL!

```bash
psql -U postgres -d nongsan_db -f schema_complete.sql
```

Chúc bạn thành công! 🚀
