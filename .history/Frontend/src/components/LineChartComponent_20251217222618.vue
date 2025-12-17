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
      <div class="flex flex-col h-full overflow-hidden">
            <!-- ========== CHART TITLE ========== -->
            <h3 class="text-sm sm:text-base font-bold text-gray-800 mb-2 sm:mb-3 flex-shrink-0">Thị trường & Loại cây</h3>

            <!-- ========== CHART CANVAS ========== -->
            <!-- Canvas element nơi Chart.js render biểu đồ -->
            <!-- Chiều cao tự động fill parent container -->
            <div class="flex-1 min-h-0 relative">
                  <canvas ref="chartCanvas"></canvas>
            </div>
      </div>
</template>

<style scoped>
.flex-1 canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
