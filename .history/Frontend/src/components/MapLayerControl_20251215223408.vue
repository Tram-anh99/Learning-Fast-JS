<script setup>
const props = defineProps({
      cheDoXem: {
            type: String,
            default: 'hanh_chinh'
      }
});

const emit = defineEmits(['toggleSauBenh', 'toggleDuLuongThuoc']);
</script>

<template>
      <div class="h-full bg-white rounded-xl shadow-md border border-white p-5 flex flex-col">
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
                  <i class="fas fa-layer-group text-green-600 text-lg"></i>
                  <h3 class="text-sm font-bold text-gray-700">Lớp dữ liệu</h3>
            </div>

            <div class="space-y-3">
                  <button 
                        :class="{ 
                              'bg-green-600 text-white': cheDoXem === 'sau_benh',
                              'bg-white text-gray-700 hover:bg-gray-50': cheDoXem !== 'sau_benh'
                        }"
                        @click="emit('toggleSauBenh')"
                        class="w-full py-3 px-4 rounded-lg border border-gray-200 text-sm font-semibold transition-all flex items-center gap-3 shadow-sm">
                        <i class="fas fa-biohazard text-lg"></i>
                        <span>Mật độ Sâu bệnh</span>
                  </button>

                  <button 
                        :class="{ 
                              'bg-green-600 text-white': cheDoXem === 'phan_bon',
                              'bg-white text-gray-700 hover:bg-gray-50': cheDoXem !== 'phan_bon'
                        }"
                        @click="emit('toggleDuLuongThuoc')"
                        class="w-full py-3 px-4 rounded-lg border border-gray-200 text-sm font-semibold transition-all flex items-center gap-3 shadow-sm">
                        <i class="fas fa-flask text-lg"></i>
                        <span>Dư lượng Thuốc</span>
                  </button>
            </div>

            <div class="mt-auto pt-4 border-t border-gray-200">
                  <div class="bg-blue-50 p-3 rounded text-xs text-gray-600">
                        <p class="font-semibold mb-1 flex items-center gap-1">
                              <i class="fas fa-info-circle text-blue-500"></i>
                              Hướng dẫn:
                        </p>
                        <p>Nhấn vào nút để bật/tắt hiển thị lớp dữ liệu tương ứng trên bản đồ</p>
                  </div>
            </div>
      </div>
</template>
