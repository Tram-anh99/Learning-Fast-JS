<script setup>
/**
 * ========== COMPONENT: HomeQRModal.vue ==========
 * Purpose: Modal hiển thị mã QR để truy xuất nguồn gốc
 * Related Files:
 *   - src/composables/useHome.js (Logic & state)
 *   - src/views/HomeView.vue (Main view)
 *   - src/assets/styles/tailwind.css (Global animations)
 */

import QrcodeVue from 'qrcode.vue';

defineProps({
  show: {
    type: Boolean,
    required: true
  },
  qrLink: {
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
    <div class="w-full max-w-sm bg-white rounded-2xl shadow-2xl p-6 text-center animate-scale-up">
      
      <!-- Title -->
      <h3 class="text-xl font-bold text-gray-800 mb-2">Mã QR Truy xuất</h3>
      <p class="text-sm text-gray-500 mb-6">Dùng Zalo hoặc Camera để quét mã này</p>

      <!-- QR Code -->
      <div class="flex justify-center mb-6">
        <div class="inline-block p-4 bg-white border-2 border-green-500 rounded-lg">
          <QrcodeVue 
            :value="qrLink" 
            :size="220" 
            level="H" 
            render-as="svg"
            foreground="#15803d"
          />
        </div>
      </div>

      <!-- Link display -->
      <p class="text-[10px] text-gray-400 bg-gray-100 p-2 rounded mb-4 truncate font-mono">
        {{ qrLink }}
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
