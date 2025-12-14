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
import { computed, ref } from 'vue';
import { exportData, totalExportValue } from '../composables/useCharts';

// ========== COLORS FOR PIE CHART ==========
const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];

// ========== COMPUTED: Pie Chart Data ==========
const pieData = computed(() => {
  return exportData.value.map((item, index) => ({
    ...item,
    percentage: (item.value / totalExportValue.value) * 100,
    color: colors[index % colors.length],
  }));
});

// ========== SVG PIE CHART FUNCTION ==========
function generatePiePath(data, index) {
  const radius = 100;
  const cx = 120;
  const cy = 120;
  
  let startAngle = 0;
  for (let i = 0; i < index; i++) {
    startAngle += (data[i].percentage / 100) * 360;
  }
  
  const endAngle = startAngle + (data[index].percentage / 100) * 360;
  const isLarge = data[index].percentage > 50 ? 1 : 0;
  
  const startRad = (startAngle * Math.PI) / 180;
  const endRad = (endAngle * Math.PI) / 180;
  
  const x1 = cx + radius * Math.cos(startRad);
  const y1 = cy + radius * Math.sin(startRad);
  const x2 = cx + radius * Math.cos(endRad);
  const y2 = cy + radius * Math.sin(endRad);
  
  const path = `M ${cx} ${cy} L ${x1} ${y1} A ${radius} ${radius} 0 ${isLarge} 1 ${x2} ${y2} Z`;
  return path;
}

// ========== LABEL POSITION FUNCTION ==========
function getLabelPosition(data, index) {
  const radius = 130;
  const cx = 120;
  const cy = 120;
  
  let angle = 0;
  for (let i = 0; i < index; i++) {
    angle += (data[i].percentage / 100) * 360;
  }
  angle += (data[index].percentage / 100) * 180;
  
  const rad = (angle * Math.PI) / 180;
  const x = cx + radius * Math.cos(rad);
  const y = cy + radius * Math.sin(rad);
  
  return { x, y };
}
</script>

<template>
  <!-- Container chính: Pie chart section -->
  <div class="w-full h-full flex flex-col">
    <!-- Tiêu đề -->
    <h3 class="text-xs font-bold text-gray-700 mb-3">Thị trường Xuất khẩu</h3>
    
    <!-- Pie Chart Section -->
    <div class="flex-1 flex items-center justify-center min-h-0">
      <div class="flex flex-col items-center gap-4 w-full">
        <!-- SVG Pie Chart -->
        <svg width="300" height="300" viewBox="0 0 240 240" class="flex-shrink-0">
          <!-- Pie slices -->
          <path
            v-for="(item, index) in pieData"
            :key="index"
            :d="generatePiePath(pieData, index)"
            :fill="item.color"
            :stroke="'white'"
            stroke-width="2"
            class="hover:opacity-80 transition-opacity cursor-pointer"
          />
          
          <!-- Labels with percentages -->
          <text
            v-for="(item, index) in pieData"
            :key="'label-' + index"
            :x="getLabelPosition(pieData, index).x"
            :y="getLabelPosition(pieData, index).y"
            text-anchor="middle"
            dominant-baseline="middle"
            class="text-xs font-bold fill-white"
          >
            {{ item.percentage.toFixed(1) }}%
          </text>
        </svg>
        
        <!-- Legend -->
        <div class="grid grid-cols-2 gap-3 text-xs w-full px-2">
          <div
            v-for="(item, index) in pieData"
            :key="'legend-' + index"
            class="flex items-center gap-2"
          >
            <div
              class="w-3 h-3 rounded-full flex-shrink-0"
              :style="{ backgroundColor: item.color }"
            ></div>
            <div class="flex flex-col">
              <span class="font-semibold text-gray-700">{{ item.market }}</span>
              <span class="text-gray-500">{{ item.value.toLocaleString() }} USD</span>
            </div>
          </div>
        </div>
        
        <!-- Total -->
        <div class="text-xs text-center text-gray-600 pt-2 border-t border-gray-200 w-full">
          <p class="font-semibold">Tổng: {{ totalExportValue.toLocaleString() }} USD</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styling nếu cần */
</style>

