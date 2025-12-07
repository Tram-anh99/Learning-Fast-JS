<script setup>
import { onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

onMounted(() => {
      // 1. Khởi tạo bản đồ
      const map = L.map('map-container').setView([10.762, 106.660], 13);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

      // --- PHẦN MỚI: VẼ VÙNG TRỒNG (POLYGON) ---

      // Giả lập tọa độ 1 vùng trồng (3 điểm tạo thành hình tam giác)
      const toaDoVungTrong = [
            [10.762, 106.660],
            [10.770, 106.670],
            [10.760, 106.670]
      ];

      // Vẽ vùng trồng lên bản đồ
      const vungTrong = L.polygon(toaDoVungTrong, {
            color: 'red',       // Màu viền
            fillColor: '#f03',  // Màu nền bên trong
            fillOpacity: 0.5    // Độ trong suốt
      }).addTo(map);

      // Thêm popup khi click vào vùng
      vungTrong.bindPopup("<b>Mã số: VT-001</b><br>Diện tích: 5000m2<br>Loại cây: Xoài");
});
</script>

<template>
      <div id="map-container"></div>
</template>

<style scoped>
#map-container {
      width: 100%;
      height: 600px;
      /* Tăng chiều cao lên cho dễ nhìn */
      border-radius: 8px;
      border: 1px solid #ccc;
}
</style>
