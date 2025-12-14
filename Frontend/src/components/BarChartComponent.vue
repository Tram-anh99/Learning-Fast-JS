<script setup>
/**
 * ========== COMPONENT: BarChartComponent.vue ==========
 * Purpose: Hiển thị biểu đồ cột năng suất cây trồng
 * 
 * Features:
 *   - Biểu đồ cột: Sản lượng theo loại cây
 *   - Responsive layout
 *   - Scrollbar support
 * 
 * Related Files:
 *   - src/views/QuanLyView.vue - Parent component
 *   - src/composables/useCharts.js - Data & logic
 */

// ========== IMPORTS ==========
import { computed } from 'vue';
import { cropData, getTopCrop, getAverageProductivity } from '../composables/useCharts';

// ========== COMPONENT SETUP ==========
// Tất cả dữ liệu đã import từ useCharts, không cần định nghĩa lại ở đây
</script>

<template>
  <!-- Container chính: Bar chart section -->
  <div class="w-full h-full flex flex-col">
    <!-- Tiêu đề -->
    <h3 class="text-xs font-bold text-gray-700 mb-3">Năng suất Cây trồng</h3>
    
    <!-- Placeholder cho Bar Chart -->
    <div class="flex-1 flex items-center justify-center min-h-0">
      <div class="text-center text-gray-400">
        <p class="text-sm mb-2">Biểu đồ cột</p>
        <p class="text-xs text-gray-500">(Bar Chart - Năng suất cây trồng)</p>
        
        <!-- Mock data display -->
        <div class="mt-4 text-left text-xs">
          <p class="text-gray-600 font-semibold mb-2">Dữ liệu cây trồng:</p>
          <div v-for="item in cropData" :key="item.crop" class="text-gray-500">
            {{ item.crop }}: {{ item.productivity.toLocaleString() }} tạ/ha
          </div>
          
          <div class="mt-3 pt-3 border-t border-gray-300">
            <p class="text-gray-600 font-semibold">Top cây trồng: {{ getTopCrop() }}</p>
            <p class="text-gray-600 font-semibold mt-1">Năng suất trung bình: {{ getAverageProductivity().toFixed(2) }} tạ/ha</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styling nếu cần */
</style>
