<script setup>
/**
 * ========== COMPONENT: CropDetailsComponent.vue ==========
 * Purpose: Hiển thị chi tiết loại cây trồng của từng vùng
 * 
 * Features:
 *   - 3 phần: Chi tiết vùng, Lịch sử canh tác, Mã QR
 *   - Danh sách loại cây trong vùng được chọn
 *   - Diện tích, năng suất, giá xuất khẩu
 *   - Thị trường xuất khẩu cho mỗi loại cây
 *   - Mã QR truy xuất
 * 
 * Props:
 *   - selectedVung: Vùng được chọn từ bảng hoặc bản đồ
 * 
 * Related Files:
 *   - src/composables/useCropData.js - Dữ liệu loại cây
 */

import { computed, watch, ref, onMounted } from 'vue';
import { getCropsByZone, getMarketsbyZone } from '../composables/useCropData';

const props = defineProps({
      selectedVung: {
            type: Object,
            default: null
      }
});

// ========== QR CODE GENERATION ==========
const qrCanvas = ref(null);
const generateQRCode = () => {
      if (!qrCanvas.value || !props.selectedVung?.maQR) return;
      
      // Sử dụng API online để tạo QR code
      const qrText = props.selectedVung.maQR || props.selectedVung.ma;
      const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrText)}`;
      
      const img = new Image();
      img.onload = () => {
            const ctx = qrCanvas.value.getContext('2d');
            ctx.drawImage(img, 0, 0, 200, 200);
      };
      img.src = qrUrl;
};

watch(() => props.selectedVung, () => {
      setTimeout(generateQRCode, 0);
}, { deep: true });

onMounted(() => {
      generateQRCode();
});

// ========== COMPUTED: Danh sách cây của vùng được chọn ==========
const cropsInZone = computed(() => {
      if (!props.selectedVung?.ma) return [];
      return getCropsByZone(props.selectedVung.ma);
});

// ========== COMPUTED: Danh sách thị trường của vùng được chọn ==========
const marketsInZone = computed(() => {
      if (!props.selectedVung?.ma) return [];
      return getMarketsbyZone(props.selectedVung.ma);
});

// ========== COMPUTED: Tổng diện tích vùng ==========
const totalAreaInZone = computed(() => {
      return cropsInZone.value.reduce((sum, crop) => sum + crop.dienTich, 0);
});

// ========== COMPUTED: Tổng giá trị xuất khẩu ước tính ==========
const totalExportValue = computed(() => {
      return cropsInZone.value.reduce((sum, crop) => {
            return sum + (crop.dienTich * crop.nangSuat * crop.giaXuat);
      }, 0);
});

// ========== FUNCTION: Format thị trường thành badge ==========
const getMarketBadgeClass = (market) => {
      const colors = {
            'Trung Quốc': 'bg-red-100 text-red-700',
            'Hoa Kỳ': 'bg-blue-100 text-blue-700',
            'Châu Âu': 'bg-yellow-100 text-yellow-700',
            'ASEAN': 'bg-green-100 text-green-700',
            'Khác': 'bg-gray-100 text-gray-700',
      };
      return colors[market] || 'bg-gray-100 text-gray-700';
};
</script>

<template>
      <!-- Container chính -->
      <div v-if="props.selectedVung" class="panel">
            <!-- Header -->
            <div class="panel-header">
                  <div class="flex-1">
                        <h3 class="panel-title">Chi tiết Vùng - {{ props.selectedVung.ma }}</h3>
                        <p class="text-xs text-gray-500 mt-1">{{ props.selectedVung.ten }} • {{ props.selectedVung.chu }}</p>
                  </div>
                  <div class="text-right">
                        <span class="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                              {{ props.selectedVung.trangThai === 'canh_tac' ? 'Đang canh tác' : 'Khác' }}
                        </span>
                  </div>
            </div>

            <!-- 3 Section Grid -->
            <div class="grid grid-cols-3 gap-4 p-4 h-[500px]">
                  <!-- SECTION 1: Chi tiết Vùng & Loại cây -->
                  <div class="border border-gray-200 rounded-lg overflow-hidden flex flex-col bg-white">
                        <div class="bg-gradient-to-r from-green-50 to-emerald-50 px-4 py-2 border-b border-gray-200">
                              <h4 class="text-xs font-bold text-gray-700 flex items-center gap-2">
                                    <i class="fas fa-leaf text-green-600"></i>
                                    Chi tiết vùng trồng
                              </h4>
                        </div>
                        
                        <div class="overflow-y-auto flex-1 scrollbar-custom">
                              <!-- Thông tin tổng quát -->
                              <div class="px-4 py-3 border-b border-gray-100">
                                    <div class="space-y-2 text-xs">
                                          <div class="flex justify-between">
                                                <span class="text-gray-500">Tổng diện tích:</span>
                                                <span class="font-semibold text-blue-600">{{ totalAreaInZone.toFixed(1) }} ha</span>
                                          </div>
                                          <div class="flex justify-between">
                                                <span class="text-gray-500">Giá trị xuất khẩu:</span>
                                                <span class="font-semibold text-green-600">${{ Math.round(totalExportValue).toLocaleString() }}</span>
                                          </div>
                                          <div v-if="marketsInZone.length > 0" class="pt-2 border-t border-gray-100">
                                                <p class="text-gray-500 mb-1">Thị trường:</p>
                                                <div class="flex flex-wrap gap-1">
                                                      <span v-for="market in marketsInZone" :key="market" 
                                                            :class="getMarketBadgeClass(market)"
                                                            class="px-1.5 py-0.5 rounded text-xs font-semibold">
                                                            {{ market }}
                                                      </span>
                                                </div>
                                          </div>
                                    </div>
                              </div>

                              <!-- Danh sách loại cây -->
                              <div class="px-4 py-3">
                                    <h5 class="text-xs font-bold text-gray-700 mb-2">Loại cây:</h5>
                                    <div class="space-y-2">
                                          <div v-for="crop in cropsInZone" :key="crop.id" 
                                                class="p-2 bg-blue-50 rounded border border-blue-100">
                                                <p class="text-xs font-semibold text-gray-700">{{ crop.tenCay }}</p>
                                                <div class="text-xs text-gray-500 mt-1 space-y-0.5">
                                                      <div><i class="fas fa-ruler-horizontal text-blue-500"></i> {{ crop.dienTich }} ha</div>
                                                      <div><i class="fas fa-chart-bar text-green-500"></i> {{ crop.nangSuat }} tạ/ha</div>
                                                      <div><i class="fas fa-dollar-sign text-yellow-500"></i> ${{ crop.giaXuat }}/kg</div>
                                                </div>
                                          </div>
                                    </div>
                              </div>
                        </div>
                  </div>

                  <!-- SECTION 2: Lịch sử Canh tác -->
                  <div class="border border-gray-200 rounded-lg overflow-hidden flex flex-col bg-white">
                        <div class="bg-gradient-to-r from-blue-50 to-cyan-50 px-4 py-2 border-b border-gray-200">
                              <h4 class="text-xs font-bold text-gray-700 flex items-center gap-2">
                                    <i class="fas fa-clipboard-list text-blue-600"></i>
                                    Lịch sử canh tác
                              </h4>
                        </div>
                        
                        <div class="overflow-y-auto flex-1 scrollbar-custom px-4 py-3">
                              <div v-if="props.selectedVung.lichSuCanhTac && props.selectedVung.lichSuCanhTac.length > 0" 
                                   class="space-y-3">
                                    <div v-for="(hoatDong, index) in props.selectedVung.lichSuCanhTac" 
                                         :key="index"
                                         class="pb-3 border-b border-gray-200 last:border-b-0">
                                          <div class="flex gap-2">
                                                <div class="flex-shrink-0 w-16">
                                                      <span class="text-xs font-bold text-blue-600">{{ hoatDong.ngay }}</span>
                                                </div>
                                                <div class="flex-1">
                                                      <p class="text-xs font-semibold text-gray-700">{{ hoatDong.hoatDong }}</p>
                                                      <p class="text-xs text-gray-500 mt-0.5">{{ hoatDong.nguoiThucHien }}</p>
                                                </div>
                                          </div>
                                    </div>
                              </div>
                              <div v-else class="flex items-center justify-center h-32 text-gray-400">
                                    <p class="text-xs">Không có dữ liệu canh tác</p>
                              </div>
                        </div>
                  </div>

                  <!-- SECTION 3: Mã QR -->
                  <div class="border border-gray-200 rounded-lg overflow-hidden flex flex-col bg-white">
                        <div class="bg-gradient-to-r from-purple-50 to-pink-50 px-4 py-2 border-b border-gray-200">
                              <h4 class="text-xs font-bold text-gray-700 flex items-center gap-2">
                                    <i class="fas fa-qrcode text-purple-600"></i>
                                    Mã QR truy xuất
                              </h4>
                        </div>
                        
                        <div class="flex flex-col items-center justify-center flex-1 p-4 gap-3">
                              <!-- QR Code Canvas -->
                              <canvas ref="qrCanvas" width="200" height="200" 
                                    class="border-2 border-purple-200 rounded-lg bg-white shadow-md"></canvas>
                              
                              <!-- Mã số -->
                              <div class="text-center">
                                    <p class="text-sm font-bold text-gray-700">{{ props.selectedVung.maQR || props.selectedVung.ma }}</p>
                                    <a :href="`/truy-xuat/${props.selectedVung.maQR || props.selectedVung.ma}`" 
                                       target="_blank" 
                                       class="text-xs text-blue-600 hover:text-blue-800 hover:underline flex items-center justify-center gap-1 mt-2">
                                          <i class="fas fa-external-link-alt"></i>
                                          Truy xuất nguồn gốc
                                    </a>
                              </div>
                        </div>
                  </div>
            </div>
      </div>

      <!-- No selection state -->
      <div v-else class="panel flex flex-col items-center justify-center min-h-[350px]">
            <div class="text-center">
                  <i class="fas fa-search text-6xl text-gray-300 mb-4"></i>
                  <p class="text-lg font-semibold text-gray-600 mb-2">Chưa chọn vùng trồng</p>
                  <p class="text-sm text-gray-400">Nhấp vào bảng hoặc bản đồ để xem chi tiết</p>
                  <ul class="mt-4 text-sm text-gray-500 space-y-1">
                        <li><i class="fas fa-check text-green-500"></i> Chi tiết vùng và loại cây</li>
                        <li><i class="fas fa-check text-green-500"></i> Lịch sử canh tác</li>
                        <li><i class="fas fa-check text-green-500"></i> Mã QR truy xuất</li>
                  </ul>
            </div>
      </div>
</template>

<style scoped>
.panel {
      @apply bg-white rounded-xl shadow-md border border-white overflow-hidden;
}

.panel-header {
      @apply bg-gradient-to-r from-slate-50 to-blue-50 px-5 py-3 border-b border-gray-200 flex justify-between items-start gap-4;
}

.panel-title {
      @apply text-sm font-bold text-gray-700 m-0;
}

.table-header {
      @apply px-4 py-2.5 text-xs font-bold text-gray-600 text-left border-b border-gray-200 bg-gray-50;
}

.table-cell {
      @apply px-4 py-2.5 text-xs text-gray-700 border-b border-gray-100;
}

.table-row-hover:hover {
      @apply bg-blue-50;
}

/* Scrollbar custom */
.scrollbar-custom::-webkit-scrollbar {
      width: 6px;
}

.scrollbar-custom::-webkit-scrollbar-track {
      background: #f1f5f9;
      border-radius: 10px;
}

.scrollbar-custom::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 10px;
}

.scrollbar-custom::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
}
</style>
