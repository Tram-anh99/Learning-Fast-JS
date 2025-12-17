<script setup>
/**
 * ========== VIEW: HomeView.vue ==========
 * Purpose: Trang tra cứu nông sản - Giao diện chính kết hợp bản đồ & danh sách
 * 
 * Architecture:
 *   - Composable: src/composables/useHome.js (Logic & state management)
 *   - Components:
 *     • MapLayerSelector.vue - Dropdown chọn lớp tile bản đồ
 *     • SidebarHeader.vue - Header search & back button + autocomplete
 *     • FilterTabs.vue - Tabs filter theo trạng thái
 *     • ProductList.vue - Danh sách sản phẩm
 *     • HomeDetailView.vue - Chi tiết vùng trồng
 *     • QRScanner.vue - Modal quét/nhập mã QR
 *     • QRModal.vue - Modal QR code share
 *   - Styling: src/assets/styles/tailwind.css (Global utilities)
 * 
 * Features:
 *   - Leaflet bản đồ tương tác với polygon vùng trồng
 *   - Danh sách tra cứu có tìm kiếm & lọc theo trạng thái
 *   - Autocomplete gợi ý khi gõ tìm kiếm
 *   - Quét mã QR hoặc nhập thủ công
 *   - View chi tiết với timeline nhật ký canh tác
 *   - Modal QR code để chia sẻ truy xuất nguồn gốc
 */

// ========== IMPORTS ==========
import { onMounted, watch, ref, computed } from 'vue'; // Vue hooks & functions
import { useRouter } from 'vue-router'; // Router untuk navigation
// Components
import MapLayerSelector from '../components/MapLayerSelector.vue'; // Layer selector component
import SidebarHeader from '../components/SidebarHeader.vue'; // Header component
import FilterTabs from '../components/FilterTabs.vue'; // Filter tabs component
import ProductList from '../components/ProductList.vue'; // Product list component
import HomeDetailView from '../components/HomeDetailView.vue'; // Component chi tiết vùng
import QRScanner from '../components/QRScanner.vue'; // QR Scanner component
import QRModal from '../components/QRModal.vue'; // Component Modal QR code
// Composable
import {
  // State & Refs
  boLocHienTai, // Bộ lọc trạng thái hiện tại
  vungDangXem, // Vùng đang xem chi tiết
  searchQuery, // Keyword tìm kiếm
  showQR, // Hiển thị QR modal hay không
  qrLink, // Link QR
  mapContainer, // Ref container bản đồ
  danhSachTimKiem, // Danh sách sau lọc & tìm kiếm
  danhSachGoc, // Danh sách gốc (tất cả sản phẩm)
  currentLayer, // Lớp tile hiện tại
  // Helper functions
  getMapColor, // Lấy màu theo trạng thái (từ useMapLogic)
  chonVung, // Chọn vùng để xem chi tiết
  quayLaiDanhSach, // Quay lại danh sách
  veLaiBanDo, // Vẽ lại bản đồ
  openQRModal, // Mở QR modal
  closeQRModal, // Đóng QR modal
  changeTileLayer, // Thay đổi tile layer
  initMap // Khởi tạo bản đồ
} from '../composables/useHome';

// Router instance
const router = useRouter();

// ========== STATE ==========
// State: Hiển thị/ẩn QR Scanner modal
const showQRScanner = ref(false);

// State: Thu nhỏ/mở rộng sidebar (desktop)
const isSidebarCollapsed = ref(false);
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};

// State: Hiển thị/ẩn sidebar trên mobile
const isMobileSidebarVisible = ref(true);
const toggleMobileSidebar = () => {
  isMobileSidebarVisible.value = !isMobileSidebarVisible.value;
};

// ========== COMPUTED ==========
/**
 * Computed: Lấy danh sách gợi ý autocomplete
 * Lọc dựa trên searchQuery từ tất cả sản phẩm
 */
const autocompleteSuggestions = computed(() => {
  // Nếu searchQuery trống, return mảng rỗng
  if (!searchQuery.value.trim()) return [];

  // Lấy từ khóa viết thường để so sánh
  const query = searchQuery.value.toLowerCase();

  // Lọc sản phẩm có tên hoặc mã chứa từ khóa
  return danhSachGoc.value
    .filter(item =>
      item.ten.toLowerCase().includes(query) ||
      item.ma.toLowerCase().includes(query)
    )
    .slice(0, 5); // Giới hạn 5 gợi ý
});

// ========== HANDLERS ==========
/**
 * Handler: Set bộ lọc
 * Cập nhật giá trị boLocHienTai khi user chọn tab
 */
const setLocFilter = (value) => {
  boLocHienTai.value = value; // Cập nhật bộ lọc hiện tại
};

/**
 * Handler: Thay đổi tile layer
 * Gọi hàm changeTileLayer từ composable
 */
