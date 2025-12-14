<script setup>
/**
 * ========== COMPONENT: ChartsComponent.vue ==========
 * Purpose: Hiển thị biểu đồ thống kê (pie chart & bar chart) cho dashboard
 * 
 * Features:
 *   - Biểu đồ tròn: Phân bổ thị trường xuất khẩu
 *   - Biểu đồ cột: Sản lượng theo loại cây
 *   - Responsive layout cho desktop/mobile
 *   - Dễ mở rộng: Thêm Line Chart, Scatter, v.v.
 * 
 * Related Files:
 *   - src/views/QuanLyView.vue - Parent component
 *   - src/composables/useCharts.js - Data & logic
 */

// ========== IMPORTS ==========
// Import computed từ Vue 3 Composition API để tính toán style động
import { computed } from 'vue';

// Import dữ liệu & logic từ composable
import {
  exportData,
  cropData,
  pieChartStyle,
  totalExportValue,
  getTopCrop,
  getAverageProductivity,
} from '../composables/useCharts';

// Import new chart components (uncomment to add to dashboard)
// import ProductivityLineChart from './ProductivityLineChart.vue';

// ========== COMPONENT SETUP ==========
// Tất cả dữ liệu đã import từ useCharts, không cần định nghĩa lại ở đây

</script>

