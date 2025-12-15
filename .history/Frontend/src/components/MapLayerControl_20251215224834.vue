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
      <div class="h-full rounded-xl shadow-md border p-5 flex flex-col"
            style="background-color: #fbfced; border-color: #fbfced;">
            <div class="flex items-center gap-2 mb-4 pb-3 border-b" style="border-color: #24504b;">
                  <i class="fas fa-layer-group text-lg" style="color: #24504b;"></i>
                  <h3 class="text-sm font-bold" style="color: #24504b;">Lớp dữ liệu</h3>
            </div>

            <div class="space-y-3">
                  <button :style="{
                        backgroundColor: cheDoXem === 'sau_benh' ? '#24504b' : '#fbfced',
                        color: cheDoXem === 'sau_benh' ? '#fbfced' : '#24504b',
                        borderColor: '#24504b'
                  }" @click="emit('toggleSauBenh')"
                        class="w-full py-3 px-4 rounded-lg border-2 text-sm font-semibold transition-all flex items-center gap-3 shadow-sm hover:opacity-90">
                        <i class="fas fa-biohazard text-lg"></i>
                        <span>Mật độ Sâu bệnh</span>
                  </button>

                  <button :style="{
                        backgroundColor: cheDoXem === 'phan_bon' ? '#24504b' : '#fbfced',
                        color: cheDoXem === 'phan_bon' ? '#fbfced' : '#24504b',
                        borderColor: '#24504b'
                  }" @click="emit('toggleDuLuongThuoc')"
                        class="w-full py-3 px-4 rounded-lg border-2 text-sm font-semibold transition-all flex items-center gap-3 shadow-sm hover:opacity-90">
                        <i class="fas fa-flask text-lg"></i>
                        <span>Dư lượng Thuốc</span>
                  </button>
            </div>

            <div class="mt-auto pt-4 border-t" style="border-color: #24504b;">
                  <div class="p-3 rounded text-xs" style="background-color: rgba(36, 80, 75, 0.1); color: #24504b;">
                        <p class="font-semibold mb-1 flex items-center gap-1">
                              <i class="fas fa-info-circle"></i>
                              Hướng dẫn:
                        </p>
                        <p>Nhấn vào nút để bật/tắt hiển thị lớp dữ liệu tương ứng trên bản đồ</p>
                  </div>
            </div>
      </div>
</template>
