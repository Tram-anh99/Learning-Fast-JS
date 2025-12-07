<script setup>
import { onMounted, ref, shallowRef, computed, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const map = shallowRef(null);
const mapContainer = ref(null);
const layerGroup = shallowRef(null); // Nhóm chứa các lớp vẽ (để dễ xóa đi vẽ lại)
const boLocHienTai = ref('all'); // Trạng thái lọc: 'all', 'sau_benh', 'thu_hoach'

// Dữ liệu mẫu
const danhSachGoc = [
  { id: 1, ma: 'VT-001', ten: 'Xoài Cát Hòa Lộc', dienTich: '5ha', trangThai: 'canh_tac', toaDo: [[10.762, 106.660], [10.770, 106.670], [10.760, 106.670]] },
  { id: 2, ma: 'VT-002', ten: 'Thanh Long Ruột Đỏ', dienTich: '3.2ha', trangThai: 'sau_benh', toaDo: [[10.780, 106.680], [10.790, 106.690], [10.780, 106.690]] },
  { id: 3, ma: 'VT-003', ten: 'Lúa ST25', dienTich: '10ha', trangThai: 'thu_hoach', toaDo: [[10.750, 106.640], [10.758, 106.660], [10.742, 106.660]]},
];

// 1. TÍNH TOÁN DANH SÁCH HIỂN THỊ DỰA VÀO BỘ LỌC
const danhSachHienThi = computed(() => {
  if (boLocHienTai.value === 'all') return danhSachGoc;
  return danhSachGoc.filter(v => v.trangThai === boLocHienTai.value);
});

// Các hàm tiện ích màu sắc
const getClassTrangThai = (tt) => {
  if (tt === 'canh_tac') return 'status-green';
  if (tt === 'sau_benh') return 'status-red';
  return 'status-yellow';
};
const getMapColor = (tt) => {
  if (tt === 'canh_tac') return '#4caf50'; // Xanh lá
  if (tt === 'sau_benh') return '#ef5350'; // Đỏ
  return '#ffca28'; // Vàng
};
const getTextTrangThai = (tt) => {
  if (tt === 'canh_tac') return 'Đang canh tác';
  if (tt === 'sau_benh') return 'Cảnh báo sâu bệnh';
  return 'Đang thu hoạch';
};

// Hàm Zoom
const zoomToVung = (vung) => {
  if (map.value && vung.toaDo) {
    const polygon = L.polygon(vung.toaDo);
    map.value.flyTo(polygon.getBounds().getCenter(), 15, { duration: 1.5 });
    L.popup()
      .setLatLng(polygon.getBounds().getCenter())
      .setContent(`<b>${vung.ten}</b><br>${getTextTrangThai(vung.trangThai)}`)
      .openOn(map.value);
  }
};

// HÀM VẼ LẠI BẢN ĐỒ (Quan trọng cho chức năng Lọc)
const veLaiBanDo = () => {
  if (!map.value || !layerGroup.value) return;

  // 1. Xóa hết các hình cũ
  layerGroup.value.clearLayers();

  // 2. Vẽ các hình mới dựa theo danh sách đã lọc
  danhSachHienThi.value.forEach(vung => {
    if (vung.toaDo) {
      const mauSac = getMapColor(vung.trangThai);
      L.polygon(vung.toaDo, {
        color: mauSac,
        fillColor: mauSac,
        fillOpacity: 0.6,
        weight: 2
      })
        .bindPopup(`<b>${vung.ten}</b><br>Trạng thái: ${getTextTrangThai(vung.trangThai)}`)
        .addTo(layerGroup.value); // Thêm vào nhóm quản lý
    }
  });
};

// Theo dõi sự thay đổi của danh sách hiển thị để vẽ lại map
watch(danhSachHienThi, () => {
  veLaiBanDo();
});

onMounted(() => {
  if (!mapContainer.value) return;

  map.value = L.map(mapContainer.value, { zoomControl: false }).setView([10.762, 106.660], 13);
  L.control.zoom({ position: 'bottomright' }).addTo(map.value);

  // Lớp vệ tinh
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { attribution: 'Esri', maxZoom: 19 }).addTo(map.value);
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}').addTo(map.value);

  // Tạo nhóm lớp để quản lý các Polygon
  layerGroup.value = L.layerGroup().addTo(map.value);

  // Vẽ lần đầu
  veLaiBanDo();

  // THÊM CHÚ GIẢI (LEGEND) Ở GÓC DƯỚI TRÁI
  const legend = L.control({ position: 'bottomleft' });
  legend.onAdd = () => {
    const div = L.DomUtil.create('div', 'info legend');
    div.innerHTML = `
      <div style="background:white; padding:10px; border-radius:8px; box-shadow:0 0 10px rgba(0,0,0,0.2);">
        <h4 style="margin:0 0 5px 0; font-size:12px; text-transform:uppercase;">Chú giải</h4>
        <div style="display:flex; align-items:center; margin-bottom:4px;"><span style="background:#4caf50; width:12px; height:12px; display:inline-block; margin-right:5px;"></span> Đang canh tác</div>
        <div style="display:flex; align-items:center; margin-bottom:4px;"><span style="background:#ef5350; width:12px; height:12px; display:inline-block; margin-right:5px;"></span> Sâu bệnh</div>
        <div style="display:flex; align-items:center;"><span style="background:#ffca28; width:12px; height:12px; display:inline-block; margin-right:5px;"></span> Thu hoạch</div>
      </div>
    `;
    return div;
  };
  legend.addTo(map.value);
});
</script>

