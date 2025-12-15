<script setup>
/**
 * ========== COMPONENT: MapLayerControl.vue ==========
 * Purpose: Panel điều khiển lớp dữ liệu cho bản đồ
 * 
 * Features:
 *   - Toggle layer sâu bệnh
 *   - Toggle layer dư lượng thuốc
 *   - Hiển thị chế độ xem hiện tại
 */

import { ref } from 'vue';

// ========== PROPS ==========
const props = defineProps({
      cheDoXem: {
            type: String,
            default: 'hanh_chinh'
      }
});

// ========== EMITS ==========
const emit = defineEmits(['toggleSauBenh', 'toggleDuLuongThuoc']);

// ========== STATE ==========
const isLayerSauBenhActive = ref(false);
const isLayerThuocActive = ref(false);

// ========== METHODS ==========
const handleToggleSauBenh = () => {
      isLayerSauBenhActive.value = !isLayerSauBenhActive.value;
      emit('toggleSauBenh', isLayerSauBenhActive.value);
};

const handleToggleThuoc = () => {
      isLayerThuocActive.value = !isLayerThuocActive.value;
      emit('toggleDuLuongThuoc', isLayerThuocActive.value);
};
</script>

<template>
      <div class="bg-white rounded-xl shadow-md border border-white p-5 h-full flex flex-col">
            <!-- Header -->
            <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
                  <i class="fas fa-layer-group text-green-600 text-lg"></i>
                  <h3 class="text-sm font-bold text-gray-700">Lớp dữ liệu</h3>
            </div>

            <!-- Layer Controls -->
            <div class="space-y-3 flex-1">
                  <!-- Toggle Mật độ sâu bệnh -->
                  <button 
                        @click="handleToggleSauBenh"
                        :class="[
                              'w-full p-4 rounded-lg border-2 transition-all text-left',
                              isLayerSauBenhActive 
                                    ? 'bg-red-50 border-red-500 shadow-md' 
                                    : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                        ]">
                        <div class="flex items-center gap-3">
                              <div :class="[
                                    'w-10 h-10 rounded-full flex items-center justify-center',
                                    isLayerSauBenhActive ? 'bg-red-500' : 'bg-gray-300'
                              ]">
                                    <i class="fas fa-biohazard text-white text-lg"></i>
                              </div>
                              <div class="flex-1">
                                    <p :class="[
                                          'text-sm font-bold',
                                          isLayerSauBenhActive ? 'text-red-700' : 'text-gray-700'
                                    ]">Mật độ Sâu bệnh</p>
                                    <p class="text-xs text-gray-500 mt-0.5">
                                          {{ isLayerSauBenhActive ? 'Đang hiển thị' : 'Nhấn để hiển thị' }}
                                    </p>
                              </div>
                              <div :class="[
                                    'w-5 h-5 rounded border-2 flex items-center justify-center transition-colors',
                                    isLayerSauBenhActive 
                                          ? 'bg-red-500 border-red-500' 
                                          : 'bg-white border-gray-300'
                              ]">
                                    <i v-if="isLayerSauBenhActive" class="fas fa-check text-white text-xs"></i>
                              </div>
                        </div>
                  </button>

                  <!-- Toggle Dư lượng thuốc -->
                  <button 
                        @click="handleToggleThuoc"
                        :class="[
                              'w-full p-4 rounded-lg border-2 transition-all text-left',
                              isLayerThuocActive 
                                    ? 'bg-orange-50 border-orange-500 shadow-md' 
                                    : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                        ]">
                        <div class="flex items-center gap-3">
                              <div :class="[
                                    'w-10 h-10 rounded-full flex items-center justify-center',
                                    isLayerThuocActive ? 'bg-orange-500' : 'bg-gray-300'
                              ]">
                                    <i class="fas fa-flask text-white text-lg"></i>
                              </div>
                              <div class="flex-1">
                                    <p :class="[
                                          'text-sm font-bold',
                                          isLayerThuocActive ? 'text-orange-700' : 'text-gray-700'
                                    ]">Dư lượng Thuốc</p>
                                    <p class="text-xs text-gray-500 mt-0.5">
                                          {{ isLayerThuocActive ? 'Đang hiển thị' : 'Nhấn để hiển thị' }}
                                    </p>
                              </div>
                              <div :class="[
                                    'w-5 h-5 rounded border-2 flex items-center justify-center transition-colors',
                                    isLayerThuocActive 
                                          ? 'bg-orange-500 border-orange-500' 
                                          : 'bg-white border-gray-300'
                              ]">
                                    <i v-if="isLayerThuocActive" class="fas fa-check text-white text-xs"></i>
                              </div>
                        </div>
                  </button>
            </div>

            <!-- Info -->
            <div class="mt-4 pt-4 border-t border-gray-200">
                  <div class="bg-blue-50 p-3 rounded text-xs text-gray-600">
                        <p class="font-semibold mb-1 flex items-center gap-1">
                              <i class="fas fa-info-circle text-blue-500"></i>
                              Thông tin:
                        </p>
                        <p>Bật/tắt các lớp dữ liệu để xem thông tin phân tích trên bản đồ</p>
                  </div>
            </div>
      </div>
</template>

<style scoped>
button {
      cursor: pointer;
}

button:active {
      transform: scale(0.98);
}
</style>
