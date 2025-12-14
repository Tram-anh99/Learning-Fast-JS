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

// Debug watch
watch(() => props.selectedVung, (newVal) => {
      console.log("👀 CropDetails watch - selectedVung changed:", newVal);
}, { deep: true });

// ========== COMPUTED: Danh sách cây của vùng được chọn ==========
const cropsInZone = computed(() => {
      // selectedVung là Object (đã unwrap từ parent's .value)
      if (!props.selectedVung?.ma) return [];
      console.log("🌾 CropDetails - Selected vung:", props.selectedVung);
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
      <div v-if="props.selectedVung" class="panel flex flex-col min-h-[350px] max-h-[600px] overflow-auto">
            <!-- Header -->
            <div class="panel-header">
                  <div class="flex-1">
                        <h3 class="panel-title">Chi tiết Loại cây - {{ props.selectedVung.ma }}</h3>
                        <p class="text-xs text-gray-500 mt-1">{{ props.selectedVung.ten }}</p>
                  </div>
                  <div class="text-right text-xs">
                        <p class="font-semibold text-gray-600">Tổng diện tích: <span class="text-blue-600">{{
                                    totalAreaInZone.toFixed(1) }} ha</span></p>
                        <p class="font-semibold text-gray-600 mt-1">Giá trị xuất khẩu: <span class="text-green-600">${{
                              Math.round(totalExportValue).toLocaleString() }}</span></p>
                  </div>
            </div>

            <!-- Thị trường xuất khẩu badges -->
            <div v-if="marketsInZone.length > 0" class="px-4 py-2 bg-gray-50 border-b border-gray-200">
                  <p class="text-xs font-semibold text-gray-600 mb-2">Thị trường xuất khẩu:</p>
                  <div class="flex flex-wrap gap-2">
                        <span v-for="market in marketsInZone" :key="market" :class="getMarketBadgeClass(market)"
                              class="px-2 py-1 rounded text-xs font-semibold">
                              {{ market }}
                        </span>
                  </div>
            </div>

            <!-- Scrollable crop table -->
            <div class="overflow-y-auto flex-grow scrollbar-custom">
                  <table class="w-full border-collapse">
                        <thead class="sticky top-0 z-10 bg-white shadow-sm">
                              <tr>
                                    <th class="table-header">Loại cây</th>
                                    <th class="table-header">Diện tích (ha)</th>
                                    <th class="table-header">Năm trồng</th>
                                    <th class="table-header">Năng suất (tạ/ha)</th>
                                    <th class="table-header">Giá xuất (USD/kg)</th>
                                    <th class="table-header">Giá trị (USD)</th>
                                    <th class="table-header">Thị trường</th>
                              </tr>
                        </thead>
                        <tbody>
                              <tr v-for="crop in cropsInZone" :key="crop.id" class="table-row-hover">
                                    <td class="table-cell"><strong>{{ crop.tenCay }}</strong></td>
                                    <td class="table-cell text-center">{{ crop.dienTich }}</td>
                                    <td class="table-cell text-center">{{ crop.namTrau }}</td>
                                    <td class="table-cell text-center font-semibold">{{ crop.nangSuat }}</td>
                                    <td class="table-cell text-center text-green-600 font-semibold">${{ crop.giaXuat }}
                                    </td>
                                    <td class="table-cell text-center font-semibold text-blue-600">${{
                                          Math.round(crop.dienTich * crop.nangSuat * crop.giaXuat).toLocaleString() }}
                                    </td>
                                    <td class="table-cell">
                                          <div class="flex flex-wrap gap-1">
                                                <span v-for="market in crop.thiBruongXuatKhau" :key="market"
                                                      :class="getMarketBadgeClass(market)"
                                                      class="px-1.5 py-0.5 rounded text-xs font-semibold">
                                                      {{ market }}
                                                </span>
                                          </div>
                                    </td>
                              </tr>
                        </tbody>
                  </table>

                  <!-- Empty state -->
                  <div v-if="cropsInZone.length === 0" class="flex items-center justify-center h-32 text-gray-400">
                        <p>Không có dữ liệu loại cây cho vùng này</p>
                  </div>
            </div>
      </div>

      <!-- No selection state -->
      <div v-else class="panel flex flex-col items-center justify-center min-h-[350px] max-h-[600px]">
            <i class="fas fa-info-circle text-4xl text-gray-300 mb-3"></i>
            <p class="text-gray-500 text-sm">Chọn vùng trồng từ bảng hoặc bản đồ để xem chi tiết loại cây</p>
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
