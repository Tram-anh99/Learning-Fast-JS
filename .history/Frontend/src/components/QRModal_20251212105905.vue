<script setup>
/**
 * ========== COMPONENT: QRModal.vue ==========
 * Purpose: Modal QR code dùng chung cho tra cứu & truy xuất nguồn gốc
 * Dùng bởi:
 *   - src/views/HomeView.vue (Tra cứu nông sản)
 *   - src/views/TraceabilityPage.vue (Truy xuất nguồn gốc)
 * Related Composables:
 *   - src/composables/useHome.js
 *   - src/composables/useTraceability.js
 * Styling:
 *   - src/assets/styles/tailwind.css (animate-fade-in, animate-scale-up)
 */

import QrcodeVue from 'qrcode.vue';

defineProps({
      show: {
            type: Boolean,
            required: true
      },
      qrValue: {
            type: String,
            required: true
      }
});

defineEmits(['close']);
</script>

<template>
  <!-- Backdrop với glassmorphism -->
  <div 
    v-if="show" 
    @click.self="$emit('close')"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-md animate-fade-in"
  >
    <!-- Modal Card -->
    <div class="relative w-full max-w-sm bg-gradient-to-br from-white via-slate-50 to-blue-50 rounded-3xl shadow-2xl p-8 text-center animate-scale-up border border-white/80 backdrop-blur-xl">
      
      <!-- Decorative gradient circles (background) -->
      <div class="absolute -top-20 -right-20 w-40 h-40 bg-gradient-to-br from-green-400/30 to-blue-400/30 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-20 -left-20 w-40 h-40 bg-gradient-to-br from-blue-400/30 to-purple-400/30 rounded-full blur-3xl"></div>

      <!-- Close button - Modern style -->
      <button 
        @click="$emit('close')"
        class="absolute top-5 right-5 p-2 hover:bg-gray-100/80 text-gray-500 hover:text-gray-700 transition-all duration-200 rounded-full group" 
        title="Đóng"
      >
        <svg class="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Header Section -->
      <div class="relative z-10 mb-8">
        <div class="flex justify-center mb-4">
          <div class="px-4 py-2 bg-gradient-to-r from-green-400 to-blue-400 rounded-full text-xs font-bold text-white shadow-lg">
            ✨ Chia sẻ nguồn gốc
          </div>
        </div>
        
        <h3 class="text-3xl font-bold bg-gradient-to-r from-gray-900 via-green-700 to-blue-700 bg-clip-text text-transparent mb-2">
          Mã QR Truy xuất
        </h3>
        <p class="text-sm text-gray-600 font-medium">
          Quét bằng Camera hoặc Zalo để xác minh nguồn gốc
        </p>
      </div>

      <!-- QR Code Container -->
      <div class="relative z-10 flex justify-center mb-8">
        <div class="relative group">
          <!-- Glow effect -->
          <div class="absolute inset-0 bg-gradient-to-r from-green-400 to-blue-400 rounded-2xl blur-xl opacity-30 group-hover:opacity-50 transition-opacity duration-300"></div>
          
          <!-- QR Card -->
          <div class="relative bg-white p-6 rounded-2xl shadow-xl border-2 border-gradient-to-r from-green-200 to-blue-200 hover:shadow-2xl transition-all duration-300">
            <QrcodeVue 
              :value="qrValue" 
              :size="240" 
              level="H" 
              render-as="svg"
              foreground="#0d7a4a"
            />
          </div>
        </div>
      </div>

      <!-- URL Display Section -->
      <div class="relative z-10 mb-6 p-4 bg-gradient-to-r from-slate-100 to-blue-50 rounded-xl border border-slate-200/50 group hover:border-slate-300 transition-all duration-200">
        <p class="text-xs text-gray-600 font-semibold uppercase tracking-wider mb-2 opacity-70">
          🔗 Đường dẫn truy cập
        </p>
        <p class="text-xs text-gray-700 font-mono break-all hover:text-gray-900 transition-colors">
          {{ qrValue }}
        </p>
        
        <!-- Copy button hint -->
        <div class="mt-2 text-xs text-gray-500 italic">
          ← Nhấn để copy đường dẫn
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="relative z-10 space-y-3">
        <button 
          @click="$emit('close')"
          class="w-full py-3 px-4 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all duration-200 active:scale-95 flex items-center justify-center gap-2 group"
        >
          <span>Tuyệt vời! Đã lưu</span>
          <svg class="w-5 h-5 group-hover:scale-110 transition-transform duration-200" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button 
          @click="$emit('close')"
          class="w-full py-2 px-4 text-gray-700 font-semibold rounded-xl hover:bg-gray-100/80 transition-all duration-200 text-sm"
        >
          Đóng
        </button>
      </div>

      <!-- Footer hint -->
      <div class="relative z-10 mt-6 pt-4 border-t border-gray-200/50 text-xs text-gray-500 text-center">
        💡 Chia sẻ mã QR này để người khác xác minh sản phẩm
      </div>

    </div>
  </div>
</template>
