<script setup>
/**
 * ========== VIEW: AboutView.vue ==========
 * Purpose: Trang Giới thiệu - Hiển thị thông tin về ứng dụng
 *
 * Architecture:
 *   - Static page với thông tin tổng quan
 *   - Không có dynamic state hoặc composables
 *
 * Features:
 *   - Giới thiệu ứng dụng VN-AgriTrace
 *   - Thông tin đội ngũ phát triển
 *   - Các tính năng chính
 *   - Liên hệ và hỗ trợ
 */

// ========== IMPORTS ==========
// (Không có imports cần thiết cho trang static này)

// ========== STATE ==========
// (Không có state cho trang này)

// ========== DATA ==========
// (Không có dữ liệu động cho trang này)

// ========== METHODS ==========
// (Không có methods cần thiết cho trang này)
</script>

<template>
  <!-- Container trang giới thiệu -->
  <div class="about">
    <!-- Tiêu đề trang -->
    <h1>This is an about page</h1>
  </div>
</template>

<style scoped>
/**
 * ========== STYLES: AboutView.vue ==========
 * Styling cho trang giới thiệu
 */

/* Responsive design: Màn hình lớn (1024px trở lên) */
@media (min-width: 1024px) {

  /* Container chính - Chiều cao toàn màn hình, flex center items */
  .about {
    min-height: 100vh;
    /* Chiều cao tối thiểu = viewport height */
    display: flex;
    /* Flex container để center content */
    align-items: center;
    /* Căn giữa theo chiều dọc */
  }
}
</style>
