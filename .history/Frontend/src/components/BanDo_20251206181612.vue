<script setup>
import { onMounted, watch } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const props = defineProps(['duLieuDauVao', 'vungCanZoom']);
let map;

// --- HÀM MỚI: Chọn màu dựa theo trạng thái ---
const layMauTheoTrangThai = (trangThai) => {
  if (trangThai === 'canh_tac') return '#42b883'; // Xanh lá (Vue)
  if (trangThai === 'thu_hoach') return '#f1c40f'; // Vàng
  if (trangThai === 'sau_benh') return '#e74c3c';  // Đỏ
  return '#3498db'; // Mặc định là Xanh dương
};

onMounted(() => {
  map = L.map('map-container').setView([10.762, 106.660], 12);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  if (props.duLieuDauVao) {
    props.duLieuDauVao.forEach(vung => {
      if (vung.toaDo && vung.toaDo.length > 0) {
        
        // Gọi hàm lấy màu ở đây
        const mauSac = layMauTheoTrangThai(vung.trangThai);

        L.polygon(vung.toaDo, { 
          color: mauSac,       // Viền theo màu trạng thái
          fillColor: mauSac,   // Nền theo màu trạng thái
          fillOpacity: 0.5 
        })
        .addTo(map)
        .bindPopup(`
          <b>${vung.ten}</b><br>
          Mã số: ${vung.maSo}<br>
          Trạng thái: ${vung.trangThai}
        `);
      }
    });
  }
});

// Giữ nguyên phần watch (zoom) như cũ
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