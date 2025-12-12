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
  <div 
    v-if="show"
    @click.self="$emit('close')"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 animate-fade-in"
  >
    <div class="relative w-full max-w-sm bg-white rounded-2xl shadow-2xl p-6 text-center animate-scale-up">
      
      <!-- Nút đóng (X) ở góc -->
      <button 
        @click="$emit('close')"
        class="absolute top-3 right-3 text-gray-400 hover:text-gray-600 transition-colors" 
        title="Đóng"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Tiêu đề -->
      <h3 class="text-xl font-bold text-gray-800 mb-2">Mã QR Truy xuất</h3>
      <p class="text-sm text-gray-500 mb-6">Dùng Zalo hoặc Camera để quét mã này</p>

      <!-- QR Code -->
      <div class="flex justify-center mb-6">
        <div class="inline-block p-4 bg-white border-2 border-green-500 rounded-lg">
          <QrcodeVue 
            :value="qrValue" 
            :size="220" 
            level="H" 
            render-as="svg"
            foreground="#15803d"
          />
        </div>
      </div>

      <!-- Link display -->
      <p class="text-[10px] text-gray-400 bg-gray-100 p-2 rounded mb-4 truncate font-mono">
        {{ qrValue }}
      </p>

      <!-- Close button -->
      <button 
        @click="$emit('close')"
        class="w-full py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold rounded-lg transition-colors"
      >
        Đóng lại
      </button>

    </div>
  </div>
</template>