const handleLayerChange = (layer) => {
  changeTileLayer(layer); // Thay đổi lớp tile bản đồ
};

/**
 * Handler: Chọn một gợi ý từ autocomplete
 * @param {Object} suggestion - Sản phẩm được chọn
 */
const handleSelectSuggestion = (suggestion) => {
  // Cập nhật searchQuery với tên sản phẩm
  searchQuery.value = suggestion.ten;
  // Chọn vùng này để xem chi tiết
  chonVung(suggestion);
};

/**
 * Handler: Mở QR Scanner modal
 */
const handleOpenQRScanner = () => {
  showQRScanner.value = true;
};

/**
 * Handler: Đóng QR Scanner modal
 */
const handleCloseQRScanner = () => {
  showQRScanner.value = false;
};

/**
 * Handler: Xử lý khi user quét/nhập mã QR
 * @param {string} qrCode - Mã QR được quét
 */
const handleQRScan = (qrCode) => {
  // Tìm sản phẩm theo mã QR (mã lô)
  const product = danhSachGoc.value.find(item => item.ma === qrCode);

  if (product) {
    // Nếu tìm thấy, chọn và xem chi tiết
    chonVung(product);
    // Đóng scanner
    showQRScanner.value = false;
  } else {
    // TODO: Hiển thị notification "không tìm thấy sản phẩm"
    console.warn('Không tìm thấy sản phẩm với mã:', qrCode);
  }
};

// ========== LIFECYCLE ==========
/**
 * Hook: Khởi tạo bản đồ khi component được mounted
 */
onMounted(() => {
  console.log('[HomeView] Mounting, initializing map with HOME mode');
  initMap('home'); // Gọi hàm khởi tạo map với mode 'home' để load ArcGIS tiles
  console.log('[HomeView] Map initialized, drawing polygons');
  veLaiBanDo(danhSachTimKiem.value); // Vẽ polygons cho danh sách hiện tại
});

/**
 * Watch: Vẽ lại bản đồ khi danh sách tìm kiếm thay đổi
 * Khi lọc hoặc tìm kiếm thay đổi, danh sách polygon cần được update
 */
watch(danhSachTimKiem, veLaiBanDo);
</script>

