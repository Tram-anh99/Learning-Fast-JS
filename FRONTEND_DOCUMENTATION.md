# 📖 FRONTEND CODEBASE DOCUMENTATION

**Project:** Agriculture Traceability Application (Vue 3)  
**Framework:** Vue 3 + Vite + Leaflet + Chart.js  
**Total Files:** 36 (24 Components, 4 Composables, 5 Views, 2 Utils, 1 Router)  
**Build Status:** ✅ 62 modules

---

## 📁 DIRECTORY STRUCTURE

```
Frontend/src/
├── App.vue
├── main.js
├── router/
│   └── index.js
├── composables/
│   ├── useHome.js
│   ├── useMapLogic.js
│   ├── useDiary.js
│   └── statusHelpers.js
├── views/
│   ├── HomeView.vue
│   ├── DiaryPage.vue
│   ├── QuanLyView.vue
│   ├── TraceabilityPage.vue
│   └── AboutView.vue
└── components/
    ├── icons/ (5 icon files)
    ├── Map-related (3)
    ├── Diary-related (6)
    ├── Data-related (3)
    ├── Modal-related (2)
    ├── Filter-related (1)
    └── Other (4)
```

---

## 🎯 COMPOSABLES (4 files)

### 1. **useHome.js** (210 lines)

**Purpose:** Tra cứu nông sản & quản lý dữ liệu vùng trồng  
**Related Views:** HomeView.vue

**Key Exports:**

```javascript
// State - Refs
export const danhSachGoc          // Mảng gốc 4 vùng (VT-001 → VT-004)
export const boLocHienTai         // Filter hiện tại (all/canh_tac/...)
export const vungDangXem          // Vùng đang xem chi tiết
export const searchQuery          // Từ khóa tìm kiếm
export const showQR               // Trạng thái modal QR
export const qrLink               // Giá trị QR code

// Map State (imported từ useMapLogic)
export const map, mapContainer, layerGroup, tileLayers, currentLayer

// Computed
export const danhSachHienThi       // Lọc theo status
export const danhSachTimKiem       // Lọc theo keyword + status

// Methods
export const chonVung()            // Chọn vùng → zoom map
export const quayLaiDanhSach()     // Quay lại danh sách
export const veLaiBanDo()          // Vẽ polygon từ danhSachTimKiem
export const openQRModal(maSP)     // Mở modal QR
export const closeQRModal()        // Đóng modal QR
export const initMap()             // Khởi tạo Leaflet (from useMapLogic)
export const changeTileLayer(layer) // Switch tile layer
export const getMapColor()         // Get color từ status
```

**Data Structure - danhSachGoc:**

```javascript
[
     {
          id: 1,
          ma: "VT-001", // Mã vùng
          ten: "Xoài Cát Hòa Lộc", // Tên vùng
          dienTich: "5ha",
          trangThai: "canh_tac", // canh_tac|sau_benh|thu_hoach|da_thu_hoach
          chungNhan: "VietGAP", // Chứng chỉ
          anh: "https://images...",
          toaDo: [
               [10.762, 106.66],
               [10.77, 106.67],
               [10.76, 106.67],
          ], // Polygon
          nhatKy: [
               { ngay: "10/12/2024", hoatDong: "Bón phân", chiTiet: "..." },
          ],
     },
     // VT-002, VT-003, VT-004...
];
```

---

### 2. **useMapLogic.js** (300 lines)

**Purpose:** Leaflet bản đồ logic (shared by HomeView & QuanLyView)  
**Library:** Leaflet.js

**Key Exports:**

