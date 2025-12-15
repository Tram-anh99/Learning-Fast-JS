<script setup>
/**
 * ========== COMPONENT: CropDetailsComponent.vue ==========
 * Purpose: Hiển thị chi tiết loại cây trồng của từng vùng
 * 
 * Features:
 *   - Danh sách loại cây trong vùng được chọn
 *   - Diện tích, năng suất, giá xuất khẩu
 *   - Thị trường xuất khẩu cho mỗi loại cây
 *   - Tính toán giá trị xuất khẩu ước tính
 * 
 * Props:
 *   - selectedVung: Vùng được chọn từ bảng hoặc bản đồ
 * 
 * Related Files:
 *   - src/composables/useCropData.js - Dữ liệu loại cây
 */

import { computed, watch } from 'vue';
import { getCropsByZone, getMarketsbyZone } from '../composables/useCropData';

const props = defineProps({
      selectedVung: {
            type: Object,
            default: null
      }
});

// ========== COMPUTED: Danh sách cây của vùng được chọn ==========
const cropsInZone = computed(() => {
      // selectedVung là Object (đã unwrap từ parent's .value)
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
      <div v-if="props.selectedVung" class="flex gap-5">
            
            <!-- PHẦN 1: CHI TIẾT VÙNG TRỒNG -->
            <div class="flex-1 bg-white rounded-xl shadow-md border border-white p-5">
                  <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
                        <i class="fas fa-map-marked-alt text-green-600 text-lg"></i>
                        <h3 class="text-sm font-bold text-gray-700">Chi tiết Vùng trồng</h3>
                  </div>
                  
                  <div class="space-y-3">
                        <!-- Mã vùng -->
                        <div class="flex justify-between items-center">
                              <span class="text-xs text-gray-500">Mã vùng:</span>
                              <span class="text-sm font-bold text-blue-600">{{ props.selectedVung.ma }}</span>
                        </div>
                        
                        <!-- Tên vùng -->
                        <div class="flex justify-between items-center">
                              <span class="text-xs text-gray-500">Tên vùng:</span>
                              <span class="text-sm font-semibold text-gray-700">{{ props.selectedVung.ten }}</span>
                        </div>
                        
                        <!-- Chủ hộ -->
                        <div class="flex justify-between items-center">
                              <span class="text-xs text-gray-500">Chủ hộ:</span>
                              <span class="text-sm font-semibold text-gray-700">{{ props.selectedVung.chu }}</span>
                        </div>
                        
                        <!-- Trạng thái -->
                        <div class="flex justify-between items-center">
                              <span class="text-xs text-gray-500">Trạng thái:</span>
                              <span :class="getStatusClass(props.selectedVung.trangThai)" 
                                    class="text-xs font-semibold px-3 py-1 rounded">
                                    {{ getStatusText(props.selectedVung.trangThai) }}
                              </span>
                        </div>

                        <!-- Thống kê loại cây -->
                        <div v-if="cropsInZone.length > 0" class="pt-3 border-t border-gray-200 mt-4">
                              <div class="grid grid-cols-2 gap-3">
                                    <div class="bg-blue-50 p-3 rounded text-center">
                                          <p class="text-xs text-gray-500 mb-1">Tổng diện tích</p>
                                          <p class="text-lg font-bold text-blue-600">{{ totalAreaInZone.toFixed(1) }}</p>
                                          <p class="text-xs text-gray-500">ha</p>
                                    </div>
                                    <div class="bg-green-50 p-3 rounded text-center">
                                          <p class="text-xs text-gray-500 mb-1">Giá trị XK</p>
                                          <p class="text-lg font-bold text-green-600">${{ Math.round(totalExportValue / 1000) }}K</p>
                                          <p class="text-xs text-gray-500">USD</p>
                                    </div>
                              </div>
                        </div>

                        <!-- Thị trường xuất khẩu -->
                        <div v-if="marketsInZone.length > 0" class="pt-3 border-t border-gray-200">
                              <p class="text-xs text-gray-500 mb-2">Thị trường xuất khẩu:</p>
                              <div class="flex flex-wrap gap-2">
                                    <span v-for="market in marketsInZone" :key="market" 
                                          :class="getMarketBadgeClass(market)"
                                          class="px-2 py-1 rounded text-xs font-semibold">
                                          {{ market }}
                                    </span>
                              </div>
                        </div>

                        <!-- Danh sách loại cây -->
                        <div v-if="cropsInZone.length > 0" class="pt-3 border-t border-gray-200">
                              <p class="text-xs text-gray-500 mb-2 flex items-center gap-2">
                                    <i class="fas fa-seedling text-green-600"></i>
                                    Loại cây trồng:
                              </p>
                              <div class="space-y-2">
                                    <div v-for="crop in cropsInZone" :key="crop.id" 
                                         class="flex justify-between items-center bg-gray-50 p-2 rounded">
                                          <span class="text-xs font-semibold text-gray-700">{{ crop.tenCay }}</span>
                                          <span class="text-xs text-gray-500">{{ crop.dienTich }} ha</span>
                                    </div>
                              </div>
                        </div>
                  </div>
            </div>

            <!-- PHẦN 2: LỊCH SỬ CANH TÁC -->
            <div class="flex-1 bg-white rounded-xl shadow-md border border-white p-5">
                  <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
                        <i class="fas fa-clipboard-list text-blue-600 text-lg"></i>
                        <h3 class="text-sm font-bold text-gray-700">Lịch sử Canh tác gần đây</h3>
                  </div>

                  <div v-if="props.selectedVung.lichSuCanhTac && props.selectedVung.lichSuCanhTac.length > 0" 
                       class="space-y-3 max-h-[450px] overflow-y-auto scrollbar-custom">
                        <div v-for="(hoatDong, index) in props.selectedVung.lichSuCanhTac" 
                             :key="index"
                             class="border-l-4 border-blue-500 pl-3 py-2 bg-blue-50 rounded-r">
                              <div class="flex items-start gap-2">
                                    <div class="flex-shrink-0 bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs font-bold">
                                          {{ hoatDong.ngay }}
                                    </div>
                                    <div class="flex-1">
                                          <p class="text-sm font-semibold text-gray-800 mb-1">{{ hoatDong.hoatDong }}</p>
                                          <p class="text-xs text-gray-600 flex items-center gap-1">
                                                <i class="fas fa-user text-gray-400"></i>
                                                {{ hoatDong.nguoiThucHien }}
                                          </p>
                                    </div>
                              </div>
                        </div>
                  </div>

                  <div v-else class="flex flex-col items-center justify-center h-40 text-gray-400">
                        <i class="fas fa-inbox text-3xl mb-2"></i>
                        <p class="text-sm">Chưa có lịch sử canh tác</p>
                  </div>
            </div>

            <!-- PHẦN 3: MÃ QR -->
            <div class="w-64 bg-white rounded-xl shadow-md border border-white p-5">
                  <div class="flex items-center gap-2 mb-4 pb-3 border-b border-gray-200">
                        <i class="fas fa-qrcode text-purple-600 text-lg"></i>
                        <h3 class="text-sm font-bold text-gray-700">Mã QR Truy xuất</h3>
                  </div>

                  <div class="flex flex-col items-center gap-3">
                        <!-- QR Code (hiển thị trực tiếp) -->
                        <div class="w-48 h-48 bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg flex items-center justify-center border-2 border-gray-200 shadow-inner">
                              <div class="text-center">
                                    <i class="fas fa-qrcode text-6xl text-gray-400 mb-2"></i>
                                    <p class="text-xs text-gray-500">QR Code</p>
                              </div>
                        </div>

                        <!-- Mã số -->
                        <div class="text-center w-full">
                              <p class="text-xs text-gray-500 mb-1">Mã số:</p>
                              <p class="text-lg font-bold text-purple-600 bg-purple-50 py-2 px-4 rounded border border-purple-200">
                                    {{ props.selectedVung.maQR || props.selectedVung.ma }}
                              </p>
                        </div>

                        <!-- Link truy xuất -->
                        <a :href="`/truy-xuat/${props.selectedVung.maQR || props.selectedVung.ma}`" 
                           target="_blank"
                           class="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 px-4 rounded text-center transition-colors flex items-center justify-center gap-2">
                              <i class="fas fa-external-link-alt"></i>
                              Xem trang truy xuất
                        </a>

                        <!-- Hướng dẫn -->
                        <div class="bg-gray-50 p-3 rounded text-xs text-gray-600 w-full">
                              <p class="font-semibold mb-1 flex items-center gap-1">
                                    <i class="fas fa-info-circle text-blue-500"></i>
                                    Hướng dẫn:
                              </p>
                              <p>Quét mã QR để xem đầy đủ thông tin truy xuất nguồn gốc sản phẩm</p>
                        </div>
                  </div>
            </div>

      </div>

      <!-- No selection state -->
      <div v-else class="bg-white rounded-xl shadow-md border border-white p-10">
            <div class="flex flex-col items-center justify-center h-64">
                  <i class="fas fa-hand-pointer text-5xl text-gray-300 mb-4"></i>
                  <p class="text-gray-600 text-base font-semibold mb-2">Chọn vùng trồng để xem chi tiết</p>
                  <p class="text-gray-400 text-sm mb-4">Nhấn vào bảng hoặc bản đồ để xem:</p>
                  <div class="grid grid-cols-3 gap-4 mt-2">
                        <div class="text-center">
                              <i class="fas fa-map-marked-alt text-3xl text-green-500 mb-2"></i>
                              <p class="text-xs text-gray-500">Thông tin vùng</p>
                        </div>
                        <div class="text-center">
                              <i class="fas fa-clipboard-list text-3xl text-blue-500 mb-2"></i>
                              <p class="text-xs text-gray-500">Lịch sử canh tác</p>
                        </div>
                        <div class="text-center">
                              <i class="fas fa-qrcode text-3xl text-purple-500 mb-2"></i>
                              <p class="text-xs text-gray-500">Mã QR</p>
                        </div>
                  </div>
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
</style>
