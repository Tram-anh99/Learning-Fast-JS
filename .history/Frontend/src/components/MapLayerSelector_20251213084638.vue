<script setup>
/**
 * ========== COMPONENT: MapLayerSelector.vue ==========
 * Purpose: Dropdown selector để thay đổi lớp tile của bản đồ (Satellite/Street)
 * Position: Góc trên bên phải của bản đồ
 * 
 * Props:
 *   - currentLayer (string): Lớp tile hiện tại ('satellite' hoặc 'street')
 * 
 * Emits:
 *   - changeLayer (string): Phát khi user chọn lớp mới
 */

// ========== IMPORTS ==========
import { ref } from 'vue'; // Vue ref hook

// ========== PROPS & EMITS ==========
// Props: Nhận lớp tile hiện tại từ parent
const props = defineProps({
     currentLayer: {
          type: String,
          default: 'satellite'
     }
});

// Emits: Phát sự kiện changeLayer với tên lớp
const emit = defineEmits(['changeLayer']);

// ========== STATE ==========
// State: Điều khiển hiển thị/ẩn dropdown menu
const showDropdown = ref(false);

// ========== METHODS ==========
/**
 * Handler: Xử lý khi user chọn một lớp tile
 * @param {string} layer - Tên lớp ('satellite' hoặc 'street')
 */
const selectLayer = (layer) => {
     // Phát event 'changeLayer' lên parent
     emit('changeLayer', layer);
     // Đóng dropdown menu sau khi chọn
     showDropdown.value = false;
};
</script>

<template>
     <!-- Layer selector container: định vị tuyệt đối ở góc trên bên phải -->
     <div class="layer-selector">
          <!-- Nút toggle dropdown: nhấn để mở/đóng menu -->
          <button
               @click="showDropdown = !showDropdown"
               class="flex items-center justify-center w-10 h-10 transition-shadow bg-white rounded-lg shadow-md hover:shadow-lg"
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
               <div v-if="showDropdown" class="layer-dropdown">
                    <!-- Option 1: Ảnh vệ tinh (Satellite) -->
                    <button
                         @click="selectLayer('satellite')"
                         :class="['layer-option', { active: currentLayer === 'satellite' }]"
                         class="flex items-center gap-2">
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
                    <button
                         @click="selectLayer('street')"
                         :class="['layer-option', { active: currentLayer === 'street' }]"
                         class="flex items-center gap-2">
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
/**
 * ========== STYLES ==========
 * Layer selector component styling
 */

/* Container: định vị tuyệt đối */
.layer-selector {
     position: absolute;
     top: 10px;
     right: 10px;
     z-index: 999;
     display: flex;
     flex-direction: column;
     align-items: flex-end;
     gap: 8px;
}

/* Dropdown menu: hộp chứa các option */
.layer-dropdown {
     background: white;
     border-radius: 8px;
     box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
     overflow: hidden;
     min-width: 180px;
}

/* Option button: từng tùy chọn trong dropdown */
.layer-option {
     width: 100%;
     padding: 10px 12px;
     display: flex;
     align-items: center;
     gap: 8px;
     background: white;
     border: none;
     cursor: pointer;
     color: #4b5563;
     font-size: 0.875rem;
     transition: all 0.2s;
}

/* Hover state: đổi màu khi hover */
.layer-option:hover {
     background-color: #f0f4f8;
     color: #1b4332;
}

/* Active state: tùy chọn đang chọn */
.layer-option.active {
     background-color: #d1f2eb;
     color: #1b4332;
     font-weight: 600;
}

/* Separator: đường ngăn cách giữa các option */
.layer-option:not(:last-child) {
     border-bottom: 1px solid #e5e7eb;
}

/* Transition: animation mở/đóng dropdown */
.fade-enter-active,
.fade-leave-active {
     transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
     opacity: 0;
}
</style>
