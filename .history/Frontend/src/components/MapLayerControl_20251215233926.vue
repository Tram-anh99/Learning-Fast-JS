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
      <div class="h-full rounded-xl shadow-md p-5 flex flex-col bg-gradient-to-br from-white to-slate-50">
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
                  <i class="fas fa-layer-group text-lg text-gray-700"></i>
                  <h3 class="text-sm font-bold text-gray-800">Lớp dữ liệu</h3>
            </div>

            <div class="space-y-3">
                  <button @click="emit('toggleSauBenh')"
                        :class="cheDoXem === 'sau_benh' ? 'ring-2 ring-orange-400 scale-105' : ''"
                        class="w-full py-3 px-4 rounded-lg text-sm font-semibold text-white transition-all flex items-center gap-3 shadow-md hover:shadow-lg"
                        style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
                        <i class="fas fa-biohazard text-lg"></i>
                        <span>Mật độ Sâu bệnh</span>
                  </button>

                  <button @click="emit('toggleDuLuongThuoc')"
                        :class="cheDoXem === 'phan_bon' ? 'ring-2 ring-green-400 scale-105' : ''"
                        class="w-full py-3 px-4 rounded-lg text-sm font-semibold text-white transition-all flex items-center gap-3 shadow-md hover:shadow-lg"
                        style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                        <i class="fas fa-flask text-lg"></i>
                        <span>Dư lượng Thuốc</span>
                  </button>
            </div>

            <div class="mt-auto pt-4 border-t border-gray-200">
                  <div class="p-3 rounded text-xs bg-blue-50 text-gray-700">
                        <p class="font-semibold mb-1 flex items-center gap-1">
                              <i class="fas fa-info-circle"></i>
                              Hướng dẫn:
                        </p>
                        <p>Nhấn vào nút để bật/tắt hiển thị lớp dữ liệu tương ứng trên bản đồ</p>
                  </div>
            </div>
      </div>
</template>