<template>
  <!-- ========== ROOT CONTAINER: WebGIS Layout ==========
       - Class: absolute inset-0 flex - Absolute positioning, chiếm 100% viewport, flex layout
       - Layout: Flex container chứa map background & floating sidebar overlay
       - Z-index layers: map (z-0) → layer selector (z-999) → sidebar (z-1000)
  -->
  <div class="absolute inset-0 flex">

    <!-- ========== LEAFLET MAP CONTAINER ==========
         - ref="mapContainer" - Reference để khởi tạo Leaflet map instance
         - Classes: w-full h-full z-0 bg-gray-200 - Full size, gray background placeholder
         - Purpose: Nền bản đồ toàn màn hình cho WebGIS
         - Library: Leaflet (initMap() khởi tạo trong onMounted)
    -->
    <div ref="mapContainer" class="z-0 w-full h-full bg-gray-200"></div>

    <!-- ========== MAP LAYER SELECTOR COMPONENT ==========
         - Component: MapLayerSelector.vue
         - Props:
           • :currentLayer - Lớp tile hiện tại (OpenStreetMap, Satellite, v.v.)
         - Emits:
           • @changeLayer - Khi user chọn lớp tile khác
         - Position: Floating absolute (góc trên bên phải)
         - Handler: handleLayerChange() - Gọi changeTileLayer() từ composable
    -->
    <MapLayerSelector :currentLayer="currentLayer" @changeLayer="handleLayerChange" />

    <!-- ========== MOBILE TOGGLE BUTTON ==========
         - Nút floating để ẩn/hiện sidebar trên mobile
         - Chỉ hiển thị trên màn hình < 640px
    -->
    <button 
      @click="toggleMobileSidebar" 
      class="mobile-sidebar-toggle"
      :class="{ 'sidebar-hidden': !isMobileSidebarVisible }"
      :title="isMobileSidebarVisible ? 'Ẩn danh sách' : 'Hiện danh sách'"
    >
      <i class="fas" :class="isMobileSidebarVisible ? 'fa-times' : 'fa-list'"></i>
    </button>

    <!-- ========== FLOATING SIDEBAR CONTAINER ==========
         - Tag: <aside> - Semantic HTML cho sidebar
         - Classes: absolute top-2.5 left-2.5 bottom-2.5 w-[360px] rounded-2xl overflow-hidden flex flex-col z-1000
         - Layout: flex flex-col để organize nội dung dọc
         - Features:
           • Glass-morphism effect (backdrop-filter blur, rgba transparency) - CSS class .floating-sidebar
           • Rounded corners rounded-2xl (16px)
           • Overflow hidden để clip nội dung vượt quá
           • Collapsible với nút toggle
         - Z-index: z-1000 (cao hơn map & layer selector)
         - Responsive: Nhỏ hơn trên mobile (< 640px), 360px trên tablet+
    -->
    <aside
      class="floating-sidebar absolute top-2 left-3 right-3 sm:right-auto bottom-[75px] sm:bottom-2.5 sm:top-2.5 sm:left-2.5 rounded-xl sm:rounded-2xl overflow-hidden flex flex-col z-[1000] transition-all duration-300"
      :class="[
        isSidebarCollapsed ? 'w-[60px]' : 'sm:w-[360px]',
        { 'mobile-sidebar-hidden': !isMobileSidebarVisible }
      ]">

      <!-- Toggle Button -->
      <button 
        @click="toggleSidebar" 
        class="sidebar-toggle-btn"
        :title="isSidebarCollapsed ? 'Mở rộng' : 'Thu nhỏ'"
      >
        <i class="fas" :class="isSidebarCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'"></i>
      </button>

      <!-- Sidebar Content with Transition -->
      <transition name="sidebar-content">
        <div v-if="!isSidebarCollapsed" class="sidebar-content-wrapper">
          <!-- ========== SIDEBAR HEADER COMPONENT ==========
           - Component: SidebarHeader.vue
           - Props:
             • :isDetailMode - Boolean, true khi xem chi tiết (điều chỉnh layout)
             • :searchQuery - String, từ khóa tìm kiếm hiện tại
             • :suggestions - Array, danh sách gợi ý autocomplete (5 items)
           - Emits:
             • @update:searchQuery - Cập nhật searchQuery (v-model pattern)
             • @selectSuggestion - Khi chọn một gợi ý (call handleSelectSuggestion)
             • @back - Khi click back button (call quayLaiDanhSach)
             • @scanQR - Khi click QR scan button (call handleOpenQRScanner)
           - Features:
             • Search input với debounce
             • Autocomplete dropdown
             • Back button hiển thị ở detail mode
             • QR scan button
      -->
      <SidebarHeader :isDetailMode="!!vungDangXem" :searchQuery="searchQuery" :suggestions="autocompleteSuggestions"
        @update:searchQuery="searchQuery = $event" @selectSuggestion="handleSelectSuggestion" @back="quayLaiDanhSach"
        @scanQR="handleOpenQRScanner" />

      <!-- ========== SIDEBAR CONTENT AREA: CONDITIONAL RENDERING ==========
           - Logic: v-if="!vungDangXem" - Kiểm tra xem có vùng nào được chọn hay không
           - Display list view nếu không xem chi tiết, detail view nếu có
      -->

      <!-- ========== LIST VIEW: Hiển thị danh sách sản phẩm ==========
           - Condition: v-if="!vungDangXem" - True khi không xem chi tiết
           - Classes: flex flex-col flex-grow overflow-y-auto scrollbar-custom
             • flex flex-col - Flex column layout
             • flex-grow - Chiếm hết không gian còn lại
             • overflow-y-auto - Enable vertical scrolling
             • scrollbar-custom - Custom scrollbar styling
      -->
      <div v-if="!vungDangXem" class="flex flex-col flex-grow overflow-y-auto scrollbar-custom">

        <!-- ========== FILTER TABS COMPONENT ==========
             - Component: FilterTabs.vue
             - Props:
               • :activeFilter - Bộ lọc được chọn (Tất cả, Đang canh tác, Thu hoạch, v.v.)
             - Emits:
               • @filterChange - Khi user chọn tab (call setLocFilter)
             - Features:
               • Hiển thị các tab: "Tất cả", "Đang canh tác", "Thu hoạch", "Nghỉ đất", v.v.
               • Tab active có highlight color
               • Cập nhật boLocHienTai trong state
        -->
        <FilterTabs :activeFilter="boLocHienTai" @filterChange="setLocFilter" />

        <!-- ========== PRODUCT LIST COMPONENT ==========
             - Component: ProductList.vue
             - Props:
               • :items - Danh sách sản phẩm/vùng sau lọc & tìm kiếm (danhSachTimKiem)
               • :getClassTrangThai - Hàm helper lấy CSS class theo trạng thái
               • :getTextTrangThai - Hàm helper lấy text trạng thái (Tiếng Việt)
             - Emits:
               • @select - Khi user chọn một sản phẩm (call chonVung)
             - Features:
               • Hiển thị danh sách từng vùng/sản phẩm
               • Mỗi item có icon trạng thái, tên, mã, diện tích
               • Empty state nếu không có sản phẩm (lọc không trùng)
               • Scrollable nếu danh sách dài
        -->
        <ProductList :items="danhSachTimKiem" @select="chonVung" />
      </div>

      <!-- ========== DETAIL VIEW: Hiển thị chi tiết vùng ==========
           - Component: HomeDetailView.vue
           - Condition: v-else - True khi vungDangXem không null
           - Props:
             • :vung - Vùng được chọn (object với đủ thông tin chi tiết)
           - Emits:
             • @back - Khi click back button (call quayLaiDanhSach)
             • @openQR - Khi click QR button, truyền mã vùng (call openQRModal)
           - Features:
             • Hiển thị thông tin chi tiết vùng (tên, mã, diện tích, trạng thái, v.v.)
             • Timeline nhật ký canh tác
             • Nút QR để share link truy xuất
             • Back button để quay lại danh sách
      -->
      <HomeDetailView v-else :vung="vungDangXem" @back="quayLaiDanhSach" @openQR="(ma) => openQRModal(ma)" />

        </div>
      </transition>

    </aside>

    <!-- ========== QR SCANNER COMPONENT: Modal quét mã QR ==========
         - Component: QRScanner.vue
         - Props:
           • :show - Boolean, điều khiển hiển thị/ẩn modal
         - Emits:
           • @close - Khi user click close/cancel button (call handleCloseQRScanner)
           • @scan - Khi quét thành công hoặc nhập mã QR (call handleQRScan)
         - Features:
           • Camera access để quét QR code
           • Fallback input field để nhập thủ công
           • Cross-browser compatibility
         - Handler: handleQRScan(qrCode) - Tìm sản phẩm theo mã, chọn nó
    -->
    <QRScanner :show="showQRScanner" @close="handleCloseQRScanner" @scan="handleQRScan" />

    <!-- ========== QR MODAL COMPONENT: Hiển thị QR code share ==========
         - Component: QRModal.vue
         - Props:
           • :show - Boolean, điều khiển hiển thị/ẩn modal
           • :qrValue - String, link hoặc mã để sinh QR (VD: "https://farm-trace.local/trace/VT-001")
         - Emits:
           • @close - Khi user click close/outside modal (call closeQRModal)
         - Features:
           • Sinh QR code từ qrValue (library QRCode.js hoặc tương tự)
           • Hiển thị QR code trong modal
           • Nút download hoặc copy link
         - Called by: HomeDetailView component khi user click QR button
    -->
    <QRModal :show="showQR" :qrValue="qrLink" @close="closeQRModal" />

  </div>
