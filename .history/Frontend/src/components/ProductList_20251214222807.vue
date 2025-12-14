<script setup>
/**
 * ========== COMPONENT: ProductList.vue ==========
 * Purpose: Display filtered product list with vertical scrolling
 */

import HomeListItem from './HomeListItem.vue';
import { getStatusBadge } from '../composables/statusHelpers';

const props = defineProps({
      items: {
            type: Array,
            default: () => []
      }
});

const emit = defineEmits(['select']);

const getClassTrangThai = (status) => getStatusBadge(status).class + " text-white";
const getTextTrangThai = (status) => getStatusBadge(status).text;

const handleSelectItem = (item) => {
      emit('select', item);
};
</script>

<template>
      <div class="flex-grow p-3 space-y-2 overflow-y-auto">
            <ul class="space-y-2">
                  <HomeListItem v-for="item in items" :key="item.id" :item="item" :getClassTrangThai="getClassTrangThai"
                        :getTextTrangThai="getTextTrangThai" @select="handleSelectItem" />
            </ul>

            <div v-if="items.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 mb-2 opacity-30" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p class="text-sm">Không tìm thấy nông sản nào</p>
            </div>
      </div>
</template>

<style scoped>
/* ProductList uses Tailwind CSS classes directly in template */
</style>
