# 🎨 MODERN STYLING GUIDE - HƯỚNG DẪN THIẾT KẾ

**Ngày cập nhật:** 16/12/2025

---

## 🎯 TRIẾT LÝ THIẾT KẾ

Dự án sử dụng phong cách thiết kế **Modern, Clean, Professional** với các yếu tố:
- **Glassmorphism** - Mờ trong suốt tạo depth
- **Gradient** - Màu chuyển đổi mượt mà
- **Smooth Animations** - Chuyển động tự nhiên
- **Shadows & Depth** - Tầng sâu rõ ràng
- **Responsive Design** - Linh hoạt mọi màn hình

---

## 🌈 COLOR PALETTE

### **Primary Colors**
```css
/* Green - Màu chủ đạo nông nghiệp */
#1b4332  /* Dark green - Headers, buttons */
#40916c  /* Medium green - Accents */
#52b788  /* Light green - Hover states */
#95d5b2  /* Pale green - Backgrounds */

/* Emerald - Gradient tươi sáng */
#0f2818  /* Deep emerald - Dark mode */
#34d399  /* Bright emerald - Success */
```

### **Secondary Colors**
```css
/* Blue - Thông tin & links */
#3b82f6  /* Primary blue */
#60a5fa  /* Light blue */

/* Slate - Neutral text & borders */
#64748b  /* Medium slate */
#94a3b8  /* Light slate */
#e2e8f0  /* Very light slate */
```

### **Status Colors**
```css
/* Success - Hoàn thành */
#d1fae5 → #a7f3d0  /* Light green gradient */

/* Warning - Cảnh báo */
#fef3c7 → #fde68a  /* Yellow gradient */

/* Danger - Thu hồi */
#fee2e2 → #fecaca  /* Red gradient */

/* Info - Thông tin */
#dbeafe → #bfdbfe  /* Blue gradient */
```

---

## 🎨 DESIGN PRINCIPLES

### **1. GRADIENT & COLOR**
```css
/* Gradient direction: 135deg (diagonal) */
background: linear-gradient(135deg, from-color, to-color);

/* Luôn dùng gradient thay vì màu flat */
✅ from-green-500 to-emerald-600
❌ bg-green-500 (quá flat)

/* Gradient tinh tế cho backgrounds */
from-white via-slate-50 to-blue-50
```

**Examples:**
```css
/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #1b4332, #0f2818);
}

/* Cards */
.card {
  background: linear-gradient(to bottom right, white, #f8fafc);
}

/* Icons */
.icon-box {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}
```

---

### **2. GLASSMORPHISM**
```css
/* Công thức cơ bản */
backdrop-blur-[sm/md/lg/xl/2xl]  /* Blur nền phía sau */
bg-white/[70-95]                 /* Nền trắng bán trong suốt */
border border-white/[30-80]      /* Viền trắng nhẹ */
shadow-[lg/xl/2xl]               /* Bóng tạo depth */
```

**Examples:**
```css
/* Modal overlay */
.modal-overlay {
  @apply bg-black/40 backdrop-blur-md;
}

/* Card glassmorphism */
.glass-card {
  @apply bg-white/90 backdrop-blur-xl border border-white/50 shadow-2xl;
}

/* Sidebar panel */
.panel {
  @apply bg-gradient-to-br from-white via-slate-50 to-blue-50
         backdrop-blur-sm border-white/30;
}
```

---

### **3. SMOOTH ANIMATIONS**
```css
/* Timing functions */
cubic-bezier(0.4, 0, 0.2, 1)        /* ease-out modern */
cubic-bezier(0.175, 0.885, 0.32, 1.275) /* bounce/spring */

/* Duration */
duration-200  /* Nhanh - Hover effects */
duration-300  /* Trung bình - Modal, dropdown */
duration-500  /* Chậm - Page transitions */
```

**Examples:**
```css
/* Hover scale up */
.card {
  @apply transition-all duration-200 hover:scale-105;
}

/* Slide in from top */
.dropdown {
  @apply transform transition-all duration-300 ease-out;
  transform: translateY(-10px);
  opacity: 0;
}
.dropdown.show {
  transform: translateY(0);
  opacity: 1;
}

/* Bounce button */
.btn-bounce {
  @apply transition-transform duration-200;
  transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.btn-bounce:active {
  @apply scale-95;
}
```

---

### **4. SHADOWS & DEPTH**
```css
/* Shadow layers */
shadow-sm   /* Subtle - Inner cards */
shadow-md   /* Default - Cards */
shadow-lg   /* Hover - Elevated cards */
shadow-xl   /* Focus - Modals */
shadow-2xl  /* Decorative - Hero elements */

/* Hover effect pattern */
shadow-md → shadow-lg/xl (khi hover)
```

**Examples:**
```css
/* Card elevation */
.card {
  @apply shadow-md hover:shadow-xl transition-shadow;
}

/* Button depth */
.btn {
  @apply shadow-lg hover:shadow-2xl;
}

/* Dropdown popup */
.dropdown {
  @apply shadow-xl;
}

/* Glow effect cho QR */
.qr-glow {
  box-shadow: 
    inset 0 0 30px rgba(255,255,255,0.5),
    0 10px 40px rgba(0,0,0,0.1);
}
```

