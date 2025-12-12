<script setup>
/**
 * ========== COMPONENT: HomeListItem.vue ==========
 * Purpose: Item trong danh sách tra cứu nông sản
 * Related Files:
 *   - src/composables/useHome.js (Logic & state)
 *   - src/views/HomeView.vue (Main view)
 *   - src/assets/styles/tailwind.css (Global utilities)
 */

defineProps({
  item: {
    type: Object,
    required: true
  },
  getClassTrangThai: {
    type: Function,
    required: true
  },
  getTextTrangThai: {
    type: Function,
    required: true
  }
});

defineEmits(['select']);
</script>

<template>
  <li 
    @click="$emit('select', item)"
    class="group bg-white p-3 rounded-xl shadow-sm border border-gray-100 flex items-center gap-3 cursor-pointer transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 active:scale-[0.98]"
  >
    <!-- Ảnh đại diện -->
    <div 
      class="w-14 h-14 rounded-lg bg-cover bg-center flex-shrink-0"
      :style="{ backgroundImage: `url(${item.anh})` }"
    ></div>

    <!-- Thông tin -->
    <div class="flex-grow min-w-0">
      <div class="font-bold text-gray-800 text-sm truncate group-hover:text-green-700 transition-colors">
        {{ item.ten }}
      </div>
      <div class="text-xs text-gray-500 flex items-center gap-1 mt-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" />
        </svg>
        <span class="truncate">{{ item.chungNhan }}</span>
      </div>
    </div>

    <!-- Badge trạng thái -->
    <div 
      :class="`${getClassTrangThai(item.trangThai)} text-white text-xs px-2 py-1 rounded-md font-semibold whitespace-nowrap flex-shrink-0`"
    >
      {{ getTextTrangThai(item.trangThai) }}
    </div>
  </li>
</template>
