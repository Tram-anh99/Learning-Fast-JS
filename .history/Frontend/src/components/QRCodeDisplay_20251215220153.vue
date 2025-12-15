<script setup>
/**
 * ========== COMPONENT: QRCodeDisplay.vue ==========
 * Purpose: Component hiển thị mã QR cho vùng trồng
 * 
 * Features:
 *   - Hiển thị QR code placeholder
 *   - Mã số vùng
 *   - Link đến trang truy xuất
 *   - Hướng dẫn sử dụng
 * 
 * Props:
 *   - vung: Object - Thông tin vùng trồng { ma, ten, maQR }
 *   - compact: Boolean - Chế độ gọn (cho sidebar)
 */

const props = defineProps({
      vung: {
            type: Object,
            required: true
      },
      compact: {
            type: Boolean,
            default: false
      }
});

const qrCode = computed(() => props.vung?.maQR || props.vung?.ma || '');
</script>

<template>
      <!-- Full version -->
      <div v-if="!compact" class="w-64 bg-white rounded-xl shadow-md border border-white p-5">
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
                  <i class="fas fa-qrcode text-purple-600 text-lg"></i>
                  <h3 class="text-sm font-bold text-gray-700">Mã QR Truy xuất</h3>
            </div>

            <div class="flex flex-col items-center gap-3">
                  <!-- QR Code (hiển thị trực tiếp) -->
                  <div class="w-48 h-48 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg flex items-center justify-center border-2 border-gray-200 shadow-inner">
                        <div class="text-center">
                              <i class="fas fa-qrcode text-6xl text-gray-400 mb-2"></i>
                              <p class="text-xs text-gray-500">QR Code</p>
                        </div>
                  </div>

                  <!-- Mã số -->
                  <div class="text-center w-full">
                        <p class="text-xs text-gray-500 mb-1">Mã số:</p>
                        <p class="text-lg font-bold text-purple-600 bg-purple-50 py-2 px-4 rounded border border-purple-200">
                              {{ qrCode }}
                        </p>
                  </div>

                  <!-- Link truy xuất -->
                  <a :href="`/truy-xuat/${qrCode}`" 
                     target="_blank"
                     class="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 px-4 rounded text-center transition-colors flex items-center justify-center gap-2">
                        <i class="fas fa-external-link-alt"></i>
                        Xem trang truy xuất
                  </a>

                  <!-- Hướng dẫn -->
                  <div class="bg-gray-50 p-3 rounded text-xs text-gray-600 w-full">
                        <p class="font-semibold mb-1 flex items-center gap-1">
                              <i class="fas fa-info-circle text-blue-500"></i>
                              Hướng dẫn:
                        </p>
                        <p>Quét mã QR để xem đầy đủ thông tin truy xuất nguồn gốc sản phẩm</p>
                  </div>
            </div>
      </div>

      <!-- Compact version (cho sidebar) -->
      <div v-else class="bg-white rounded-lg border border-gray-200 p-3">
            <div class="flex items-center gap-2 mb-2">
                  <i class="fas fa-qrcode text-purple-600"></i>
                  <span class="text-xs font-bold text-gray-700">Mã QR</span>
            </div>

            <div class="flex flex-col items-center gap-2">
                  <!-- QR Code compact -->
                  <div class="w-32 h-32 bg-gradient-to-br from-gray-50 to-gray-100 rounded flex items-center justify-center border border-gray-200">
                        <i class="fas fa-qrcode text-4xl text-gray-400"></i>
                  </div>

                  <!-- Mã số compact -->
                  <div class="text-center w-full">
                        <p class="text-xs font-bold text-purple-600 bg-purple-50 py-1 px-2 rounded border border-purple-200">
                              {{ qrCode }}
                        </p>
                  </div>

                  <!-- Link truy xuất compact -->
                  <a :href="`/truy-xuat/${qrCode}`" 
                     target="_blank"
                     class="w-full bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold py-1.5 px-3 rounded text-center transition-colors flex items-center justify-center gap-1">
                        <i class="fas fa-external-link-alt text-xs"></i>
                        Truy xuất
                  </a>
            </div>
      </div>
</template>

<style scoped>
/* Optional: Add any specific styles here */
</style>
