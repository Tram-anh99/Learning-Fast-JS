<script setup>
import { ref } from 'vue';
import 'leaflet/dist/leaflet.css';
// Import các component chính
import StatsBarComponent from '../components/StatsBarComponent.vue';
import MapComponent from '../components/MapComponent.vue';
import DataTableComponent from '../components/DataTableComponent.vue';
// Import mock data và helpers
import { mockDataThongKe, mockDataVung, mockDiemNongSauBenh } from '../composables/statusHelpers';

// Dữ liệu thống kê hệ thống
const thongKe = ref(mockDataThongKe);
// Danh sách vùng trồng được quản lý
const danhSachVung = ref(mockDataVung);
</script>

<template>
  <!-- Container layout chính - flex column -->
  <div class="admin-container">
    <!-- 1. Thanh thống kê ở trên cùng -->
    <StatsBarComponent :thongKe="thongKe" />
    
    <!-- 2. Bản đồ ở giữa -->
    <MapComponent :danhSachVung="danhSachVung" :diemNongSauBenh="mockDiemNongSauBenh" />
    
    <!-- 3. Bảng danh sách vùng ở dưới -->
    <DataTableComponent :danhSachVung="danhSachVung" />
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
</style>