```javascript
// State
export const map               // L.map instance
export const mapContainer      // DOM ref
export const layerGroup        // L.layerGroup() cho polygon
export const lopSauBenh        // L.layerGroup() cho disease points
export const cheDoXem          // "hanh_chinh" | "sau_benh"
export const tileLayers        // { satellite, street }
export const currentLayer      // Tile hiện tại

// Initialization
export const initMap(mode='dashboard', coordinates, zoom)
  // mode: 'home' → ArcGIS tiles
  //       'dashboard' → CartoDB Positron

// Layer Management
export const veLaiBanDo(danhSachVung)      // Vẽ polygon từ danh sách
export const vẽMarkerVùng(danhSachVung)    // Vẽ circle markers
export const batCheDoSauBenh(points)       // Hiện layer sâu bệnh
export const batCheDoHanhChinh()           // Ẩn layer sâu bệnh
export const changeTileLayer(layer)        // Thay tile layer
export const getMapColor(status)           // Status → Hex color
```

**Tile Layers:**

```javascript
// Mode 'home' (HomeView)
- Satellite: ArcGIS World Imagery
- Street: OpenStreetMap
- Overlay: ArcGIS Administrative Boundaries

// Mode 'dashboard' (QuanLyView)
- CartoDB Positron (light, minimal)
```

**Color Mapping:**

```javascript
canh_tac → #4caf50 (green)
sau_benh → #ef5350 (red)
thu_hoach → #ffca28 (yellow)
da_thu_hoach → #2563eb (blue)
```

---

### 3. **statusHelpers.js** (140 lines)

**Purpose:** Centralized status mapping & helpers  
**Usage:** Tất cả components cần hiển thị status

**Key Exports:**

```javascript
// Status Mapping
export const getStatusBadge(status)   // → { text, class, color }
export const getClassTrangThai(status)  // → CSS class
export const getTextTrangThai(status)   // → Vietnamese text
export const getMapColor(status)        // → Hex color

// Status Values
canh_tac        → "Đang canh tác", bg-green-500, #4caf50
sau_benh        → "Cảnh báo dịch hại", bg-red-500, #ef5350
thu_hoach       → "Đang thu hoạch", bg-yellow-500, #ffca28
da_thu_hoach    → "Đã thu hoạch", bg-blue-600, #2563eb

// Mock Data (for development)
export const mockDataThongKe    // Stats: 124 vùng, 450ha, 1.2 tấn
export const mockDataVung       // 4 mock regions (VT-001 → VT-004)
export const mockDiemNongSauBenh // 4 disease points for map
```

---

### 4. **useDiary.js** (108 lines)

**Purpose:** Quản lý dữ liệu nhật ký canh tác  
**Related Views:** DiaryPage.vue

**Key Exports:**

```javascript
export function useDiary() {
  // Activity Types (6 hoạt động)
  const activityTypes = [
    { id: 1, name: "Gieo sạ", emoji: "🌱", color: "bg-yellow-200" },
    { id: 2, name: "Bón phân", emoji: "💨", color: "bg-green-200" },
    { id: 3, name: "Phun thuốc", emoji: "🧪", color: "bg-blue-200" },
    { id: 4, name: "Tưới nước", emoji: "💧", color: "bg-blue-100" },
    { id: 5, name: "Làm cỏ", emoji: "🌾", color: "bg-yellow-100" },
    { id: 6, name: "Thu hoạch", emoji: "🎃", color: "bg-orange-200" }
  ]

  // Fields (3 mảnh đất)
  const fields = [
    { id: "field1", name: "Mảnh 1", code: "VT-001" },
    { id: "field2", name: "Mảnh 2", code: "VT-002" },
    { id: "field3", name: "Mảnh 3", code: "VT-003" }
  ]

  // Diary entries (mock)
  const diaryList = [...]

  return { activityTypes, fields, diaryList }
}
```

---

## 🖼️ VIEWS (5 files)

### 1. **HomeView.vue** (346 lines)

**Purpose:** Trang tra cứu nông sản chính  
**Route:** `/`  
**Layout:** 2-pane (Map sidebar + Product list)

**Components Used:**

-    MapLayerSelector (dropdown tile layer)
-    SidebarHeader (search + back button)
-    FilterTabs (status filter)
-    ProductList (danh sách sản phẩm)
-    HomeDetailView (chi tiết vùng)
-    QRScanner (quét/nhập QR)
-    QRModal (hiển thị QR code)

