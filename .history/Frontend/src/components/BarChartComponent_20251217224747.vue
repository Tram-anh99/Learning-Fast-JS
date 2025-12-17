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
import { cropData } from '../composables/useCharts';

// ========== REFS ==========
const chartContainer = ref(null);
let chartInstance = null;

// ========== COMPUTED: Average Productivity ==========
const getAverageProductivity = computed(() => {
      if (cropData.value.length === 0) return 0;
      const total = cropData.value.reduce((sum, item) => sum + item.nangSuat, 0);
      return total / cropData.value.length;
});

// ========== COMPUTED: Bar Chart Data ==========
const chartData = computed(() => {
      return {
            labels: cropData.value.map(item => item.tenCay),
            datasets: [
                  {
                        label: 'Năng suất (tạ/ha)',
                        data: cropData.value.map(item => item.nangSuat),
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
                  padding: 8,
                  titleFont: {
                        size: 11,
                        weight: 'bold',
                  },
                  bodyFont: {
                        size: 10,
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
                        display: false,
                  },
                  ticks: {
                        color: '#6B7280',
                        font: {
                              size: 9,
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
                              size: 9,
                        },
                        maxRotation: 45,
                        minRotation: 0,
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
      <div class="w-full h-full flex flex-col overflow-hidden">
            <!-- Tiêu đề -->
            <div class="flex-shrink-0 mb-2 sm:mb-3">
                  <h3 class="text-sm sm:text-base font-bold text-gray-800">Năng suất theo Loại cây</h3>
                  <p class="text-[10px] sm:text-xs text-gray-500">Đơn vị: tạ/ha - Cây có năng suất cao → ưu tiên mở rộng</p>
            </div>

            <!-- Chart container -->
            <div class="flex-1 min-h-0 relative">
                  <canvas ref="chartContainer"></canvas>
            </div>

            <!-- Stats footer -->
            <div class="text-xs sm:text-sm text-center text-gray-600 pt-2 sm:pt-3 border-t border-gray-200 mt-2 sm:mt-3 flex-shrink-0">
                  <p class="font-semibold">Trung bình: <span class="text-blue-600">{{
                        getAverageProductivity.toFixed(2) }} tạ/ha</span></p>
            </div>
      </div>
</template>

<style scoped>
/* Styling nếu cần */
</style>
