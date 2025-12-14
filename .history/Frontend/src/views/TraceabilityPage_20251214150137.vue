<script setup>
/**
 * ========== VIEW: TraceabilityPage.vue ==========
 * Purpose: Trang truy xuất nguồn gốc sản phẩm - Hiển thị lịch sử và thông tin sản phẩm
 * 
 * Architecture:
 *   - Composable: src/composables/useTraceability.js (Logic & state management)
 *   - Components:
 *     • QRModal.vue - Modal hiển thị mã QR để chia sẻ
 *   - Routing: Trang này được truy cập qua route `/truy-xuat/:id`
 * 
 * Features:
 *   - Hiển thị thông tin sản phẩm dựa trên mã QR hoặc ID
 *   - Lịch sử canh tác và xử lý sản phẩm
 *   - Mã QR để chia sẻ thông tin truy xuất
 *   - Chứng chỉ và thông tin chất lượng
 */

// ========== IMPORTS ==========
// Import composable quản lý logic truy xuất nguồn gốc
import { useTraceability } from '../composables/useTraceability';

// Import component modal hiển thị mã QR
import QRModal from '../components/QRModal.vue';

// ========== STATE ==========
/**
 * State quản lý modal QR và giá trị QR từ composable
 * - showQR: boolean - Trạng thái hiển thị modal QR
 * - qrValue: string - Giá trị QR code (URL hoặc dữ liệu)
 * - openQR: function - Mở modal QR
 * - closeQR: function - Đóng modal QR
 */
const { showQR, qrValue, openQR, closeQR } = useTraceability();

// ========== DATA ==========
// (Dữ liệu được quản lý bởi composable useTraceability)

// ========== METHODS ==========
// (Các phương thức được quản lý bởi composable useTraceability)
</script>

<template>
  <!-- Container chính - Min height toàn màn hình với padding dưới -->
  <div class="relative min-h-screen pb-10 font-sans bg-gray-50">

    <!-- Nút QR nằm trên cùng bên phải (Floating Action Button) -->
    <div class="absolute z-20 top-4 right-4">
      <!-- Nút mở modal QR với tooltip -->
      <button @click="openQR"
        class="p-2 text-gray-700 transition rounded-full shadow-lg bg-white/90 hover:text-green-600" title="Hiện mã QR">
        <!-- Icon QR Code (SVG) -->
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>
    </div>

    <!-- Nút QR toàn màn hình (Primary Action Button) -->
    <div class="px-4 mt-8 mb-4">
      <!-- Nút lớn để mở modal QR với icon và text -->
      <button @click="openQR"
        class="flex items-center justify-center w-full py-3 font-bold text-white transition-colors bg-green-800 shadow-lg hover:bg-green-900 rounded-xl">
        <!-- Icon QR Code (SVG) -->
        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <!-- Text nút -->
        Hiện mã QR để chia sẻ
      </button>
    </div>

    <!-- Modal QR Code (Component riêng) -->
    <!-- Props:
         - show: boolean - Trạng thái hiển thị modal
         - qrValue: string - Giá trị/URL mã QR
         Events:
         - @close - Sự kiện đóng modal
    -->
    <QRModal :show="showQR" :qrValue="qrValue" @close="closeQR" />

  </div>
</template>

<style scoped>
/**
 * ========== STYLES: TraceabilityPage.vue ==========
 * Styling cho trang truy xuất nguồn gốc
 */

/* Responsive design: Màn hình lớn (1024px trở lên) */
@media (min-width: 1024px) {
  /* Container chính - Chiều cao toàn màn hình, flex center */
  /* (Hiện tại không còn class .about nên không cần style này) */
}
</style>
