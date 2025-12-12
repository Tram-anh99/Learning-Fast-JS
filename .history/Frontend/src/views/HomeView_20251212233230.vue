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

import { onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import HomeListItem from '../components/HomeListItem.vue';
import HomeDetailView from '../components/HomeDetailView.vue';
import QRModal from '../components/QRModal.vue';
import {
  boLocHienTai,
  vungDangXem,
  searchQuery,
  showQR,
  qrLink,
  mapContainer,
  danhSachTimKiem,
  getClassTrangThai,
  getTextTrangThai,
  chonVung,
  quayLaiDanhSach,
  veLaiBanDo,
  openQRModal,
  closeQRModal,
  initMap
} from '../composables/useHome';

const router = useRouter();

// Handler để set filter - unwrap ref tự động
const setLocFilter = (value) => {
  boLocHienTai.value = value;
};

// Handler for wheel scroll on filter tabs
const handleFilterWheel = (e) => {
  const container = e.currentTarget;
  if (container.scrollWidth > container.clientWidth) {
    e.preventDefault();
    container.scrollLeft += e.deltaY > 0 ? 100 : -100;
  }
};

// Khởi tạo bản đồ khi component mounted
onMounted(() => {
  initMap();
});

// Vẽ lại bản đồ khi danh sách thay đổi
watch(danhSachTimKiem, veLaiBanDo);
</script>

<template>
  <div class="webgis-container">

    <!-- Map -->
    <div ref="mapContainer" class="map-container"></div>

    <!-- Sidebar -->
    <aside class="floating-sidebar">

      <!-- ========== HEADER ========== -->
      <header class="sidebar-header" :class="{ 'detail-mode': vungDangXem }">
        <div v-if="!vungDangXem" class="w-full">
          <div class="p-4 bg-green-900 rounded-t-2xl">
            <div class="relative">
              <!-- Search icon -->
              <svg class="absolute w-5 h-5 text-green-300 -translate-y-1/2 pointer-events-none left-3 top-1/2"
                fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>

              <!-- Search input -->
              <input v-model="searchQuery" type="text" placeholder="Tìm nông sản..."
                class="w-full py-2 pl-10 pr-3 text-white placeholder-green-300 transition-colors bg-green-800 rounded-lg focus:outline-none focus:bg-green-700 focus:ring-1 focus:ring-green-400">
            </div>
          </div>
        </div>

        <div v-else class="header-content detail">
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
        <div class="flex flex-shrink-0 gap-2 p-3 overflow-x-auto overflow-y-hidden border-b border-slate-200/50 bg-gradient-to-r from-slate-50 to-blue-50 no-scrollbar" @wheel="handleFilterWheel">
          <!-- Tab All -->
          <button 
            @click="setLocFilter('all')" 
            :class="[
              'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
              boLocHienTai === 'all'
                ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
                : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
            ]"
          >
            Tất cả
          </button>

          <!-- Tab Canh tác -->
          <button 
            @click="setLocFilter('canh_tac')" 
            :class="[
              'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
              boLocHienTai === 'canh_tac'
                ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
                : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
            ]"
          >
            Canh tác
          </button>

          <!-- Tab Thu hoạch -->
          <button 
            @click="setLocFilter('thu_hoach')" 
            :class="[
              'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
              boLocHienTai === 'thu_hoach'
                ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
                : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
            ]"
          >
            Thu hoạch
          </button>

          <!-- Tab Đã thu hoạch -->
          <button 
            @click="setLocFilter('da_thu_hoach')" 
            :class="[
              'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
              boLocHienTai === 'da_thu_hoach'
                ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
                : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
            ]"
          >
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

/* Hide scrollbar but allow scrolling */
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>