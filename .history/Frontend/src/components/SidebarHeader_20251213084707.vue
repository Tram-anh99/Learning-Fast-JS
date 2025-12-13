<script setup>
/**
 * ========== COMPONENT: SidebarHeader.vue ==========
 * Purpose: Header của sidebar - hiển thị search khi danh sách, back button khi chi tiết
 * 
 * Features:
 *   - Search input cho tìm kiếm nông sản (khi xem danh sách)
 *   - Back button (khi xem chi tiết)
 * 
 * Props:
 *   - isDetailMode (boolean): true = xem chi tiết, false = xem danh sách
 *   - searchQuery (string): Giá trị search input
 * 
 * Emits:
 *   - update:searchQuery: Cập nhật từ khóa tìm kiếm
 *   - back: Quay lại danh sách
 */

// ========== IMPORTS ==========
// (No additional imports needed - using only Vue core features)

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
     }
});

// Emits: Phát sự kiện lên parent
const emit = defineEmits(['update:searchQuery', 'back']);
</script>

<template>
     <!-- Header wrapper: container chính của header -->
     <header class="sidebar-header" :class="{ 'detail-mode': isDetailMode }">

          <!-- Search view: hiển thị khi xem danh sách (isDetailMode = false) -->
          <div v-if="!isDetailMode" class="w-full">
               <!-- Search container: background xanh -->
               <div class="p-4 bg-green-900 rounded-t-2xl">
                    <!-- Search input wrapper: relative positioning cho icon -->
                    <div class="relative">
                         <!-- Icon search: SVG định vị tuyệt đối bên trái -->
                         <svg
                              class="absolute w-5 h-5 text-green-300 -translate-y-1/2 pointer-events-none left-3 top-1/2"
                              fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <!-- Icon path: kính lúp -->
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                   d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                         </svg>

                         <!-- Input search: v-model binding với searchQuery -->
                         <input
                              :value="searchQuery"
                              @input="$emit('update:searchQuery', $event.target.value)"
                              type="text"
                              placeholder="Tìm nông sản..."
                              class="w-full py-2 pl-10 pr-3 text-white placeholder-green-300 transition-colors bg-green-800 rounded-lg focus:outline-none focus:bg-green-700 focus:ring-1 focus:ring-green-400">
                    </div>
               </div>
          </div>

          <!-- Detail view header: hiển thị khi xem chi tiết (isDetailMode = true) -->
          <div v-else class="header-content detail">
               <!-- Back button: nút quay lại danh sách -->
               <button
                    @click="$emit('back')"
                    class="p-2 transition-colors rounded-lg hover:bg-white/20"
                    title="Quay lại danh sách">
                    <!-- Icon back: mũi tên sang trái -->
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-white" fill="none"
                         viewBox="0 0 24 24" stroke="currentColor">
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
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