</template>

<style scoped>
/**
 * ========== STYLES: HomeView.vue ==========
 * Trang WebGIS tra cứu nông sản - Minimal CSS (chủ yếu dùng Tailwind)
 * 
 * Note: Hầu hết styling được thực hiện bằng Tailwind utilities trong template.
 * Chỉ CSS custom phức tạp mới được định nghĩa ở đây.
 */

/* Glass-morphism effect cho sidebar - Cần custom CSS do backdrop-filter phức tạp */
.floating-sidebar {
  background: rgba(251, 252, 237, 0.85);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  box-shadow: 0 8px 32px rgba(36, 80, 75, 0.2);
}

/* Toggle Button for Sidebar */
.sidebar-toggle-btn {
  position: absolute;
  right: -15px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: #24504b;
  color: #fbfced;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

/* Ẩn toggle button trên mobile vì sidebar đã full width */
@media (max-width: 639px) {
  .sidebar-toggle-btn {
    display: none;
  }
  
  /* Ẩn sidebar trên mobile khi state = false */
  .mobile-sidebar-hidden {
    transform: translateX(-100%);
    opacity: 0;
    pointer-events: none;
  }
}

/* Nút toggle sidebar trên mobile */
.mobile-sidebar-toggle {
  display: none;
  position: absolute;
  bottom: 90px;
  left: 12px;
  z-index: 1100;
  background: #24504b;
  color: #fbfced;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
  transition: all 0.3s ease;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.mobile-sidebar-toggle:hover {
  background: #1a3d39;
  transform: scale(1.1);
}

.mobile-sidebar-toggle:active {
  transform: scale(0.95);
}

/* Khi sidebar ẩn, di chuyển nút sang vị trí khác */
.mobile-sidebar-toggle.sidebar-hidden {
  background: #10b981;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4);
}

@media (max-width: 639px) {
  .mobile-sidebar-toggle {
    display: flex;
  }
}

.sidebar-toggle-btn:hover {
  background: #1a3d39;
  transform: translateY(-50%) scale(1.15);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

/* Sidebar Content Wrapper */
.sidebar-content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

/* Sidebar Content Animation */
.sidebar-content-enter-active,
.sidebar-content-leave-active {
  transition: all 0.3s ease;
}

.sidebar-content-enter-from,
.sidebar-content-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.sidebar-content-enter-to,
.sidebar-content-leave-from {
  opacity: 1;
  transform: translateX(0);
}

/* Gradient background cho sidebar header */
.sidebar-header {
  background: #24504b;
  transition: all 0.3s;
}
</style>