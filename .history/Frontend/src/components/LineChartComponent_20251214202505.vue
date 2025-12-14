<script setup>
/**
 * ========== COMPONENT: LineChartComponent.vue ==========
 * Purpose: Biểu đồ đường hiển thị mối quan hệ giữa thị trường xuất khẩu và loại cây
 * 
 * Features:
 *   - Chart.js Line Chart với dữ liệu thực tế
 *   - Hiển thị 4 thị trường chính (Nhật Bản, Mỹ, EU, Trung Quốc)
 *   - Y-axis: Sản lượng xuất khẩu (tấn)
 *   - X-axis: Loại cây trồng
 *   - Tooltip hiển thị giá trị cụ thể mỗi thị trường
 *   - Legend ở dưới để phân biệt các đường
 */

import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';
import { lineChartData, lineChartOptions } from '../composables/useLineChartData';

// Ref cho canvas element
const chartCanvas = ref(null);
let chartInstance = null;

// Lifecycle: Khởi tạo chart khi component mounted
onMounted(() => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: lineChartData,
      options: lineChartOptions
    });
  }
});

// Cleanup: Hủy chart instance khi component unmounted
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});

import { onBeforeUnmount } from 'vue';
</script>

<template>
  <!-- ========== LINE CHART CONTAINER ========== -->
  <!-- Wrapper cho biểu đồ đường -->
  <div class="flex flex-col h-full">
    <!-- ========== CHART TITLE ========== -->
    <h3 class="text-lg font-bold text-gray-800 mb-2">Mối quan hệ: Thị trường xuất khẩu & Loại cây</h3>
    
    <!-- ========== MARKET LEGEND ========== -->
    <!-- Chú thích để phân biệt các thị trường theo màu -->
    <div class="grid grid-cols-2 gap-2 mb-3 text-sm">
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-[#FF6B6B]"></div>
        <span class="text-gray-700 font-medium">Nhật Bản</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-[#4ECDC4]"></div>
        <span class="text-gray-700 font-medium">Mỹ</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-[#FFE66D]"></div>
        <span class="text-gray-700 font-medium">EU</span>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-[#95E1D3]"></div>
        <span class="text-gray-700 font-medium">Trung Quốc</span>
      </div>
    </div>
    
    <!-- ========== CHART CANVAS ========== -->
    <!-- Canvas element nơi Chart.js render biểu đồ -->
    <!-- Chiều cao tự động fill parent container -->
    <div class="flex-1 relative min-h-[280px]">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<style scoped>
/* Custom styles cho line chart component */
</style>
