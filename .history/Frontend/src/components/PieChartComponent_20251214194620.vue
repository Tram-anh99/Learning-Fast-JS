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
import { computed, onMounted, ref, onBeforeUnmount } from 'vue';
import Chart from 'chart.js/auto';
import { exportData, totalExportValue } from '../composables/useCharts';

// ========== REFS ==========
const chartContainer = ref(null);
let chartInstance = null;

// ========== COMPUTED: Pie Chart Data ==========
const chartData = computed(() => {
  return {
    labels: exportData.value.map(item => item.market),
    datasets: [
      {
        label: 'Giá trị xuất khẩu (USD)',
        data: exportData.value.map(item => item.value),
        backgroundColor: [
          '#FF6B6B',
          '#4ECDC4',
          '#45B7D1',
          '#FFA07A',
          '#98D8C8',
        ],
        borderColor: '#ffffff',
        borderWidth: 2,
      },
    ],
  };
});

// ========== CHART OPTIONS ==========
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        padding: 15,
        font: {
          size: 12,
          weight: 'bold',
        },
        color: '#374151',
      },
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 10,
      titleFont: {
        size: 12,
        weight: 'bold',
      },
      bodyFont: {
        size: 11,
      },
      callbacks: {
        label: function (context) {
          const value = context.parsed;
          const total = totalExportValue.value;
          const percentage = ((value / total) * 100).toFixed(1);
          return `${value.toLocaleString()} USD (${percentage}%)`;
        },
      },
    },
  },
};

// ========== LIFECYCLE: Create Chart ==========
onMounted(() => {
  if (chartContainer.value && chartData.value.labels.length > 0) {
    const ctx = chartContainer.value.getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: chartData.value,
      options: chartOptions,
    });
  }
});

// ========== CLEANUP: Destroy Chart ==========
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});
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

