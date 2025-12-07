<script setup>
import { onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Nhận dữ liệu từ App.vue
const props = defineProps(['duLieuDauVao']);

onMounted(() => {
  // Tạo bản đồ
  const map = L.map('map-container').setView([10.762, 106.660], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Vẽ dữ liệu được nhận
  if (props.duLieuDauVao) {
    props.duLieuDauVao.forEach(vung => {
      if (vung.toaDo && vung.toaDo.length > 0) {
        
        // Vẽ Polygon
        const polygon = L.polygon(vung.toaDo, {
          color: 'red',
          fillColor: '#f03',
          fillOpacity: 0.4
        }).addTo(map);

        // Hiện popup tên
        polygon.bindPopup(`<b>${vung.ten}</b>`);
      }
    });
  }
});
</script>

<template>
  <div id="map-container"></div>
</template>

<style scoped>
#map-container {
  width: 100%;
  height: 100%; /* Ăn theo chiều cao của cha (map-wrapper) */
  z-index: 1;
}
</style>