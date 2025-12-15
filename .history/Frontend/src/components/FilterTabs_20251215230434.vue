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
      <!-- ========== FILTER TABS CONTAINER ========== -->
      <!-- Tab bar container: flex layout with horizontal scroll capability -->
      <!-- flex-shrink-0 = doesn't shrink below content size (prevents compression) -->
      <!-- gap-2 = 8px spacing between tab buttons -->
      <!-- p-3 = 12px padding all around -->
      <!-- overflow-x-auto = allow horizontal scrolling if tabs exceed width -->
      <!-- border-b border-slate-200/50 = subtle gray bottom border for tab bar separation -->
      <!-- bg-gradient-to-r from-slate-50 to-blue-50 = subtle gradient background (white to light blue) -->
      <div
            class="flex flex-shrink-0 gap-2 p-3 overflow-x-auto border-b border-slate-200/50 bg-gradient-to-r from-slate-50 to-blue-50">

            <!-- ========== TAB BUTTON LOOP ========== -->
            <!-- v-for: Loop through filterOptions array -->
            <!-- :key: Unique identifier (option.value) for Vue's list rendering -->
            <!-- @click: Handle click by emitting filterChange event with filter value -->
            <!-- :class: Dynamic styling based on selected state -->
            <button v-for="option in filterOptions" :key="option.value" @click="handleFilterClick(option.value)" :class="[
                  // Base tab button classes: Always applied
                  'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200 active:scale-95 whitespace-nowrap',
                  // Conditional styling based on activeFilter value
                  activeFilter === option.value
                        // Active tab styling:
                        // bg-gradient-to-r from-green-600 to-emerald-700 = green gradient (left green-600 to right emerald-700)
                        // text-white = white text for good contrast on green
                        // shadow-lg = large shadow for elevation/depth
                        // flex-1 = take full available space (grow to fill)
                        ? 'bg-gradient-to-r from-green-600 to-emerald-700 text-white shadow-lg flex-1'
                        // Inactive tab styling:
                        // text-gray-600 = medium gray text
                        // hover:bg-white/50 = slight white overlay on hover for lightness
                        // flex-1 = take full available space (grow to fill)
                        : 'text-gray-600 hover:bg-white/50 flex-1'
            ]">
                  <!-- ========== TAB LABEL ========== -->
                  <!-- Display the filter option label (Vietnamese text) -->
                  <!-- Label from filterOptions: 'Tất cả', 'Canh tác', 'Thu hoạch', 'Đã thu hoạch' -->
                  {{ option.label }}
            </button>
      </div>
</template>

<style scoped>
/* FilterTabs uses Tailwind CSS classes directly in template */
</style>
