# 📦 COMPONENT STRUCTURE - CẤU TRÚC COMPONENTS

**Ngày cập nhật:** 16/12/2025

## 🎯 TỔNG QUAN

Dự án được tổ chức theo mô hình **Component-based Architecture** với Vue 3 Composition API.
Tất cả components đã được refactor để tối ưu, tái sử dụng và dễ bảo trì.

---

## 📊 THỐNG KÊ

- **Tổng số components:** 20
- **Components đang sử dụng:** 20 (100%)
- **Components đã xóa:** 1 (ChartsComponent.vue - trùng lặp)
- **Composables:** 7
- **Views:** 4

---

## 🗂️ CẤU TRÚC THƯ MỤC

\`\`\`
src/
├── components/ (20 files)
│   ├── BarChartComponent.vue
│   ├── LineChartComponent.vue
│   ├── PieChartComponent.vue
│   ├── CropDetailsComponent.vue
│   ├── DataTableComponent.vue
│   ├── StatsBarComponent.vue
│   ├── MapComponent.vue
│   ├── MapLayerControl.vue
│   ├── MapLayerSelector.vue
│   ├── ProductivityLineChart.vue
│   ├── DiaryActivityForm.vue
│   ├── DiaryActivityHistory.vue
│   ├── DiaryActivitySelector.vue
│   ├── FilterTabs.vue
│   ├── HomeDetailView.vue
│   ├── HomeListItem.vue
│   ├── ProductList.vue
│   ├── QRModal.vue
│   ├── QRScanner.vue
│   ├── SidebarHeader.vue
│   └── icons/ (5 icon components)
│
├── composables/ (7 files)
│   ├── statusHelpers.js
│   ├── useCharts.js
│   ├── useCropData.js
│   ├── useDiary.js
│   ├── useHome.js
│   ├── useLineChartData.js
│   └── useMapLogic.js
│
└── views/ (4 pages)
    ├── HomeView.vue
    ├── QuanLyView.vue
    ├── DiaryPage.vue
    └── TraceabilityPage.vue
\`\`\`

---

## 🏗️ COMPONENT HIERARCHY

### 1. **HomeView** (Trang tra cứu WebGIS)

\`\`\`
HomeView.vue
├── MapLayerSelector.vue       → Chọn lớp bản đồ (satellite/street)
├── SidebarHeader.vue          → Search bar + QR scan button
├── FilterTabs.vue             → Lọc theo trạng thái (Tất cả/Canh tác/...)
├── ProductList.vue            → Danh sách sản phẩm
│   └── HomeListItem.vue       → Item trong danh sách
├── HomeDetailView.vue         → Chi tiết vùng trồng + timeline
├── QRScanner.vue              → Modal nhập/quét mã QR
├── QRModal.vue                → Modal hiển thị QR code
└── MapComponent.vue           → Bản đồ Leaflet với polygons
\`\`\`

**Logic:** \`composables/useHome.js\`

---

### 2. **QuanLyView** (Trang quản lý Dashboard)

\`\`\`
QuanLyView.vue
├── StatsBarComponent.vue      → Thống kê tổng quan (4 cards)
├── PieChartComponent.vue      → Biểu đồ tròn (Thị trường xuất khẩu)
├── BarChartComponent.vue      → Biểu đồ cột (Năng suất cây trồng)
├── LineChartComponent.vue     → Biểu đồ đường (Quan hệ TT & Loại cây)
├── MapComponent.vue           → Bản đồ với layer control
├── MapLayerControl.vue        → Điều khiển layer (Sâu bệnh, Dư lượng)
├── CropDetailsComponent.vue   → Chi tiết cây trồng + QR code
└── DataTableComponent.vue     → Bảng danh sách vùng trồng
\`\`\`

**Logic:** 
- \`composables/useCharts.js\` (Biểu đồ)
- \`composables/useCropData.js\` (Chi tiết cây)
- \`composables/useLineChartData.js\` (Line chart config)
- \`composables/useMapLogic.js\` (Bản đồ)
- \`composables/statusHelpers.js\` (Mock data & helpers)

---

### 3. **DiaryPage** (Nhật ký canh tác)

\`\`\`
DiaryPage.vue
├── DiaryActivitySelector.vue  → Chọn loại hoạt động
├── DiaryActivityForm.vue      → Form nhập thông tin
└── DiaryActivityHistory.vue   → Lịch sử timeline
\`\`\`

**Logic:** \`composables/useDiary.js\`

---

### 4. **TraceabilityPage** (Truy xuất nguồn gốc)

\`\`\`
TraceabilityPage.vue
└── QRModal.vue                → Hiển thị QR code
\`\`\`

---

## 🔄 DATA FLOW PATTERN

\`\`\`
┌──────────────┐
│  View Page   │ (HomeView, QuanLyView, etc.)
└──────┬───────┘
       │ imports
       ↓
┌──────────────┐
│ Composable   │ (useHome, useCharts, useDiary, etc.)
└──────┬───────┘
       │ provides: state, computed, methods
       ↓
┌──────────────┐
│  Components  │ (MapComponent, DataTable, Charts, etc.)
└──────┬───────┘
       │ props + emits
       ↓
┌──────────────┐
│ Child Items  │ (HomeListItem, DiaryActivityCard, etc.)
└──────────────┘
\`\`\`

---

## 📋 COMPONENT DETAILS

### **Chart Components**

#### **PieChartComponent.vue**
- **Purpose:** Biểu đồ tròn thị trường xuất khẩu
- **Props:** None (dùng composable)
- **Data source:** \`useCharts.js → exportData\`
- **Library:** Chart.js (Doughnut)

#### **BarChartComponent.vue**
- **Purpose:** Biểu đồ cột năng suất cây trồng
- **Props:** None (dùng composable)
- **Data source:** \`useCharts.js → cropData\`
- **Library:** Chart.js (Bar)
- **Features:** Màu sắc đa dạng mỗi cột, stats footer

#### **LineChartComponent.vue**
- **Purpose:** Biểu đồ đường mối quan hệ thị trường & loại cây
- **Props:** None (dùng composable)
- **Data source:** \`useLineChartData.js → lineChartData\`
- **Library:** Chart.js (Line)
- **Features:** 5 datasets (TQ, Mỹ, EU, Nhật, ASEAN)

---

### **Map Components**

#### **MapComponent.vue**
- **Purpose:** Bản đồ tương tác với polygons vùng trồng
- **Props:** 
  - \`danhSachVung\` (Array)
  - \`diemNongSauBenh\` (Array - optional)
  - \`selectedVung\` (Object - optional)
  - \`cheDoXem\` (String: 'hanh_chinh' | 'sau_benh' | 'phan_bon')
- **Emits:** \`selectVung\` (Object)
- **Library:** Leaflet.js
- **Features:** ArcGIS tiles, zoom controls, polygon click

#### **MapLayerControl.vue**
- **Purpose:** Panel điều khiển layer bản đồ
- **Props:** \`cheDoXem\` (String)
- **Emits:** \`toggleSauBenh\`, \`toggleDuLuongThuoc\`
- **Features:** 2 buttons toggle layer

#### **MapLayerSelector.vue**
- **Purpose:** Dropdown chọn tile layer
- **Props:** \`currentLayer\` (String)
- **Emits:** \`changeLayer\` (String)
- **Options:** Satellite / Street

---

### **Data Components**

#### **DataTableComponent.vue**
- **Purpose:** Bảng danh sách vùng trồng
- **Props:**
  - \`danhSachVung\` (Array)
  - \`selectedVung\` (Object - optional)
- **Emits:** \`selectVung\` (Object)
- **Features:** Scrollable, highlight selected, action buttons

#### **CropDetailsComponent.vue**
- **Purpose:** Chi tiết loại cây & lịch sử canh tác
- **Props:** \`selectedVung\` (Object)
- **Features:** 
  - Thông tin vùng trồng
  - Danh sách cây
  - Thị trường xuất khẩu
  - Lịch sử canh tác timeline
  - QR code truy xuất

#### **StatsBarComponent.vue**
- **Purpose:** Thanh thống kê 4 cards
- **Props:** \`thongKe\` (Object)
- **Features:** Responsive grid (1→2→4 columns)
- **Cards:** Tổng vùng, Diện tích, Cảnh báo, Thu hồi

---

### **Search & Filter Components**

#### **SidebarHeader.vue**
- **Purpose:** Header sidebar với search & QR button
- **Props:** 
  - \`isDetailMode\` (Boolean)
  - \`searchQuery\` (String)
  - \`suggestions\` (Array)
- **Emits:** 
  - \`update:searchQuery\` (String)
  - \`back\` ()
  - \`scanQR\` ()
  - \`selectSuggestion\` (Object)
- **Features:** Autocomplete dropdown

#### **FilterTabs.vue**
- **Purpose:** Tabs filter trạng thái
- **Props:** \`activeFilter\` (String)
- **Emits:** \`filterChange\` (String)
- **Options:** Tất cả, Canh tác, Thu hoạch, Đã thu hoạch

---

### **List Components**

#### **ProductList.vue**
- **Purpose:** Danh sách sản phẩm/vùng
- **Props:** \`items\` (Array)
- **Emits:** \`select\` (Object)
- **Features:** Scrollable, empty state

#### **HomeListItem.vue**
- **Purpose:** Item trong ProductList
- **Props:** \`item\` (Object)
- **Features:** Thumbnail, status badge, hover effect

---

### **Detail Components**

#### **HomeDetailView.vue**
- **Purpose:** Chi tiết vùng trồng + timeline
- **Props:** \`vung\` (Object)
- **Emits:** \`openQR\` (String)
- **Features:**
  - Thông tin vùng
  - Chủ thể canh tác
  - Nhật ký timeline
  - QR button

---

### **Modal Components**

#### **QRModal.vue**
- **Purpose:** Modal hiển thị QR code
- **Props:**
  - \`show\` (Boolean)
  - \`qrValue\` (String)
- **Emits:** \`close\` ()
- **Features:** Glassmorphism style, gradient, animations
- **Library:** qrcode.vue

#### **QRScanner.vue**
- **Purpose:** Modal nhập/quét QR
- **Props:** \`show\` (Boolean)
- **Emits:** 
  - \`close\` ()
  - \`scan\` (String)
- **Features:** Input manual, camera placeholder (future)

---

### **Diary Components**

#### **DiaryActivitySelector.vue**
- **Purpose:** Grid chọn loại hoạt động
- **Emits:** \`select\` (String)
- **Types:** Gieo trồng, Bón phân, Phun thuốc, Tưới nước, Thu hoạch, Khác

#### **DiaryActivityForm.vue**
- **Purpose:** Form nhập thông tin hoạt động
- **Props:** \`selectedActivity\` (String)
- **Emits:** \`submit\` (Object)
- **Fields:** Mô tả, Ngày, Ghi chú

#### **DiaryActivityHistory.vue**
- **Purpose:** Timeline lịch sử
- **Props:** \`activities\` (Array)
- **Emits:** \`delete\` (Number)
- **Features:** Vertical timeline với emoji icons

---

## 🎨 STYLING CONVENTIONS

### **Class Naming**
- \`.panel\` - Container chính
- \`.panel-header\` - Header với title
- \`.panel-title\` - Tiêu đề panel
- \`.stat-card\` - Card thống kê
- \`.icon-box-{color}\` - Icon container
- \`.btn-primary\` - Button chính
- \`.badge-{status}\` - Status badge
- \`.table-cell\` - Table cell

### **Responsive Breakpoints**
- \`sm:\` - ≥640px (Mobile landscape)
- \`md:\` - ≥768px (Tablet)
- \`lg:\` - ≥1024px (Desktop)
- \`xl:\` - ≥1280px (Large desktop)

### **Typography**
- H1: \`text-base font-bold\`
- H2: \`text-sm font-semibold\`
- Body: \`text-xs\` / \`text-sm\`
- Small: \`text-xs\`

---

## ✅ COMPONENT CHECKLIST

Mỗi component đảm bảo:

- ✅ Header comment đầy đủ
- ✅ Props được định nghĩa với type
- ✅ Emits được khai báo
- ✅ Logic tách ra composable (nếu cần)
- ✅ Responsive design
- ✅ Cleanup trong onBeforeUnmount (nếu có)
- ✅ Comments cho sections quan trọng

---

**Cập nhật lần cuối:** 16/12/2025  
**Trạng thái:** ✅ Hoàn chỉnh & Production Ready
