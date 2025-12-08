<template>
  <div class="relative min-h-screen pb-10 font-sans bg-gray-50">
    
    <div class="absolute z-20 top-4 right-4">
      <button @click="showQR = true" class="p-2 text-gray-700 transition rounded-full shadow-lg bg-white/90 hover:text-green-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </button>
    </div>

    <div class="px-4 mt-8 mb-4">
        <button 
            @click="showQR = true" 
            class="flex items-center justify-center w-full py-3 font-bold text-white bg-green-800 shadow-lg hover:bg-green-900 rounded-xl">
            <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4h2v-4zM6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
            Hiện mã QR để chia sẻ
        </button>
    </div>

    <div v-if="showQR" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in" @click.self="showQR = false">
      <div class="relative w-full max-w-sm p-6 text-center bg-white shadow-2xl rounded-2xl animate-scale-up">
        
        <button @click="showQR = false" class="absolute text-gray-400 top-3 right-3 hover:text-gray-600">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>

        <h3 class="mb-1 text-lg font-bold text-gray-800">Quét mã truy xuất</h3>
        <p class="mb-4 text-sm text-gray-500">Sử dụng Zalo hoặc Camera để quét</p>

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

        <p class="p-2 font-mono text-xs text-gray-400 truncate bg-gray-100 rounded">
          {{ qrValue }}
        </p>
        
        <button @click="showQR = false" class="w-full py-2 mt-5 font-semibold text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200">
            Đóng
        </button>
      </div>
    </div>

  </div>
</template>

<script>
// 1. Import thư viện
import QrcodeVue from 'qrcode.vue'

export default {
  name: 'TraceabilityPage',
  components: {
    QrcodeVue // 2. Khai báo component
  },
  data() {
    return {
      showQR: false, // Biến điều khiển bật/tắt Popup
      // Lấy đường dẫn hiện tại của trình duyệt để tạo mã QR
      qrValue: window.location.href 
    }
  },
  // Nếu muốn mã QR thay đổi động theo ID sản phẩm:
  /*
  computed: {
    qrValue() {
        // Ví dụ: https://webgis-cuaban.com/truy-xuat/123
        return `https://your-domain.com/truy-xuat/${this.$route.params.id}`;
    }
  }
  */
}
</script>

<style scoped>
/* Hiệu ứng Popup hiện ra mượt mà */
.animate-fade-in { animation: fadeIn 0.2s ease-out; }
.animate-scale-up { animation: scaleUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}
</style>