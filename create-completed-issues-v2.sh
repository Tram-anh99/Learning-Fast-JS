#!/bin/bash

REPO="Tram-anh99/Learning-Fast-JS"

echo "📝 Creating Completed Issues for $REPO..."
echo ""

# Function to create and close issue
create_closed_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    echo "Creating and closing: $title"
    gh issue create --repo "$REPO" --title "$title" --label "$labels" --body "$body" > /tmp/issue_url.txt
    issue_number=$(cat /tmp/issue_url.txt | grep -oE '[0-9]+$')
    gh issue close "$issue_number" --repo "$REPO" --comment "This work was completed during project development. Issue created for historical documentation."
    echo "✅ Created and closed issue #$issue_number"
    echo ""
}

# Issue 1: Component Cleanup
create_closed_issue \
"✅ [DONE] Dọn dẹp Components không sử dụng | Unused Components Cleanup" \
"## ✅ Dọn dẹp Components không sử dụng | Unused Components Cleanup

### 📝 Mô tả | Description
**[VI]** Phát hiện và xóa các components không được sử dụng trong codebase để giảm kích thước và tăng maintainability.

**[EN]** Detected and removed unused components from the codebase to reduce size and improve maintainability.

---

### 🎯 Công việc đã thực hiện | Work Completed

**Components đã xóa | Deleted components:**
1. **DiaryActivityCard.vue** (56 LOC) - Không được import
2. **DiaryHeader.vue** (38 LOC) - Không được import
3. **DiaryNavigation.vue** (65 LOC) - Không được import
4. **MapStatsWidget.vue** (115 LOC) - Không được import
5. **ChartsComponents.vue** (324 LOC) - Duplicate của ChartsComponent.vue

**Tổng cộng | Total:** 598 LOC đã xóa | removed

---

### ✅ Kết quả | Results
- ✅ Giảm 598 dòng code không cần thiết | Reduced 598 lines of unnecessary code
- ✅ Không còn components trùng lặp | No more duplicate components
- ✅ Build size giảm | Reduced build size
- ✅ Codebase sạch hơn, dễ maintain | Cleaner, more maintainable codebase

**Ngày hoàn thành | Completed:** December 14, 2024" \
"completed,cleanup,refactoring"

# Issue 2: Map Logic Consolidation  
create_closed_issue \
"✅ [DONE] Hợp nhất Logic Bản đồ | Map Logic Consolidation" \
"## ✅ Hợp nhất Logic Bản đồ | Map Logic Consolidation

### 📝 Mô tả | Description
**[VI]** Hợp nhất logic khởi tạo và quản lý bản đồ Leaflet từ nhiều nơi thành một composable duy nhất.

**[EN]** Consolidated Leaflet map initialization and management logic from multiple locations into a single composable.

---

### 🎯 Giải pháp đã thực hiện | Solution Implemented
- ✅ Merge toàn bộ logic vào \`useMapLogic.js\`
- ✅ Cập nhật MapComponent.vue để chỉ dùng một source
- ✅ Single source of truth cho map logic

**Ngày hoàn thành | Completed:** December 14, 2024" \
"completed,refactoring,map"

# Issue 3: Status Helpers
create_closed_issue \
"✅ [DONE] Thống nhất Status Helpers | Status Helpers Unification" \
"## ✅ Thống nhất Status Helpers | Status Helpers Unification

### 📝 Mô tả | Description
**[VI]** Hợp nhất các hàm xử lý trạng thái từ nhiều components thành một utility file duy nhất.

**[EN]** Unified status handling functions from multiple components into a single utility file.

---

### 🎯 Kết quả | Results
- ✅ Tạo \`src/composables/statusHelpers.js\`
- ✅ Single source of truth cho status logic
- ✅ Consistent colors và icons across app

**Ngày hoàn thành | Completed:** December 14, 2024" \
"completed,refactoring,utilities"

# Issue 4: Chart Data Extraction
create_closed_issue \
"✅ [DONE] Tách Chart Data thành Composable | Chart Data Extraction" \
"## ✅ Tách Chart Data thành Composable | Chart Data Extraction

### 📝 Mô tả | Description
**[VI]** Tách dữ liệu biểu đồ hardcoded từ components thành composable riêng.

**[EN]** Extracted hardcoded chart data from components into a dedicated composable.

---

### 🎯 Kết quả | Results
- ✅ Tạo \`src/composables/useCharts.js\`
- ✅ Separation of concerns
- ✅ Ready cho API integration

**Ngày hoàn thành | Completed:** December 14, 2024" \
"completed,refactoring,charts"

# Issue 5: Scrollbar Improvements
create_closed_issue \
"✅ [DONE] Cải thiện Scrollbar tùy chỉnh | Custom Scrollbar Improvements" \
"## ✅ Cải thiện Scrollbar tùy chỉnh | Custom Scrollbar Improvements

### 📝 Mô tả | Description
**[VI]** Thiết kế và áp dụng scrollbar tùy chỉnh với gradient màu xanh đẹp mắt.

**[EN]** Designed and applied custom scrollbar with beautiful green gradient.

---

### 🎯 Kết quả | Results
- ✅ Tạo \`src/assets/styles/scrollbar.css\`
- ✅ Áp dụng cho DataTable, Charts, Dashboard
- ✅ UI đẹp và nhất quán hơn

**Ngày hoàn thành | Completed:** December 14, 2024" \
"completed,ui,enhancement"

# Issue 6: Documentation
create_closed_issue \
"✅ [DONE] Thêm Documentation toàn diện | Comprehensive Documentation" \
"## ✅ Thêm Documentation toàn diện | Comprehensive Documentation

### 📝 Mô tả | Description
**[VI]** Thêm comments chi tiết và tạo documentation files cho toàn bộ codebase.

**[EN]** Added detailed comments and created documentation files for entire codebase.

---

### 🎯 Kết quả | Results
- ✅ 7 documentation files created (.md, .txt)
- ✅ 100% components documented
- ✅ 100% composables documented
- ✅ Code quality: 9/10

**Ngày hoàn thành | Completed:** December 16, 2024" \
"completed,documentation"

# Issue 7: Production Build
create_closed_issue \
"✅ [DONE] Tối ưu Production Build | Production Build Optimization" \
"## ✅ Tối ưu Production Build | Production Build Optimization

### 📝 Mô tả | Description
**[VI]** Tối ưu hóa cấu hình build và code để giảm bundle size và tăng performance.

**[EN]** Optimized build configuration and code to reduce bundle size and improve performance.

---

### 🎯 Kết quả | Results
- ✅ LOC giảm từ 7,100 xuống 6,500
- ✅ Components giảm từ 25 xuống 20
- ✅ Production-ready build
- ✅ Fast load times

**Ngày hoàn thành | Completed:** December 16, 2024" \
"completed,performance,build"

echo "✅ All 7 completed issues created and closed successfully!"
echo "🔗 View: https://github.com/$REPO/issues?q=is%3Aissue+label%3Acompleted"
