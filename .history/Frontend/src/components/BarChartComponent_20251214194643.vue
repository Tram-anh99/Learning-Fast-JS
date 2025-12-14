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
import { computed, onMounted, ref, onBeforeUnmount } from 'vue';
import Chart from 'chart.js/auto';
import { cropData, getAverageProductivity } from '../composables/useCharts';

// ========== REFS ==========
const chartContainer = ref(null);
let chartInstance = null;

// ========== COMPUTED: Bar Chart Data ==========
const chartData = computed(() => {
  return {
    labels: cropData.value.map(item => item.crop),
    datasets: [
      {
        label: 'Năng suất (tạ/ha)',
        data: cropData.value.map(item => item.productivity),
        backgroundColor: [
          '#3B82F6',
          '#10B981',
          '#F59E0B',
          '#EF4444',
          '#8B5CF6',
        ],
        borderColor: '#ffffff',
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };
});

// ========== CHART OPTIONS ==========
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'x',
  plugins: {
    legend: {
      display: false,
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
          return `${context.parsed.y.toFixed(2)} tạ/ha`;
        },
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Năng suất (tạ/ha)',
      },
      ticks: {
        color: '#6B7280',
        font: {
          size: 11,
        },
      },
      grid: {
        color: 'rgba(209, 213, 219, 0.3)',
      },
    },
    x: {
      ticks: {
        color: '#6B7280',
        font: {
          size: 11,
        },
      },
      grid: {
        display: false,
      },
    },
  },
};

// ========== LIFECYCLE: Create Chart ==========
onMounted(() => {
  if (chartContainer.value && chartData.value.labels.length > 0) {
    const ctx = chartContainer.value.getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'bar',
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
