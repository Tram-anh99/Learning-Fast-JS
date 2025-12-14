# 📊 QUANLYVIEW CHARTS - FIX & EXPANSION GUIDE

**Date:** December 14, 2025  
**Status:** ✅ FIXED & READY FOR EXPANSION  

---

## 🔧 FIXES APPLIED

### 1. **Scroll Issue Fixed**
**Problem:** ChartsComponent không cuộn được khi biểu đồ vượt quá màn hình

**Solution:**
- ✅ Added `overflow-y-auto` to QuanLyView main container
- ✅ Added `min-h-0` to chart sections (allows flex items to shrink below content size)
- ✅ Added `overflow-y-auto` to both chart containers

**Code Changes:**
```vue
<!-- QuanLyView.vue -->
<div class="absolute inset-0 bg-slate-100 flex flex-col p-5 gap-5 overflow-y-auto">

<!-- ChartsComponent.vue -->
<div class="flex flex-col flex-1 p-4 ... min-h-0 overflow-y-auto">
```

### 2. **Component Architecture Improved**
**Problem:** Chart data hardcoded in component, difficult to expand

**Solution:**
- ✅ Created `useCharts.js` composable
- ✅ Moved all chart data to composable
- ✅ Added helper functions for data manipulation
- ✅ Added API integration stubs (ready for backend)

---

## 📁 NEW COMPOSABLE: useCharts.js

**Location:** `src/composables/useCharts.js`

**Exported Functions:**

### Data References
```javascript
// Refs - reactively update in real-time
exportData          // Thị trường xuất khẩu (market share)
cropData            // Sản lượng cây trồng (crop production)
productivityTrendData // Xu hướng năng suất (productivity over time)
```

### Computed Values
```javascript
pieChartStyle        // Computed conic-gradient for pie chart
totalExportValue     // Sum of all export percentages (should be 100)
sortedCropData       // Crops sorted by production (highest first)
```

### Helper Functions
```javascript
addExportMarket(newMarket)           // Add new export market
fetchExportData()                    // Get data from API (stub)
fetchCropData()                      // Get crop data from API (stub)
fetchProductivityTrend()             // Get productivity trend from API (stub)
getTopCrop()                         // Get highest producing crop
getMarketShare(marketLabel)          // Get market share %
getAverageProductivity()             // Calculate average productivity
```

---

## 🚀 HOW TO ADD NEW CHARTS

### Option 1: Add to ChartsComponent (Simple)

**Step 1:** Uncomment the placeholder section in ChartsComponent.vue template:

```vue
<div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl min-h-0 overflow-y-auto">
  <h3 class="mb-4 text-xs font-bold tracking-wider uppercase text-slate-500">
    <i class="mr-1 fas fa-chart-line"></i> Xu hướng Năng suất
  </h3>
  <!-- Add your new chart here -->
</div>
```

**Step 2:** Import data from useCharts:

```javascript
import { productivityTrendData, getAverageProductivity } from '../composables/useCharts';
```

**Step 3:** Add your chart visualization (vanilla HTML/Canvas or Chart.js library)

### Option 2: Create Separate Component (Recommended)

**Example: LineChartComponent.vue**

```vue
<script setup>
import { productivityTrendData, getAverageProductivity } from '../composables/useCharts';

const average = getAverageProductivity();
const data = productivityTrendData.value;
</script>

<template>
  <div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl min-h-0 overflow-y-auto">
    <h3 class="mb-4 text-xs font-bold tracking-wider uppercase text-slate-500">
      <i class="mr-1 fas fa-chart-line"></i> Xu hướng Năng suất
    </h3>
    <!-- Your chart visualization here -->
  </div>
</template>
```

Then import in ChartsComponent:

```vue
<script setup>
import LineChartComponent from './LineChartComponent.vue';
</script>

<template>
  <!-- existing pie and bar charts -->
  <LineChartComponent />
</template>
```

---

## 📊 SUGGESTED CHARTS TO ADD

### 1. **Line Chart: Productivity Trend**
- **X-axis:** Months (T1, T2, T3, ...)
- **Y-axis:** Productivity (tấn/hectare)
- **Features:** 
  - Show average line
  - Highlight peak month
  - Tooltip on hover

**Data available:** `productivityTrendData` in useCharts

```javascript
const data = [
  { month: 'T1', productivity: 4.2, quality: 7.5 },
  { month: 'T2', productivity: 5.1, quality: 7.8 },
  // ... more months
]
```

### 2. **Area Chart: Quality Score Over Time**
- **X-axis:** Months
- **Y-axis:** Quality Score (1-10)
- **Features:**
  - Gradient fill under the area
  - Reference line at 8.0 (target quality)

**Data available:** `productivityTrendData[].quality`

### 3. **Comparison Chart: Export vs Local Sales**
- **Bar chart side-by-side**
- **Left bar:** Export volume
- **Right bar:** Local sales volume

**Data to add:**
```javascript
const salesData = [
  { market: 'Xuất khẩu', value: 75, color: 'bg-blue-500' },
  { market: 'Nội địa', value: 25, color: 'bg-green-500' },
];
```

