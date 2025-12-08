<script setup>
import { onMounted, ref, shallowRef, computed, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const map = shallowRef(null);
const mapContainer = ref(null);
const layerGroup = shallowRef(null);
const boLocHienTai = ref('all');
const vungDangXem = ref(null); // Biến lưu vùng đang được khách click xem chi tiết

// --- DỮ LIỆU MẪU ĐÃ NÂNG CẤP (Kèm nhật ký & hình ảnh) ---
const danhSachGoc = [
  {
    id: 1, ma: 'VT-001', ten: 'Xoài Cát Hòa Lộc', dienTich: '5ha', trangThai: 'canh_tac',
    chungNhan: 'VietGAP', anh: 'https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=1000&auto=format&fit=crop',
    toaDo: [[10.762, 106.660], [10.770, 106.670], [10.760, 106.670]],
    nhatKy: [
      { ngay: '10/12/2024', hoatDong: 'Bón phân hữu cơ', chiTiet: 'Bón lót 50kg phân vi sinh' },
      { ngay: '01/12/2024', hoatDong: 'Tỉa cành', chiTiet: 'Tỉa cành tạo tán sau thu hoạch vụ trước' }
    ]
  },
  {
    id: 2, ma: 'VT-002', ten: 'Thanh Long Ruột Đỏ', dienTich: '3.2ha', trangThai: 'sau_benh',
    chungNhan: 'GlobalGAP', anh: 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?q=80&w=1000&auto=format&fit=crop',
    toaDo: [[10.780, 106.680], [10.790, 106.690], [10.780, 106.690]],
    nhatKy: [
      { ngay: '05/12/2024', hoatDong: 'Cảnh báo', chiTiet: 'Phát hiện nấm tắc kè, đã phun thuốc sinh học' }
    ]
  },
  {
    id: 3, ma: 'VT-003', ten: 'Lúa ST25', dienTich: '10ha', trangThai: 'thu_hoach',
    chungNhan: 'OCOP 4 Sao', anh: 'https://images.unsplash.com/photo-1536617621572-1d5f1e6269a0?q=80&w=1000&auto=format&fit=crop',
    toaDo: [[10.750, 106.640], [10.758, 106.660], [10.742, 106.660]],
    nhatKy: [
      { ngay: '07/12/2024', hoatDong: 'Thu hoạch', chiTiet: 'Bắt đầu gặt đợt 1, năng suất tốt' },
      { ngay: '20/09/2024', hoatDong: 'Gieo sạ', chiTiet: 'Sạ giống xác nhận cấp 1' }
    ]
  },
];

const danhSachHienThi = computed(() => {
  if (boLocHienTai.value === 'all') return danhSachGoc;
  return danhSachGoc.filter(v => v.trangThai === boLocHienTai.value);
});

// Helper functions
const getClassTrangThai = (tt) => {
  if (tt === 'canh_tac') return 'status-green';
  if (tt === 'sau_benh') return 'status-red';
  return 'status-yellow';
};
const getMapColor = (tt) => {
  if (tt === 'canh_tac') return '#4caf50';
  if (tt === 'sau_benh') return '#ef5350';
  return '#ffca28';
};
const getTextTrangThai = (tt) => {
  if (tt === 'canh_tac') return 'Đang canh tác';
  if (tt === 'sau_benh') return 'Cảnh báo dịch hại';
  return 'Đang thu hoạch';
};

// --- LOGIC TƯƠNG TÁC ---
const chonVung = (vung) => {
  // 1. Zoom tới map
  if (map.value && vung.toaDo) {
    const polygon = L.polygon(vung.toaDo);
    map.value.flyTo(polygon.getBounds().getCenter(), 16, { duration: 1.2 });
  }
  // 2. Chuyển Sidebar sang chế độ xem chi tiết
  vungDangXem.value = vung;
};

const quayLaiDanhSach = () => {
  vungDangXem.value = null;
  // Zoom out nhẹ ra ngoài để nhìn tổng quan
  map.value.flyTo([10.762, 106.660], 13, { duration: 1 });
};

const veLaiBanDo = () => {
  if (!map.value || !layerGroup.value) return;
  layerGroup.value.clearLayers();
  danhSachHienThi.value.forEach(vung => {
    if (vung.toaDo) {
      const mauSac = getMapColor(vung.trangThai);
      const poly = L.polygon(vung.toaDo, { color: mauSac, fillColor: mauSac, fillOpacity: 0.6, weight: 2 })
        .addTo(layerGroup.value);

      // Khi click vào hình trên bản đồ thì cũng mở chi tiết
      poly.on('click', () => chonVung(vung));
    }
  });
};

watch(danhSachHienThi, veLaiBanDo);

onMounted(() => {
  if (!mapContainer.value) return;
  map.value = L.map(mapContainer.value, { zoomControl: false }).setView([10.762, 106.660], 13);
  L.control.zoom({ position: 'bottomright' }).addTo(map.value);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19 }).addTo(map.value);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}').addTo(map.value);
  layerGroup.value = L.layerGroup().addTo(map.value);
  veLaiBanDo();
});



</script>

<template>
  <div class="webgis-container">
    <div ref="mapContainer" class="map-container"></div>

    <aside class="floating-sidebar">

      <div class="sidebar-header" :class="{ 'detail-mode': vungDangXem }">
        <div v-if="!vungDangXem" class="header-content">
          <h3><i class="fas fa-search-location"></i> Tra cứu Nông sản</h3>
          <span class="count-badge">{{ danhSachHienThi.length }} kết quả</span>
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

          <button class="btn-qr"><i class="fas fa-qrcode"></i> Quét mã Truy xuất nguồn gốc</button>
          <button 
        @click="goToTraceability('LUA-ST25-003')" 
        class="flex items-center justify-center w-full py-3 font-bold text-white transition transform bg-green-800 shadow-lg hover:bg-green-900 rounded-xl active:scale-95">
          
        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        Quét mã Truy xuất nguồn gốc
      </button>
        </div>
      </div>

    </aside>
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
</style>