<script setup>
/**
 * ========== COMPONENT: SidebarHeader.vue ==========
 * Purpose: Header của sidebar - hiển thị search khi danh sách, back button khi chi tiết
 * 
 * Features:
 *   - Search input cho tìm kiếm nông sản (khi xem danh sách)
 *   - Autocomplete suggestions khi user gõ
 *   - Back button (khi xem chi tiết)
 *   - QR Scanner button
 * 
 * Props:
 *   - isDetailMode (boolean): true = xem chi tiết, false = xem danh sách
 *   - searchQuery (string): Giá trị search input
 *   - suggestions (Array): Danh sách gợi ý autocomplete
 * 
 * Emits:
 *   - update:searchQuery: Cập nhật từ khóa tìm kiếm
 *   - selectSuggestion: Chọn một gợi ý
 *   - back: Quay lại danh sách
 *   - scanQR: Nhấn nút scan QR
 */

// ========== IMPORTS ==========
import { ref } from 'vue'; // Vue ref hook

// ========== PROPS & EMITS ==========
// Props: Nhận dữ liệu từ parent
const props = defineProps({
      // isDetailMode: Chế độ chi tiết hay danh sách
      isDetailMode: {
            type: Boolean,
            default: false
      },
      // searchQuery: Từ khóa tìm kiếm hiện tại
      searchQuery: {
            type: String,
            default: ''
      },
      // suggestions: Danh sách gợi ý autocomplete
      suggestions: {
            type: Array,
            default: () => []
      }
});

// Emits: Phát sự kiện lên parent
const emit = defineEmits(['update:searchQuery', 'selectSuggestion', 'back', 'scanQR']);

// ========== STATE ==========
// State: Điều khiển hiển thị/ẩn danh sách gợi ý
const showSuggestions = ref(false);

// ========== METHODS ==========
/**
 * Handler: Xử lý khi user chọn một gợi ý từ autocomplete
 * @param {Object} suggestion - Gợi ý được chọn
 */
const selectSuggestion = (suggestion) => {
     // Phát event selectSuggestion lên parent
     emit('selectSuggestion', suggestion);
     // Đóng danh sách gợi ý
     showSuggestions.value = false;
};

/**
 * Handler: Xử lý khi input được focus
 * Hiển thị danh sách gợi ý nếu có
 */
const handleInputFocus = () => {
     if (props.suggestions.length > 0) {
          showSuggestions.value = true;
     }
};

/**
 * Handler: Xử lý khi input mất focus
 * Ẩn danh sách gợi ý sau 200ms
 */
const handleInputBlur = () => {
     // Delay để cho phép click vào suggestion trước
     setTimeout(() => {
          showSuggestions.value = false;
     }, 200);
};
</script>