<template>
      <!-- Container chính: flex column, chiếm hết không gian và chia phần bằng -->
      <!-- h-full = 100% height, gap-5 = khoảng cách giữa các biểu đồ -->
      <!-- NOTE: Dễ dàng mở rộng thêm biểu đồ (Line, Scatter, v.v.) bằng cách thêm div mới -->
      <div class="flex flex-col h-full gap-5">
            <!-- ========== SECTION 1: Biểu đồ Tròn (Pie Chart) ========== -->
            <!-- Hiển thị phân bổ thị trường xuất khẩu -->
            <!-- flex-1 = chiếm 50% height, p-4 = padding bên trong -->
            <div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl min-h-0 overflow-y-auto">
                  <!-- Tiêu đề: "Thị trường Xuất khẩu" -->
                  <!-- text-xs font-bold = font chữ nhỏ, in đậm -->
                  <!-- uppercase = chữ in hoa, tracking-wider = giãn cách chữ -->
                  <h3 class="mb-4 text-xs font-bold tracking-wider uppercase text-slate-500">
                        <!-- Icon: biểu tượng bản đồ thế giới -->
                        <i class="mr-1 fas fa-globe-americas"></i> Thị trường Xuất khẩu
                  </h3>

                  <!-- Layout chính: flex row, items-center justify-center = căn giữa -->
                  <div class="flex items-center justify-center flex-1 gap-4">
                        <!-- ========== Pie Chart Circle ========== -->
                        <!-- Biểu đồ tròn được vẽ bằng conic-gradient -->
                        <!-- :style="pieChartStyle" = áp dụng computed gradient style -->
                        <!-- w-28 h-28 = 112px x 112px, rounded-full = hình tròn -->
                        <div class="relative flex-shrink-0 rounded-full shadow-inner w-28 h-28" :style="pieChartStyle">
                              <!-- Donut hole: vòng trắng ở giữa để tạo hiệu ứng donut -->
                              <!-- absolute inset-0 m-auto = centered, w-14 h-14 = 56px x 56px -->
                              <div class="absolute inset-0 m-auto bg-white rounded-full shadow-sm w-14 h-14"></div>
                        </div>

                        <!-- ========== Legend (Chú thích) ========== -->
                        <!-- Danh sách các màu & tỉ lệ của mỗi thị trường -->
                        <!-- space-y-2 = khoảng cách giữa các item 8px -->
                        <div class="space-y-2 min-w-[100px]">
                              <!-- Loop qua từng item trong exportData -->
                              <div v-for="item in exportData" :key="item.label"
                                    class="flex items-center justify-between text-xs">
                                    <!-- Khối bên trái: item square + label -->
                                    <div class="flex items-center gap-2">
                                          <!-- Indicator square: hình vuông nhỏ với màu item -->
                                          <!-- w-2.5 h-2.5 = 10px x 10px, rounded-full = hình tròn -->
                                          <span class="w-2.5 h-2.5 rounded-full shadow-sm"
                                                :style="{ backgroundColor: item.color }"></span>
                                          <!-- Label text: tên thị trường -->
                                          <span class="font-medium text-slate-600">{{ item.label }}</span>
                                    </div>
                                    <!-- Giá trị phần trăm: bên phải -->
                                    <span class="font-bold text-slate-800">{{ item.value }}%</span>
                              </div>
                        </div>
                  </div>
            </div>

            <!-- ========== SECTION 2: Biểu đồ Cột (Bar Chart) ========== -->
            <!-- Hiển thị sản lượng theo loại cây trồng -->
            <!-- flex-1 = chiếm 50% height còn lại -->
            <div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl min-h-0 overflow-y-auto">
                  <!-- Tiêu đề: "Sản lượng Cây trồng" -->
                  <h3 class="mb-4 text-xs font-bold tracking-wider uppercase text-slate-500">
                        <!-- Icon: biểu tượng cây nhỏ (seedling) -->
                        <i class="mr-1 fas fa-seedling"></i> Sản lượng Cây trồng
                  </h3>

                  <!-- ========== Bars Container ========== -->
                  <!-- flex items-end = căn các cột ở dưới, justify-around = chia đều -->
                  <!-- gap-3 = khoảng cách giữa cột, pb-2 = padding dưới, min-h-[140px] = cao tối thiểu -->
                  <div class="flex items-end justify-around gap-3 flex-1 pb-2 border-b border-slate-100 min-h-[140px]">
                        <!-- Loop qua từng loại cây -->
                        <div v-for="crop in cropData" :key="crop.label"
                              class="flex flex-col items-center justify-end w-full h-full gap-1 group">
                              <!-- Giá trị ở trên cùng cột -->
                              <!-- text-[10px] = font rất nhỏ, font-bold = in đậm -->
                              <div class="text-[10px] font-bold text-slate-600 mb-0.5">
                                    {{ crop.value }}</div>
                              <!-- Cột (bar) chính -->
                              <!-- max-w-[30px] = chiều rộng tối đa 30px để không quá rộng -->
                              <!-- :style="{ height: `${crop.value}%` }" = chiều cao tỉ lệ với giá trị -->
                              <!-- rounded-t-md = bo góc trên, hover:opacity-80 = mờ khi hover -->
                              <div class="w-full max-w-[30px] rounded-t-md transition-all duration-500 hover:opacity-80 relative shadow-sm"
                                    :class="crop.color" :style="{ height: `${crop.value}%` }">
                              </div>
                        </div>
                  </div>
                  <!-- Labels -->
                  <div class="flex justify-around gap-2 mt-2">
                        <div v-for="crop in cropData" :key="crop.label"
                              class="text-[10px] font-semibold text-slate-500 text-center w-full truncate">
                              {{ crop.label }}
                        </div>
                  </div>
            </div>

            <!-- ========== SECTION 3: PLACEHOLDER FOR FUTURE CHARTS ========== -->
            <!-- Các biểu đồ khác có thể thêm ở đây (Line Chart, Area Chart, Scatter, v.v.) -->
            <!-- Uncomment và thêm component khi cần -->
            <!--
            <div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl min-h-0 overflow-y-auto">
                  <h3 class="mb-4 text-xs font-bold tracking-wider uppercase text-slate-500">
                        <i class="mr-1 fas fa-chart-line"></i> Xu hướng Năng suất
                  </h3>
                  <div class="flex-1 flex items-center justify-center text-slate-400">
                        <p>Line Chart sẽ được thêm ở đây</p>
                  </div>
            </div>
            -->
      </div>
</template>