---

### **5. ROUNDED CORNERS**
```css
/* Kích thước border-radius */
rounded-lg   /* 8px - Nhỏ (tránh dùng) */
rounded-xl   /* 12px - Thường dùng */
rounded-2xl  /* 16px - Card lớn */
rounded-3xl  /* 24px - Modal, hero */
rounded-full /* Circle/pill */

/* Quy tắc: Càng lớn càng modern */
✅ rounded-xl, rounded-2xl, rounded-3xl
❌ rounded-md, rounded-lg (quá nhỏ)
```

**Examples:**
```css
/* Buttons */
.btn {
  @apply rounded-xl;
}

/* Cards */
.card {
  @apply rounded-2xl;
}

/* Modals */
.modal {
  @apply rounded-3xl;
}

/* Avatar/Icons */
.avatar {
  @apply rounded-full;
}
```

---

### **6. HOVER & INTERACTION**
```css
/* Pattern chung */
hover:shadow-lg/xl     /* Tăng bóng */
hover:scale-105/110    /* Phóng to nhẹ */
hover:-translate-y-1   /* Nâng lên */
active:scale-95        /* Ấn xuống */
group-hover:           /* Hover element cha ảnh hưởng con */
```

**Examples:**
```css
/* Card lift effect */
.card {
  @apply transition-all duration-200
         hover:shadow-xl hover:-translate-y-1;
}

/* Button press */
.btn {
  @apply transition-transform active:scale-95;
}

/* Icon scale */
.icon {
  @apply transition-transform hover:scale-110;
}

/* Group hover pattern */
.card-group:hover .icon {
  @apply scale-110 rotate-12;
}
```

---

## �� COMPONENT STYLING PATTERNS

### **MODAL (QRModal, QRScanner)**
```css
/* Backdrop */
.modal-backdrop {
  @apply fixed inset-0 
         bg-black/40 backdrop-blur-md
         flex items-center justify-center
         z-50;
}

/* Modal card */
.modal-card {
  @apply bg-gradient-to-br from-white via-slate-50 to-blue-50
         border border-white/80
         rounded-3xl shadow-2xl
         backdrop-blur-xl
         p-8 max-w-md w-full;
}

/* Decorative circles */
.decorative-circle {
  @apply absolute rounded-full blur-3xl opacity-30;
  background: radial-gradient(circle, #3b82f6, transparent);
}

/* Close button */
.close-btn {
  @apply text-gray-400 hover:text-gray-600
         transition-colors duration-200;
}
```

---

### **STAT CARDS (StatsBarComponent)**
```css
/* Card container */
.stat-card {
  @apply bg-gradient-to-br from-white to-slate-50
         border border-white/50
         rounded-2xl shadow-md
         backdrop-blur-sm
         p-4 flex items-center gap-4
         transition-all duration-200
         hover:shadow-lg hover:border-white/80;
}

/* Icon box */
.icon-box {
  @apply w-12 h-12 rounded-xl
         flex items-center justify-center
         shadow-lg
         transition-transform duration-200
         hover:scale-110 hover:shadow-xl;
}

/* Color variants */
.icon-box-green {
  @apply bg-gradient-to-br from-green-500 to-emerald-600;
}
.icon-box-blue {
  @apply bg-gradient-to-br from-blue-500 to-blue-600;
}
.icon-box-yellow {
  @apply bg-gradient-to-br from-yellow-500 to-amber-600;
}
.icon-box-red {
  @apply bg-gradient-to-br from-red-500 to-rose-600;
}
```

---

### **BUTTONS**
```css
/* Primary button */
.btn-primary {
  @apply px-4 py-2.5 rounded-xl
         bg-gradient-to-r from-green-600 to-emerald-700
         text-white font-semibold
         shadow-lg hover:shadow-xl
         transition-all duration-200
         hover:from-green-700 hover:to-emerald-800
         active:scale-95;
}

/* Secondary button */
.btn-secondary {
  @apply px-4 py-2.5 rounded-xl
         bg-white/80 text-gray-700
         border border-gray-300
         hover:bg-gray-100/80
         transition-all duration-200
         active:scale-95;
}

/* Icon button */
.btn-icon {
  @apply w-10 h-10 rounded-xl
         flex items-center justify-center
         hover:bg-gray-100
         transition-colors duration-200;
}
```

---

### **BADGES**
```css
/* Badge base */
.badge {
  @apply inline-flex items-center gap-1
         px-3 py-1.5 rounded-xl
         text-xs font-bold
         shadow-sm;
}

/* Status variants */
.badge-success {
  @apply bg-gradient-to-r from-green-100 to-emerald-100
         text-green-800;
}
.badge-warning {
  @apply bg-gradient-to-r from-yellow-100 to-amber-100
         text-yellow-800;
}
.badge-danger {
  @apply bg-gradient-to-r from-red-100 to-rose-100
         text-red-800;
}
.badge-info {
  @apply bg-gradient-to-r from-blue-100 to-cyan-100
         text-blue-800;
}
```

