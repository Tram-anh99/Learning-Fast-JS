<script setup>
/**
 * ========== COMPONENT: ChartsComponent.vue ==========
 * Purpose: Hiển thị biểu đồ thống kê (pie chart & bar chart) cho dashboard
 * 
 * Features:
 *   - Biểu đồ tròn: Phân bổ thị trường xuất khẩu
 *   - Biểu đồ cột: Sản lượng theo loại cây
 *   - Responsive layout cho desktop/mobile
 * 
 * Related Files:
 *   - src/views/QuanLyView.vue - Parent component
 */

// ========== IMPORTS ==========
// Import computed từ Vue 3 Composition API để tính toán style động
import { computed } from 'vue';

// ========== DATA: Thị trường xuất khẩu ==========
/**
 * Mock data cho biểu đồ tròn (conic-gradient)
 * Mỗi item chứa: label (tên thị trường), value (%), color (hex)
 */
const exportData = [
      { label: 'Trung Quốc', value: 45, color: '#ef4444' }, // red-500
      { label: 'Hoa Kỳ', value: 25, color: '#3b82f6' },     // blue-500
      { label: 'Châu Âu', value: 20, color: '#10b981' },    // emerald-500
      { label: 'Khác', value: 10, color: '#f59e0b' },       // amber-500
];

// ========== COMPUTED ==========
/**
 * Computed: Tính toán style gradient conic cho biểu đồ tròn
 * Chuyển đổi data array thành conic-gradient string
 * VD: "red 0deg 162deg, blue 162deg 252deg, ..."
 */
const pieChartStyle = computed(() => {
      // Theo dõi angle hiện tại để tính segment tiếp theo
      let currentAngle = 0;
      // Map mỗi item thành phần gradient
      const gradientParts = exportData.map(item => {
            // Góc bắt đầu segment hiện tại
            const start = currentAngle;
            // Góc kết thúc = bắt đầu + (giá trị / 100) * 360 độ
            const end = currentAngle + (item.value / 100) * 360;
            // Cập nhật currentAngle cho item tiếp theo
            currentAngle = end;
            // Trả về chuỗi gradient cho segment này
            return `${item.color} ${start}deg ${end}deg`;
      });
      // Trả về object style với conic-gradient background
      return {
            background: `conic-gradient(${gradientParts.join(', ')})`
      };
});

// ========== DATA: Loại cây trồng ==========
/**
 * Mock data cho biểu đồ cột (bar chart)
 * Mỗi item chứa: label (tên cây), value (sản lượng %), color (Tailwind class)
 */
const cropData = [
      { label: 'Lúa', value: 85, color: 'bg-yellow-400' },
      { label: 'Xoài', value: 65, color: 'bg-green-500' },
      { label: 'Thanh Long', value: 45, color: 'bg-red-500' },
      { label: 'Sầu Riêng', value: 30, color: 'bg-orange-400' },
];
</script>

<template>
      <!-- Container chính: flex column, chiếm hết không gian và chia 2 phần bằng -->
      <!-- h-full = 100% height, gap-5 = khoảng cách giữa 2 biểu đồ -->
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
            <div class="flex flex-col flex-1 p-4 bg-white border border-white shadow-md rounded-xl">
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
      </div>
</template>