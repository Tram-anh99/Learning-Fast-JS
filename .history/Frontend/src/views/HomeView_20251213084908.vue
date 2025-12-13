<script setup>
/**
 * ========== VIEW: HomeView.vue ==========
 * Purpose: Trang tra cứu nông sản - Giao diện chính kết hợp bản đồ & danh sách
 * 
 * Architecture:
 *   - Composable: src/composables/useHome.js (Logic & state management)
 *   - Components:
 *     • MapLayerSelector.vue - Dropdown chọn lớp tile bản đồ
 *     • SidebarHeader.vue - Header search & back button
 *     • FilterTabs.vue - Tabs filter theo trạng thái
 *     • ProductList.vue - Danh sách sản phẩm
 *     • HomeDetailView.vue - Chi tiết vùng trồng
 *     • QRModal.vue - Modal QR code
 *   - Styling: src/assets/styles/tailwind.css (Global utilities)
 * 
 * Features:
 *   - Leaflet bản đồ tương tác với polygon vùng trồng
 *   - Danh sách tra cứu có tìm kiếm & lọc theo trạng thái
 *   - View chi tiết với timeline nhật ký canh tác
 *   - Modal QR code để chia sẻ truy xuất nguồn gốc
 */

// ========== IMPORTS ==========
import { onMounted, watch } from 'vue'; // Vue hooks
import { useRouter } from 'vue-router'; // Router untuk navigation
// Components
import MapLayerSelector from '../components/MapLayerSelector.vue'; // Layer selector component
import SidebarHeader from '../components/SidebarHeader.vue'; // Header component
import FilterTabs from '../components/FilterTabs.vue'; // Filter tabs component
import ProductList from '../components/ProductList.vue'; // Product list component
import HomeDetailView from '../components/HomeDetailView.vue'; // Component chi tiết vùng
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
  currentLayer, // Lớp tile hiện tại
  // Helper functions
  getClassTrangThai, // Lấy class CSS theo trạng thái
  getTextTrangThai, // Lấy text trạng thái
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

/**
 * Handler set bộ lọc
 * Cập nhật giá trị boLocHienTai khi user chọn tab
 */
const setLocFilter = (value) => {
  boLocHienTai.value = value; // Cập nhật bộ lọc hiện tại
};

/**
 * Handler thay đổi tile layer
 * Gọi hàm changeTileLayer từ composable
 */
const handleLayerChange = (layer) => {
  changeTileLayer(layer); // Thay đổi lớp tile bản đồ
};

/**
 * Hook: Khởi tạo bản đồ khi component được mounted
 */
onMounted(() => {
  initMap(); // Gọi hàm khởi tạo map từ composable
});

/**
 * Watch: Vẽ lại bản đồ khi danh sách tìm kiếm thay đổi
 * Khi lọc hoặc tìm kiếm thay đổi, danh sách polygon cần được update
 */
watch(danhSachTimKiem, veLaiBanDo);
</script>

<template>
  <!-- Container chính: flex container chứa map & sidebar -->
  <div class="webgis-container">

    <!-- Leaflet Map container: toàn bộ nền -->
    <div ref="mapContainer" class="map-container"></div>

    <!-- Layer selector component: dropdown thay đổi lớp tile (góc trên bên phải) -->
    <MapLayerSelector :currentLayer="currentLayer" @changeLayer="handleLayerChange" />

    <!-- Sidebar: floating sidebar bên trái hiển thị danh sách hoặc chi tiết -->
    <aside class="floating-sidebar">

      <!-- Header component: search input hoặc back button -->
      <SidebarHeader
        :isDetailMode="!!vungDangXem"
        :searchQuery="searchQuery"
        @update:searchQuery="searchQuery = $event"
        @back="quayLaiDanhSach" />

      <!-- ========== CONTENT AREA ========== -->

      <!-- List view: hiển thị khi không xem chi tiết -->
      <div v-if="!vungDangXem" class="flex flex-col flex-grow overflow-hidden">

        <!-- Filter tabs component: các tab lọc theo trạng thái -->
        <FilterTabs :activeFilter="boLocHienTai" @filterChange="setLocFilter" />

        <!-- Product list component: danh sách sản phẩm hoặc empty state -->
        <ProductList
          :items="danhSachTimKiem"
          :getClassTrangThai="getClassTrangThai"
          :getTextTrangThai="getTextTrangThai"
          @select="chonVung" />
      </div>

      <!-- Detail view -->
      <HomeDetailView v-else :vung="vungDangXem" @back="quayLaiDanhSach" @openQR="(ma) => openQRModal(ma)" />

    </aside>

    <!-- QR Modal -->
    <QRModal :show="showQR" :qrValue="qrLink" @close="closeQRModal" />

  </div>
</template>

<style scoped>
/* ========== LAYOUT CONTAINER ========== */
.webgis-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
}

/* Map container */
.map-container {
  width: 100%;
  height: 100%;
  z-index: 0;
  background-color: #e5e7eb;
}

/* ========== SIDEBAR ========== */
.floating-sidebar {
  position: absolute;
  top: 10px;
  left: 10px;
  bottom: 10px;
  width: 360px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  border: 1px solid rgba(255, 255, 255, 0.5);
  overflow: hidden;
}

/* ========== SIDEBAR HEADER ========== */
.sidebar-header {
  background: linear-gradient(to right, #1b4332, #2d6a4f);
  color: white;
  display: flex;
  align-items: center;
  transition: all 0.3s;
}

.sidebar-header.detail-mode {
  padding: 0;
}
</style>