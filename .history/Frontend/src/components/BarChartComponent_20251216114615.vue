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
                              '#FF6B6B',
                              '#4ECDC4',
                              '#FFE66D',
                              '#95E1D3',
                              '#A8DADC',
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

            <!-- Chart container -->
            <div class="flex-1 min-h-0">
                  <canvas ref="chartContainer" class="w-full h-full"></canvas>
            </div>

            <!-- Stats footer -->
            <div class="text-xs text-center text-gray-600 pt-3 border-t border-gray-200 mt-3">
                  <p class="font-semibold">Năng suất trung bình: <span class="text-blue-600">{{
                        getAverageProductivity.toFixed(2) }} tạ/ha</span></p>
            </div>
      </div>
</template>

<style scoped>
/* Styling nếu cần */
</style>
