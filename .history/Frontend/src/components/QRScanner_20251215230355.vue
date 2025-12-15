<script setup>
/**
 * ========== COMPONENT: QRScanner.vue ==========
 * Purpose: Component quét mã QR để tra cứu nông sản
 * 
 * Features:
 *   - Mở modal với input để nhập/scan mã QR
 *   - Tự động điều hướng đến trang chi tiết khi scan xong
 *   - Hỗ trợ camera hoặc input thủ công
 * 
 * Props:
 *   - show (boolean): Hiển thị/ẩn modal
 * 
 * Emits:
 *   - close: Đóng modal
 *   - scan: Phát khi user quét thành công (code)
 */

// ========== IMPORTS ==========
import { ref } from 'vue'; // Vue ref hook

// ========== PROPS & EMITS ==========
// Props: Nhận trạng thái hiển thị từ parent
const props = defineProps({
      // show: Hiển thị modal hay không
      show: {
            type: Boolean,
            default: false
      }
});

// Emits: Phát sự kiện lên parent
const emit = defineEmits(['close', 'scan']);

// ========== STATE ==========
// State: Giá trị QR code được nhập
const qrCode = ref('');
// State: Đang quét từ camera hay không
const isScanning = ref(false);
// State: Lỗi quét
const scanError = ref('');

// ========== METHODS ==========
/**
 * Handler: Xử lý khi form được submit
 * Phát event scan với mã QR
 */
const handleSubmit = () => {
      // Trim whitespace
      const code = qrCode.value.trim();

      // Kiểm tra mã không trống
      if (!code) {
            scanError.value = 'Vui lòng nhập hoặc quét mã QR';
            return;
      }

      // Reset error
      scanError.value = '';

      // Phát event scan lên parent
      emit('scan', code);

      // Reset input
      qrCode.value = '';
};

/**
 * Handler: Xử lý khi đóng modal
 */
const handleClose = () => {
      // Reset state
      qrCode.value = '';
      scanError.value = '';
      isScanning.value = false;

      // Phát event close lên parent
      emit('close');
};

/**
 * Handler: Khởi tạo quét từ camera (future feature)
 */
const startCamera = () => {
      isScanning.value = true;
      scanError.value = '';
      // TODO: Implement HTML5 QR code scanner
      // Có thể dùng library như: jsQR, html5-qrcode, etc.
};

/**
 * Handler: Dừng quét camera
 */
const stopCamera = () => {
      isScanning.value = false;
};
</script>

<template>
      <!-- Modal wrapper: background mờ -->
      <transition name="fade">
            <div v-if="show" class="fixed inset-0 z-40 flex items-end justify-center bg-black/50 sm:items-center">

                  <!-- Modal container: phần chính -->
                  <div class="w-full overflow-hidden bg-white shadow-xl sm:w-96 rounded-t-3xl sm:rounded-2xl"
                        @click.stop>

                        <!-- Modal header: tiêu đề + close button -->
                        <div class="flex items-center justify-between p-4 border-b border-gray-200">
                              <!-- Title: "Quét mã QR" -->
                              <h3 class="text-lg font-bold text-gray-800">Quét mã QR</h3>

                              <!-- Close button: nút đóng -->
                              <button @click="handleClose"
                                    class="p-1 text-gray-500 transition-colors hover:text-gray-700">
                                    <!-- Icon close: X -->
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none"
                                          viewBox="0 0 24 24" stroke="currentColor">
                                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                              </button>
                        </div>

                        <!-- Modal body: nội dung chính -->
                        <div class="p-6 space-y-4">

                              <!-- Camera section: nếu đang quét (future) -->
                              <div v-if="isScanning"
                                    class="flex items-center justify-center bg-gray-900 rounded-lg aspect-square">
                                    <!-- Placeholder: camera feed -->
                                    <div class="text-center text-white">
                                          <svg xmlns="http://www.w3.org/2000/svg"
                                                class="w-16 h-16 mx-auto mb-2 opacity-50" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                      d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                      d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                                          </svg>
                                          <p class="text-sm">Camera scanning...</p>
                                    </div>
                              </div>

                              <!-- Input section: nhập thủ công -->
                              <div v-if="!isScanning" class="space-y-3">
                                    <!-- Label: nhập mã QR -->
                                    <label class="block text-sm font-medium text-gray-700">
                                          Nhập hoặc quét mã QR tại đây
                                    </label>

                                    <!-- QR code input -->
                                    <input v-model="qrCode" @keyup.enter="handleSubmit" type="text"
                                          placeholder="VT-001-2024-LOT-001" autofocus
                                          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent">

                                    <!-- Error message: hiển thị lỗi nếu có -->
                                    <div v-if="scanError" class="p-3 border border-red-200 rounded-lg bg-red-50">
                                          <p class="text-sm text-red-700">{{ scanError }}</p>
                                    </div>
                              </div>

                              <!-- Info: hướng dẫn -->
                              <div class="p-3 border border-blue-200 rounded-lg bg-blue-50">
                                    <p class="text-xs text-blue-700">
                                          💡 Bạn có thể scan trực tiếp từ camera hoặc nhập mã thủ công
                                    </p>
                              </div>

                        </div>

                        <!-- Modal footer: nút hành động -->
                        <div class="flex gap-3 p-6 border-t border-gray-200">

                              <!-- Camera button: nút quét từ camera (future) -->
                              <button v-if="!isScanning" @click="startCamera"
                                    class="flex items-center justify-center flex-1 gap-2 px-4 py-3 font-semibold text-gray-700 transition-colors rounded-lg hover:bg-gray-100">
                                    <!-- Icon camera -->
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor"
                                          viewBox="0 0 20 20">
                                          <path
                                                d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                                    </svg>
                                    <span class="hidden sm:inline">Camera</span>
                              </button>

                              <!-- Stop button: nút dừng quét (khi scanning) -->
                              <button v-else @click="stopCamera"
                                    class="flex-1 px-4 py-3 font-semibold text-gray-700 transition-colors bg-gray-200 rounded-lg hover:bg-gray-300">
                                    Dừng
                              </button>

                              <!-- Submit button: nút tra cứu -->
                              <button @click="handleSubmit"
                                    class="flex-1 px-4 py-3 font-semibold text-white transition-colors bg-green-600 rounded-lg hover:bg-green-700">
                                    Tra cứu
                              </button>

                        </div>

                  </div>

            </div>
      </transition>
</template>

<style scoped>
/* Fade transition: animation mở/đóng modal */
.fade-enter-active,
.fade-leave-active {
      transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
      opacity: 0;
}
</style>
