<script setup>
import { onMounted } from 'vue';
import { useMapLogic } from '../composables/useMapLogic';

// Props nhận danh sách vùng và điểm sâu bệnh từ component cha
const props = defineProps({
  danhSachVung: {
    type: Array,
    required: true
  },
  diemNongSauBenh: {
    type: Array,
    required: true
  }
});

// Sử dụng composable bản đồ
const { mapContainer, cheDoXem, batCheDoSauBenh, batCheDoHanhChinh, initMap, vẽMarkerVùng } = useMapLogic();

// Khởi tạo bản đồ khi component mounted
onMounted(() => {
  initMap();
  vẽMarkerVùng(props.danhSachVung);
});

// Wrapper function để gọi batCheDoSauBenh với dữ liệu sâu bệnh
const handleBatCheDoSauBenh = () => batCheDoSauBenh(props.diemNongSauBenh);
</script>

<template>
  <!-- Container chứa bản đồ - flex 2 -->
  <div class="flex-[2] relative rounded-xl overflow-hidden shadow-md border border-white">
    <!-- Element DOM cho Leaflet map -->
    <div ref="mapContainer" class="w-full h-full z-0"></div>
    
    <!-- Controls chế độ xem - fixed position -->
    <div class="absolute top-5 right-5 z-50 bg-white p-2.5 rounded-lg shadow-lg flex flex-col gap-2 w-44">
      <h4 class="m-0 text-xs text-slate-600 uppercase font-semibold">
        <i class="fas fa-layer-group"></i> Lớp dữ liệu
      </h4>
      
      <!-- Nút chế độ hành chính -->
      <button 
        :class="{ 'map-control-btn-active': cheDoXem === 'hanh_chinh' }" 
        @click="batCheDoHanhChinh"
        class="map-control-btn"
      >
        <i class="fas fa-map"></i> Hành chính
      </button>
      
      <!-- Nút chế độ sâu bệnh -->
      <button 
        :class="{ 'map-control-btn-active': cheDoXem === 'sau_benh' }" 
        @click="handleBatCheDoSauBenh"
        class="map-control-btn"
      >
        <i class="fas fa-biohazard"></i> Mật độ Sâu bệnh
      </button>
      
      <!-- Nút chế độ dư lượng thuốc (placeholder) -->
      <button 
        :class="{ 'map-control-btn-active': cheDoXem === 'phan_bon' }"
        class="map-control-btn"
      >
        <i class="fas fa-flask"></i> Dư lượng Thuốc
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Container bản đồ - chiếm không gian flex 2 -->
.map-section {
  flex: 2;
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: 1px solid white;
}

/* Element chứa bản đồ Leaflet */
.map-view {
  width: 100%;
  height: 100%;
  z-index: 0;
}

/* Panel controls trên bản đồ - fixed position */
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

/* Tiêu đề controls */
.map-controls h4 {
  margin: 0 0 5px 0;
  font-size: 0.85rem;
  color: #64748b;
  text-transform: uppercase;
}

/* Nút chế độ */
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

/* Hover effect cho nút */
.map-controls button:hover {
  background: #e2e6ea;
}

/* Style cho nút active */
.map-controls button.active {
  background: #1b4332;
  color: white;
  border-color: #1b4332;
}
</style>