**Key Features:**

```
┌─────────────────┬──────────────────┐
│  Sidebar Map    │   Product List   │
│ (Leaflet)       │ (Scrollable)     │
│ - Polygon vùng  │ - 4 items        │
│ - Click zoom    │ - Status filter  │
│ - Tile toggle   │ - Search query   │
└─────────────────┴──────────────────┘
```

**Data Flow:**

```
useHome.js
├── danhSachGoc → filtered by boLocHienTai
├── searchQuery → danhSachTimKiem
└── vungDangXem → HomeDetailView OR ProductList

Map updates when:
- boLocHienTai changes (new filter)
- searchQuery changes (new keyword)
```

---

### 2. **DiaryPage.vue** (272 lines)

**Purpose:** Nhật ký canh tác trang trại  
**Route:** `/diary`  
**Layout:** 3-section (Header + Form + History)

**Components Used:**

-    DiaryActivitySelector (6 activity buttons)
-    DiaryActivityForm (dynamic form inputs)
-    DiaryActivityHistory (timeline)

**Key Features:**

```
Header
└─ "Nhật ký canh tác" title + date

Selector
└─ 6 buttons: Gieo sạ, Bón phân, Phun thuốc, Tưới, Làm cỏ, Thu hoạch

Form (Dynamic)
├─ Activity type selected
├─ 3 field select: Mảnh 1, 2, 3
├─ Text input: Activity details
└─ Date picker: Pick date

History
└─ Timeline: Recent 4 activities
    ├─ Activity emoji + name
    ├─ Field name
    ├─ Activity details
    └─ Time (DD/MM)
```

**Data Structure:**

```javascript
formData = {
     selectedActivity: null, // selected from 6
     selectedField: null, // VT-001, VT-002, VT-003
     activityDetails: "",
     selectedDate: new Date(),
};

recentActivities = [
     { activity: "Bón phân", field: "Mảnh 1", details: "...", time: "10/12" },
];
```

---

### 3. **QuanLyView.vue** (123 lines)

**Purpose:** Dashboard quản lý vùng trồng  
**Route:** `/quan-ly`  
**Layout:** 3-section (Stats + Charts/Map + Table)

**Components Used:**

-    StatsBarComponent (3 stat cards)
-    MapComponent (Leaflet map full)
-    ChartsComponent (pie + bar charts)
-    DataTableComponent (vùng table)

**Key Features:**

```
Stats Bar
├─ Tổng vùng: 124
├─ Diện tích: 450 ha
└─ Cảnh báo: 5

Charts + Map (side by side)
├─ Pie Chart: Thị trường xuất khẩu
│  ├─ Trung Quốc (45%)
│  ├─ Hoa Kỳ (25%)
│  ├─ Châu Âu (20%)
│  └─ Khác (10%)
└─ Map: Full Leaflet with circle markers

Bar Chart
└─ Sử dụng thuốc: Hóa học, Sinh học, Thảo mộc

Table
└─ Danh sách 4 vùng (VT-001 → VT-004)
   ├─ Mã vùng, tên, chủ hộ
   ├─ Trạng thái badge
   └─ Diện tích
```

---

### 4. **TraceabilityPage.vue** (124 lines)

**Purpose:** Trang truy xuất nguồn gốc sản phẩm  
**Route:** `/truy-xuat/:id`  
**Features:**

-    Hiển thị thông tin sản phẩm
-    Timeline lịch sử canh tác
-    Button mở QR modal để chia sẻ
-    Chứng chỉ & thông tin chất lượng

**Components Used:**

-    QRModal (display QR code)

**Key Layout:**

```
┌──────────────────────────────┐
│  Primary Button: Mở QR Code  │
└──────────────────────────────┘
│
│ Product Info
├─ Hình ảnh sản phẩm
├─ Tên, mã, mô tả
└─ Chứng chỉ (VietGAP, OCOP)

Timeline
└─ Gieo sạ → Bón phân → Phun thuốc → Tưới → Làm cỏ → Thu hoạch → Bán

QR Modal (when open)
└─ Mã QR code để chia sẻ link truy xuất
```

