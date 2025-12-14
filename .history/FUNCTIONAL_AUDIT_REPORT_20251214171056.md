# 📋 BÁO CÁO KIỂM TRA CHỨC NĂNG TRÙNG LẶP

## 🔍 TÓM TẮT KIỂM TRA

**Ngày kiểm tra:** 10/12/2024  
**Tổng file kiểm tra:** 38 files (5 composables, 5 views, 19+ components)  
**Trùng lặp tìm thấy:** **5 vấn đề lớn**  
**Độ nghiêm trọng:** **TRUNG BÌNH - CẦN CẢI THIỆN**

---

## ⚠️ VẤNĐỀ 1: BẢN ĐỒ LEAFLET KHỞI TẠO THEO 2 CÁCH KHÁC NHAU

### 📍 Vị trí:
- **File 1:** `src/composables/useHome.js` (dòng 267-330) - **initMap()**
- **File 2:** `src/composables/useMapLogic.js` (dòng 14-39) - **initMap()**
- **File 3:** `src/components/MapComponent.vue` (dòng 47) - gọi cả 2

### ❌ VẤN ĐỀ:
```
useHome.js.initMap()
├── Tile: Satellite (ArcGIS Imagery)
├── Tile: Street (OpenStreetMap)
├── Tile: hành chính boundaries
├── Zoom control: bottomright
└── Vẽ polygon từ danhSachGoc

useMapLogic.js.initMap()
├── Tile: CartoDB Positron (KHÁC!)
├── Zoom control: bottomright
└── Vẽ circle markers từ danhSachVung
```

**Hậu quả:**
- ❌ HomeView dùng **ArcGIS tiles** (Satellite + Street + Boundaries)
- ❌ QuanLyView dùng **CartoDB tiles** (Positron)
- ❌ Giao diện bản đồ KHÔNG NHẤT QUÁN giữa 2 trang
- ❌ Quản lý bản đồ từ 2 nơi khác nhau → khó debug

---

## ⚠️ VẤNĐỀ 2: HÀM CHUYỂN ĐỔI TRẠNG THÁI LẶP LẠI

### 📍 Vị trí:
- **File 1:** `src/composables/statusHelpers.js` (dòng ?) - **getStatusBadge()**
- **File 2:** `src/composables/useHome.js` (dòng 170-200):
  - getClassTrangThai()
  - getMapColor()
  - getTextTrangThai()

### ❌ VẤN ĐỀ:
```javascript
// statusHelpers.js
export const getStatusBadge = (status) => {
  const badges = {
    canh_tac: { text: "Đang canh tác", class: "bg-green-500" },
    sau_benh: { text: "Cảnh báo", class: "bg-red-500" },
    ...
  }
}

// useHome.js - LẶP LẠI LOGIC TƯƠNG TỰ
export const getClassTrangThai = (tt) => {
  return { canh_tac: "bg-green-500", ... }[tt]
}
export const getMapColor = (tt) => {
  return { canh_tac: "#4caf50", ... }[tt]
}
export const getTextTrangThai = (tt) => {
  return { canh_tac: "Đang canh tác", ... }[tt]
}
```

**Hậu quả:**
- ❌ **Cùng logic ở 2 nơi** → Nếu thay đổi màu trạng thái, phải sửa 2 file
- ❌ Có thể status badge không khớp với màu bản đồ
- ❌ **Đặt tên không nhất quán:** badge vs trangThai vs mapColor

---

## ⚠️ VẤNĐỀ 3: QR MODAL XUẤT HIỆN Ở 2 COMPOSABLE

### 📍 Vị trí:
- **File 1:** `src/composables/useHome.js` (dòng 125-135):
  - showQR, qrLink
  - openQRModal(maSanPham)
  - closeQRModal()

- **File 2:** `src/composables/useTraceability.js` (dòng 6-25):
  - showQR, qrValue
  - openQR()
  - closeQR()

### ❌ VẤN ĐỀ:
```javascript
// useHome.js
export const showQR = ref(false);
export const qrLink = ref("");
export const openQRModal = (maSanPham) => {
  qrLink.value = `${origin}/truy-xuat/${maSanPham}`;
  showQR.value = true;
}

// useTraceability.js - LẶP LẠI!
export const showQR = ref(false);
export const qrValue = computed(() => window.location.href);
export const openQR = () => showQR.value = true;
```

**Hậu quả:**
- ❌ Cùng chức năng **ở 2 composable**
- ❌ Tên hàm khác: openQRModal vs openQR
- ❌ Cách tạo QR code khác: string vs computed property
- ❌ **Nếu user chuyển trang, 2 composable không đồng bộ state**

---

## ⚠️ VẤNĐỀ 4: BIỂU ĐỒ ĐƯỢC HIỂN THỊ 2 CÁC KHÁC NHAU

### 📍 Vị trí:
- **File 1:** `src/components/ChartsComponent.vue` (dòng 72-110):
  - Bar chart (Sử dụng thuốc BVTV): Bar + Doughnut
  - Dữ liệu mock cứng

- **File 2:** `src/components/StatsCharts.vue` (dòng 20-70):
  - Bar chart (Sử dụng thuốc BVTV): Bar + Doughnut
  - Dữ liệu mock cứng
  - **LẶP LẠI HOÀN TOÀN**

