/**
 * ========== COMPONENT STRUCTURE REFACTORING ==========
 * 
 * HomeView.vue đã được tách thành các components nhỏ hơn:
 * 
 * 1. MapLayerSelector.vue
 *    - Chức năng: Dropdown chọn lớp tile bản đồ (Ảnh vệ tinh / Bản đồ đường phố)
 *    - Vị trí: Góc trên bên phải
 *    - Props: currentLayer (string)
 *    - Emits: changeLayer (string)
 * 
 * 2. SidebarHeader.vue
 *    - Chức năng: Header sidebar - search input hoặc back button
 *    - Hiển thị: Search khi xem danh sách, Back button khi xem chi tiết
 *    - Props: isDetailMode (boolean), searchQuery (string)
 *    - Emits: update:searchQuery (string), back ()
 * 
 * 3. FilterTabs.vue
 *    - Chức năng: Tabs filter theo trạng thái nông sản
 *    - Options: Tất cả, Canh tác, Thu hoạch, Đã thu hoạch
 *    - Props: activeFilter (string)
 *    - Emits: filterChange (string)
 * 
 * 4. ProductList.vue
 *    - Chức năng: Danh sách sản phẩm hoặc empty state
 *    - Features: Cuộn dọc, empty state khi không có kết quả
 *    - Props: items (Array), getClassTrangThai (Function), getTextTrangThai (Function)
 *    - Emits: select (Object)
 * 
 * ========== BENEFITS ==========
 * 
 * ✓ Code tách rõ ràng - mỗi component có một trách nhiệm duy nhất
 * ✓ Dễ bảo trì - mỗi component độc lập, dễ test và debug
 * ✓ Tái sử dụng - các components có thể dùng lại ở chỗ khác
 * ✓ Dễ đọc - HomeView.vue giờ gọn gàng, dễ hiểu luồng dữ liệu
 * ✓ Flexible - dễ sửa đổi, cải thiện từng component riêng
 * 
 * ========== FILE LOCATIONS ==========
 * 
 * src/
 * ├── views/
 * │   └── HomeView.vue (Main view - orchestrator)
 * ├── components/
 * │   ├── MapLayerSelector.vue
 * │   ├── SidebarHeader.vue
 * │   ├── FilterTabs.vue
 * │   ├── ProductList.vue
 * │   ├── HomeListItem.vue
 * │   ├── HomeDetailView.vue
 * │   └── QRModal.vue
 * └── composables/
 *     └── useHome.js (State management & logic)
 */