<template>
  <div class="webgis-container">
    <div ref="mapContainer" class="map-container"></div>

    <aside class="floating-sidebar">
      <div class="sidebar-header">
        <h3><i class="fas fa-list"></i> Danh sách Vùng trồng</h3>
        <span class="count-badge">{{ danhSachHienThi.length }} vùng</span>
      </div>

      <div class="sidebar-tabs">
        <button class="tab-btn" :class="{ active: boLocHienTai === 'all' }" @click="boLocHienTai = 'all'">Tất
          cả</button>
        <button class="tab-btn" :class="{ active: boLocHienTai === 'sau_benh' }" @click="boLocHienTai = 'sau_benh'">Cảnh
          báo</button>
        <button class="tab-btn" :class="{ active: boLocHienTai === 'thu_hoach' }"
          @click="boLocHienTai = 'thu_hoach'">Thu hoạch</button>
      </div>

      <div class="sidebar-content">
        <ul class="layer-list">
          <li v-for="vung in danhSachHienThi" :key="vung.id" class="layer-item" @click="zoomToVung(vung)">
            <div class="item-icon"><i class="fas fa-map-marker-alt"></i></div>
            <div class="item-info">
              <span class="item-name">{{ vung.ten }}</span>
              <span class="item-sub">{{ vung.ma }} - {{ vung.dienTich }}</span>
            </div>
            <div class="item-status" :class="getClassTrangThai(vung.trangThai)">
              {{ getTextTrangThai(vung.trangThai) }}
            </div>
          </li>
          <li v-if="danhSachHienThi.length === 0" style="padding:20px; text-align:center; color:#666;">
            Không tìm thấy vùng nào.
          </li>
        </ul>
      </div>
    </aside>

    <div class="map-toolbar">
      <button class="tool-btn" title="Tìm kiếm"><i class="fas fa-search"></i></button>
      <div class="divider"></div>
      <button class="tool-btn"><i class="fas fa-layer-group"></i></button>
      <button class="tool-btn"><i class="fas fa-ruler-combined"></i></button>
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

.floating-sidebar {
  position: absolute;
  top: 10px;
  left: 10px;
  bottom: 10px;
  /* Cập nhật vị trí sát lề */
  width: 340px;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  border: 1px solid rgba(255, 255, 255, 0.4);
}

.sidebar-header {
  padding: 16px 20px;
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
  background: rgba(255, 255, 255, 0.3);
}

.tab-btn {
  flex: 1;
  padding: 10px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: #333;
  border-bottom: 3px solid transparent;
}

.tab-btn.active {
  color: #1b4332;
  border-bottom-color: #1b4332;
  font-weight: bold;
  background: rgba(255, 255, 255, 0.6);
}

.sidebar-content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px;
}

.layer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.layer-item {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.layer-item:hover {
  transform: translateY(-2px);
  background: white;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.item-icon {
  width: 32px;
  height: 32px;
  background: #e8f5e9;
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
  font-size: 0.9rem;
  color: #111;
}

.item-sub {
  font-size: 0.75rem;
  color: #555;
}

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