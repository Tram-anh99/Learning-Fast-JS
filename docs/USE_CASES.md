# Use Case Documentation

## Hệ Thống Quản Lý Nông Nghiệp & Truy Xuất Nguồn Gốc

**Version:** 2.0  
**Last Updated:** January 10, 2026

---

## 📋 Table of Contents

1. [Actors](#actors)
2. [Use Case Diagram](#use-case-diagram)
3. [Use Case Specifications](#use-case-specifications)
4. [Scenarios](#scenarios)

---

## 👥 Actors

### 1. Nông Dân (Farmer)

**Role:** Chủ vùng trồng, người trực tiếp canh tác

**Responsibilities:**

-    Quản lý vùng trồng của mình
-    Ghi nhật ký hoạt động canh tác hàng ngày
-    Xem thống kê năng suất
-    Tạo QR code cho sản phẩm

**Access Level:** Standard User

### 2. Quản Lý (Manager/Admin)

**Role:** Quản lý hệ thống, giám sát toàn bộ hoạt động

**Responsibilities:**

-    Xem tổng quan toàn bộ vùng trồng
-    Phân tích thống kê, báo cáo
-    Quản lý danh mục (cây trồng, phân bón, thuốc BVTV)
-    Phê duyệt, cấp chứng nhận
-    Quản lý người dùng

**Access Level:** Administrator

### 3. Người Tiêu Dùng (Consumer)

**Role:** Người mua sản phẩm nông sản

**Responsibilities:**

-    Quét QR code trên sản phẩm
-    Xem thông tin truy xuất nguồn gốc
-    Xem lịch sử canh tác
-    Xác minh chứng nhận

**Access Level:** Public (No login required)

### 4. Cơ Quan Nhà Nước (Government Officer)

**Role:** Thanh tra, kiểm soát chất lượng nông sản

**Responsibilities:**

-    Giám sát hoạt động canh tác
-    Kiểm tra việc sử dụng phân bón, thuốc BVTV
-    Cấp chứng nhận VietGAP, GlobalGAP
-    Xem báo cáo thống kê

**Access Level:** Inspector

---

## 🎯 Use Case Diagram

```
                    Hệ Thống Quản Lý Nông Nghiệp
┌────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌─────────┐                                                       │
│  │ Nông dân│                                                       │
│  └────┬────┘                                                       │
│       │                                                            │
│       │──────► UC01: Đăng nhập hệ thống                           │
│       │                                                            │
│       │──────► UC02: Quản lý vùng trồng                           │
│       │         ├─► Thêm vùng trồng mới                           │
│       │         ├─► Sửa thông tin vùng trồng                      │
│       │         ├─► Xóa vùng trồng                                │
│       │         └─► Xem chi tiết vùng trồng                       │
│       │                                                            │
│       │──────► UC03: Ghi nhật ký canh tác                         │
│       │         ├─► Ghi hoạt động gieo trồng                      │
│       │         ├─► Ghi hoạt động bón phân                        │
│       │         ├─► Ghi hoạt động phun thuốc                      │
│       │         ├─► Ghi hoạt động tưới nước                       │
│       │         └─► Ghi hoạt động thu hoạch                       │
│       │                                                            │
│       │──────► UC04: Xem bản đồ vùng trồng                        │
│       │         ├─► Xem vị trí vùng trồng trên map                │
│       │         └─► Lọc theo tỉnh/huyện/xã                        │
│       │                                                            │
│       │──────► UC05: Tạo QR code sản phẩm                         │
│       │                                                            │
│       │──────► UC06: Xem thống kê năng suất                       │
│       │                                                            │
│                                                                     │
│  ┌─────────┐                                                       │
│  │ Quản lý │                                                       │
│  └────┬────┘                                                       │
│       │                                                            │
│       │──────► UC07: Xem dashboard tổng quan                      │
│       │         ├─► Tổng số vùng trồng                            │
│       │         ├─► Tổng diện tích canh tác                       │
│       │         ├─► Số lượng cơ sở sản xuất                       │
│       │         └─► Biểu đồ thống kê                              │
│       │                                                            │
│       │──────► UC08: Quản lý danh mục                             │
│       │         ├─► Quản lý loại cây trồng                        │
│       │         ├─► Quản lý phân bón                              │
│       │         ├─► Quản lý thuốc BVTV                            │
│       │         └─► Quản lý giống cây                             │
│       │                                                            │
│       │──────► UC09: Quản lý cơ sở sản xuất                       │
│       │         ├─► Cơ sở đóng gói                                │
│       │         ├─► Cơ sở phân bón                                │
│       │         ├─► Cơ sở thuốc BVTV                              │
│       │         └─► Cơ sở giống                                   │
│       │                                                            │
│       │──────► UC10: Xem báo cáo thống kê                         │
│       │         ├─► Thống kê theo tỉnh                            │
│       │         ├─► Thống kê theo loại cây                        │
│       │         ├─► Thống kê theo thời gian                       │
│       │         └─► Export báo cáo (Excel, PDF)                   │
│       │                                                            │
│       │──────► UC11: Quản lý người dùng                           │
│       │         ├─► Thêm người dùng                               │
│       │         ├─► Phân quyền                                    │
│       │         └─► Khóa/Mở khóa tài khoản                        │
│       │                                                            │
│                                                                     │
│  ┌──────────┐                                                      │
│  │Người tiêu│                                                      │
│  │   dùng   │                                                      │
│  └────┬─────┘                                                      │
│       │                                                            │
│       │──────► UC12: Quét QR code sản phẩm                        │
│       │                                                            │
│       │──────► UC13: Xem thông tin truy xuất                      │
│       │         ├─► Thông tin vùng trồng                          │
│       │         ├─► Thông tin cây trồng                           │
│       │         ├─► Lịch sử canh tác                              │
│       │         │    ├─ Ngày gieo trồng                           │
│       │         │    ├─ Phân bón đã sử dụng                       │
│       │         │    ├─ Thuốc BVTV đã sử dụng                     │
│       │         │    └─ Ngày thu hoạch                            │
│       │         ├─► Chứng nhận (VietGAP, Organic)                 │
│       │         └─► Thông tin chủ sở hữu                          │
│       │                                                            │
│                                                                     │
│  ┌─────────┐                                                       │
│  │Cơ quan  │                                                       │
│  │nhà nước │                                                       │
│  └────┬────┘                                                       │
│       │                                                            │
│       │──────► UC14: Giám sát hoạt động canh tác                  │
│       │                                                            │
│       │──────► UC15: Kiểm tra việc sử dụng                        │
│       │         ├─► Kiểm tra phân bón                             │
│       │         └─► Kiểm tra thuốc BVTV                           │
│       │                                                            │
│       │──────► UC16: Cấp chứng nhận                               │
│       │         ├─► Cấp VietGAP                                   │
│       │         ├─► Cấp GlobalGAP                                 │
│       │         └─► Cấp Organic                                   │
│       │                                                            │
│       │──────► UC17: Xem báo cáo tổng hợp                         │
│       │                                                            │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Use Case Specifications

### UC02: Quản lý vùng trồng

**Actor:** Nông dân  
**Pre-conditions:** User đã đăng nhập  
**Post-conditions:** Vùng trồng được tạo/cập nhật/xóa trong database

**Main Flow:**

1. User chọn menu "Quản lý"
2. System hiển thị danh sách vùng trồng
3. User chọn "Thêm vùng trồng mới"
4. System hiển thị form nhập liệu
5. User nhập thông tin:
     - Mã vùng (auto-generate)
     - Tên vùng trồng
     - Diện tích (hectares)
     - Tỉnh/Huyện/Xã
     - Chủ sở hữu
     - Loại cây trồng
     - Tọa độ (optional)
6. User click "Lưu"
7. System validate dữ liệu
8. System lưu vào database
9. System hiển thị thông báo thành công

**Alternative Flow 1:** Sửa vùng trồng

-    3a. User chọn vùng trồng cần sửa
-    3b. System hiển thị form với dữ liệu hiện tại
-    Continue from step 5

**Alternative Flow 2:** Xóa vùng trồng

-    3a. User chọn vùng trồng cần xóa
-    3b. System hiển thị xác nhận
-    3c. User confirm
-    3d. System soft delete (hoặc hard delete)
-    3e. System hiển thị thông báo

**Exception Flow:**

-    E1: Validation failed (thiếu field bắt buộc)
     -    System hiển thị lỗi
     -    User sửa lại
-    E2: Database error
     -    System hiển thị lỗi generic
     -    Log error để admin xử lý

**Business Rules:**

-    `ma_vung` phải unique
-    `dien_tich` phải > 0
-    `tinh_id` phải tồn tại trong bảng `tinh`

---

### UC03: Ghi nhật ký canh tác

**Actor:** Nông dân  
**Pre-conditions:**

-    User đã đăng nhập
-    Vùng trồng đã được tạo

**Post-conditions:** Hoạt động được ghi vào `lich_su_canh_tac`

**Main Flow:**

1. User chọn menu "Nhật ký canh tác"
2. System hiển thị danh sách hoạt động của user
3. User chọn "Thêm hoạt động"
4. System hiển thị form
5. User nhập:
     - Chọn vùng trồng (dropdown)
     - Chọn loại hoạt động (Gieo trồng, Bón phân, Phun thuốc, Thu hoạch...)
     - Ngày thực hiện
     - Chi tiết hoạt động
     - [If Bón phân] Chọn loại phân bón, liều lượng
     - [If Phun thuốc] Chọn loại thuốc BVTV, liều lượng
     - [If Gieo trồng] Chọn giống cây
     - Người thực hiện
6. User click "Lưu"
7. System validate
8. System lưu vào database
9. System hiển thị timeline cập nhật

**Alternative Flow:** Sửa/Xóa hoạt động

-    Similar to UC02

**Business Rules:**

-    `ngay_thuc_hien` không được là tương lai
-    `lieu_luong` phải phù hợp với khuyến nghị (warning nếu quá cao)
-    Một vùng trồng chỉ được "Gieo trồng" một lần trước khi "Thu hoạch"

---

### UC04: Xem bản đồ vùng trồng

**Actor:** Nông dân, Quản lý  
**Pre-conditions:** User đã đăng nhập

**Main Flow:**

1. User chọn menu "Bản đồ"
2. System load vùng trồng có tọa độ
3. System gọi API `/api/geojson/provinces`
4. System hiển thị bản đồ (Leaflet.js)
5. System render:
     - Province polygons
     - Farm markers (nếu có tọa độ)
     - Facility markers
6. User có thể:
     - Zoom in/out
     - Click vào polygon → hiển thị info popup
     - Filter theo tỉnh/huyện
     - Toggle layers (provinces/districts/farms)
7. System update map khi user filter

**Alternative Flow:** Click vào farm marker

-    User click marker
-    System gọi API `/api/geojson/info/farms/{id}`
-    System hiển thị popup với:
     -    Tên vùng trồng
     -    Diện tích
     -    Cây trồng
     -    Chủ sở hữu
     -    Link "Xem chi tiết"

---

### UC05: Tạo QR code sản phẩm

**Actor:** Nông dân  
**Pre-conditions:**

-    User đã đăng nhập
-    Vùng trồng có ít nhất 1 hoạt động thu hoạch

**Post-conditions:** QR code được generate chứa `ma_vung`

**Main Flow:**

1. User vào chi tiết vùng trồng
2. User click "Tạo QR code"
3. System gọi API `/api/qr/generate/{ma_vung}`
4. Backend:
     - Generate QR code image (base64)
     - Return QR data + public URL
5. System hiển thị modal với:
     - QR code image
     - Public URL: `https://domain.com/truy-xuat/{ma_vung}`
     - Nút "Tải xuống"
     - Nút "In"
6. User có thể:
     - Download QR image
     - Print QR
     - Copy public URL

**Business Logic:**

```python
import qrcode

def generate_qr(ma_vung):
    url = f"https://domain.com/truy-xuat/{ma_vung}"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img
```

---

### UC12: Quét QR code sản phẩm

**Actor:** Người tiêu dùng  
**Pre-conditions:** None (Public access)

**Main Flow:**

1. Consumer quét QR code trên sản phẩm
2. QR code chứa URL: `https://domain.com/truy-xuat/VT000123`
3. Browser mở URL
4. Vue Router route to `/truy-xuat/:id`
5. Component `TraceabilityPage.vue` load
6. Component gọi API `/api/qr/trace/VT000123`
7. Backend query:
     ```sql
     SELECT
         vt.ma_vung, vt.ten_vung, vt.dien_tich,
         t.ten_tinh, h.ten_huyen,
         tch.ten_to_chuc as chu_so_huu,
         STRING_AGG(lc.ten_cay, ', ') as cay_trong
     FROM vung_trong vt
     LEFT JOIN tinh t ON vt.tinh_id = t.id
     LEFT JOIN huyen h ON vt.huyen_id = h.id
     LEFT JOIN to_chuc_ca_nhan tch ON vt.chu_so_huu_id = tch.id
     LEFT JOIN vung_cay_trong vct ON vt.id = vct.vung_trong_id
     LEFT JOIN loai_cay lc ON vct.loai_cay_id = lc.id
     WHERE vt.ma_vung = 'VT000123'
     GROUP BY vt.id, t.ten_tinh, h.ten_huyen, tch.ten_to_chuc;
     ```
8. Backend query activities:
     ```sql
     SELECT
         lh.ngay_thuc_hien,
         lh.loai_hoat_dong_id,
         lh.chi_tiet,
         pb.ten_phan_bon,
         tb.ten_thuoc,
         g.ten_giong
     FROM lich_su_canh_tac lh
     LEFT JOIN phan_bon pb ON lh.phan_bon_id = pb.id
     LEFT JOIN thuoc_bvtv tb ON lh.thuoc_bvtv_id = tb.id
     LEFT JOIN giong_cay g ON lh.giong_id = g.id
     WHERE lh.vung_trong_id = <vung_id>
     ORDER BY lh.ngay_thuc_hien DESC;
     ```
9. System hiển thị:
     - **Header:** Thông tin vùng trồng
     - **Section 1:** Thông tin chủ sở hữu
     - **Section 2:** Timeline hoạt động canh tác
     - **Section 3:** Chứng nhận (nếu có)
     - **Footer:** "Được cấp bởi Hệ thống Truy xuất Nông sản Việt Nam"

**UI Layout:**

```
┌────────────────────────────────────────┐
│  🌾 Truy Xuất Nguồn Gốc Nông Sản       │
├────────────────────────────────────────┤
│                                        │
│  Mã sản phẩm: VT000123                │
│  Tên vùng: Vườn Cà Phê Đắk Lắk        │
│  Diện tích: 5.5 ha                     │
│  Địa điểm: Xã ABC, Huyện XYZ, Đắk Lắk │
│                                        │
│  🏠 Chủ sở hữu                          │
│  Hợp tác xã Nông nghiệp Đắk Lắk       │
│  Điện thoại: 0123456789                │
│                                        │
│  🌱 Cây trồng                           │
│  Cà phê Arabica, Tiêu                  │
│                                        │
│  📅 Lịch sử canh tác                    │
│  ┌──────────────────────────────────┐ │
│  │ 2025-12-01: Thu hoạch            │ │
│  │ - Năng suất: 2.5 tấn/ha          │ │
│  ├──────────────────────────────────┤ │
│  │ 2025-11-15: Phun thuốc BVTV     │ │
│  │ - Thuốc: Abamectin 1.8% EC       │ │
│  │ - Liều lượng: 500ml/ha           │ │
│  ├──────────────────────────────────┤ │
│  │ 2025-10-20: Bón phân             │ │
│  │ - Phân: NPK 16-16-8              │ │
│  │ - Liều lượng: 200kg/ha           │ │
│  ├──────────────────────────────────┤ │
│  │ 2025-01-10: Gieo trồng           │ │
│  │ - Giống: Arabica TR4-resistant   │ │
│  └──────────────────────────────────┘ │
│                                        │
│  ✅ Chứng nhận                          │
│  🏆 VietGAP (Số: VG-2025-0123)        │
│     Hết hạn: 2026-12-31               │
│                                        │
└────────────────────────────────────────┘
```

---

### UC07: Xem dashboard tổng quan

**Actor:** Quản lý  
**Pre-conditions:** User có quyền Admin

**Main Flow:**

1. User chọn menu "Dashboard"
2. System gọi API `/api/dashboard/stats`
3. Backend query:
     ```sql
     SELECT
         (SELECT COUNT(*) FROM vung_trong) as total_farms,
         (SELECT SUM(dien_tich) FROM vung_trong) as total_area,
         (SELECT COUNT(*) FROM co_so) as total_facilities,
         (SELECT COUNT(*) FROM lich_su_canh_tac WHERE ngay_thuc_hien >= CURRENT_DATE - INTERVAL '30 days') as activities_last_30d
     ```
4. System hiển thị:
     - **KPI Cards:** Total farms, area, facilities, activities
     - **Bar Chart:** Facilities by type
     - **Pie Chart:** Farm status distribution
     - **Line Chart:** Monthly activities trend
     - **Map:** Geographic distribution
5. User có thể:
     - Click vào chart để xem chi tiết
     - Filter theo thời gian
     - Export báo cáo

---

## 🎬 Scenarios

### Scenario 1: Nông dân ghi nhật ký thu hoạch

**Context:** Anh Nam là nông dân trồng cà phê ở Đắk Lắk. Hôm nay 01/12/2025, anh vừa thu hoạch 2.5 tấn cà phê cherry.

**Steps:**

1. Anh Nam đăng nhập hệ thống trên điện thoại
2. Chọn menu "Nhật ký canh tác"
3. Click "Thêm hoạt động"
4. Điền form:
     - Vùng trồng: "Vườn cà phê 1" (5.5 ha)
     - Loại hoạt động: "Thu hoạch"
     - Ngày: 01/12/2025
     - Chi tiết: "Thu hoạch đợt 1, cà phê chín đỏ"
     - Năng suất: 2.5 tấn
     - Người thực hiện: Anh Nam + 5 công nhân
5. Click "Lưu"
6. Hệ thống lưu thành công
7. Timeline cập nhật hoạt động mới

**Result:**

-    Record mới trong `lich_su_canh_tac`
-    Anh Nam có thể tạo QR code cho lô cà phê này
-    Consumer quét QR sẽ thấy info thu hoạch

---

### Scenario 2: Người tiêu dùng quét QR sản phẩm

**Context:** Chị Lan mua 1 kg cà phê rang xay tại siêu thị. Bao bì có QR code truy xuất nguồn gốc.

**Steps:**

1. Chị Lan mở camera điện thoại
2. Quét QR code trên bao bì
3. QR code chứa: `https://tracuunongsan.vn/truy-xuat/VT000123`
4. Trình duyệt mở trang truy xuất
5. Trang load thông tin:
     - "Vườn cà phê 1 - Đắk Lắk"
     - Chủ sở hữu: Hợp tác xã ABC
     - Cà phê Arabica, trồng 10/01/2025
     - Timeline: Gieo trồng → Bón phân (3 lần) → Phun thuốc (2 lần) → Thu hoạch 01/12/2025
     - Chứng nhận VietGAP
6. Chị Lan xem toàn bộ quy trình canh tác
7. Chị Lan thấy an tâm vì minh bạch

**Result:**

-    Tăng niềm tin người tiêu dùng
-    Nông sản có giá trị cao hơn
-    Truy xuất được 100%

---

### Scenario 3: Quản lý xem báo cáo thống kê

**Context:** Anh Tuấn là quản lý cấp tỉnh Đắk Lắk. Cần báo cáo tổng kết tháng 12/2025.

**Steps:**

1. Anh Tuấn đăng nhập với tài khoản Admin
2. Chọn "Dashboard"
3. Hệ thống hiển thị:
     - Tổng vùng trồng: 1,250
     - Tổng diện tích: 15,500 ha
     - Hoạt động tháng 12: 3,420
4. Anh Tuấn chọn "Báo cáo" → "Thống kê theo loại cây"
5. Hệ thống hiển thị:
     - Cà phê: 8,500 ha (55%)
     - Tiêu: 4,200 ha (27%)
     - Cao su: 2,800 ha (18%)
6. Anh Tuấn click "Export Excel"
7. File Excel download với đầy đủ dữ liệu
8. Anh Tuấn nộp báo cáo lên Sở Nông nghiệp

**Result:**

-    Báo cáo chính xác, kịp thời
-    Tiết kiệm thời gian tổng hợp
-    Dữ liệu visualize dễ hiểu

---

## 🔄 Use Case Relationships

### Extend Relationships

```
UC03: Ghi nhật ký canh tác
  └──« extend »── UC05: Tạo QR code
                   (Chỉ khi có hoạt động thu hoạch)

UC12: Quét QR code
  └──« extend »── UC13: Xem thông tin truy xuất
```

### Include Relationships

```
UC02: Quản lý vùng trồng
  └──« include »── UC01: Đăng nhập
  └──« include »── Validate input

UC03: Ghi nhật ký canh tác
  └──« include »── UC01: Đăng nhập
  └──« include »── UC02: Chọn vùng trồng
```

### Generalization

```
UC10: Xem báo cáo thống kê
  ├── UC10.1: Báo cáo theo tỉnh
  ├── UC10.2: Báo cáo theo loại cây
  └── UC10.3: Báo cáo theo thời gian
```

---

## 📊 Priority Matrix

| Use Case                 | Priority | Complexity | Status     |
| ------------------------ | -------- | ---------- | ---------- |
| UC01: Đăng nhập          | High     | Low        | ⏳ Pending |
| UC02: Quản lý vùng trồng | High     | Medium     | ✅ Done    |
| UC03: Ghi nhật ký        | High     | Medium     | ✅ Done    |
| UC04: Xem bản đồ         | High     | High       | ✅ Done    |
| UC05: Tạo QR code        | High     | Medium     | ✅ Done    |
| UC07: Dashboard          | High     | Medium     | ✅ Done    |
| UC12: Quét QR            | High     | Low        | ✅ Done    |
| UC13: Truy xuất          | High     | Medium     | ✅ Done    |
| UC08: Quản lý danh mục   | Medium   | Low        | ✅ Done    |
| UC11: Quản lý user       | Medium   | Medium     | ⏳ Pending |
| UC16: Cấp chứng nhận     | Low      | Medium     | ⏳ Pending |

---

**Document Owner:** Business Analyst  
**Approved By:** Project Manager  
**Date:** January 10, 2026
