<script setup>
import { onMounted } from 'vue';
import { useMapLogic } from '../composables/useMapLogic';

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

const { mapContainer, cheDoXem, batCheDoSauBenh, batCheDoHanhChinh, initMap, vẽMarkerVùng } = useMapLogic();

onMounted(() => {
  initMap();
  vẽMarkerVùng(props.danhSachVung);
});

const handleBatCheDoSauBenh = () => batCheDoSauBenh(props.diemNongSauBenh);
</script>

<template>
  <div class="map-section">
    <div ref="mapContainer" class="map-view"></div>
    <div class="map-controls">
      <h4><i class="fas fa-layer-group"></i> Lớp dữ liệu</h4>
      <button :class="{ active: cheDoXem === 'hanh_chinh' }" @click="batCheDoHanhChinh">
        <i class="fas fa-map"></i> Hành chính
      </button>
      <button :class="{ active: cheDoXem === 'sau_benh' }" @click="handleBatCheDoSauBenh">
        <i class="fas fa-biohazard"></i> Mật độ Sâu bệnh
      </button>
      <button :class="{ active: cheDoXem === 'phan_bon' }">
        <i class="fas fa-flask"></i> Dư lượng Thuốc
      </button>
    </div>
  </div>
</template>

<style scoped>
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
</style>
