<template>

  <div 
    class="absolute bottom-4 left-4 z-[9999] transition-all duration-300 ease-in-out"
    :class="isExpanded ? 'w-96' : 'w-auto'"
  >
    
    <button 
      @click="isExpanded = !isExpanded"
      class="flex items-center gap-2 p-2 mb-2 text-white transition bg-green-700 rounded-lg shadow-lg hover:bg-green-800"
      :class="{ 'rounded-b-none mb-0': isExpanded }"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z" />
      </svg>
      <span v-if="isExpanded" class="text-sm font-bold">Thống kê Vùng trồng</span>
    </button>

    <div 
      v-if="isExpanded"
      class="p-4 text-gray-800 border rounded-tl-none shadow-2xl bg-white/80 backdrop-blur-md rounded-xl border-white/50 animate-fade-in-up"
    >
      
      <div class="mb-4">
        <h4 class="mb-1 text-xs font-bold text-gray-600 uppercase">Sử dụng thuốc BVTV</h4>
        <div class="w-full h-32">
          <Bar :data="barData" :options="miniChartOptions" />
        </div>
      </div>

      <div class="flex items-center justify-between">
        <div class="w-24 h-24">
          <Doughnut :data="pieData" :options="miniPieOptions" />
        </div>
        <div class="flex-1 pl-4">
          <h4 class="mb-1 text-xs font-bold text-gray-600">Tỷ lệ phân bón</h4>
          <ul class="text-[10px] text-gray-500 space-y-1">
            <li class="flex items-center"><span class="w-2 h-2 mr-1 bg-blue-600 rounded-full"></span> Hữu cơ (45%)</li>
            <li class="flex items-center"><span class="w-2 h-2 mr-1 bg-teal-600 rounded-full"></span> Vô cơ (30%)</li>
            <li class="flex items-center"><span class="w-2 h-2 mr-1 rounded-full bg-lime-500"></span> Vi sinh (25%)</li>
          </ul>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>
/* Hiệu ứng trượt lên nhẹ */
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out;
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>