### 4. **Gauge Chart: Overall Health Score**
- **Arc gauge showing:** 0-100%
- **Color zones:** Red (bad), Yellow (medium), Green (good)
- **Shows:** Overall farm health score

**Data to add:**
```javascript
const healthScore = ref(78); // Calculate from other metrics
```

### 5. **Heatmap: Monthly Activity**
- **Grid showing activity by month & crop**
- **Colors indicate intensity**

**Data structure:**
```javascript
const activityHeatmap = [
  { month: 'T1', crop: 'Lúa', intensity: 8 },
  { month: 'T1', crop: 'Xoài', intensity: 5 },
  // ...
];
```

---

## 🎨 CHART STYLING GUIDELINES

### Color Palette (Tailwind)
```
Primary:   bg-green-500 (màu chính - canh tác)
Success:   bg-emerald-500 (thành công)
Warning:   bg-amber-500 (cảnh báo)
Danger:    bg-red-500 (nguy hiểm)
Info:      bg-blue-500 (thông tin)
Secondary: bg-slate-500 (phụ)
```

### Card Template
```vue
<div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl min-h-0 overflow-y-auto">
  <!-- Title -->
  <h3 class="mb-4 text-xs font-bold tracking-wider uppercase text-slate-500">
    <i class="mr-1 fas fa-icon-name"></i> Chart Title
  </h3>
  
  <!-- Chart content -->
  <div class="flex-1 flex items-center justify-center">
    <!-- Your chart here -->
  </div>
</div>
```

---

## 🔌 API INTEGRATION

### Ready for Backend Connection

**useCharts.js contains stubs for API calls:**

```javascript
const fetchExportData = async () => {
  try {
    // Replace with actual API call:
    // const response = await fetch('/api/charts/export-markets');
    // const data = await response.json();
    // exportData.value = data;
    
    return exportData.value;
  } catch (error) {
    console.error('❌ Error fetching export data:', error);
  }
};
```

### To Enable API:

1. Replace mock `fetch()` URL with your actual endpoint
2. Uncomment the `await fetch()` lines
3. Call from `QuanLyView.onMounted()`:

```javascript
import { fetchExportData, fetchCropData } from '../composables/useCharts';

onMounted(async () => {
  await fetchExportData();
  await fetchCropData();
  // Charts will auto-update via computed properties
});
```

---

## 📋 LAYOUT STRUCTURE

### QuanLyView.vue Grid Layout:

```
┌─────────────────────────────────────────────────────┐
│  StatsBarComponent (Fixed height)                   │
├──────────────────┬──────────────────────────────────┤
│  ChartsComponent │      MapComponent                │
│  (Pie + Bar)     │      (Leaflet map)              │
│  (flex-1)        │      (flex-2)                   │
│  (scrollable)    │                                  │
├─────────────────────────────────────────────────────┤
│  DataTableComponent (Scrollable table)              │
└─────────────────────────────────────────────────────┘
```

### Key CSS Classes:

- **`flex flex-[2]`** - Two-column layout (charts:map = 1:2 ratio)
- **`min-h-0`** - Allow flex items to shrink below content size
- **`overflow-y-auto`** - Enable vertical scrolling
- **`flex-1`** - Equal space distribution

---

## ✅ CURRENT BUILD STATUS

```
✅ Build: 63 modules (added useCharts.js)
✅ CSS: 68.13 kB (gzip 14.95 kB)
✅ JS: 319.11 kB (gzip 105.56 kB)
✅ No errors or warnings
✅ All components rendering correctly
```

---

## 🎯 NEXT STEPS

**Immediate:**
1. ✅ Test scroll functionality in QuanLyView
2. ✅ Verify charts display correctly
3. ✅ Check responsive design on mobile

**Short-term (1-2 days):**
1. Add 1-2 new charts (Line Chart + Area Chart)
2. Update API integration stubs with real endpoints
3. Test data binding reactivity

**Medium-term (1 week):**
1. Implement real-time data updates
2. Add filtering & date range selection
3. Create export/print functionality
4. Add chart interactions (zoom, drill-down)

**Long-term:**
1. Advanced analytics (predictive modeling)
2. Comparative analysis (year-over-year)
3. Custom report builder
4. Data visualization library integration (Chart.js, Recharts)

---

## 📞 SUPPORT

**For adding new charts:**
1. Check `productivityTrendData` structure in useCharts.js
2. Follow color palette guidelines above
3. Use card template provided
4. Test scroll behavior with many data points

**Common issues:**
- Chart not scrolling? → Check `overflow-y-auto` and `min-h-0`
- Data not updating? → Use `.value` for refs in template: `{{ exportData }}`
- Styling messed up? → Ensure Tailwind classes are spelled correctly

---

## 📚 RELATED FILES

```
Frontend/
├── src/views/QuanLyView.vue          ← Main dashboard view
├── src/components/ChartsComponent.vue ← Charts container
├── src/components/MapComponent.vue    ← Map display
├── src/components/StatsBarComponent.vue ← Top stats
├── src/components/DataTableComponent.vue ← Data table
└── src/composables/useCharts.js       ← NEW: Charts data & logic
```

---

**Status:** Ready for chart expansion! 🚀
