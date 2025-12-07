<script setup>
import { onMounted, ref, shallowRef } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Sử dụng shallowRef cho đối tượng bản đồ Leaflet để tối ưu hiệu suất
const map = shallowRef(null);
const mapContainer = ref(null);

onMounted(() => {
  if (!mapContainer.value) return;

  // Khởi tạo bản đồ
  map.value = L.map(mapContainer.value, {
    zoomControl: false, // Tắt zoom control mặc định
    attributionControl: false // Tắt attribution control mặc định
  }).setView([10.762622, 106.660172], 13); // Tọa độ ví dụ TP.HCM

  // Thêm lớp bản đồ nền vệ tinh (Sử dụng Esri World Imagery)
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
    maxZoom: 19
  }).addTo(map.value);

  // Thêm một lớp nhãn địa danh mờ lên trên (tùy chọn, để dễ nhìn hơn)
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
      pane: 'shadowPane', // Đặt ở pane thấp hơn để không che phủ các lớp dữ liệu
      opacity: 0.6
  }).addTo(map.value);
});

// Dữ liệu mẫu cho danh sách lớp
const layerItems = ref([
  { name: 'Bievants', icon: 'fa-layer-group' },
  { name: 'Scattnrs', icon: 'fa-vector-square' },
  { name: 'Monitor Updates', icon: 'fa-chart-line' },
]);

// Các hàm điều khiển bản đồ
const zoomIn = () => map.value && map.value.zoomIn();
const zoomOut = () => map.value && map.value.zoomOut();
</script>

<template>
  <div class="webgis-container">
    <div ref="mapContainer" class="map-container"></div>

    <aside class="floating-sidebar">
      <div class="sidebar-header">
        <h3>Map trras</h3>
        <button class="close-btn"><i class="fas fa-times"></i></button>
      </div>
      <div class="sidebar-tabs">
        <button class="tab-btn active">Map</button>
        <button class="tab-btn">Data btld</button>
        <button class="tab-btn">Ehw Stose</button>
      </div>
      <div class="sidebar-content">
        <ul class="layer-list">
          <li v-for="(item, index) in layerItems" :key="index" class="layer-item">
            <span class="layer-icon"><i :class="'fas ' + item.icon"></i></span>
            <span class="layer-name">{{ item.name }}</span>
            <span class="layer-arrow"><i class="fas fa-chevron-right"></i></span>
          </li>
        </ul>
      </div>
    </aside>

    <div class="map-toolbar">
      <button class="tool-btn" title="Tìm kiếm"><i class="fas fa-search"></i></button>
      <div class="tool-group">
        <button class="tool-btn" title="Phóng to" @click="zoomIn"><i class="fas fa-plus"></i></button>
        <button class="tool-btn" title="Thu nhỏ" @click="zoomOut"><i class="fas fa-minus"></i></button>
      </div>
      <button class="tool-btn" title="Đo đạc"><i class="fas fa-ruler-combined"></i></button>
      <button class="tool-btn" title="Lớp bản đồ"><i class="fas fa-layer-group"></i></button>
      <button class="tool-btn" title="Cài đặt"><i class="fas fa-cog"></i></button>
    </div>
  </div>
</template>

<style scoped>
/* Container chính */
.webgis-container {
  position: relative;
  height: 100%;
  width: 100%;
}

/* Bản đồ */
.map-container {
  height: 100%;
  width: 100%;
  z-index: 0;
}

/* Thanh bên nổi */
.floating-sidebar {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 300px;
  max-height: calc(100% - 40px); /* Đảm bảo không tràn màn hình */
  background-color: var(--sidebar-bg);
  backdrop-filter: blur(12px); /* Hiệu ứng kính mờ mạnh hơn */
  -webkit-backdrop-filter: blur(12px); /* Hỗ trợ Safari */
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.3); /* Viền mờ nhẹ */
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background-color: var(--primary-color);
  color: var(--light-text-color);
}

.sidebar-header h3 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 500;
}

.close-btn {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
  transition: color 0.2s;
  display: flex;
  align-items: center;
}

.close-btn:hover {
  color: var(--light-text-color);
}

.sidebar-tabs {
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.5);
}

.tab-btn {
  flex: 1;
  padding: 12px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: 500;
  color: var(--text-color);
  transition: all 0.2s;
  font-size: 0.95rem;
}

.tab-btn.active {
  border-bottom-color: var(--primary-color);
  color: var(--primary-color);
  background-color: rgba(255, 255, 255, 0.8);
}

.sidebar-content {
  flex-grow: 1;
  overflow-y: auto; /* Cho phép cuộn nội dung danh sách */
}

.layer-list {
  list-style: none;
  padding: 10px 0;
  margin: 0;
}

.layer-item {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: background-color 0.2s;
  color: var(--text-color);
}

.layer-item:hover {
  background-color: rgba(var(--primary-color-rgb), 0.08); /* Cần định nghĩa biến RGB nếu muốn dùng */
  background-color: rgba(0, 0, 0, 0.04);
}

.layer-icon {
  margin-right: 16px;
  color: #666;
  font-size: 1.1rem;
  width: 24px;
  text-align: center;
}

.layer-name {
  flex-grow: 1;
  font-weight: 500;
  font-size: 1rem;
}

.layer-arrow {
  color: #999;
  font-size: 0.9rem;
}

/* Thanh công cụ bản đồ */
.map-toolbar {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
}

.tool-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.tool-group .tool-btn {
  border-radius: 0;
  box-shadow: none;
  border: none;
}

.tool-group .tool-btn:not(:last-child) {
  border-bottom: 1px solid #f0f0f0;
}

.tool-btn {
  width: 44px;
  height: 44px;
  background-color: #fff;
  border: none;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
  color: #555;
  font-size: 1.2rem;
}

.tool-btn:hover {
  background-color: #f5f5f5;
  color: var(--primary-color);
  box-shadow: var(--shadow-md);
}
</style>