<script setup>
/**
 * ========== VIEW: HomeView.vue ==========
 * Purpose: Trang tra cứu nông sản - Giao diện chính kết hợp bản đồ & danh sách
 * 
 * Architecture:
 *   - Composable: src/composables/useHome.js (Logic & state management)
 *   - Components:
 *     • HomeListItem.vue - Item trong danh sách
 *     • HomeDetailView.vue - Chi tiết vùng trồng
 *     • QRModal.vue - Modal QR code (dùng chung)
 *   - Styling: src/assets/styles/tailwind.css (Global utilities)
 * 
 * Features:
 *   - Leaflet bản đồ tương tác với polygon vùng trồng
 *   - Danh sách tra cứu có tìm kiếm & lọc theo trạng thái
 *   - View chi tiết với timeline nhật ký canh tác
 *   - Modal QR code để chia sẻ truy xuất nguồn gốc
 */

// ========== IMPORTS ==========
import { onMounted, watch, ref } from 'vue'; // Vue hooks
import { useRouter } from 'vue-router'; // Router untuk navigation
import HomeListItem from '../components/HomeListItem.vue'; // Component item danh sách
import HomeDetailView from '../components/HomeDetailView.vue'; // Component chi tiết vùng
import QRModal from '../components/QRModal.vue'; // Component Modal QR code
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

const router = useRouter();

// State để hiển thị/ẩn layer selector dropdown
const showLayerSelector = ref(false);

/**
 * Handler set bộ lọc
 * Unwrap ref tự động (Vue sẽ tự bỏ .value)
 */
