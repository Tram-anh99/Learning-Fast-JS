<script setup>
import { onMounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps(['duLieuDauVao', 'vungCanZoom']);
let map;

onMounted(() => {
      // Tạo bản đồ
      map = L.map('map-container').setView([10.762, 106.660], 12);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

      // Vẽ dữ liệu ban đầu
      if (props.duLieuDauVao) {
            props.duLieuDauVao.forEach(vung => {
                  if (vung.toaDo && vung.toaDo.length > 0) {
                        L.polygon(vung.toaDo, { color: 'red', fillColor: '#f03', fillOpacity: 0.5 })
                              .addTo(map)
                              .bindPopup(`<b>${vung.ten}</b>`);
                  }
            });
      }
});

// Watch để zoom
watch(() => props.vungCanZoom, (newVung) => {
      if (newVung && newVung.toaDo && map) {
            const polygon = L.polygon(newVung.toaDo);
            map.flyTo(polygon.getBounds().getCenter(), 15, { duration: 1.5 });

            L.popup()
                  .setLatLng(polygon.getBounds().getCenter())
                  .setContent(`Đang chọn: <b>${newVung.ten}</b>`)
                  .openOn(map);
      }
});
</script>

<template>
      <div id="map-container"></div>
</template>

<style scoped>
/* Bắt buộc bản đồ phải có chiều cao */
#map-container {
      width: 100%;
      height: 100vh !important;
      /* Dùng !important để ép nó hiện ra bằng mọi giá */
      z-index: 1;
}
</style>