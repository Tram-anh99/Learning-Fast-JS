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
 *     • HomeQRModal.vue - Modal QR code
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
import HomeQRModal from '../components/HomeQRModal.vue';
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
          <div class="bg-green-900 rounded-t-2xl p-4">
            <div class="relative">
              <!-- Search icon -->
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-green-300 pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              
              <!-- Search input -->
              <input 
                v-model="searchQuery" 
                type="text" 
                placeholder="Tìm nông sản..." 
                class="w-full pl-10 pr-3 py-2 bg-green-800 text-white placeholder-green-300 rounded-lg focus:outline-none focus:bg-green-700 focus:ring-1 focus:ring-green-400 transition-colors"
              >
            </div>
          </div>
        </div>

        <div v-else class="header-content detail">
          <button 
            @click="quayLaiDanhSach"
            class="p-2 hover:bg-white/20 rounded-lg transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
          <h3 class="text-white font-bold">Thông tin Chi tiết</h3>
        </div>
      </header>

      <!-- ========== CONTENT AREA ========== -->
      
      <!-- List view -->
      <div v-if="!vungDangXem" class="flex flex-col flex-grow overflow-hidden">
        
        <!-- Tabs -->
        <div class="flex gap-1 p-2 bg-white/30 border-b border-gray-100">
          <button 
            v-for="tab in ['all', 'canh_tac', 'thu_hoach']"
            :key="tab"
            @click="boLocHienTai = tab"
            :class="[
              'flex-1 py-2 px-3 rounded-lg text-sm font-semibold transition-all',
              boLocHienTai === tab 
                ? 'bg-white text-green-700 shadow-sm' 
                : 'text-gray-600 hover:text-gray-800'
            ]"
          >
            {{ tab === 'all' ? 'Tất cả' : tab === 'canh_tac' ? 'Canh tác' : 'Thu hoạch' }}
          </button>
        </div>

        <!-- Item list -->
        <div class="flex-grow overflow-y-auto p-3 space-y-2">
          <ul class="space-y-2">
            <HomeListItem 
              v-for="item in danhSachTimKiem"
              :key="item.id"
              :item="item"
              :getClassTrangThai="getClassTrangThai"
              :getTextTrangThai="getTextTrangThai"
              @select="chonVung"
            />
          </ul>
          
          <!-- Empty state -->
          <div v-if="danhSachTimKiem.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 mb-2 opacity-30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-sm">Không tìm thấy nông sản nào</p>
          </div>
        </div>
      </div>

      <!-- Detail view -->
      <HomeDetailView 
        v-else
        :vung="vungDangXem"
        @back="quayLaiDanhSach"
        @openQR="(ma) => openQRModal(ma)"
      />

    </aside>

    <!-- QR Modal -->
    <HomeQRModal 
      :show="showQR"
      :qrLink="qrLink"
      @close="closeQRModal"
    />

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
</style>

<template>
  <div>
  <div class="webgis-container">
    <div ref="mapContainer" class="map-container"></div>

    <aside class="floating-sidebar">

      <div class="sidebar-header" :class="{ 'detail-mode': vungDangXem }">
        <div v-if="!vungDangXem" class="header-content">
          <!-- <h3><i class="fas fa-search-location"></i> Tra cứu Nông sản</h3>
          <span class="count-badge">{{ danhSachHienThi.length }} kết quả</span> -->
          <div class="p-4 bg-green-900 shadow-md rounded-t-2xl">
  <div class="relative">
    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
      <svg class="w-5 h-5 text-green-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>

    <input 
      v-model="searchQuery" 
      type="text" 
      placeholder="Tìm nông sản..." 
      class="block w-full py-2 pl-10 pr-3 leading-5 text-white placeholder-green-300 transition bg-green-800 border-transparent rounded-lg focus:outline-none focus:bg-green-700 focus:ring-1 focus:ring-green-400 sm:text-sm"
    >
  </div>
