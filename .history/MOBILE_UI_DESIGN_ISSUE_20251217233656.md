# 📱 Thiết Kế Giao Diện Mobile / Mobile UI Design

**Issue Title:** Thiết kế giao diện responsive cho mobile 6 inch / Responsive UI design for 6-inch mobile devices

---

## 🇻🇳 Mô tả (Vietnamese)

### Tổng quan

Tối ưu hóa toàn bộ giao diện ứng dụng WebGIS Nông Nghiệp Smart để hoạt động mượt mà trên thiết bị di động màn hình 6 inch (360x640px - 390x844px).

### Trạng thái hiện tại

-    ✅ Sidebar HomeView đã responsive cho mobile
-    ✅ Navigation bar với icon và label inline
-    ✅ Charts (Pie, Bar, Line) đã tối ưu font size
-    ✅ Data Table có scroll ngang, ẩn cột trên mobile
-    ✅ DiaryActivityForm có nút cân đối
-    ✅ QuanLyView có insight panel giải thích biểu đồ

### Các thay đổi đã thực hiện

#### 1. HomeView.vue - Sidebar

-    Sidebar floating với margin: `left-3 right-3 bottom-[75px]`
-    Chiều rộng cố định 360px trên desktop
-    Border radius: `rounded-xl` (mobile) / `rounded-2xl` (desktop)
-    Z-index: 1000 để hiện trên map

#### 2. App.vue - Navigation Bar

-    Chiều cao giảm từ 70px xuống 56px
-    Thêm border-radius: `20px 20px 0 0`
-    Hiển thị label trực tiếp dưới icon thay vì popup tooltip
-    Font size label: 0.6rem (10px)

#### 3. Chart Components

-    Font size legend: 9-10px
-    Font size tooltip: 8-10px
-    `maintainAspectRatio: false` cho responsive sizing
-    Thêm subtitle giải thích mối quan hệ giữa các biểu đồ

#### 4. DataTableComponent.vue

-    Horizontal scroll cho mobile: `overflow-x-auto`
-    Ẩn các cột ít quan trọng trên mobile: `hidden sm:table-cell`
-    Min-width cho table: 600px

#### 5. DiaryActivityForm.vue

-    Cả hai nút Hủy và Lưu đều dùng `flex-1` để kích thước bằng nhau

#### 6. QuanLyView.vue

-    Thêm insight panel với gradient background
-    Giải thích cách các biểu đồ liên quan đến nhau

### Breakpoints sử dụng

-    **< 640px (sm):** Mobile layout
-    **640px - 768px (md):** Tablet layout
-    **768px - 1024px (lg):** Desktop nhỏ
-    **> 1024px (xl):** Desktop lớn

---

## 🇺🇸 Description (English)

### Overview

Optimize the entire Smart Agriculture WebGIS application interface for smooth operation on 6-inch mobile devices (360x640px - 390x844px).

### Current Status

-    ✅ HomeView sidebar is responsive for mobile
-    ✅ Navigation bar with inline icons and labels
-    ✅ Charts (Pie, Bar, Line) with optimized font sizes
-    ✅ Data Table with horizontal scroll, hidden columns on mobile
-    ✅ DiaryActivityForm with balanced buttons
-    ✅ QuanLyView with insight panel explaining chart relationships

### Changes Implemented

#### 1. HomeView.vue - Sidebar

-    Floating sidebar with margin: `left-3 right-3 bottom-[75px]`
-    Fixed width 360px on desktop
-    Border radius: `rounded-xl` (mobile) / `rounded-2xl` (desktop)
-    Z-index: 1000 to display above map

#### 2. App.vue - Navigation Bar

-    Height reduced from 70px to 56px
-    Added border-radius: `20px 20px 0 0`
-    Display labels directly below icons instead of popup tooltips
-    Label font size: 0.6rem (10px)

#### 3. Chart Components

-    Legend font size: 9-10px
-    Tooltip font size: 8-10px
-    `maintainAspectRatio: false` for responsive sizing
-    Added subtitles explaining relationships between charts

#### 4. DataTableComponent.vue

