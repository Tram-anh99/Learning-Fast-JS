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
// Composable: Quản lý state QR, dữ liệu vùng trồng & tra cứu sản phẩm
import { showQR, openQRModal, closeQRModal } from '../composables/useHome';
import QRModal from '../components/QRModal.vue';

// ========== STATE & METHODS ==========
/**
 * State từ composable useHome
 * - showQR: Ref<Boolean> - Trạng thái modal QR
 * - openQRModal: Function(maSanPham) - Mở QR modal với mã sản phẩm
 * - closeQRModal: Function - Đóng QR modal
 */
// Từ useHome (imported above)
</script>

<template>
  <!-- ========== MAIN CONTAINER ========== -->
  <!-- Container chính: Độ cao tối thiểu là toàn màn hình, background xám nhạt -->
  <!-- relative: Position context cho FAB button (absolute positioning) -->
  <!-- min-h-screen: Chiều cao tối thiểu 100vh -->
  <!-- pb-10: Padding dưới 40px (tránh nội dung bị che bởi FAB) -->
  <!-- font-sans: Font chữ sans-serif (Tailwind default) -->
  <!-- bg-gray-50: Background màu xám rất nhạt -->
  <div class="relative min-h-screen pb-10 font-sans bg-gray-50">

    <!-- ========== FLOATING ACTION BUTTON (FAB) ========== -->
    <!-- FAB container: Positioned tuyệt đối ở góc trên phải -->
    <!-- absolute: Position tuyệt đối trong parent (relative) -->
    <!-- z-20: z-index 20 (phía trên hầu hết nội dung) -->
    <!-- top-4: 16px từ đỉnh -->
    <!-- right-4: 16px từ bên phải -->
    <div class="absolute z-20 top-4 right-4">
      <!-- Nút QR FAB: Compact button với tooltip -->
      <!-- p-2: Padding 8px -->
      <!-- text-gray-700: Màu icon xám đậm -->
      <!-- transition: Smooth animation cho hover effects -->
      <!-- rounded-full: Hình tròn (border-radius 9999px) -->
      <!-- shadow-lg: Large shadow cho elevation -->
      <!-- bg-white/90: White background với 90% opacity (transparent effect) -->
      <!-- hover:text-green-600: Đổi icon sang xanh khi hover -->
      <!-- title: Tooltip text "Hiện mã QR" -->
      <!-- @click: Gọi openQRModal() để mở modal QR -->
      <button @click="openQRModal('product-id')"
        class="p-2 text-gray-700 transition rounded-full shadow-lg bg-white/90 hover:text-green-600" title="Hiện mã QR">
        <!-- Icon: QR Code (SVG) -->
        <!-- w-6 h-6: 24px x 24px icon size -->
        <!-- viewBox="0 0 24 24": SVG coordinate system -->
        <!-- stroke-currentColor: Icon stroke color kế thừa từ text-gray-700 -->
        <!-- stroke-width="2": 2px stroke width -->
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <!-- Path: QR code icon (hình vuông lồng nhau) -->
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>
    </div>

    <!-- ========== PRIMARY ACTION BUTTON ========== -->
    <!-- Main QR button: Toàn chiều rộng, dưới header -->
    <!-- px-4: Padding ngang 16px -->
    <!-- mt-8: Margin trên 32px (distance từ top) -->
    <!-- mb-4: Margin dưới 16px (space trước nội dung) -->
    <div class="px-4 mt-8 mb-4">
      <!-- Button lớn: Mở modal QR -->
      <!-- flex items-center justify-center: Flex layout, center content -->
      <!-- w-full: Chiều rộng 100% -->
      <!-- py-3: Padding dọc 12px -->
      <!-- font-bold: Text bold (700) -->
      <!-- text-white: Text màu trắng -->
      <!-- transition-colors: Smooth animation cho color changes -->
      <!-- bg-green-800: Background xanh lá đậm (#1f5233) -->
      <!-- shadow-lg: Large shadow cho elevation -->
      <!-- hover:bg-green-900: Đổi sang xanh lá tối hơn khi hover -->
      <!-- rounded-xl: Rounded corners (xl = 12px) -->
      <!-- @click: Gọi openQR() để mở modal QR -->
      <button @click="openQR"
        class="flex items-center justify-center w-full py-3 font-bold text-white transition-colors bg-green-800 shadow-lg hover:bg-green-900 rounded-xl">
        <!-- Icon: QR Code (SVG) -->
        <!-- w-5 h-5: 20px x 20px icon size -->
        <!-- mr-2: Margin phải 8px (space trước text) -->
        <!-- fill="none": No fill, chỉ stroke (outline) -->
        <!-- stroke="currentColor": Stroke color kế thừa từ text-white -->
        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <!-- Path: QR code icon -->
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        <!-- Button text: "Hiện mã QR để chia sẻ" = Show QR code to share -->
        Hiện mã QR để chia sẻ
      </button>
    </div>

    <!-- ========== QR CODE MODAL ========== -->
    <!-- Modal component: Hiển thị mã QR code -->
    <!-- v-if: Conditionally render dựa trên showQR.value -->
    <!-- Props:
         - show: showQR (Boolean) - Trạng thái hiển thị modal
         - qrValue: qrValue (String) - Giá trị/URL trong QR code
         Events:
         - @close: Gọi closeQR() khi user đóng modal (click X hoặc backdrop)
    -->
    <QRModal :show="showQR" :qrValue="qrValue" @close="closeQR" />
  </div>
</template>