</div>
        </div>
        
        <div v-else class="header-content detail">
          <button @click="quayLaiDanhSach" class="btn-back"><i class="fas fa-arrow-left"></i></button>
          <h3>Thông tin Chi tiết</h3>
        </div>
        
      </div>

      <div v-if="!vungDangXem" class="list-view">
        <div class="sidebar-tabs">
          <button class="tab-btn" :class="{ active: boLocHienTai === 'all' }" @click="boLocHienTai = 'all'">Tất
            cả</button>
          <button class="tab-btn" :class="{ active: boLocHienTai === 'canh_tac' }"
            @click="boLocHienTai = 'canh_tac'">Canh tác</button>
          <button class="tab-btn" :class="{ active: boLocHienTai === 'thu_hoach' }"
            @click="boLocHienTai = 'thu_hoach'">Thu hoạch</button>
        </div>

        <div class="sidebar-content">
          <ul class="layer-list">
            <li v-for="vung in danhSachHienThi" :key="vung.id" class="layer-item" @click="chonVung(vung)">
              <div class="item-thumb" :style="{ backgroundImage: `url(${vung.anh})` }"></div>
              <div class="item-info">
                <span class="item-name">{{ vung.ten }}</span>
                <span class="item-sub"> <i class="fas fa-certificate"></i> {{ vung.chungNhan }}</span>
              </div>
              <div class="item-status" :class="getClassTrangThai(vung.trangThai)">{{ getTextTrangThai(vung.trangThai) }}
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div v-else class="detail-view">
        <div class="detail-cover" :style="{ backgroundImage: `url(${vungDangXem.anh})` }">
          <div class="overlay">
            <h2>{{ vungDangXem.ten }}</h2>
            <span class="cert-badge"><i class="fas fa-check-circle"></i> {{ vungDangXem.chungNhan }}</span>
          </div>
        </div>

        <div class="detail-content">
          <div class="info-grid">
            <div class="info-box">
              <label>Mã số</label>
              <strong>{{ vungDangXem.ma }}</strong>
            </div>
            <div class="info-box">
              <label>Diện tích</label>
              <strong>{{ vungDangXem.dienTich }}</strong>
            </div>
          </div>

          <div class="timeline-section">
            <h4><i class="fas fa-history"></i> Nhật ký Canh tác</h4>
            <div class="timeline">
              <div v-for="(log, idx) in vungDangXem.nhatKy" :key="idx" class="timeline-item">
                <div class="time-dot"></div>
                <div class="time-content">
                  <span class="time-date">{{ log.ngay }}</span>
                  <strong class="time-action">{{ log.hoatDong }}</strong>
                  <p class="time-desc">{{ log.chiTiet }}</p>
                </div>
              </div>
            </div>
          </div>

          <button class="btn-qr" @click="openQRModal('LUA-ST25-003')" ><i class="fas fa-qrcode"></i> Quét mã Truy xuất nguồn gốc</button>
     
        </div>
      </div>

    </aside>
  </div>
  <div v-if="showQR" class="fixed inset-0 z-50 flex items-center justify-center p-4" style="background-color: rgba(0,0,0,0.6);" @click.self="showQR = false">
  
  <div class="w-full max-w-sm p-6 text-center bg-white shadow-2xl rounded-2xl animate-scale">
    
    <h3 class="mb-2 text-xl font-bold text-gray-800">Mã QR Truy xuất</h3>
    <p class="mb-6 text-sm text-gray-500">Dùng Zalo hoặc Camera để quét mã này</p>

    <div class="flex justify-center mb-6">
      <div class="inline-block p-4 bg-white border-2 border-green-500 rounded-xl">
        <qrcode-vue 
          :value="qrLink" 
          :size="220" 
          level="H" 
          render-as="svg"
          foreground="#15803d"
        />
      </div>
    </div>

    <p class="text-[10px] text-gray-400 bg-gray-100 p-2 rounded truncate mb-4">
      {{ qrLink }}
    </p>

    <button 
      @click="showQR = false"
      class="w-full py-3 font-bold text-gray-800 transition bg-gray-200 hover:bg-gray-300 rounded-xl">
      Đóng lại
    </button>
  </div>

</div>
</div>

</template>

