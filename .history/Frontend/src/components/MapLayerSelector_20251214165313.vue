<script setup>
/**
 * ========== COMPONENT: MapLayerSelector.vue ==========
 * Purpose: Dropdown selector to switch map tile layers (Satellite/Street/Hybrid)
 * Position: Top-right corner of map widget
 * Used by: MapComponent.vue to allow users to change base layer
 * 
 * Architecture:
 *   - Parent: MapComponent or map container
 *   - Child: None
 *   - Communication: Props in, emit event on layer selection
 * 
 * Features:
 *   - Toggle dropdown menu on button click
 *   - Two layer options: Satellite imagery (ảnh vệ tinh) and Street map (bản đồ đường phố)
 *   - Active state highlighting (background color changes for selected layer)
 *   - Smooth fade transition animation
 *   - SVG icons for visual representation
 * 
 * Props:
 *   - currentLayer (String): Currently selected layer ('satellite' | 'street')
 * 
 * Emits:
 *   - changeLayer (String): Layer name when user selects option
 */

// ========== IMPORTS ==========
// ref: Vue 3 Composition API for reactive state management
import { ref } from 'vue';

// ========== PROPS & EMITS ==========
// Define props for tracking current selected layer
const props = defineProps({
  // currentLayer: Currently displayed map tile layer
  // Type: String
  // Values: 'satellite' | 'street'
  // Default: 'satellite' (satellite imagery as default view)
  currentLayer: {
    type: String,
    default: 'satellite'
  }
});

// Emit custom events to parent component
const emit = defineEmits(
  // changeLayer: Emit when user selects a map layer
  // Payload: layer (string) - 'satellite' or 'street'
  // Parent responsibility: Update map tiles to new layer
  ['changeLayer']
);

// ========== STATE ==========
/**
 * showDropdown: Controls visibility of layer selection dropdown menu
 * Type: Ref<Boolean>
 * Initial: false (menu closed)
 * Usage: Toggle with button click, close after selection
 */
const showDropdown = ref(false);

// ========== METHODS ==========
/**
 * selectLayer: Handle map layer selection
 * Parameters:
 *   @param {string} layer - Selected layer value ('satellite' or 'street')
 * Behavior:
 *   1. Emit 'changeLayer' event to parent with selected layer
 *   2. Close dropdown menu after selection
 *   3. Parent component handles tile update
 */
const selectLayer = (layer) => {
  // Emit event to parent component
  // Parent responsibility: Update Leaflet tiles with new layer
  emit('changeLayer', layer);
  
  // Close dropdown menu after selection
  showDropdown.value = false;
};
</script>

