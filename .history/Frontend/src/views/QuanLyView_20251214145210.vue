<script setup>
/**
 * ========== VIEW: QuanLyView.vue ==========
 * Purpose: Trang quản lý vùng trồng - Dashboard với thống kê, bản đồ và bảng dữ liệu
 * 
 * Architecture:
 *   - Components:
 *     • StatsBarComponent.vue - Thanh thống kê (số vùng, diện tích, v.v.)
 *     • MapComponent.vue - Bản đồ tương tác với polygon vùng trồng
 *     • DataTableComponent.vue - Bảng danh sách vùng với các chỉ số
 *     • ChartsComponent.vue - Biểu đồ thống kê
 *   - Styling: src/assets/styles/tailwind.css (Global utilities)
 *   - Libraries: Leaflet, Chart.js
 * 
 * Features:
 *   - Thống kê tổng quát hệ thống
 *   - Bản đồ tương tác hiển thị các vùng trồng
 *   - Biểu đồ phân tích dữ liệu
 *   - Bảng danh sách vùng trồng có thể sắp xếp và lọc
 */

// ========== IMPORTS ==========
import { ref } from 'vue';
import 'leaflet/dist/leaflet.css';

// Components
import StatsBarComponent from '../components/StatsBarComponent.vue';
import MapComponent from '../components/MapComponent.vue';
import DataTableComponent from '../components/DataTableComponent.vue';
import ChartsComponent from '../components/ChartsComponent.vue';

// Composables & Mock data
import { mockDataThongKe, mockDataVung, mockDiemNongSauBenh } from '../composables/statusHelpers';

// ========== STATE ==========
// Dữ liệu thống kê hệ thống (số vùng, diện tích, tình trạng, v.v.)
const thongKe = ref(mockDataThongKe);

// ========== DATA ==========
// Danh sách vùng trồng được quản lý
const danhSachVung = ref(mockDataVung);

// ========== METHODS ==========
// (Có thể thêm các hàm xử lý sự kiện nếu cần: editVung, deleteVung, exportData, v.v.)
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
