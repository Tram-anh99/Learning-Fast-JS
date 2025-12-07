<script setup>
import { onMounted, ref, shallowRef } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const map = shallowRef(null);
const mapContainer = ref(null);

// Dữ liệu giả lập cho luận văn (Sau này lấy từ DB)
const danhSachVung = ref([
  { id: 1, ma: 'VT-001', ten: 'Xoài Cát Hòa Lộc', dienTich: '5ha', trangThai: 'canh_tac', toaDo: [10.762, 106.660] },
  { id: 2, ma: 'VT-002', ten: 'Thanh Long Ruột Đỏ', dienTich: '3.2ha', trangThai: 'sau_benh', toaDo: [10.770, 106.670] },
  { id: 3, ma: 'VT-003', ten: 'Lúa ST25', dienTich: '10ha', trangThai: 'thu_hoach', toaDo: [10.750, 106.650] },
]);

// Hàm lấy màu badge trạng thái
const getClassTrangThai = (tt) => {
  if (tt === 'canh_tac') return 'status-green';
  if (tt === 'sau_benh') return 'status-red';
  return 'status-yellow';
}

const getTextTrangThai = (tt) => {
  if (tt === 'canh_tac') return 'Đang canh tác';
  if (tt === 'sau_benh') return 'Cảnh báo sâu bệnh';˙
  return 'Đang thu hoạch';
}

onMounted(() => {
  if (!mapContainer.value) return;

  // 1. Tạo bản đồ
  map.value = L.map(mapContainer.value, { zoomControl: false }).setView([10.762, 106.660], 13);

  // 2. Lớp nền Vệ tinh (ESRI World Imagery) - Nhìn rất chuyên nghiệp cho WebGIS nông nghiệp
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri',
    maxZoom: 19
  }).addTo(map.value);

  // 3. Lớp tên đường (đè lên vệ tinh để dễ nhìn)
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}').addTo(map.value);
});
</script>

<template>
  <div class="webgis-container">
    <div ref="mapContainer" class="map-container"></div>

    <aside class="floating-sidebar">
      <div class="sidebar-header">
        <h3><i class="fas fa-list"></i> Danh sách Vùng trồng</h3>
        <span class="count-badge">{{ danhSachVung.length }} vùng</span>
      </div>

      <div class="sidebar-tabs">
        <button class="tab-btn active">Tất cả</button>
        <button class="tab-btn">Cảnh báo</button>
        <button class="tab-btn">Thu hoạch</button>
      </div>

      <div class="sidebar-content">
        <ul class="layer-list">
          <li v-for="vung in danhSachVung" :key="vung.id" class="layer-item">
            <div class="item-icon">
              <i class="fas fa-map-marker-alt"></i>
            </div>
            <div class="item-info">
              <span class="item-name">{{ vung.ten }}</span>
              <span class="item-sub">{{ vung.ma }} - {{ vung.dienTich }}</span>
            </div>
            <div class="item-status" :class="getClassTrangThai(vung.trangThai)">
              {{ getTextTrangThai(vung.trangThai) }}
            </div>
          </li>
        </ul>
      </div>
    </aside>

    <div class="map-toolbar">
      <button class="tool-btn" title="Tìm kiếm địa điểm"><i class="fas fa-search"></i></button>
      <div class="divider"></div>
      <button class="tool-btn" title="Lớp bản đồ (Vệ tinh/Giao thông)"><i class="fas fa-layer-group"></i></button>
      <button class="tool-btn" title="Đo diện tích"><i class="fas fa-ruler-combined"></i></button>
      <button class="tool-btn" title="In bản đồ"><i class="fas fa-print"></i></button>
      <div class="divider"></div>
      <button class="tool-btn zoom-btn" title="Phóng to"><i class="fas fa-plus"></i></button>
      <button class="tool-btn zoom-btn" title="Thu nhỏ"><i class="fas fa-minus"></i></button>
    </div>
  </div>
</template>

<style scoped>
.webgis-container {
  position: relative;
  height: 100%;
  width: 100%;
}

.map-container {
  height: 100%;
  width: 100%;
  z-index: 0;
}

/* SIDEBAR TRONG SUỐT (GLASSMORPHISM) */
.floating-sidebar {
  position: absolute;
  top: 20px;
  left: 20px;
  bottom: 20px;
  /* Cách đều trên dưới trái */
  width: 340px;

  /* Hiệu ứng kính */
  background: rgba(255, 255, 255, 0.85);
  /* Trắng đục 85% để dễ đọc chữ */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);

  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  border: 1px solid rgba(255, 255, 255, 0.6);
}

.sidebar-header {
  padding: 16px 20px;
  background-color: var(--primary-color);
  /* Dùng màu xanh của App.vue */
  background: linear-gradient(to right, #1b4332, #2d6a4f);
  color: white;
  border-radius: 12px 12px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.count-badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
}

.sidebar-tabs {
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.5);
}

.tab-btn {
  flex: 1;
  padding: 10px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: #555;
  border-bottom: 3px solid transparent;
}

.tab-btn.active {
  color: #1b4332;
  border-bottom-color: #1b4332;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.8);
}

.sidebar-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
}

/* DANH SÁCH ITEM */
.layer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.layer-item {
  background: white;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  border: 1px solid transparent;
  transition: all 0.2s;
}

.layer-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  border-color: #4caf50;
}

.item-icon {
  width: 32px;
  height: 32px;
  background: #f1f8e9;
  color: #2e7d32;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-info {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.item-name {
  font-weight: 600;
  font-size: 0.95rem;
  color: #333;
}

.item-sub {
  font-size: 0.8rem;
  color: #666;
}

/* Badge trạng thái nhỏ */
.item-status {
  font-size: 0.7rem;
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

/* TOOLBAR PHẢI */
.map-toolbar {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 1000;
}

.tool-btn {
  width: 40px;
  height: 40px;
  background: white;
  border: none;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  color: #444;
  font-size: 1rem;
  transition: all 0.2s;
}

.tool-btn:hover {
  background: #1b4332;
  color: white;
}

.divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.1);
  margin: 2px 0;
}
</style>