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
import { exportData } from '../composables/useCharts';

// ========== REFS ==========
const chartContainer = ref(null);
let chartInstance = null;

// ========== COMPUTED: Pie Chart Data ==========
const chartData = computed(() => {
      const total = exportData.value.reduce((sum, item) => sum + item.value, 0);
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

// ========== COMPUTED: Total Export Value ==========
const totalExportValue = computed(() => {
      return exportData.value.reduce((sum, item) => sum + item.value, 0);
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
            <h3 class="text-base font-bold text-gray-800 mb-3">Thị trường Xuất khẩu</h3>

            <!-- Chart container -->
            <div class="flex-1 min-h-0">
                  <canvas ref="chartContainer" class="w-full h-full"></canvas>
            </div>
      </div>
</template>

<style scoped>
/* Styling nếu cần */
</style>
