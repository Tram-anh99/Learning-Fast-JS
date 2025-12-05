<script setup>
import { onMounted } from 'vue';
import L from 'leaflet'; // Import thư viện Leaflet
import 'leaflet/dist/leaflet.css'; // Import giao diện (CSS) của bản đồ

// Hàm onMounted chạy ngay khi trang web hiện ra
onMounted(() => {
  // 1. Khởi tạo bản đồ tại thẻ div có id="map"
  // Tọa độ [10.762, 106.660] là TP.HCM, Zoom level 10
  const map = L.map('map').setView([10.762, 106.660], 10);

  // 2. Thêm lớp nền bản đồ (Base Map) từ OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // 3. Thêm thử một cái ghim (Marker) để test
  L.marker([10.762, 106.660]).addTo(map)
    .bindPopup('Trung tâm TP.HCM<br>Đây là ví dụ Marker.')
    .openPopup();
});
</script>

<template>
  <div>
    <h1>Hệ thống Quản lý Vùng trồng</h1>
    <div id="map"></div>
  </div>
</template>

<style>
/* Bắt buộc phải có chiều cao (height) thì bản đồ mới hiện ra */
#map {
  width: 100%;
  height: 500px; /* Chiều cao 500 pixel */
  border: 2px solid #42b883; /* Viền xanh cho đẹp */
  border-radius: 8px;
}
</style>