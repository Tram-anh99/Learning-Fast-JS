<script setup>
/**
 * ========== COMPONENT: FilterTabs.vue ==========
 * Purpose: Horizontal tab filter for product list - Filter by status categories
 * Allows user to filter products: All, Cultivating, Harvesting, Harvested
 * 
 * Architecture:
 *   - Parent: Home page or product list container
 *   - Child: None
 *   - Communication: Props in, emit event on filter change
 * 
 * Features:
 *   - 4 filter options: Tất cả, Canh tác, Thu hoạch, Đã thu hoạch
 *   - Highlight active filter with green gradient background
 *   - Horizontal scroll if space limited
 *   - Smooth transition animations (200ms)
 *   - Click scale feedback (active:scale-95) for button press
 * 
 * Props:
 *   - activeFilter (String): Currently active filter value ('all', 'canh_tac', 'thu_hoach', 'da_thu_hoach')
 * 
 * Emits:
 *   - filterChange (String): Filter value when user clicks tab
 */

// ========== IMPORTS ==========
// (No imports needed - using only Vue template features)

// ========== PROPS & EMITS ==========
// Define props for tracking active filter state
const props = defineProps({
  // activeFilter: Currently selected filter value
  // Type: String
  // Default: 'all' (show all products initially)
  // Values: 'all' | 'canh_tac' | 'thu_hoach' | 'da_thu_hoach'
  activeFilter: {
    type: String,
    default: 'all'
  }
});

// Emit custom events to parent component
const emit = defineEmits(
  // filterChange: Emitted when user clicks a filter tab
  // Payload: filterValue (string) - the value of selected filter option
  ['filterChange']
);

// ========== DATA ==========
/**
 * filterOptions: Array of available filter choices
 * Structure: Array<{value: string, label: string}>
 * 
 * Used for:
 *   1. Rendering filter tab buttons
 *   2. Matching clicked button to filter value
 *   3. Display labels (Vietnamese text)
 * 
 * Values correspond to product status:
 *   - 'all': Show all products regardless of status
 *   - 'canh_tac': Show products currently being cultivated
 *   - 'thu_hoach': Show products ready for harvest
 *   - 'da_thu_hoach': Show products already harvested
 */
const filterOptions = [
  { value: 'all', label: 'Tất cả' },              // All products
  { value: 'canh_tac', label: 'Canh tác' },       // Cultivating
  { value: 'thu_hoach', label: 'Thu hoạch' },     // Harvesting
  { value: 'da_thu_hoach', label: 'Đã thu hoạch' } // Harvested
];

// ========== METHODS ==========
/**
 * handleFilterClick: Handle tab click event
 * Parameters:
 *   @param {string} filterValue - The filter value from clicked option
 * Behavior:
 *   1. Receive filter value from event handler
 *   2. Emit 'filterChange' event to parent with this value
 *   3. Parent updates activeFilter prop
 *   4. Component re-renders with new active state
 */
const handleFilterClick = (filterValue) => {
  // Emit event to parent component
  // Parent responsibility: update activeFilter and filter product list
  emit('filterChange', filterValue);
};
</script>

<template>
      <!-- Filter tabs container: cuộn ngang nếu cần -->
      <div
            class="flex flex-shrink-0 gap-2 p-3 overflow-x-auto border-b border-slate-200/50 bg-gradient-to-r from-slate-50 to-blue-50">

            <!-- Tab button: từng tab filter -->
            <button v-for="option in filterOptions" :key="option.value" @click="handleFilterClick(option.value)" :class="[
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