---

### 5. **AboutView.vue** (30 lines)

**Purpose:** Trang thông tin về ứng dụng  
**Route:** `/about`  
**Content:**

```
About Agriculture Traceability App
├─ Mục đích ứng dụng
├─ Tính năng chính
├─ Hướng dẫn sử dụng
└─ Liên hệ hỗ trợ
```

---

## 🧩 COMPONENTS (24 files)

### Map Components (3)

#### **MapComponent.vue** (113 lines)

**Usage:** QuanLyView dashboard  
**Features:**

-    Leaflet interactive map
-    Layer control (hành chính, sâu bệnh, phân bón)
-    Polygon vùng trồng with color by status
-    Floating layer control panel

**Props:**

```javascript
danhSachVung; // Array of regions with coordinates
diemNongSauBenh; // Array of disease points
```

**Methods:**

```javascript
initMap(); // Initialize Leaflet instance
vẽMarkerVùng(); // Draw circle markers
batCheDoSauBenh(); // Show disease layer
batCheDoHanhChinh(); // Show admin boundaries
```

---

#### **MapLayerSelector.vue** (80 lines)

**Usage:** HomeView sidebar map  
**Features:**

-    Dropdown to select tile layer
-    Shows current layer name
-    Switches between Satellite & Street

**Props:**

```javascript
currentLayer; // "satellite" | "street"
```

---

#### **MapStatsWidget.vue** (100 lines)

**Usage:** Floating widget on map (QuanLyView)  
**Features:**

-    Expandable floating panel (bottom-left)
-    Mini bar chart (sử dụng thuốc)
-    Mini doughnut chart (phân bón %)
-    Smooth animations

**State:**

```javascript
isExpanded; // ref(true)
```

---

### Diary Components (6)

#### **DiaryActivityForm.vue** (260 lines)

**Usage:** DiaryPage form section  
**Features:**

-    Dynamic form based on selected activity
-    3-field selector (Mảnh 1, 2, 3)
-    Rich text input for details
-    Date picker
-    Submit button

**Props:**

```javascript
modelValue; // Form data binding
```

**Emits:**

```javascript
@update:modelValue // Update parent form data
```

---

#### **DiaryActivitySelector.vue** (80 lines)

**Usage:** DiaryPage selector section  
**Features:**

-    6 activity buttons with emoji & color
-    Selected state highlight
-    Smooth hover effects

**Emits:**

```javascript
@select // Activity ID selected
```

---

#### **DiaryActivityHistory.vue** (150 lines)

**Usage:** DiaryPage history section  
**Features:**

-    Timeline display of recent activities
-    Card layout for each entry
-    Activity emoji, name, field, details
-    Date formatting (DD/MM)

**Props:**

```javascript
activities; // Array of activity entries
```

---

#### **DiaryActivityCard.vue** (60 lines)

**Usage:** Individual activity display  
**Features:**

-    Card layout for one activity
-    Emoji + title + field
-    Details text
-    Date/time info

---

#### **DiaryHeader.vue** (40 lines)

**Usage:** DiaryPage header  
**Features:**

-    Page title "Nhật ký canh tác"
-    Current date display
-    Back button (optional)

---

#### **DiaryNavigation.vue** (50 lines)

**Usage:** Navigation between diary sections  
**Features:**

-    Tab-like navigation
-    Selector, Form, History tabs
-    Active state indicator

---

### Data Display Components (3)

#### **ProductList.vue** (120 lines)

**Usage:** HomeView product list section  
**Features:**

-    v-for loop rendering HomeListItem components
-    Empty state when no results
-    Scrollable container
-    Responsive layout

**Props:**

```javascript
items; // Filtered product array
```

**Emits:**

```javascript
@select // Product selected
```

---

#### **HomeListItem.vue** (60 lines)

**Usage:** Single item in ProductList  
**Features:**