const setLocFilter = (value) => {
  boLocHienTai.value = value; // Cập nhật bộ lọc hiện tại
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

    <!-- Layer selector: dropdown thay đổi lớp tile (góc trên bên phải) -->
    <div class="layer-selector">
      <!-- Nút chính để toggle dropdown -->
      <button @click="showLayerSelector = !showLayerSelector" 
        class="flex items-center justify-center w-10 h-10 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow">
        <!-- Icon layers -->
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.5a2 2 0 00-1 .267V5a2 2 0 10-4 0v5.75a2 2 0 00-1-.267H5a2 2 0 00-2 2v4a2 2 0 002 2z" />
        </svg>
      </button>

      <!-- Dropdown menu -->
      <transition name="fade">
        <div v-if="showLayerSelector" class="layer-dropdown">
          <!-- Option Satellite -->
          <button @click="changeTileLayer('satellite'); showLayerSelector = false"
            :class="['layer-option', { active: currentLayer === 'satellite' }]">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5 2a1 1 0 011 1v1h1V3a1 1 0 112 0v1h1V3a1 1 0 112 0v1h1V3a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v1h1a1 1 0 110 2h-1v1h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1h-1v1a1 1 0 11-2 0v-1H6v1a1 1 0 11-2 0v-1H3a2 2 0 01-2-2v-2H0a1 1 0 110-2h1V9H0a1 1 0 110-2h1V6H0a1 1 0 110-2h1V4a2 2 0 012-2h2V3a1 1 0 011-1zm9 5a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
            </svg>
            Ảnh vệ tinh
          </button>

          <!-- Option Street Map -->
          <button @click="changeTileLayer('street'); showLayerSelector = false"
            :class="['layer-option', { active: currentLayer === 'street' }]">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10.5A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10.5A7.968 7.968 0 0014.5 4c-1.669 0-3.218.51-4.5 1.385A7.968 7.968 0 009 4.804z" />
            </svg>
            Bản đồ đường phố
          </button>
        </div>
      </transition>
    </div>

    <!-- Sidebar: floating sidebar bên trái hiển thị danh sách hoặc chi tiết -->
    <aside class="floating-sidebar">

      <!-- ========== HEADER ========== -->
      <!-- Header thay đổi nội dung dựa vào vungDangXem -->
      <header class="sidebar-header" :class="{ 'detail-mode': vungDangXem }">

        <!-- Search view: hiển thị khi không xem chi tiết vùng -->
        <div v-if="!vungDangXem" class="w-full">
          <div class="p-4 bg-green-900 rounded-t-2xl">
            <!-- Search input container -->
            <div class="relative">
              <!-- Icon tìm kiếm: SVG được định vị tuyệt đối -->
              <svg class="absolute w-5 h-5 text-green-300 -translate-y-1/2 pointer-events-none left-3 top-1/2"
                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>

              <!-- Input tìm kiếm: v-model binding với searchQuery -->
              <!-- Khi user nhập, searchQuery update tự động trigger watch và veLaiBanDo -->
              <input v-model="searchQuery" type="text" placeholder="Tìm nông sản..."
                class="w-full py-2 pl-10 pr-3 text-white placeholder-green-300 transition-colors bg-green-800 rounded-lg focus:outline-none focus:bg-green-700 focus:ring-1 focus:ring-green-400">
            </div>
          </div>
        </div>

        <!-- Detail view header: hiển thị khi xem chi tiết vùng -->
        <div v-else class="header-content detail">
          <!-- Nút quay lại: click để trở lại danh sách -->
          <button @click="quayLaiDanhSach" class="p-2 transition-colors rounded-lg hover:bg-white/20">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <h3 class="font-bold text-white">Thông tin Chi tiết</h3>
        </div>
      </header>

      <!-- ========== CONTENT AREA ========== -->

      <!-- List view -->
      <div v-if="!vungDangXem" class="flex flex-col flex-grow overflow-hidden">

        <!-- Tabs - Modern style with proper state management -->
        <div
          class="flex flex-shrink-0 gap-2 p-3 overflow-x-auto border-b border-slate-200/50 bg-gradient-to-r from-slate-50 to-blue-50">
          <!-- Tab All -->
          <button @click="setLocFilter('all')" :class="[
            'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
            boLocHienTai === 'all'
              ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
              : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
          ]">
            Tất cả
          </button>

          <!-- Tab Canh tác -->
          <button @click="setLocFilter('canh_tac')" :class="[
            'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
            boLocHienTai === 'canh_tac'
              ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
              : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
          ]">
            Canh tác
          </button>

          <!-- Tab Thu hoạch -->
          <button @click="setLocFilter('thu_hoach')" :class="[
            'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
            boLocHienTai === 'thu_hoach'
              ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
              : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
          ]">
            Thu hoạch
          </button>

          <!-- Tab Đã thu hoạch -->
          <button @click="setLocFilter('da_thu_hoach')" :class="[
            'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
            boLocHienTai === 'da_thu_hoach'
              ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
              : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
          ]">
            Đã thu hoạch
          </button>
        </div>

        <!-- Item list -->
        <div class="flex-grow p-3 space-y-2 overflow-y-auto">
          <ul class="space-y-2">
            <HomeListItem v-for="item in danhSachTimKiem" :key="item.id" :item="item"
              :getClassTrangThai="getClassTrangThai" :getTextTrangThai="getTextTrangThai" @select="chonVung" />
          </ul>

          <!-- Empty state -->
          <div v-if="danhSachTimKiem.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 mb-2 opacity-30" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-sm">Không tìm thấy nông sản nào</p>
          </div>
        </div>
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

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
}

.header-content.detail {
  justify-content: flex-start;
  gap: 12px;
  padding: 12px 16px;
}

.header-content.detail h3 {
  margin: 0;
  font-size: 1rem;
}

/* ========== LAYER SELECTOR ========== */
.layer-selector {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}

.layer-dropdown {
  background: white;
  border-radius: 8px;
  shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  min-width: 180px;
}

.layer-option {
  width: 100%;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: white;
  border: none;
  cursor: pointer;
  color: #4b5563;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.layer-option:hover {
  background-color: #f0f4f8;
  color: #1b4332;
}

.layer-option.active {
  background-color: #d1f2eb;
  color: #1b4332;
  font-weight: 600;
}

.layer-option:not(:last-child) {
  border-bottom: 1px solid #e5e7eb;
}

/* Transition animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>