<script setup>
/**
 * ========== COMPONENT: ProductList.vue ==========
 * Purpose: Hiển thị danh sách sản phẩm (nông sản) sau lọc & tìm kiếm
 * 
 * Features:
 *   - Danh sách items với scroll dọc
 *   - Empty state khi không có kết quả
 *   - Emit select event khi click item
 * 
 * Props:
 *   - items (Array): Danh sách sản phẩm
 *   - getClassTrangThai (Function): Hàm lấy class CSS theo trạng thái
 *   - getTextTrangThai (Function): Hàm lấy text trạng thái
 * 
 * Emits:
 *   - select (Object): Phát khi user click vào item
 */

// ========== IMPORTS ==========
import HomeListItem from './HomeListItem.vue'; // Component item trong danh sách

// ========== PROPS & EMITS ==========
// Props: Nhận dữ liệu từ parent
const props = defineProps({
     // items: Danh sách sản phẩm cần hiển thị
     items: {
          type: Array,
          default: () => []
     },
     // getClassTrangThai: Hàm lấy class CSS theo trạng thái
     getClassTrangThai: {
          type: Function,
          required: true
     },
     // getTextTrangThai: Hàm lấy text trạng thái
     getTextTrangThai: {
          type: Function,
          required: true
     }
});

// Emits: Phát sự kiện select lên parent
const emit = defineEmits(['select']);

// ========== METHODS ==========
/**
 * Handler: Xử lý khi user chọn một item
 * @param {Object} item - Item được chọn
 */
const handleSelectItem = (item) => {
     // Phát event select lên parent
     emit('select', item);
};
</script>

<template>
     <!-- Item list container: cuộn dọc để xem nhiều item -->
     <div class="flex-grow p-3 space-y-2 overflow-y-auto">

          <!-- List wrapper: chứa tất cả item hoặc empty state -->
          <ul class="space-y-2">
               <!-- Render từng item trong danh sách -->
               <HomeListItem
                    v-for="item in items"
                    :key="item.id"
                    :item="item"
                    :getClassTrangThai="getClassTrangThai"
                    :getTextTrangThai="getTextTrangThai"
                    @select="handleSelectItem" />
          </ul>

          <!-- Empty state: hiển thị khi không có kết quả -->
          <div v-if="items.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
               <!-- Icon: khó chịu -->
               <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 mb-2 opacity-30" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                         d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
               </svg>
               <!-- Message: thông báo không tìm thấy -->
               <p class="text-sm">Không tìm thấy nông sản nào</p>
          </div>
     </div>
</template>

<style scoped>
/**
 * ========== STYLES ==========
 * Product list component styling
 * 
 * Note: Styles được định nghĩa inline trong template bằng Tailwind classes
 * để dễ quản lý layout responsive
 */

/* Flex-grow: chiếm hết không gian còn lại */
/* overflow-y-auto: cho phép cuộn dọc */
/* space-y-2: khoảng cách giữa các item */
</style>
