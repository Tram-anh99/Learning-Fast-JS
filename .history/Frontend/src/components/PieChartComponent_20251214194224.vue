<script setup>
/**
 * ========== COMPONENT: PieChartComponent.vue ==========
 * Purpose: Hiển thị biểu đồ tròn phân bổ thị trường xuất khẩu
 * 
 * Features:
 *   - Biểu đồ tròn: Thị trường xuất khẩu
 *   - Responsive layout
 *   - Scrollbar support
 * 
 * Related Files:
 *   - src/views/QuanLyView.vue - Parent component
 *   - src/composables/useCharts.js - Data & logic
 */

// ========== IMPORTS ==========
import { computed } from 'vue';
import { exportData, pieChartStyle, totalExportValue } from '../composables/useCharts';

// ========== COMPONENT SETUP ==========
// Tất cả dữ liệu đã import từ useCharts, không cần định nghĩa lại ở đây
</script>

<template>
  <!-- Container chính: Pie chart section -->
  <div class="w-full h-full flex flex-col">
    <!-- Tiêu đề -->
    <h3 class="text-xs font-bold text-gray-700 mb-3">Thị trường Xuất khẩu</h3>
    
    <!-- Placeholder cho Pie Chart -->
    <div class="flex-1 flex items-center justify-center min-h-0">
      <div class="text-center text-gray-400">
        <p class="text-sm mb-2">Biểu đồ tròn</p>
        <p class="text-xs text-gray-500">(Pie Chart - Thị trường xuất khẩu)</p>
        
        <!-- Mock data display -->
        <div class="mt-4 text-left text-xs">
          <p class="text-gray-600 font-semibold mb-2">Dữ liệu xuất khẩu:</p>
          <div v-for="item in exportData" :key="item.market" class="text-gray-500">
            {{ item.market }}: {{ item.value.toLocaleString() }} USD
          </div>
          <p class="text-gray-600 font-semibold mt-2">Tổng: {{ totalExportValue.toLocaleString() }} USD</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styling nếu cần */
</style>
