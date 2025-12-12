<script setup>
// Props nhận dữ liệu hoạt động và hàm lấy icon
const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  getActivityIcon: {
    type: Function,
    required: true
  }
});
</script>

<template>
  <!-- Thẻ hoạt động nhật ký -->
  <div class="group bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex items-start transition-all duration-200 hover:shadow-md active:scale-[0.98] cursor-pointer">
    
    <!-- Ô ngày tháng -->
    <div class="flex flex-col items-center justify-center flex-shrink-0 p-2 mr-4 border bg-slate-50 rounded-xl w-14 border-slate-100">
      <span class="text-xs font-bold text-red-500 uppercase">{{ item.dateMonth }}</span>
      <span class="text-2xl font-extrabold text-gray-700 leading-none mt-0.5">{{ item.dateDay }}</span>
    </div>

    <!-- Nội dung hoạt động -->
    <div class="flex-grow pt-1">
      <!-- Tiêu đề + Icon -->
      <div class="flex items-start justify-between">
        <h3 class="font-bold text-gray-800 text-[17px] leading-tight group-hover:text-green-700 transition-colors">
          {{ item.title }}
        </h3>
        <span class="ml-2 text-lg opacity-70">{{ getActivityIcon(item.type) }}</span>
      </div>

      <!-- Vị trí thửa đất -->
      <div class="flex items-center mt-2 text-sm font-medium text-gray-500">
        <svg xmlns="http://www.w3.org/2000/svg" class="flex-shrink-0 w-4 h-4 mr-1 text-green-500" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
        </svg>
        <span class="truncate">{{ item.field }}</span>
      </div>

      <!-- Chi tiết hoạt động -->
      <div class="mt-1 text-sm text-gray-600 pl-5 relative before:absolute before:left-2 before:top-2 before:w-1.5 before:h-1.5 before:bg-gray-300 before:rounded-full line-clamp-2">
        {{ item.details }}
      </div>
    </div>
  </div>
</template>
