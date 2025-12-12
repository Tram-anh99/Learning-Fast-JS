<script setup>
import { useTraceability } from '../composables/useTraceability';
import TraceabilityQRModal from '../components/TraceabilityQRModal.vue';

// Sử dụng composable truy xuất
const { showQR, qrValue, openQR, closeQR } = useTraceability();
</script>

<template>
  <div class="relative min-h-screen pb-10 font-sans bg-gray-50">
    
    <!-- Nút QR nằm trên cùng bên phải -->
    <div class="absolute z-20 top-4 right-4">
      <button 
        @click="openQR" 
        class="p-2 text-gray-700 transition rounded-full shadow-lg bg-white/90 hover:text-green-600"
        title="Hiện mã QR"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>
    </div>

    <!-- Nút QR toàn màn hình -->
    <div class="px-4 mt-8 mb-4">
      <button 
        @click="openQR" 
        class="flex items-center justify-center w-full py-3 font-bold text-white bg-green-800 shadow-lg hover:bg-green-900 rounded-xl transition-colors"
      >
        <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        Hiện mã QR để chia sẻ
      </button>
    </div>

    <!-- Modal QR Code -->
    <TraceabilityQRModal :show="showQR" :qrValue="qrValue" @close="closeQR" />

  </div>
</template>
