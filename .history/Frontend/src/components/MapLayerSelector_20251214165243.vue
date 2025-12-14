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
      <!-- Layer selector container: Tailwind positioning & flexbox -->
      <div class="absolute top-2.5 right-2.5 z-[999] flex flex-col items-end gap-2">
            <!-- Nút toggle dropdown: nhấn để mở/đóng menu -->
            <button @click="showDropdown = !showDropdown"
                  class="flex items-center justify-center w-10 h-10 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow"
                  :title="'Chọn lớp bản đồ: ' + (currentLayer === 'satellite' ? 'Ảnh vệ tinh' : 'Bản đồ đường phố')">
                  <!-- Icon layers: biểu tượng các lớp -->
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-700" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.5a2 2 0 00-1 .267V5a2 2 0 10-4 0v5.75a2 2 0 00-1-.267H5a2 2 0 00-2 2v4a2 2 0 002 2z" />
                  </svg>
            </button>

            <!-- Dropdown menu: hiển thị khi showDropdown = true -->
            <transition name="fade">
                  <div v-if="showDropdown" class="bg-white rounded-lg shadow-lg overflow-hidden w-[180px] z-50">
                        <!-- Option 1: Ảnh vệ tinh (Satellite) -->
                        <button @click="selectLayer('satellite')" :class="[
                              'w-full px-3 py-2.5 flex items-center gap-2 text-sm text-gray-600 hover:bg-blue-50 hover:text-green-700 transition-colors',
                              currentLayer === 'satellite' && 'bg-teal-100 text-green-700 font-semibold border-b border-gray-200'
                        ]">
                              <!-- Icon: biểu tượng vệ tinh -->
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor"
                                    viewBox="0 0 20 20">
                                    <path fill-rule="evenodd"
                                          d="M5 2a1 1 0 011 1v1h1V3a1 1 0 112 0v1h1V3a1 1 0 112 0v1h1V3a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v1h1a1 1 0 110 2h-1v1h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1h-1v1a1 1 0 11-2 0v-1H6v1a1 1 0 11-2 0v-1H3a2 2 0 01-2-2v-2H0a1 1 0 110-2h1V9H0a1 1 0 110-2h1V6H0a1 1 0 110-2h1V4a2 2 0 012-2h2V3a1 1 0 011-1zm9 5a1 1 0 100-2 1 1 0 000 2z"
                                          clip-rule="evenodd" />
                              </svg>
                              <!-- Text: Ảnh vệ tinh -->
                              <span>Ảnh vệ tinh</span>
                        </button>

                        <!-- Option 2: Bản đồ đường phố (Street Map) -->
                        <button @click="selectLayer('street')" :class="[
                              'w-full px-3 py-2.5 flex items-center gap-2 text-sm text-gray-600 hover:bg-blue-50 hover:text-green-700 transition-colors',
                              currentLayer === 'street' && 'bg-teal-100 text-green-700 font-semibold border-t border-gray-200'
                        ]">
                              <!-- Icon: biểu tượng bản đồ -->
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor"
                                    viewBox="0 0 20 20">
                                    <path
                                          d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10.5A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10.5A7.968 7.968 0 0014.5 4c-1.669 0-3.218.51-4.5 1.385A7.968 7.968 0 009 4.804z" />
                              </svg>
                              <!-- Text: Bản đồ đường phố -->
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