<template>
      <!-- Header wrapper: container chính của header -->
      <header class="sidebar-header" :class="{ 'detail-mode': isDetailMode }">

            <!-- Search view: hiển thị khi xem danh sách (isDetailMode = false) -->
            <div v-if="!isDetailMode" class="w-full">
                  <!-- Search container: background xanh -->
                  <div class="p-4 bg-green-900 rounded-t-2xl">
                        <!-- Search input wrapper: relative positioning cho icon -->
                        <div class="flex gap-2">
                              <!-- Search input section: phần lớn -->
                              <div class="relative flex-1">
                                    <!-- Icon search: SVG định vị tuyệt đối bên trái -->
                                    <svg class="absolute w-5 h-5 text-green-300 -translate-y-1/2 pointer-events-none left-3 top-1/2"
                                          fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                          <!-- Icon path: kính lúp -->
                                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                                    </svg>

                                    <!-- Input search: v-model binding với searchQuery -->
                                    <input
                                          :value="searchQuery"
                                          @input="$emit('update:searchQuery', $event.target.value)"
                                          @focus="handleInputFocus"
                                          @blur="handleInputBlur"
                                          type="text"
                                          placeholder="Tìm nông sản..."
                                          autocomplete="off"
                                          class="w-full py-2 pl-10 pr-3 text-white placeholder-green-300 transition-colors bg-green-800 rounded-lg focus:outline-none focus:bg-green-700 focus:ring-1 focus:ring-green-400">

                                    <!-- Autocomplete suggestions dropdown: hiển thị khi có gợi ý -->
                                    <transition name="slide">
                                          <div v-if="showSuggestions && suggestions.length > 0"
                                                class="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-48 overflow-y-auto z-10">
                                                <!-- Suggestion items: từng gợi ý -->
                                                <button
                                                      v-for="(suggestion, index) in suggestions"
                                                      :key="index"
                                                      @click="selectSuggestion(suggestion)"
                                                      class="w-full px-3 py-2 text-left text-sm text-gray-800 hover:bg-green-50 border-b border-gray-100 last:border-b-0 transition-colors">
                                                      <!-- Suggestion text: tên + mã -->
                                                      <div class="font-medium">{{ suggestion.ten }}</div>
                                                      <div class="text-xs text-gray-500">{{ suggestion.ma }}</div>
                                                </button>
                                          </div>
                                    </transition>
                              </div>

                              <!-- QR Scanner button: nút quét mã QR -->
                              <button
                                    @click="$emit('scanQR')"
                                    title="Quét mã QR"
                                    class="flex items-center justify-center px-3 py-2 text-white transition-colors bg-green-700 rounded-lg hover:bg-green-600">
                                    <!-- Icon QR: biểu tượng QR code -->
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor"
                                          viewBox="0 0 20 20">
                                          <path fill-rule="evenodd"
                                                d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zm10-9a2 2 0 110 4 2 2 0 010-4zM2 15a1 1 0 101 2h1a1 1 0 100-2H3z"
                                                clip-rule="evenodd" />
                                    </svg>
                              </button>
                        </div>
                  </div>
            </div>

            <!-- Detail view header: hiển thị khi xem chi tiết (isDetailMode = true) -->
            <div v-else class="header-content detail">
                  <!-- Back button: nút quay lại danh sách -->
                  <button @click="$emit('back')" class="p-2 transition-colors rounded-lg hover:bg-white/20"
                        title="Quay lại danh sách">
                        <!-- Icon back: mũi tên sang trái -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none"
                              viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 19l-7-7 7-7" />
                        </svg>
                  </button>

                  <!-- Title: "Thông tin Chi tiết" -->
                  <h3 class="font-bold text-white">Thông tin Chi tiết</h3>
            </div>
      </header>
</template>

<style scoped>
/**
 * ========== STYLES ==========
 * Sidebar header component styling
 */

/* Header: container chính */
.sidebar-header {
      /* Background: gradient từ xanh đậm sang xanh nhạt */
      background: linear-gradient(to right, #1b4332, #2d6a4f);
      /* Text color: trắng */
      color: white;
      /* Display: flex layout */
      display: flex;
      /* Align items: căn giữa theo chiều dọc */
      align-items: center;
      /* Transition: hoạt ảnh mượt mà */
      transition: all 0.3s;
}

/* Detail mode: chế độ chi tiết */
.sidebar-header.detail-mode {
      /* Padding: xóa padding khi ở detail mode */
      padding: 0;
}

/* Header content: chứa back button + title */
.header-content {
      /* Width: chiếm toàn bộ chiều rộng */
      width: 100%;
      /* Display: flex layout */
      display: flex;
      /* Justify content: căn đều các item */
      justify-content: space-between;
      /* Align items: căn giữa theo chiều dọc */
      align-items: center;
      /* Padding: khoảng cách bên trong */
      padding: 16px 20px;
}

/* Header content detail mode: khi ở chi tiết */
.header-content.detail {
      /* Justify content: căn từ trái sang phải */
      justify-content: flex-start;
      /* Gap: khoảng cách giữa icon & text */
      gap: 12px;
      /* Padding: nhỏ hơn để gọn gàng */
      padding: 12px 16px;
}

/* Title: tiêu đề "Thông tin Chi tiết" */
.header-content.detail h3 {
      /* Margin: xóa margin mặc định */
      margin: 0;
      /* Font size: 1rem */
      font-size: 1rem;
}
</style>
