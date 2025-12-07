<script setup>
import { onMounted, watch } from 'vue'; // Nhớ import thêm watch
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// 1. Nhận thêm prop vungCanZoom
const props = defineProps(['duLieuDauVao', 'vungCanZoom']);

let map; // Khai báo biến map ra ngoài để dùng được ở mọi nơi

onMounted(() => {
  map = L.map('map-container').setView([10.762, 106.660], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Vẽ dữ liệu (Giữ nguyên code vẽ cũ của bạn ở đây)
  if (props.duLieuDauVao) {
    props.duLieuDauVao.forEach(vung => {
      if (vung.toaDo && vung.toaDo.length > 0) {
        L.polygon(vung.toaDo, { color: 'red', fillColor: '#f03', fillOpacity: 0.4 })
         .addTo(map)
         .bindPopup(`<b>${vung.ten}</b>`);
      }
    });
  }
});

// 2. THEO DÕI (WATCH): Khi cha bảo zoom vùng nào thì bay tới đó
watch(() => props.vungCanZoom, (newVung) => {
  if (newVung && newVung.toaDo && map) {
    
    // Tạo một hình tạm thời để tính toán tâm của vùng đất
    const polygon = L.polygon(newVung.toaDo);
    const center = polygon.getBounds().getCenter(); // Lấy tâm

    // Hiệu ứng bay (Fly) mượt mà tới tâm đó
    map.flyTo(center, 16, { // 16 là độ zoom cận cảnh
      duration: 2 // Bay trong 2 giây
    });

    // Hiện popup ngay lập tức (Optional)
    L.popup()
      .setLatLng(center)
      .setContent(`Đang xem: <b>${newVung.ten}</b>`)
      .openOn(map);
  }
});
</script>

<template>
      <div id="map-container"></div>
</template>


<style scoped>
#map-container {
      width: 100%;
      height: 100%;
      /* Lúc này 100% mới có tác dụng vì cha nó đã có chiều cao */
      z-index: 1;
}
</style>