-    Product image (bg-cover)
-    Product name + truncated
-    Certification badge
-    Status badge with color
-    Hover effects (shadow, translate)

**Props:**

```javascript
item; // { id, ten, chungNhan, trangThai, anh, ... }
```

---

#### **DataTableComponent.vue** (120 lines)

**Usage:** QuanLyView bottom table  
**Features:**

-    Table display of 4 vùng
-    Sortable columns
-    Status badge in table
-    Responsive grid layout
-    Edit/Delete buttons (placeholder)

**Props:**

```javascript
data; // Array of vùng objects
```

---

### Modal Components (2)

#### **QRModal.vue** (80 lines)

**Usage:** Display QR code for sharing  
**Features:**

-    Centered modal backdrop
-    QR code display (qrcode.vue library)
-    Download QR button
-    Copy link button
-    Close button (X)

**Props:**

```javascript
show; // Boolean to show/hide
qrValue; // URL string to encode
```

**Emits:**

```javascript
@close // Close modal
```

---

#### **QRScanner.vue** (140 lines)

**Usage:** HomeView QR input modal  
**Features:**

-    Two methods: Camera scan OR manual input
-    Tab toggle between scan/input
-    Text input field for manual entry
-    Camera permission handling
-    Search on enter

**State:**

```javascript
showModal; // Modal visible
scanMode; // "camera" | "manual"
qrInput; // Manual QR text
```

**Emits:**

```javascript
@scan   // QR scanned/entered
@close  // Modal closed
```

---

### Filter & Header Components (3)

#### **FilterTabs.vue** (80 lines)

**Usage:** HomeView status filter  
**Features:**

-    4 tabs: Tất cả, Đang canh tác, Thu hoạch, Đã thu hoạch
-    Active tab highlight
-    Tab click updates filter

**Props:**

```javascript
activeFilter; // Current filter value
```

**Emits:**

```javascript
@filter // New filter selected
```

---

#### **SidebarHeader.vue** (120 lines)

**Usage:** HomeView search header  
**Features:**

-    Search input with icon
-    Autocomplete dropdown (debounced)
-    Back button (v-if vungDangXem)
-    Placeholder suggestions
-    Real-time filtering

**Emits:**

```javascript
@search // Search query updated
@back   // Back button clicked
```

---

#### **StatsBarComponent.vue** (90 lines)

**Usage:** QuanLyView top stats  
**Features:**

-    3 stat cards side-by-side
-    Large number display
-    Label text
-    Icon per card
-    Responsive: 1 col (mobile) → 3 cols (desktop)

**Props:**

```javascript
thongKe; // { tongVung, dienTich, canhBao }
```

---

### Chart Components (2)

#### **ChartsComponent.vue** (160 lines)

**Usage:** QuanLyView middle-right section  
**Features:**

-    Pie chart: Export markets (Trung Quốc 45%, USA 25%, EU 20%, khác 10%)
-    Bar chart: Pesticide usage (Hóa học, Sinh học, Thảo mộc)
-    Doughnut chart: Fertilizer ratio
-    Responsive layout with flex

**Computed:**

```javascript
pieChartStyle; // conic-gradient CSS
exportData; // [{ label, value, color }]
cropData; // [{ label, value, color }]
```

---

### Other Components (4)

#### **HomeDetailView.vue** (150 lines)

**Usage:** HomeView right panel when vùng selected  
**Features:**

-    Product image (large)
-    Product info (tên, mã, diện tích)
-    Chứng chỉ badge
-    Timeline nhật ký activities
-    Back button

**Props:**

```javascript
vung; // Selected region object
```

---

#### **App.vue** (20 lines)

**Purpose:** Root Vue component  
**Features:**

-    RouterView for page rendering
-    Global styles (Tailwind)
-    No visible content (router-driven)

---

### Icon Components (5)

Located in `components/icons/`:

-    IconCommunity.vue
-    IconDocumentation.vue
-    IconEcosystem.vue
-    IconSupport.vue
-    IconTooling.vue

**Purpose:** Reusable icon components (SVG wrapped)