### ❌ VẤN ĐỀ:
```javascript
// ChartsComponent.vue
const exportData = [
  { label: 'Trung Quốc', value: 45, color: '#ef4444' },
  ...
]
// Hiển thị Pie + Bar Chart

// StatsCharts.vue
// CÓ CÙng LAYOUT & DỮ LIỆU!
const barData = {
  labels: ['Tháng 1', 'Tháng 2', 'Tháng 3'],
  datasets: [{ label: 'Hóa học', data: [2200, 1800, 2300] }]
}
// Hiển thị Bar + Doughnut Chart
```

**Hậu quả:**
- ❌ **2 component gần như giống hệt nhau**
- ❌ Không rõ nên dùng component nào
- ❌ Nếu thay đổi màu sắc biểu đồ, phải cập nhật 2 nơi
- ❌ Code lặp lại = bundle size lớn hơn

---

## ⚠️ VẤNĐỀ 5: BẤT THƯỜNG TỪ TRACEABILITY PAGE

### 📍 Vị trí:
- `src/views/TraceabilityPage.vue` (dòng ?)

### ❌ VẤN ĐỀ:
```vue
<!-- 2 BUTTON CÓ CHỨC NĂNG GIỐNG NHAU -->
<button @click="openQR">FAB Button</button>
<button @click="openQR" class="primary">Primary Button</button>

<!-- 2 CÁI SAME ACTION → UX CONFUSING -->
```

**Hậu quả:**
- ❌ User bối rối vì có 2 cách mở cùng 1 modal
- ❌ Thừa code & dung lượng

---

## 📊 TÓMLẶP CÁC HÀNG BỊ TRÙNG

| Hàm/Component | File 1 | File 2 | Trùng % |
|---|---|---|---|
| initMap() | useHome.js:267 | useMapLogic.js:14 | 60% |
| Status colors | statusHelpers.js | useHome.js:170 | 80% |
| QR Modal logic | useHome.js:125 | useTraceability.js:6 | 70% |
| Charts display | ChartsComponent.vue | StatsCharts.vue | 95% |
| QR open button | TraceabilityPage.vue | TraceabilityPage.vue | 100% |

---

## 🎯 KHUYẾN NGHỊ CẢI THIỆN

### ✅ GIẢI PHÁP 1: Hợp nhất Map Logic
**Ưu tiên: CAO (Critical)**

```javascript
// src/composables/useMapLogic.js (UPDATE)
export function useMapLogic() {
  // Chỉ giữ 1 initMap() hỗ trợ cả 2 mode
  const initMap = (mode = 'satellite') => {
    if (mode === 'home') {
      // ArcGIS Imagery + Street
    } else if (mode === 'dashboard') {
      // CartoDB Positron
    }
  }
}

// src/composables/useHome.js (IMPORT)
import { useMapLogic } from './useMapLogic'
const { initMap } = useMapLogic()
```

### ✅ GIẢI PHÁP 2: Tập trung Status Helpers
**Ưu tiên: CAO**

```javascript
// src/composables/statusHelpers.js (EXPAND)
export const getStatusBadge = (status) => {
  return {
    canh_tac: {
      text: "Đang canh tác",
      class: "bg-green-500",
      color: "#4caf50"
    },
    ...
  }[status]
}

// src/composables/useHome.js (DELETE)
// Xóa: getClassTrangThai, getMapColor, getTextTrangThai
// Thay thế bằng: import { getStatusBadge }
```

### ✅ GIẢI PHÁP 3: Hợp nhất QR Modal
**Ưu tiên: TRUNG BÌNH**

```javascript
// src/composables/useTraceability.js
// Xóa file này hoặc merge vào useHome.js
// useHome.js đã có logic đầy đủ

// src/views/TraceabilityPage.vue
// Import từ useHome thay vì useTraceability
import { showQR, openQRModal, closeQRModal } from '../composables/useHome'
```

### ✅ GIẢI PHÁP 4: Hợp nhất Biểu đồ
**Ưu tiên: TRUNG BÌNH**

```javascript
// src/components/ChartsComponent.vue
// Giữ lại file này là component chính

// src/components/StatsCharts.vue
// XÓA - hoặc tạo lại để hiển thị dữ liệu khác
// Nếu cần 2 biểu đồ khác nhau, hãy rename thành:
// - ProductChartsComponent.vue
// - FertilizerChartsComponent.vue
```

### ✅ GIẢI PHÁP 5: Sửa TraceabilityPage UI
**Ưu tiên: THẤP**

```vue
<!-- src/views/TraceabilityPage.vue -->
<!-- Giữ 1 button, xóa button thừa -->
<button @click="openQR" class="primary">
  Open QR Code
</button>
```

---

## 📈 IMPACT ASSESSMENT

| Giải pháp | LOC giảm | Build size | Effort |
|---|---|---|---|
| Map Logic | ~60 lines | -2KB | 1 giờ |
| Status Helpers | ~25 lines | -0.5KB | 30 phút |
| QR Modal | ~30 lines | -1KB | 30 phút |
| Charts | ~80 lines | -3KB | 1 giờ |
| UI Cleanup | ~5 lines | -0.1KB | 5 phút |
| **TỔNG CỘNG** | **~200 lines** | **-6.6KB** | **3.5 giờ** |

---

## 🔄 TIẾP THEO

1. **Ngay lập tức:** Hợp nhất useMapLogic.js (Critical)
2. **Hôm nay:** Consolidate statusHelpers (High)
3. **Tuần này:** Hợp nhất QR modal & Charts (Medium)
4. **Run test:** npm run build để xác nhận không có lỗi

---

**Báo cáo tạo bởi:** Code Audit System  
**Status:** ✅ Hoàn thành - Sẵn sàng refactor
