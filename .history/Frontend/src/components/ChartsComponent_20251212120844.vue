<script setup>
import { computed } from 'vue';

// Mock data cho biểu đồ tròn (Thị trường xuất khẩu)
const exportData = [
      { label: 'Trung Quốc', value: 45, color: '#ef4444' }, // red-500
      { label: 'Hoa Kỳ', value: 25, color: '#3b82f6' },     // blue-500
      { label: 'Châu Âu', value: 20, color: '#10b981' },    // emerald-500
      { label: 'Khác', value: 10, color: '#f59e0b' },       // amber-500
];

// Tính toán style background cho biểu đồ tròn
const pieChartStyle = computed(() => {
      let currentAngle = 0;
      const gradientParts = exportData.map(item => {
            const start = currentAngle;
            const end = currentAngle + (item.value / 100) * 360;
            currentAngle = end;
            return `${item.color} ${start}deg ${end}deg`;
      });
      return {
            background: `conic-gradient(${gradientParts.join(', ')})`
      };
});

// Mock data cho biểu đồ cột (Loại cây trồng - đơn vị ha)
const cropData = [
      { label: 'Lúa', value: 85, color: 'bg-yellow-400' },
      { label: 'Xoài', value: 65, color: 'bg-green-500' },
      { label: 'Thanh Long', value: 45, color: 'bg-red-500' },
      { label: 'Sầu Riêng', value: 30, color: 'bg-orange-400' },
];
</script>

<template>
      <div class="flex flex-col gap-5 h-full">
            <!-- Biểu đồ tròn: Thị trường xuất khẩu -->
            <div class="bg-white p-4 rounded-xl shadow-md border border-white flex-1 flex flex-col">
                  <h3 class="text-xs font-bold text-slate-500 uppercase mb-4 tracking-wider">
                        <i class="fas fa-globe-americas mr-1"></i> Thị trường Xuất khẩu
                  </h3>

                  <div class="flex items-center gap-4 flex-1 justify-center">
                        <!-- Pie Chart Circle -->
                        <div class="relative w-28 h-28 rounded-full shadow-inner flex-shrink-0" :style="pieChartStyle">
                              <div class="absolute inset-0 m-auto bg-white w-14 h-14 rounded-full shadow-sm"></div>
                        </div>

                        <!-- Legend -->
                        <div class="space-y-2 min-w-[100px]">
                              <div v-for="item in exportData" :key="item.label"
                                    class="flex items-center justify-between text-xs">
                                    <div class="flex items-center gap-2">
                                          <span class="w-2.5 h-2.5 rounded-full shadow-sm"
                                                :style="{ backgroundColor: item.color }"></span>
                                          <span class="text-slate-600 font-medium">{{ item.label }}</span>
                                    </div>
                                    <span class="font-bold text-slate-800">{{ item.value }}%</span>
                              </div>
                        </div>
                  </div>
            </div>

            <!-- Biểu đồ cột: Loại cây trồng -->
            <div class="bg-white p-4 rounded-xl shadow-md border border-white flex-1 flex flex-col">
                  <h3 class="text-xs font-bold text-slate-500 uppercase mb-4 tracking-wider">
                        <i class="fas fa-seedling mr-1"></i> Sản lượng Cây trồng
                  </h3>

                  <div class="flex items-end justify-around gap-3 flex-1 pb-2 border-b border-slate-100">
                        <div v-for="crop in cropData" :key="crop.label"
                              class="flex flex-col items-center gap-1 w-full group h-full justify-end">
                              <div
                                    class="text-[10px] font-bold text-slate-600 opacity-0 group-hover:opacity-100 transition-opacity -mb-1">
                                    {{ crop.value }}</div>
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