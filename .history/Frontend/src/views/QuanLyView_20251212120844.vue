<script setup>
import { ref } from 'vue';
import 'leaflet/dist/leaflet.css';
// Import các component chính
import StatsBarComponent from '../components/StatsBarComponent.vue';
import MapComponent from '../components/MapComponent.vue';
import DataTableComponent from '../components/DataTableComponent.vue';
import ChartsComponent from '../components/ChartsComponent.vue';
// Import mock data và helpers
import { mockDataThongKe, mockDataVung, mockDiemNongSauBenh } from '../composables/statusHelpers';

// Dữ liệu thống kê hệ thống
const thongKe = ref(mockDataThongKe);
// Danh sách vùng trồng được quản lý
const danhSachVung = ref(mockDataVung);
</script>

<template>
      <!-- Container layout chính - flex column -->
      <div class="absolute inset-0 bg-slate-100 flex flex-col p-5 gap-5">
            <!-- 1. Thanh thống kê ở trên cùng -->
            <StatsBarComponent :thongKe="thongKe" />

            <!-- 2. Khu vực giữa: Biểu đồ & Bản đồ -->
            <div class="flex flex-[2] gap-5 min-h-0">
                  <!-- Biểu đồ bên trái (chiếm 1 phần) -->
                  <div class="flex-1 min-w-[300px]">
                        <ChartsComponent />
                  </div>
                  <!-- Bản đồ bên phải (chiếm 2 phần - do class flex-[2] trong MapComponent) -->
                  <MapComponent :danhSachVung="danhSachVung" :diemNongSauBenh="mockDiemNongSauBenh" />
            </div>

            <!-- 3. Bảng danh sách vùng ở dưới -->
            <DataTableComponent :danhSachVung="danhSachVung" />
      </div>
</template>
