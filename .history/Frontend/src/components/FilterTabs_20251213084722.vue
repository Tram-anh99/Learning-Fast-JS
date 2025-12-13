<script setup>
/**
 * ========== COMPONENT: FilterTabs.vue ==========
 * Purpose: Tabs filter để lọc danh sách theo trạng thái nông sản
 * 
 * Features:
 *   - 4 tab: Tất cả, Canh tác, Thu hoạch, Đã thu hoạch
 *   - Highlight tab đang chọn
 *   - Cuộn ngang nếu cần
 * 
 * Props:
 *   - activeFilter (string): Bộ lọc đang chọn ('all', 'canh_tac', 'thu_hoach', 'da_thu_hoach')
 * 
 * Emits:
 *   - filterChange (string): Phát khi user chọn tab khác
 */

// ========== IMPORTS ==========
// (No additional imports needed - using only Vue core features)

// ========== PROPS & EMITS ==========
// Props: Nhận bộ lọc hiện tại từ parent
const props = defineProps({
     // activeFilter: Bộ lọc đang hoạt động
     activeFilter: {
          type: String,
          default: 'all'
     }
});

// Emits: Phát sự kiện filterChange lên parent
const emit = defineEmits(['filterChange']);

// ========== FILTER OPTIONS ==========
// Danh sách các tùy chọn filter
const filterOptions = [
     { value: 'all', label: 'Tất cả' },
     { value: 'canh_tac', label: 'Canh tác' },
     { value: 'thu_hoach', label: 'Thu hoạch' },
     { value: 'da_thu_hoach', label: 'Đã thu hoạch' }
];

// ========== METHODS ==========
/**
 * Handler: Xử lý khi user nhấn vào một tab
 * @param {string} filterValue - Giá trị filter
 */
const handleFilterClick = (filterValue) => {
     // Phát event filterChange lên parent
     emit('filterChange', filterValue);
};
</script>

<template>
     <!-- Filter tabs container: cuộn ngang nếu cần -->
     <div
          class="flex flex-shrink-0 gap-2 p-3 overflow-x-auto border-b border-slate-200/50 bg-gradient-to-r from-slate-50 to-blue-50">

          <!-- Tab button: từng tab filter -->
          <button
               v-for="option in filterOptions"
               :key="option.value"
               @click="handleFilterClick(option.value)"
               :class="[
                    'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
                    activeFilter === option.value
                         ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
                         : 'text-gray-600 border-2 border-slate-300 hover:border-slate-400 hover:bg-white/50 flex-1'
               ]">
               <!-- Tab label: tên bộ lọc -->
               {{ option.label }}
          </button>
     </div>
</template>

<style scoped>
/**
 * ========== STYLES ==========
 * Filter tabs component styling
 * 
 * Note: Styles được định nghĩa inline trong template bằng :class bindings
 * (Tailwind utilities) để dễ quản lý trạng thái active/inactive
 */

/* Các style scoped khác nếu cần */
</style>
