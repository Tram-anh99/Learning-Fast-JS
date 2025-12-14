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

// ========== COMPUTED: Bar Chart Data ==========
const maxProductivity = computed(() => {
  return Math.max(...cropData.value.map(item => item.productivity));
});

const barHeight = computed(() => {
  return cropData.value.map(item => (item.productivity / maxProductivity.value) * 100);
});
</script>

<template>
  <!-- Container chính: Bar chart section -->
  <div class="w-full h-full flex flex-col">
    <!-- Tiêu đề -->
    <h3 class="text-xs font-bold text-gray-700 mb-3">Năng suất Cây trồng (tạ/ha)</h3>
    
    <!-- Bar Chart -->
    <div class="flex-1 flex flex-col items-center justify-center min-h-0 overflow-hidden">
      <!-- Chart container with horizontal scroll -->
      <div class="w-full h-full flex items-end justify-center gap-6 px-4 py-8 overflow-x-auto">
        <!-- Bars -->
        <div
          v-for="(item, index) in cropData"
          :key="index"
          class="flex flex-col items-center gap-2 flex-shrink-0"
        >
          <!-- Bar -->
          <div class="flex flex-col items-center gap-1">
            <span class="text-xs font-semibold text-gray-700">
              {{ item.productivity.toFixed(1) }}
            </span>
            <div
              class="bg-gradient-to-t from-blue-500 to-blue-400 rounded-t-lg transition-all hover:from-blue-600 hover:to-blue-500 cursor-pointer"
              :style="{
                width: '40px',
                height: `${(item.productivity / maxProductivity) * 200}px`,
                minHeight: '20px',
              }"
            ></div>
          </div>
          
          <!-- Label -->
          <span class="text-xs text-gray-600 font-medium text-center whitespace-nowrap">
            {{ item.crop }}
          </span>
        </div>
      </div>
      
      <!-- Y-axis label -->
      <div class="text-xs text-gray-500 mt-2">
        (Cao nhất: {{ maxProductivity.toFixed(1) }} tạ/ha)
      </div>
    </div>
    
    <!-- Stats footer -->
    <div class="grid grid-cols-2 gap-4 text-xs border-t border-gray-200 pt-3 mt-3">
      <div class="text-center">
        <p class="text-gray-600 font-semibold">Top cây:</p>
        <p class="text-blue-600 font-bold">{{ getTopCrop() }}</p>
      </div>
      <div class="text-center">
        <p class="text-gray-600 font-semibold">TB năng suất:</p>
        <p class="text-blue-600 font-bold">{{ getAverageProductivity().toFixed(2) }} tạ/ha</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Smooth scrollbar */
::-webkit-scrollbar {
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
