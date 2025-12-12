<script setup>
import QrcodeVue from 'qrcode.vue';

// Props nhận giá trị QR code và trạng thái modal
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

// Emit sự kiện đóng modal
const emit = defineEmits(['close']);

// Hàm xử lý close modal
const handleClose = () => {
  emit('close');
};
</script>

<template>
  <!-- Modal QR Code - overlay backdrop mờ -->
  <div 
    v-if="show" 
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in"
    @click.self="handleClose"
  >
    <!-- Card modal QR -->
    <div class="relative w-full max-w-sm p-6 text-center bg-white shadow-2xl rounded-2xl animate-scale-up">
      
      <!-- Nút đóng -->
      <button 
        @click="handleClose" 
        class="absolute text-gray-400 top-3 right-3 hover:text-gray-600 transition-colors"
        title="Đóng"
      >
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Tiêu đề -->
      <h3 class="mb-1 text-lg font-bold text-gray-800">Quét mã truy xuất</h3>
      <p class="mb-4 text-sm text-gray-500">Sử dụng Zalo hoặc Camera để quét</p>

      <!-- QR Code -->
      <div class="flex justify-center mb-4">
        <div class="inline-block p-3 border-2 border-green-500 rounded-xl">
          <qrcode-vue 
            :value="qrValue" 
            :size="200" 
            level="H"
            render-as="svg"
            foreground="#15803d" 
          />
        </div>
      </div>

      <!-- Link text (copy được) -->
      <p class="p-2 font-mono text-xs text-gray-400 truncate bg-gray-100 rounded">
        {{ qrValue }}
      </p>
      
      <!-- Nút đóng -->
      <button 
        @click="handleClose" 
        class="w-full py-2 mt-5 font-semibold text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
      >
        Đóng
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Hiệu ứng fade in cho modal */
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}

/* Hiệu ứng scale up cho card */
.animate-scale-up {
  animation: scaleUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Keyframe fade in */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Keyframe scale up */
@keyframes scaleUp {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
