<script setup>
import { onMounted, ref, shallowRef } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
// 1. Import component biểu đồ
import StatsCharts from '../components/StatsCharts.vue' // (Sửa đường dẫn nếu cần)
// 1. Import Widget mới tạo
import MapStatsWidget from '../components/MapStatsWidget.vue'
// ...
const map = shallowRef(null);
const mapContainer = ref(null);
const lopSauBenh = shallowRef(L.layerGroup()); // Lớp chứa các điểm nhiệt sâu bệnh

// --- DỮ LIỆU THỐNG KÊ (MOCK DATA) ---
const thongKe = ref({
      tongVung: 124,
      dienTich: '450 ha',
      sanLuongDuKien: '1.200 tấn',
      canhBao: 5
});

// --- DỮ LIỆU VÙNG TRỒNG QUẢN LÝ ---
const danhSachVung = ref([
      { id: 1, ma: 'VT-001', ten: 'HTX Xoài Mỹ Xương', chu: 'Nguyễn Văn A', trangThai: 'active', toaDo: [10.762, 106.660] },
      { id: 2, ma: 'VT-002', ten: 'Thanh Long VietGAP', chu: 'Trần Thị B', trangThai: 'warning', toaDo: [10.770, 106.670] },
      { id: 3, ma: 'VT-003', ten: 'Lúa Chất lượng cao', chu: 'HTX Lúa Vàng', trangThai: 'revoked', toaDo: [10.750, 106.650] },
      { id: 4, ma: 'VT-004', ten: 'Sầu Riêng Ri6', chu: 'Lê Văn C', trangThai: 'active', toaDo: [10.780, 106.640] },
]);

// --- DỮ LIỆU PHÂN TÍCH (Giả lập các điểm bùng phát dịch hại) ---
const diemNongSauBenh = [
      [10.770, 106.670], [10.771, 106.671], [10.769, 106.669], // Tập trung ở vùng 2
      [10.750, 106.650] // Vùng 3 lẻ tẻ
];

const cheDoXem = ref('hanh_chinh'); // 'hanh_chinh' | 'sau_benh' | 'phan_bon'

// Hàm vẽ bản đồ nhiệt
const batCheDoSauBenh = () => {
      cheDoXem.value = 'sau_benh';
      lopSauBenh.value.clearLayers();

      diemNongSauBenh.forEach(coord => {
            L.circle(coord, {
                  color: 'red', fillColor: '#f03', fillOpacity: 0.4, radius: 300
            }).addTo(lopSauBenh.value);
      });
};

const batCheDoHanhChinh = () => {
      cheDoXem.value = 'hanh_chinh';
      lopSauBenh.value.clearLayers();
};

const getStatusBadge = (status) => {
      if (status === 'active') return { text: 'Đang hoạt động', class: 'badge-active' };
      if (status === 'warning') return { text: 'Cảnh báo', class: 'badge-warning' };
      return { text: 'Đã thu hồi', class: 'badge-danger' };
};

onMounted(() => {
      if (!mapContainer.value) return;

      // Khởi tạo Map
      map.value = L.map(mapContainer.value, { zoomControl: false }).setView([10.765, 106.660], 13);
      L.control.zoom({ position: 'bottomright' }).addTo(map.value);

      // Nền bản đồ sáng (CartoDB Positron)
      L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '© CartoDB'
      }).addTo(map.value);

      lopSauBenh.value.addTo(map.value);

      // Vẽ Marker vùng trồng
      danhSachVung.value.forEach(vung => {
            let color = vung.trangThai === 'active' ? '#1b4332' : (vung.trangThai === 'warning' ? '#f59e0b' : '#ef4444');
            L.circleMarker(vung.toaDo, {
                  radius: 8, fillColor: color, color: '#fff', weight: 2, fillOpacity: 1
            }).bindPopup(`<b>${vung.ten}</b><br>Chủ hộ: ${vung.chu}`).addTo(map.value);
      });
});
</script>

