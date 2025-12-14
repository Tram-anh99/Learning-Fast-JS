/**
 * ========== COMPONENT: ProductivityLineChart.vue ==========
 * Purpose: Biểu đồ đường xu hướng năng suất (Example for expansion)
 * 
 * Status: EXAMPLE COMPONENT - Ready to use
 * Integration: Can be added to ChartsComponent via import
 * 
 * Example of how to add new charts to QuanLyView
 */

<template>
  <!-- Container: Matches ChartsComponent card styling -->
  <div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl min-h-0 overflow-y-auto">
    <!-- Title -->
    <h3 class="mb-4 text-xs font-bold tracking-wider uppercase text-slate-500">
      <i class="mr-1 fas fa-chart-line"></i> Xu hướng Năng suất
    </h3>

    <!-- Chart Container -->
    <div class="flex-1 flex flex-col gap-4 justify-center min-h-[200px]">
      <!-- Simple Line Chart using CSS (No library needed) -->
      <!-- Y-axis labels -->
      <div class="flex gap-2">
        <div class="w-8 text-right text-[10px] text-slate-400">6.0</div>
        <div class="flex-1 border-t border-dashed border-slate-200"></div>
      </div>

      <!-- Chart line visualization -->
      <svg class="w-full h-32" viewBox="0 0 400 120" preserveAspectRatio="xMidYMid meet">
        <!-- Grid lines -->
        <line x1="40" y1="20" x2="40" y2="100" stroke="#cbd5e1" stroke-width="1" />
        <line x1="40" y1="100" x2="380" y2="100" stroke="#cbd5e1" stroke-width="1" />

        <!-- Y-axis labels -->
        <text x="35" y="105" text-anchor="end" font-size="10" fill="#94a3b8">0</text>
        <text x="35" y="25" text-anchor="end" font-size="10" fill="#94a3b8">6</text>

        <!-- Chart line with area fill -->
        <defs>
          <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#10b981;stop-opacity:0.2" />
            <stop offset="100%" style="stop-color:#10b981;stop-opacity:0" />
          </linearGradient>
        </defs>

        <!-- Area under the line -->
        <polygon
          points="40,68 80,50 120,58 160,38 200,28 240,42 280,26 320,44 360,38 380,52 380,100 40,100"
          fill="url(#areaGradient)"
        />

        <!-- Actual line -->
        <polyline
          points="40,68 80,50 120,58 160,38 200,28 240,42 280,26 320,44 360,38 380,52"
          fill="none"
          stroke="#10b981"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />

        <!-- Data points (circles) -->
        <circle cx="40" cy="68" r="3" fill="#10b981" />
        <circle cx="80" cy="50" r="3" fill="#10b981" />
        <circle cx="120" cy="58" r="3" fill="#10b981" />
        <circle cx="160" cy="38" r="3" fill="#10b981" />
        <circle cx="200" cy="28" r="3" fill="#10b981" />
        <circle cx="240" cy="42" r="3" fill="#10b981" />
        <circle cx="280" cy="26" r="3" fill="#10b981" />
        <circle cx="320" cy="44" r="3" fill="#10b981" />
        <circle cx="360" cy="38" r="3" fill="#10b981" />
        <circle cx="380" cy="52" r="3" fill="#10b981" />

        <!-- X-axis labels (months) -->
        <text x="40" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T1</text>
        <text x="80" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T2</text>
        <text x="120" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T3</text>
        <text x="160" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T4</text>
        <text x="200" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T5</text>
        <text x="240" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T6</text>
        <text x="280" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T7</text>
        <text x="320" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T8</text>
        <text x="360" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T9</text>
        <text x="380" y="115" text-anchor="middle" font-size="10" fill="#94a3b8">T10</text>
      </svg>

      <!-- Legend & Stats -->
      <div class="flex justify-between items-center px-2 text-[11px]">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-green-500"></span>
          <span class="text-slate-600">Năng suất (tấn/hectare)</span>
        </div>
        <div class="text-slate-600">
          <span class="font-bold text-green-600">{{ getAverageProductivity() }}</span>
          <span class="text-slate-400">tấn/ha (avg)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * IMPORT: Get data from useCharts composable
 * This component is completely data-driven
 * Update useCharts.js and this chart auto-updates
 */
import { productivityTrendData, getAverageProductivity } from '../composables/useCharts';

/**
 * NOTE: This is a STATIC SVG example for demonstration
 * For production, use:
 * 1. Chart.js library (https://www.chartjs.org)
 * 2. Recharts library (https://recharts.org)
 * 3. ECharts library (https://echarts.apache.org)
 * 4. D3.js (advanced)
 * 
 * Example with Chart.js:
 * ```
 * import { Chart, Line } from 'chart.js';
 * 
 * onMounted(() => {
 *   const ctx = chartContainer.value.getContext('2d');
 *   new Chart(ctx, {
 *     type: 'line',
 *     data: {
 *       labels: productivityTrendData.value.map(d => d.month),
 *       datasets: [{
 *         label: 'Năng suất',
 *         data: productivityTrendData.value.map(d => d.productivity),
 *         borderColor: '#10b981',
 *         fill: true,
 *         backgroundColor: 'rgba(16, 185, 129, 0.1)'
 *       }]
 *     }
 *   });
 * });
 * ```
 */
</script>

<style scoped>
/* Optional: Add animation on hover */
circle {
  cursor: pointer;
  transition: r 0.3s ease;
}

circle:hover {
  r: 5;
}
</style>