-    Horizontal scroll for mobile: `overflow-x-auto`
-    Hide less important columns on mobile: `hidden sm:table-cell`
-    Min-width for table: 600px

#### 5. DiaryActivityForm.vue

-    Both Cancel and Save buttons use `flex-1` for equal sizing

#### 6. QuanLyView.vue

-    Added insight panel with gradient background
-    Explains how charts relate to each other

### Breakpoints Used

-    **< 640px (sm):** Mobile layout
-    **640px - 768px (md):** Tablet layout
-    **768px - 1024px (lg):** Small desktop
-    **> 1024px (xl):** Large desktop

---

## 📋 Tiêu chí chấp nhận / Acceptance Criteria

| 🇻🇳 Tiếng Việt | 🇺🇸 English | Status |
|----------------|-------------|--------|
| Sidebar hiển thị đúng trên mobile 6 inch | Sidebar displays correctly on 6-inch mobile | ✅ |
| Navigation bar có icon và label rõ ràng | Navigation bar has clear icons and labels | ✅ |
| Charts đọc được trên màn hình nhỏ | Charts are readable on small screens | ✅ |
| Bảng dữ liệu scroll được ngang | Data table has horizontal scroll | ✅ |
| Forms dễ sử dụng trên touch screen | Forms are easy to use on touch screen | ✅ |
| Không có overflow hoặc element bị che khuất | No overflow or hidden elements | ✅ |
| Touch targets ≥ 44px | Touch targets ≥ 44px | ✅ |
| Font size tối thiểu 10px | Minimum font size 10px | ✅ |

---

## 🏷️ Labels

`enhancement`, `ui/ux`, `mobile`, `responsive`, `completed`

---

## 📸 Screenshots / Ảnh chụp màn hình

### Giao diện Mobile (6 inch - 390x844px) / Mobile View (6 inch - 390x844px)

#### HomeView với Sidebar / HomeView with Sidebar

```
┌─────────────────────────────┐
│  🔍 Tìm kiếm...             │
├─────────────────────────────┤
│                             │
│    📍 MAP COMPONENT         │
│                             │
├─────────────────────────────┤
│ ┌─────────────────────────┐ │
│ │    FLOATING SIDEBAR     │ │
│ │   - Search bar          │ │
│ │   - Filter tabs         │ │
│ │   - List items          │ │
│ └─────────────────────────┘ │
├─────────────────────────────┤
│  🗺️    📖    📊             │
│ Bản đồ Nhật ký Quản lý      │
└─────────────────────────────┘
```

#### Thanh điều hướng / Navigation Bar

```
┌─────────────────────────────┐
│   🗺️       📖       📊      │
│  Bản đồ  Nhật ký  Quản lý   │
└─────────────────────────────┘
Height: 56px | Border-radius: 20px 20px 0 0
```

---

## 🔗 Related Files / Files liên quan

-    [Frontend/src/views/HomeView.vue](Frontend/src/views/HomeView.vue)
-    [Frontend/src/views/QuanLyView.vue](Frontend/src/views/QuanLyView.vue)
-    [Frontend/src/views/DiaryPage.vue](Frontend/src/views/DiaryPage.vue)
-    [Frontend/src/App.vue](Frontend/src/App.vue)
-    [Frontend/src/components/PieChartComponent.vue](Frontend/src/components/PieChartComponent.vue)
-    [Frontend/src/components/BarChartComponent.vue](Frontend/src/components/BarChartComponent.vue)
-    [Frontend/src/components/LineChartComponent.vue](Frontend/src/components/LineChartComponent.vue)
-    [Frontend/src/components/DataTableComponent.vue](Frontend/src/components/DataTableComponent.vue)
-    [Frontend/src/components/DiaryActivityForm.vue](Frontend/src/components/DiaryActivityForm.vue)

---

## ✅ Trạng thái / Status: COMPLETED ✅

| Field | Value |
|-------|-------|
| **Ngày hoàn thành / Completed Date** | December 2024 |
| **Đã test trên / Tested On** | iPhone SE (375px), iPhone 14 Pro (393px), Samsung Galaxy S21 (360px) |
| **Người thực hiện / Implemented By** | Development Team |
