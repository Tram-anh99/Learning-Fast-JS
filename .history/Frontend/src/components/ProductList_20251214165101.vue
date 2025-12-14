<script setup>
/**
 * ========== COMPONENT: ProductList.vue ==========
 * Purpose: Display filtered product list with vertical scrolling
 * Renders HomeListItem components for each product
 * Shows empty state when no products found
 * 
 * Architecture:
 *   - Parent: Home page or filter container
 *   - Child: HomeListItem (item component, imported)
 *   - Communication: Props in, emit event on item selection
 * 
 * Features:
 *   - Dynamic product list rendering via v-for
 *   - Empty state with icon & message when items.length === 0
 *   - Vertical scroll (overflow-y-auto) for lists > screen height
 *   - Pass helper functions to child: getClassTrangThai, getTextTrangThai
 *   - Delegate item click to parent via select event
 * 
 * Props:
 *   - items (Array): Array of product objects to display
 *   - getClassTrangThai (Function): Returns CSS class based on product status
 *   - getTextTrangThai (Function): Returns Vietnamese text for product status
 * 
 * Emits:
 *   - select (Object): Product object when user clicks item
 */

// ========== IMPORTS ==========
// Import child component: HomeListItem - Renders individual product items in list
import HomeListItem from './HomeListItem.vue';

// ========== PROPS & EMITS ==========
// Define props received from parent component
const props = defineProps({
  // items: Array of product objects to render
  // Structure: Array<{id, name, status, image, ...other product properties}>
  // Used in v-for loop to render list items
  items: {
    type: Array,
    default: () => []  // Default to empty array if not provided
  },
  
  // getClassTrangThai: Function that returns CSS class based on product status
  // Parameters: @param {string} status - Product status string ('canh_tac', 'thu_hoach', 'da_thu_hoach')
  // Returns: {string} CSS class name (e.g., 'bg-blue-100 text-blue-700')
  // Usage: Apply status badge styling
  getClassTrangThai: {
    type: Function,
    required: true
  },
  
  // getTextTrangThai: Function that returns Vietnamese text for status
  // Parameters: @param {string} status - Product status string
  // Returns: {string} Vietnamese status label (e.g., 'Canh tác', 'Thu hoạch', 'Đã thu hoạch')
  // Usage: Display status badge text
  getTextTrangThai: {
    type: Function,
    required: true
  }
});

// Emit custom events to parent component
const emit = defineEmits(
  // select: Emitted when user clicks a product item
  // Payload: item (Object) - Full product object from items array
  ['select']
);

// ========== METHODS ==========
/**
 * handleSelectItem: Handler for when user clicks product item
 * Parameters:
 *   @param {Object} item - Product object from items array
 * Behavior:
 *   1. Receive item object from child component
 *   2. Emit 'select' event to parent with item data
 *   3. Parent responsible for routing/navigating to product detail
 */
const handleSelectItem = (item) => {
  // Emit select event with clicked product
  // Parent component will handle navigation or detail view
  emit('select', item);
};
</script>

<template>
  <!-- ========== ITEM LIST CONTAINER ========== -->
  <!-- Main list wrapper: flex-grow = expand to fill available space -->
  <!-- p-3 = 12px padding all around -->
  <!-- space-y-2 = 8px gap between each item -->
  <!-- overflow-y-auto = vertical scroll when list exceeds container height -->
  <div class="flex-grow p-3 space-y-2 overflow-y-auto">

    <!-- ========== LIST WRAPPER ========== -->
    <!-- UL element: semantic HTML for unordered list -->
    <!-- space-y-2 = 8px margin-bottom between list items -->
    <ul class="space-y-2">
      
      <!-- ========== ITEM LOOP ========== -->
      <!-- v-for: Loop through items array, render HomeListItem for each -->
      <!-- :key: Unique identifier (item.id) for Vue's list rendering and performance -->
      <!-- HomeListItem child component renders individual product card -->
      <HomeListItem
        v-for="item in items"
        :key="item.id"
        :item="item"
        :getClassTrangThai="getClassTrangThai"
        :getTextTrangThai="getTextTrangThai"
        @select="handleSelectItem"
      />
    </ul>

    <!-- ========== EMPTY STATE ========== -->
    <!-- Empty state container: Show when items list is empty -->
    <!-- v-if: Conditionally render only when items.length === 0 -->
    <!-- flex flex-col items-center justify-center = centered content -->
    <!-- py-8 = 32px vertical padding for vertical centering -->
    <!-- text-gray-500 = muted gray color for secondary content -->
    <div v-if="items.length === 0" class="flex flex-col items-center justify-center py-8 text-gray-500">
      
      <!-- ========== EMPTY STATE ICON ========== -->
      <!-- SVG sad face icon: symbolizes no results found -->
      <!-- xmlns, viewBox: SVG standard attributes -->
      <!-- w-12 h-12 = 48px x 48px icon size -->
      <!-- mb-2 = 8px bottom margin before message text -->
      <!-- opacity-30 = very faded icon (30% opacity) for subtle appearance -->
      <!-- stroke-currentColor = inherit text color (gray-500) for strokes -->
      <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12 mb-2 opacity-30" fill="none"
            viewBox="0 0 24 24" stroke="currentColor">
        <!-- Path 1: stroke-linecap="round" = rounded line ends -->
        <!-- stroke-linejoin="round" = rounded line joins -->
        <!-- stroke-width="2" = 2px line thickness -->
        <!-- d: SVG path data for sad face illustration -->
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      
      <!-- ========== EMPTY STATE MESSAGE ========== -->
      <!-- Message text: "Không tìm thấy nông sản nào" = No products found -->
      <!-- text-sm = 14px font size -->
      <p class="text-sm">Không tìm thấy nông sản nào</p>
    </div>
  </div>
</template>