<template>
  <!-- ========== LAYER SELECTOR CONTAINER ========== -->
  <!-- Main container: absolute positioning in top-right corner of parent (map) -->
  <!-- absolute top-2.5 right-2.5 = position 10px from top and right edges -->
  <!-- z-[999] = very high z-index to appear above map controls -->
  <!-- flex flex-col items-end gap-2 = vertical flex layout, items aligned right, 8px gap -->
  <div class="absolute top-2.5 right-2.5 z-[999] flex flex-col items-end gap-2">
    
    <!-- ========== TOGGLE BUTTON ========== -->
    <!-- Button: Opens/closes layer selector dropdown -->
    <!-- w-10 h-10 = 40px x 40px square button -->
    <!-- flex items-center justify-center = center icon inside button -->
    <!-- bg-white = white background -->
    <!-- rounded-lg = slightly rounded corners (lg = 8px border-radius) -->
    <!-- shadow-md = medium shadow for depth -->
    <!-- hover:shadow-lg = larger shadow on hover for interactive feedback -->
    <!-- transition-shadow = smooth animation for shadow changes -->
    <!-- @click: Toggle dropdown visibility -->
    <!-- :title: Tooltip text showing current layer name -->
    <button
      @click="showDropdown = !showDropdown"
      class="flex items-center justify-center w-10 h-10 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
      :title="'Chọn lớp bản đồ: ' + (currentLayer === 'satellite' ? 'Ảnh vệ tinh' : 'Bản đồ đường phố')"
    >
      <!-- Icon: layers = Material Symbol representing map layers/stacked content -->
      <!-- w-5 h-5 = 20px x 20px icon size -->
      <!-- text-gray-700 = dark gray icon color -->
      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <!-- SVG path: layers icon (3 overlapping rectangular shapes) -->
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.5a2 2 0 00-1 .267V5a2 2 0 10-4 0v5.75a2 2 0 00-1-.267H5a2 2 0 00-2 2v4a2 2 0 002 2z" />
      </svg>
    </button>

    <!-- ========== DROPDOWN MENU ========== -->
    <!-- Dropdown: Layer selection options list -->
    <!-- v-if: Conditionally render only when showDropdown === true -->
    <!-- transition name="fade": Apply fade animation on mount/unmount -->
    <!-- bg-white = white background -->
    <!-- rounded-lg = rounded corners (lg = 8px radius) -->
    <!-- shadow-lg = large shadow for elevation -->
    <!-- overflow-hidden = hide content overflow (for rounded corners) -->
    <!-- w-[180px] = fixed width 180px for layer option list -->
    <!-- z-50 = high z-index to appear above other elements -->
    <transition name="fade">
      <div v-if="showDropdown" class="bg-white rounded-lg shadow-lg overflow-hidden w-[180px] z-50">
        
        <!-- ========== OPTION 1: SATELLITE LAYER ========== -->
        <!-- Satellite option button: Switch to satellite imagery view -->
        <!-- w-full = full width (stretch to container) -->
        <!-- px-3 py-2.5 = 12px horizontal, 10px vertical padding -->
        <!-- flex items-center gap-2 = horizontal layout for icon + text -->
        <!-- text-sm = 14px font size -->
        <!-- text-gray-600 = medium gray text by default -->
        <!-- hover:bg-blue-50 = light blue background on hover -->
        <!-- hover:text-green-700 = change text to green on hover -->
        <!-- transition-colors = smooth animation for color changes -->
        <!-- :class: Dynamic styling based on currentLayer value -->
        <button
          @click="selectLayer('satellite')"
          :class="[
            'w-full px-3 py-2.5 flex items-center gap-2 text-sm text-gray-600 hover:bg-blue-50 hover:text-green-700 transition-colors',
            // Active state: When satellite is selected
            // bg-teal-100 = light teal/cyan background to highlight selection
            // text-green-700 = darker green text to indicate active state
            // font-semibold = slightly bolder text (600 weight)
            // border-b border-gray-200 = bottom border to separate options
            currentLayer === 'satellite' && 'bg-teal-100 text-green-700 font-semibold border-b border-gray-200'
          ]"
        >
          <!-- Satellite icon: SVG representing satellite/grid pattern -->
          <!-- w-4 h-4 = 16px x 16px icon size -->
          <!-- fill="currentColor" = inherit text color (gray-600 or green-700) -->
          <!-- viewBox="0 0 20 20" = SVG coordinate system -->
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <!-- SVG path: Grid pattern icon for satellite imagery -->
            <path fill-rule="evenodd"
                  d="M5 2a1 1 0 011 1v1h1V3a1 1 0 112 0v1h1V3a1 1 0 112 0v1h1V3a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v1h1a1 1 0 110 2h-1v1h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1h-1v1a1 1 0 11-2 0v-1H6v1a1 1 0 11-2 0v-1H3a2 2 0 01-2-2v-2H0a1 1 0 110-2h1V9H0a1 1 0 110-2h1V6H0a1 1 0 110-2h1V4a2 2 0 012-2h2V3a1 1 0 011-1zm9 5a1 1 0 100-2 1 1 0 000 2z"
                  clip-rule="evenodd" />
          </svg>
          <!-- Label: "Ảnh vệ tinh" = Satellite imagery -->
          <span>Ảnh vệ tinh</span>
        </button>

        <!-- ========== OPTION 2: STREET MAP LAYER ========== -->
        <!-- Street map option button: Switch to street/street map view -->
        <!-- Same styling as satellite option -->
        <!-- :class: Dynamic styling based on currentLayer value -->
        <button
          @click="selectLayer('street')"
          :class="[
            'w-full px-3 py-2.5 flex items-center gap-2 text-sm text-gray-600 hover:bg-blue-50 hover:text-green-700 transition-colors',
            // Active state: When street is selected
            // bg-teal-100 = light teal background
            // text-green-700 = darker green text
            // font-semibold = slightly bolder text
            // border-t border-gray-200 = top border to separate options
            currentLayer === 'street' && 'bg-teal-100 text-green-700 font-semibold border-t border-gray-200'
          ]"
        >
          <!-- Street map icon: SVG representing map/navigation -->
          <!-- w-4 h-4 = 16px x 16px icon size -->
          <!-- fill="currentColor" = inherit text color -->
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <!-- SVG path: Map icon for street/road maps -->
            <path
                  d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10.5A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10.5A7.968 7.968 0 0014.5 4c-1.669 0-3.218.51-4.5 1.385A7.968 7.968 0 009 4.804z" />
          </svg>
          <!-- Label: "Bản đồ đường phố" = Street map -->
          <span>Bản đồ đường phố</span>
        </button>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* Fade transition: animation mở/đóng dropdown */
.fade-enter-active,
.fade-leave-active {
      transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
      opacity: 0;
}
</style>
