# 🏗️ Kiến Trúc Hệ Thống / System Architecture

## Tổng quan / Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    📱 Frontend (Vue 3)                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │HomeView │  │QuanLyVw │  │DiaryPage│  │TraceabilityPage │ │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────────┬────────┘ │
│       │            │            │                │          │
│  ┌────▼────────────▼────────────▼────────────────▼────────┐ │
│  │              🔧 Composables (Business Logic)           │ │
│  │  useHome | useCharts | useDiary | useMapLogic | etc.   │ │
│  └─────────────────────────┬──────────────────────────────┘ │
│                            │                                │
│  ┌─────────────────────────▼──────────────────────────────┐ │
│  │              📦 Components (20 components)              │ │
│  │  Charts | Map | Forms | Modals | Data Display | etc.   │ │
│  └────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  🎨 Tailwind CSS  |  🗺️ Leaflet.js  |  📊 Chart.js        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    🔌 Backend (Planned)                     │
│            FastAPI / Python | PostgreSQL + PostGIS         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Cấu trúc thư mục / Directory Structure

```
Frontend/
├── src/
│   ├── views/                    # 4 Pages
│   │   ├── HomeView.vue          # Trang tra cứu WebGIS
│   │   ├── QuanLyView.vue        # Dashboard quản lý
│   │   ├── DiaryPage.vue         # Nhật ký canh tác
│   │   └── TraceabilityPage.vue  # Truy xuất nguồn gốc
│   │
│   ├── components/               # 20 Vue Components
│   │   ├── Charts/
│   │   │   ├── PieChartComponent.vue
│   │   │   ├── BarChartComponent.vue
│   │   │   └── LineChartComponent.vue
│   │   ├── Map/
│   │   │   ├── MapComponent.vue
│   │   │   ├── MapLayerControl.vue
│   │   │   └── MapLayerSelector.vue
│   │   ├── Data/
│   │   │   ├── DataTableComponent.vue
│   │   │   ├── CropDetailsComponent.vue
│   │   │   └── StatsBarComponent.vue
│   │   ├── Modal/
│   │   │   ├── QRModal.vue
│   │   │   └── QRScanner.vue
│   │   ├── Diary/
│   │   │   ├── DiaryActivitySelector.vue
│   │   │   ├── DiaryActivityForm.vue
│   │   │   └── DiaryActivityHistory.vue
│   │   └── Other/
│   │       ├── FilterTabs.vue
│   │       ├── HomeListItem.vue
│   │       ├── HomeDetailView.vue
│   │       ├── ProductList.vue
│   │       ├── ProductivityLineChart.vue
│   │       └── SidebarHeader.vue
│   │
│   ├── composables/              # 7 Composition API Logic
│   │   ├── useHome.js            # HomeView state & logic
│   │   ├── useCharts.js          # Chart data & config
│   │   ├── useDiary.js           # Diary CRUD operations
│   │   ├── useMapLogic.js        # Leaflet map logic
│   │   ├── useCropData.js        # Crop mock data
│   │   ├── useLineChartData.js   # Line chart specific
│   │   └── statusHelpers.js      # Status utilities
│   │
│   ├── router/
│   │   └── index.js              # Vue Router config
│   │
│   ├── assets/
│   │   ├── main.css              # Global styles
│   │   └── styles/
│   │       ├── tailwind.css
│   │       └── scrollbar.css
│   │
│   ├── App.vue                   # Root component
│   └── main.js                   # Entry point
│
├── public/                       # Static assets
├── package.json                  # Dependencies
├── vite.config.js               # Vite config
├── tailwind.config.js           # Tailwind config
└── postcss.config.js            # PostCSS config
```

---

## 🔄 Data Flow

```
┌──────────────┐     ┌────────────────┐     ┌──────────────┐
│   User       │────▶│    View        │────▶│  Composable  │
│   Action     │     │ (HomeView.vue) │     │ (useHome.js) │
└──────────────┘     └────────────────┘     └──────┬───────┘
                                                   │
                     ┌────────────────┐            │
                     │   Component    │◀───────────┘
                     │ (MapComponent) │
                     └────────┬───────┘
                              │
                     ┌────────▼───────┐
                     │   Re-render    │
                     │   with Props   │
                     └────────────────┘
```

---

## 📊 Component Categories

### 1. Chart Components

| Component          | Library     | Purpose                        |
| ------------------ | ----------- | ------------------------------ |
| PieChartComponent  | vue-chartjs | Phân bố thị trường             |
| BarChartComponent  | vue-chartjs | Năng suất cây trồng            |
| LineChartComponent | vue-chartjs | Quan hệ thị trường × cây trồng |

### 2. Map Components

| Component        | Library | Purpose                             |
| ---------------- | ------- | ----------------------------------- |
| MapComponent     | Leaflet | Hiển thị bản đồ + polygons          |
| MapLayerControl  | Leaflet | Control layers (sâu bệnh, dư lượng) |
| MapLayerSelector | Custom  | Toggle layer visibility             |

### 3. Data Components

| Component            | Props         | Purpose                       |
| -------------------- | ------------- | ----------------------------- |
| DataTableComponent   | data, columns | Hiển thị danh sách vùng trồng |
| CropDetailsComponent | crop          | Chi tiết một cây trồng        |
| StatsBarComponent    | stats         | 4 cards thống kê              |

### 4. Diary Components

| Component             | Events           | Purpose             |
| --------------------- | ---------------- | ------------------- |
| DiaryActivitySelector | @select          | Chọn loại hoạt động |
| DiaryActivityForm     | @submit, @cancel | Form nhập liệu      |
| DiaryActivityHistory  | -                | Timeline lịch sử    |

---

## 🎯 Design Patterns Used

### 1. Composition API

```javascript
// composables/useHome.js
export function useHome() {
     const searchQuery = ref("");
     const selectedItem = ref(null);

     const filteredItems = computed(() => {
          // filter logic
     });

     return { searchQuery, selectedItem, filteredItems };
}
```

### 2. Props Down, Events Up

```vue
<!-- Parent -->
<ChildComponent :data="items" @update="handleUpdate" />

<!-- Child -->
<script setup>
const props = defineProps(["data"]);
const emit = defineEmits(["update"]);
</script>
```

### 3. Provide/Inject (where needed)

```javascript
// Parent
provide("mapInstance", mapRef);

// Child
const map = inject("mapInstance");
```

---

## 🔗 Related Documentation

-    [[Components Reference|Components]]
-    [[Composables Reference|Composables]]
-    [[Styling Guide|Styling Guide]]