<template>
      <div class="admin-container">

            <div class="stats-bar">
                  <div class="stat-card">
                        <div class="icon-box green"><i class="fas fa-layer-group"></i></div>
                        <div class="stat-info">
                              <h3>{{ thongKe.tongVung }}</h3>
                              <p>Mã số vùng trồng</p>
                        </div>
                  </div>
                  <div class="stat-card">
                        <div class="icon-box blue"><i class="fas fa-ruler-combined"></i></div>
                        <div class="stat-info">
                              <h3>{{ thongKe.dienTich }}</h3>
                              <p>Tổng diện tích</p>
                        </div>
                  </div>
                  <div class="stat-card">
                        <div class="icon-box yellow"><i class="fas fa-exclamation-triangle"></i></div>
                        <div class="stat-info">
                              <h3>{{ thongKe.canhBao }}</h3>
                              <p>Cảnh báo vi phạm</p>
                        </div>
                  </div>
            </div>

            <div class="map-section">
                  <div ref="mapContainer" class="map-view"></div>
                  <div class="map-controls">
                        <h4><i class="fas fa-layer-group"></i> Lớp dữ liệu</h4>
                        <button :class="{ active: cheDoXem === 'hanh_chinh' }" @click="batCheDoHanhChinh">
                              <i class="fas fa-map"></i> Hành chính
                        </button>
                        <button :class="{ active: cheDoXem === 'sau_benh' }" @click="batCheDoSauBenh">
                              <i class="fas fa-biohazard"></i> Mật độ Sâu bệnh
                        </button>
                        <button :class="{ active: cheDoXem === 'phan_bon' }">
                              <i class="fas fa-flask"></i> Dư lượng Thuốc
                        </button>
                  </div>
            </div>

            <div class="admin-panel">
                  <div class="panel-header">
                        <h3>Danh sách Vùng trồng & Giám sát</h3>
                        <button class="btn-export"><i class="fas fa-file-export"></i> Xuất báo cáo</button>
                  </div>
                  <div class="table-container">
                        <table>
                              <thead>
                                    <tr>
                                          <th>Mã số</th>
                                          <th>Tên vùng</th>
                                          <th>Chủ hộ</th>
                                          <th>Trạng thái</th>
                                          <th>Thao tác</th>
                                    </tr>
                              </thead>
                              <tbody>
                                    <tr v-for="vung in danhSachVung" :key="vung.id">
                                          <td><strong>{{ vung.ma }}</strong></td>
                                          <td>{{ vung.ten }}</td>
                                          <td>{{ vung.chu }}</td>
                                          <td><span :class="['status-badge', getStatusBadge(vung.trangThai).class]">{{
                                                getStatusBadge(vung.trangThai).text }}</span></td>
                                          <td>
                                                <button class="btn-action edit"><i class="fas fa-edit"></i></button>
                                                <button class="btn-action warn"><i class="fas fa-bell"></i></button>
                                          </td>
                                    </tr>
                              </tbody>
                        </table>
                  </div>
            </div>

            <div class="flex w-full h-screen">
    
      <div class="w-80...">...</div>

      <div class="relative flex-1 w-full h-full"> 
            
            <div id="map" class="z-0 w-full h-full">
            </div>

            <MapStatsWidget />

      </div>

  </div>
      </div>

</template>

<style scoped>
.admin-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #f1f5f9;
      display: flex;
      flex-direction: column;
      padding: 20px;
      box-sizing: border-box;
      gap: 20px;
}

.stats-bar {
      display: flex;
      gap: 20px;
}

.stat-card {
      flex: 1;
      background: white;
      padding: 15px 20px;
      border-radius: 12px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
      display: flex;
      align-items: center;
      gap: 15px;
}

.icon-box {
      width: 50px;
      height: 50px;
      border-radius: 10px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 1.5rem;
      color: white;
}

.icon-box.green {
      background: #10b981;
}

.icon-box.blue {
      background: #3b82f6;
}

.icon-box.yellow {
      background: #f59e0b;
}

.stat-info h3 {
      margin: 0;
      font-size: 1.5rem;
      color: #1e293b;
}

.stat-info p {
      margin: 0;
      color: #64748b;
      font-size: 0.9rem;
}

.map-section {
      flex: 2;
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      border: 1px solid white;
}

.map-view {
      width: 100%;
      height: 100%;
      z-index: 0;
}

.map-controls {
      position: absolute;
      top: 20px;
      right: 20px;
      z-index: 1000;
      background: white;
      padding: 10px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 180px;
}

.map-controls h4 {
      margin: 0 0 5px 0;
      font-size: 0.85rem;
      color: #64748b;
      text-transform: uppercase;
}

.map-controls button {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 8px;
      border-radius: 6px;
      text-align: left;
      cursor: pointer;
      font-size: 0.9rem;
      color: #333;
      transition: all 0.2s;
}

.map-controls button:hover {
      background: #e2e6ea;
}

.map-controls button.active {
      background: #1b4332;
      color: white;
      border-color: #1b4332;
}

.admin-panel {
      flex: 1.5;
      background: white;
      border-radius: 12px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
      display: flex;
      flex-direction: column;
      overflow: hidden;
}

.panel-header {
      padding: 15px 20px;
      border-bottom: 1px solid #e2e8f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
}

.panel-header h3 {
      margin: 0;
      font-size: 1.1rem;
      color: #1e293b;
}

.btn-export {
      background: #1b4332;
      color: white;
      border: none;
      padding: 8px 15px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
}

.table-container {
      overflow-y: auto;
      flex-grow: 1;
}

table {
      width: 100%;
      border-collapse: collapse;
}

th {
      text-align: left;
      padding: 12px 20px;
      background: #f8fafc;
      color: #64748b;
      font-weight: 600;
      font-size: 0.85rem;
      position: sticky;
      top: 0;
}

td {
      padding: 12px 20px;
      border-bottom: 1px solid #f1f5f9;
      color: #333;
      font-size: 0.9rem;
}

tr:hover {
      background: #f8fafc;
}

.status-badge {
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 600;
}

.badge-active {
      background: #d1fae5;
      color: #065f46;
}

.badge-warning {
      background: #fef3c7;
      color: #92400e;
}

.badge-danger {
      background: #fee2e2;
      color: #991b1b;
}

.btn-action {
      width: 30px;
      height: 30px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-right: 5px;
}

.btn-action.edit {
      background: #e0f2fe;
      color: #0284c7;
}

.btn-action.warn {
      background: #ffedd5;
      color: #ea580c;
}
</style>