---

### **TABLE ROWS**
```css
/* Table header */
.table-header {
  @apply bg-gradient-to-r from-slate-100 to-slate-50
         border-b border-slate-200
         text-xs font-semibold text-gray-700
         uppercase tracking-wider;
}

/* Table row */
.table-row {
  @apply border-b border-slate-200
         transition-all duration-200
         hover:bg-blue-50/50 hover:scale-[1.01];
}

/* Table cell */
.table-cell {
  @apply px-4 py-3 text-sm text-gray-900;
}

/* Selected row */
.table-row-selected {
  @apply bg-blue-100 border-blue-200;
}
```

---

### **PANELS (Sidebar, Dashboard)**
```css
/* Panel container */
.panel {
  @apply bg-gradient-to-br from-white to-slate-50
         border border-white/50
         rounded-2xl shadow-md
         backdrop-blur-sm
         overflow-hidden;
}

/* Panel header */
.panel-header {
  @apply bg-gradient-to-r from-green-700 to-emerald-800
         text-white px-6 py-4
         border-b border-white/20;
}

/* Panel title */
.panel-title {
  @apply text-base font-bold;
}

/* Panel body */
.panel-body {
  @apply p-6;
}
```

---

## 📱 RESPONSIVE DESIGN

### **Breakpoints**
```javascript
sm: '640px',   // Mobile landscape
md: '768px',   // Tablet
lg: '1024px',  // Desktop
xl: '1280px',  // Large desktop
2xl: '1536px', // Extra large
```

### **Responsive Patterns**
```css
/* Mobile-first approach */
.sidebar {
  @apply w-full;           /* Mobile */
  @apply md:w-80;          /* Tablet+ */
  @apply lg:w-96;          /* Desktop+ */
}

/* Grid responsive */
.stats-grid {
  @apply grid grid-cols-1;    /* 1 col mobile */
  @apply sm:grid-cols-2;      /* 2 cols tablet */
  @apply lg:grid-cols-4;      /* 4 cols desktop */
  @apply gap-4;
}

/* Font size responsive */
.title {
  @apply text-sm;          /* Mobile */
  @apply md:text-base;     /* Tablet+ */
  @apply lg:text-lg;       /* Desktop+ */
}

/* Hide/show elements */
.desktop-only {
  @apply hidden lg:block;
}
.mobile-only {
  @apply block lg:hidden;
}
```

---

## 🎭 TYPOGRAPHY

### **Font Sizes**
```css
/* Tailwind utility classes */
text-xs     /* 12px - Small text, badges */
text-sm     /* 14px - Body text */
text-base   /* 16px - Default, headings */
text-lg     /* 18px - Large headings */
text-xl     /* 20px - Hero titles */
text-2xl    /* 24px - Page titles */
```

### **Font Weights**
```css
font-normal    /* 400 - Body text */
font-medium    /* 500 - Emphasis */
font-semibold  /* 600 - Headings */
font-bold      /* 700 - Strong emphasis */
```

### **Usage**
```css
/* H1 - Page title */
.title-h1 {
  @apply text-2xl font-bold text-gray-900;
}

/* H2 - Section title */
.title-h2 {
  @apply text-lg font-semibold text-gray-800;
}

/* Body text */
.body-text {
  @apply text-sm text-gray-700;
}

/* Small text */
.small-text {
  @apply text-xs text-gray-500;
}
```

---

## ✨ SPECIAL EFFECTS

### **Glow Effect**
```css
.glow {
  box-shadow: 
    0 0 20px rgba(59, 130, 246, 0.3),
    inset 0 0 20px rgba(255, 255, 255, 0.1);
}
```

### **Gradient Text**
```css
.gradient-text {
  @apply bg-gradient-to-r from-green-600 to-emerald-600
         bg-clip-text text-transparent;
}
```

### **Shimmer Animation**
```css
@keyframes shimmer {
  0% { background-position: -1000px 0; }
  100% { background-position: 1000px 0; }
}

.shimmer {
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255,255,255,0.4),
    transparent
  );
  background-size: 1000px 100%;
  animation: shimmer 2s infinite;
}
```

---

## 🎯 DO'S AND DON'TS

### **✅ DO**
- Sử dụng gradient thay vì màu flat
- Rounded corners lớn (xl, 2xl, 3xl)
- Hover effects: scale + shadow
- Glassmorphism cho modals
- Smooth transitions (200-300ms)
- Mobile-first responsive

### **❌ DON'T**
- Màu flat không gradient
- Rounded-md/lg quá nhỏ
- Góc vuông (không rounded)
- Animations quá nhanh (<100ms)
- Quá nhiều màu sắc rối mắt
- Bỏ qua responsive mobile

---

**Cập nhật lần cuối:** 16/12/2025  
**Trạng thái:** ✅ Production Design System Complete
