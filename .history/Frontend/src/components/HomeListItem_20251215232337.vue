<script setup>
/**
 * ========== COMPONENT: HomeListItem.vue ==========
 * Purpose: Item trong danh sách tra cứu nông sản
 * Related Files:
 *   - src/composables/useHome.js (Logic & state)
 *   - src/composables/statusHelpers.js (Status helpers)
 *   - src/views/HomeView.vue (Main view)
 */

import { getClassTrangThai, getTextTrangThai } from '../composables/statusHelpers';

defineProps({
      item: {
            type: Object,
            required: true
      }
});

defineEmits(['select']);
</script>

<template>
      <li @click="$emit('select', item)"
            class="group p-3 rounded-xl shadow-sm flex items-center gap-3 cursor-pointer transition-all duration-200 hover:shadow-md hover:-translate-y-0.5 active:scale-[0.98]" style="background-color: #fbfced;">
            <!-- Ảnh đại diện -->
            <div class="w-14 h-14 rounded-lg bg-cover bg-center flex-shrink-0"
                  :style="{ backgroundImage: `url(${item.anh})` }"></div>

            <!-- Thông tin -->
            <div class="flex-grow min-w-0">
                  <div class="font-bold text-sm truncate transition-colors" style="color: #24504b;">
                        {{ item.ten }}
                  </div>
                  <div class="text-xs flex items-center gap-1 mt-1" style="color: #6b7280;">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" viewBox="0 0 20 20" fill="currentColor">
                              <path fill-rule="evenodd"
                                    d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"
                                    clip-rule="evenodd" />
                        </svg>
                        <span class="truncate">{{ item.chungNhan }}</span>
                  </div>
            </div>

            <!-- Badge trạng thái -->
            <div
                  :class="`${getClassTrangThai(item.trangThai)} text-white text-xs px-2 py-1 rounded-md font-semibold whitespace-nowrap flex-shrink-0`">
                  {{ getTextTrangThai(item.trangThai) }}
            </div>
      </li>
</template>