---

## 🛣️ ROUTER (router/index.js)

**Routes:**

```javascript
/                 → HomeView (default)
/diary            → DiaryPage
/quan-ly          → QuanLyView
/truy-xuat/:id    → TraceabilityPage
/about            → AboutView
```

**Mode:** history (clean URLs, no #)

---

## 🚀 ENTRY POINTS

### **main.js** (30 lines)

```javascript
// Bootstrap Vue 3 app
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

createApp(App).use(router).mount("#app");
```

---

## 📊 STATISTICS

| Category      | Count | Remarks                                                    |
| ------------- | ----- | ---------------------------------------------------------- |
| Views         | 5     | Home, Diary, QuanLy, Traceability, About                   |
| Components    | 24    | 3 Map, 6 Diary, 3 Data, 2 Modal, 3 Filter, 2 Chart, 5 Icon |
| Composables   | 4     | useHome, useMapLogic, useDiary, statusHelpers              |
| Total Files   | 36    | .vue + .js                                                 |
| Total LOC     | 3000+ | Approx                                                     |
| Build Modules | 62    | Via Vite                                                   |

---

## 🎨 STYLING

**CSS Framework:** Tailwind CSS  
**Color Palette:**

```
Primary Green: #4caf50 (canh_tac)
Alert Red: #ef5350 (sau_benh)
Warning Yellow: #ffca28 (thu_hoach)
Info Blue: #2563eb (da_thu_hoach)
```

**Responsive Breakpoints (Tailwind):**

```
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
```

---

## 🔄 DATA FLOW DIAGRAM

```
HomeView
├── SidebarHeader
│   └── @search → updateQuery()
├── FilterTabs
│   └── @filter → updateBoLoc()
├── MapLayerSelector
│   └── @change → changeTileLayer()
├── ProductList
│   ├── HomeListItem (x4)
│   └── @select → chonVung()
└── HomeDetailView (when vungDangXem)
    └── History timeline

Data Sources:
- useHome.danhSachGoc (base data)
  ├── filtered by boLocHienTai
  ├── filtered by searchQuery
  └── sorted for display

- useMapLogic for map state
  ├── Leaflet instance
  ├── Tile layers
  └── Polygon layers

- statusHelpers for display values
  ├── Status badges
  ├── Colors
  └── Vietnamese text
```

---

## 🔌 INTEGRATIONS

**Libraries:**

-    **Leaflet.js:** Interactive maps (HomeView, QuanLyView)
-    **Chart.js:** Data visualization (QuanLyView)
-    **qrcode.vue:** QR code generation (QRModal)
-    **Tailwind CSS:** Styling (all components)
-    **Vue Router:** Page navigation

**External Data Sources:**

-    Mock data: statusHelpers.js
-    Real data: Would come from backend API

---

## 📝 NOTES

1. **Mock Data:** All data is currently hardcoded in composables/components. Should be replaced with API calls for production.

2. **Leaflet Tiles:**

     - HomeView uses ArcGIS tiles (detailed satellite/street)
     - QuanLyView uses CartoDB Positron (lighter, cleaner)

3. **Status Values:** 4 main states

     - `canh_tac`: 🌱 Đang canh tác
     - `sau_benh`: ⚠️ Cảnh báo dịch hại
     - `thu_hoach`: 🎃 Đang thu hoạch
     - `da_thu_hoach`: ✅ Đã thu hoạch

4. **Regional Data:** 4 hardcoded regions (VT-001 → VT-004) in useHome.danhSachGoc

5. **Date Format:** DD/MM/YYYY used throughout (Vietnamese standard)

---

## ✅ CURRENT BUILD STATUS

```
✓ 62 modules transformed
✓ CSS: 70.26 kB (gzip: 15.42 kB)
✓ JS: 318.63 kB (gzip: 105.49 kB)
✓ Build time: 1.99s
✓ Zero errors
```

---

**Generated:** 14/12/2024  
**Version:** 1.0.0 (Post-Refactoring)