<style scoped>
/* --- GIỮ CSS LAYOUT CŨ --- */
.webgis-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
}

.map-container {
  width: 100%;
  height: 100%;
  z-index: 0;
  background-color: #e5e7eb;
}

/* --- SIDEBAR CHO KHÁCH --- */
.floating-sidebar {
  position: absolute;
  top: 10px;
  left: 10px;
  bottom: 10px;
  width: 360px;
  /* Rộng hơn chút để hiện ảnh đẹp */
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

/* HEADER */
.sidebar-header {
  padding: 16px 20px;
  background: linear-gradient(to right, #1b4332, #2d6a4f);
  color: white;
  display: flex;
  align-items: center;
  transition: all 0.3s;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-content.detail {
  justify-content: flex-start;
  gap: 15px;
}

.count-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.btn-back {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
}

/* LIST VIEW */
.sidebar-tabs {
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.3);
  padding: 5px;
  gap: 5px;
}

.tab-btn {
  flex: 1;
  padding: 8px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
  border-radius: 6px;
}

.tab-btn.active {
  background: white;
  color: #1b4332;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.list-view,
.detail-view {
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.sidebar-content {
  padding: 10px;
}

.layer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.layer-item {
  background: rgba(255, 255, 255, 0.6);
  border-radius: 12px;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid white;
}

.layer-item:hover {
  transform: translateY(-3px);
  background: white;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.item-thumb {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  background-size: cover;
  background-position: center;
  flex-shrink: 0;
}

.item-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.item-name {
  font-weight: 700;
  font-size: 0.95rem;
  color: #1b4332;
}

.item-sub {
  font-size: 0.75rem;
  color: #555;
  display: flex;
  align-items: center;
  gap: 4px;
}

.item-status {
  font-size: 0.65rem;
  padding: 2px 6px;
  border-radius: 4px;
  color: white;
  white-space: nowrap;
}

.status-green {
  background: #4caf50;
}

.status-red {
  background: #ef5350;
}

.status-yellow {
  background: #ffca28;
  color: #333;
}

/* DETAIL VIEW STYLES (ĐẸP & HIỆN ĐẠI) */
.detail-cover {
  height: 180px;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: flex-end;
}

.detail-cover .overlay {
  width: 100%;
  padding: 15px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
}

.detail-cover h2 {
  margin: 0;
  font-size: 1.4rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.cert-badge {
  background: #ffca28;
  color: #333;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: bold;
  margin-top: 5px;
  display: inline-block;
}

.detail-content {
  padding: 15px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.info-box {
  background: rgba(255, 255, 255, 0.5);
  padding: 10px;
  border-radius: 8px;
  border: 1px solid white;
}

.info-box label {
  display: block;
  font-size: 0.75rem;
  color: #666;
  margin-bottom: 2px;
}

.info-box strong {
  color: #1b4332;
  font-size: 1rem;
}

/* TIMELINE (DÒNG THỜI GIAN) */
.timeline-section h4 {
  margin: 0 0 15px 0;
  color: #1b4332;
  border-bottom: 2px solid rgba(27, 67, 50, 0.1);
  padding-bottom: 5px;
}

.timeline {
  border-left: 2px solid #ddd;
  margin-left: 5px;
  padding-left: 20px;
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.time-dot {
  width: 12px;
  height: 12px;
  background: #4caf50;
  border-radius: 50%;
  position: absolute;
  left: -27px;
  top: 5px;
  border: 2px solid white;
  box-shadow: 0 0 0 2px #4caf50;
}

.time-date {
  font-size: 0.75rem;
  color: #888;
  display: block;
  margin-bottom: 2px;
}

.time-action {
  color: #333;
  display: block;
  font-weight: 600;
}

.time-desc {
  margin: 2px 0 0 0;
  font-size: 0.85rem;
  color: #555;
}

.btn-qr {
  margin-top: auto;
  background: #1b4332;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-qr:hover {
  background: #2d6a4f;
}
/* Hiệu ứng phóng to nhẹ khi hiện popup */
.animate-scale {
  animation: scaleUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}
</style>