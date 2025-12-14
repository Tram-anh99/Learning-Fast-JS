<script setup>
/**
 * ========== VIEW: TraceabilityPage.vue ==========
 * Mục đích: Trang truy xuất nguồn gốc sản phẩm - Hiển thị lịch sử và thông tin sản phẩm nông sản
 * 
 * Kiến trúc:
 *   - Composable: src/composables/useTraceability.js (Quản lý state & logic)
 *   - Thành phần con:
 *     • QRModal.vue - Modal hiển thị mã QR để chia sẻ thông tin truy xuất
 *   - Routing: Trang này được truy cập qua route `/truy-xuat/:id` hoặc từ quét QR
 * 
 * Tính năng:
 *   - Hiển thị thông tin sản phẩm dựa trên mã QR hoặc ID sản phẩm
 *   - Lịch sử đầy đủ: Từ gieo hạt → bón phân → phun thuốc → tưới → làm cỏ → thu hoạch → bán
 *   - Mã QR để chia sẻ thông tin truy xuất với người khác
 *   - Chứng chỉ và thông tin chất lượng sản phẩm
 *   - Button FAB (Floating Action Button) để mở QR modal
 */

// ========== IMPORTS ==========
// Composable: Quản lý state modal QR và dữ liệu truy xuất
import { useTraceability } from '../composables/useTraceability';

// Component: Modal hiển thị mã QR code
import QRModal from '../components/QRModal.vue';

// ========== STATE ==========
/**
 * State từ composable useTraceability
 * - showQR: Ref<Boolean> - Trạng thái hiển thị/ẩn modal QR
 * - qrValue: Ref<String> - Giá trị/URL trong mã QR code
 * - openQR: Function - Mở modal QR (showQR.value = true)
 * - closeQR: Function - Đóng modal QR (showQR.value = false)
 * 
 * Ứng dụng:
 *   - Điều khiển việc hiển thị modal QR
 *   - Lưu trữ URL truy xuất để tạo QR code
 */
const { showQR, qrValue, openQR, closeQR } = useTraceability();

// ========== DATA ==========
// (Tất cả dữ liệu được quản lý bởi composable useTraceability)
// Ví dụ: Thông tin sản phẩm, lịch sử canh tác, chứng chỉ, v.v.

// ========== METHODS ==========
// (Tất cả phương thức được quản lý bởi composable useTraceability)
// Ví dụ: loadProductInfo(), generateQRCode(), shareTraceability(), v.v.
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
