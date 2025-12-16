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
import QrcodeVue from 'qrcode.vue';

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

// ========== FUNCTION: Lấy class cho trạng thái ==========
const getStatusClass = (status) => {
      const classes = {
            'canh_tac': 'bg-green-100 text-green-700',
            'sau_benh': 'bg-red-100 text-red-700',
            'thu_hoach': 'bg-yellow-100 text-yellow-700',
            'da_thu_hoach': 'bg-blue-100 text-blue-700',
      };
      return classes[status] || 'bg-gray-100 text-gray-700';
};

// ========== FUNCTION: Lấy text cho trạng thái ==========
const getStatusText = (status) => {
      const texts = {
            'canh_tac': 'Đang canh tác',
            'sau_benh': 'Cảnh báo dịch hại',
            'thu_hoach': 'Đang thu hoạch',
            'da_thu_hoach': 'Đã thu hoạch',
      };
      return texts[status] || 'Không xác định';
};

// ========== COMPUTED: QR Code URL ==========
const qrCodeUrl = computed(() => {
      const baseUrl = window.location.origin;
      const maQR = props.selectedVung?.maQR || props.selectedVung?.ma || '';
      return `${baseUrl}/truy-xuat/${maQR}`;
});
</script>

<template>
      <!-- Container chính - Responsive -->
      <div v-if="props.selectedVung" class="flex flex-col lg:flex-row gap-5">

            <!-- PHẦN 1: CHI TIẾT VÙNG TRỒNG -->
            <div class="w-full lg:flex-1 p-5 shadow-md rounded-xl" style="background-color: white;">
                  <div class="flex items-center gap-2 pb-3 mb-4 border-b-2" style="border-color: #24504b;">
                        <i class="text-lg fas fa-map-marked-alt" style="color: #24504b;"></i>
                        <h3 class="text-sm font-bold" style="color: #24504b;">Chi tiết Vùng trồng</h3>
                  </div>

                  <div class="space-y-3">
                        <!-- Mã vùng -->
                        <div class="flex items-center justify-between">
                              <span class="text-xs" style="color: rgba(36, 80, 75, 0.6);">Mã vùng:</span>
                              <span class="text-sm font-bold" style="color: #24504b;">{{ props.selectedVung.ma }}</span>
                        </div>

                        <!-- Tên vùng -->
                        <div class="flex items-center justify-between">
                              <span class="text-xs" style="color: rgba(36, 80, 75, 0.6);">Tên vùng:</span>
                              <span class="text-sm font-semibold" style="color: #24504b;">{{ props.selectedVung.ten
                              }}</span>
                        </div>

                        <!-- Chủ hộ -->
                        <div class="flex items-center justify-between">
                              <span class="text-xs" style="color: rgba(36, 80, 75, 0.6);">Chủ hộ:</span>
                              <span class="text-sm font-semibold" style="color: #24504b;">{{ props.selectedVung.chu
                              }}</span>
                        </div>

                        <!-- Trạng thái -->
                        <div class="flex items-center justify-between">
                              <span class="text-xs" style="color: rgba(36, 80, 75, 0.6);">Trạng thái:</span>
                              <span :class="getStatusClass(props.selectedVung.trangThai)"
                                    class="px-3 py-1 text-xs font-semibold rounded">
                                    {{ getStatusText(props.selectedVung.trangThai) }}
                              </span>
                        </div>

                        <!-- Thống kê loại cây -->
                        <div v-if="cropsInZone.length > 0" class="pt-3 mt-4 border-t" style="border-color: #24504b;">
                              <div class="grid grid-cols-2 gap-3">
                                    <div class="p-3 text-center rounded"
                                          style="background-color: rgba(36, 80, 75, 0.1);">
                                          <p class="mb-1 text-xs" style="color: rgba(36, 80, 75, 0.6);">Tổng diện tích
                                          </p>
                                          <p class="text-lg font-bold" style="color: #24504b;">{{
                                                totalAreaInZone.toFixed(1) }}
                                          </p>
                                          <p class="text-xs" style="color: rgba(36, 80, 75, 0.6);">ha</p>
                                    </div>
                                    <div class="p-3 text-center rounded"
                                          style="background-color: rgba(36, 80, 75, 0.1);">
                                          <p class="mb-1 text-xs" style="color: rgba(36, 80, 75, 0.6);">Giá trị XK</p>
                                          <p class="text-lg font-bold" style="color: #24504b;">${{
                                                Math.round(totalExportValue /
                                                      1000) }}K</p>
                                          <p class="text-xs" style="color: rgba(36, 80, 75, 0.6);">USD</p>
                                    </div>
                              </div>
                        </div>

                        <!-- Thị trường xuất khẩu -->
                        <div v-if="marketsInZone.length > 0" class="pt-3 border-t" style="border-color: #24504b;">
                              <p class="mb-2 text-xs" style="color: rgba(36, 80, 75, 0.6);">Thị trường xuất khẩu:</p>
                              <div class="flex flex-wrap gap-2">
                                    <span v-for="market in marketsInZone" :key="market"
                                          :class="getMarketBadgeClass(market)"
                                          class="px-2 py-1 text-xs font-semibold rounded">
                                          {{ market }}
                                    </span>
                              </div>
                        </div>

                        <!-- Danh sách loại cây -->
                        <div v-if="cropsInZone.length > 0" class="pt-3 border-t" style="border-color: #24504b;">
                              <p class="flex items-center gap-2 mb-2 text-xs" style="color: rgba(36, 80, 75, 0.6);">
                                    <i class="fas fa-seedling" style="color: #24504b;"></i>
                                    Loại cây trồng:
                              </p>
                              <div class="space-y-2">
                                    <div v-for="crop in cropsInZone" :key="crop.id"
                                          class="flex items-center justify-between p-2 rounded"
                                          style="background-color: rgba(36, 80, 75, 0.05);">
                                          <span class="text-xs font-semibold" style="color: #24504b;">{{ crop.tenCay
                                          }}</span>
                                          <span class="text-xs" style="color: rgba(36, 80, 75, 0.6);">{{ crop.dienTich
                                          }} ha</span>
                                    </div>
                              </div>
                        </div>
                  </div>
            </div>

            <!-- PHẦN 2: LỊCH SỬ CANH TÁC -->
            <div class="w-full lg:flex-1 p-5 shadow-md rounded-xl" style="background-color: white;">
                  <div class="flex items-center gap-2 pb-3 mb-4 border-b-2" style="border-color: #24504b;">
                        <i class="text-lg fas fa-clipboard-list" style="color: #24504b;"></i>
                        <h3 class="text-sm font-bold" style="color: #24504b;">Lịch sử Canh tác gần đây</h3>
                  </div>

                  <div v-if="props.selectedVung.lichSuCanhTac && props.selectedVung.lichSuCanhTac.length > 0"
                        class="space-y-3 max-h-[450px] overflow-y-auto scrollbar-custom">
                        <div v-for="(hoatDong, index) in props.selectedVung.lichSuCanhTac" :key="index"
                              class="py-2 pl-3 border-l-4 rounded-r"
                              style="border-color: #24504b; background-color: rgba(36, 80, 75, 0.1);">
                              <div class="flex items-start gap-2">
                                    <div class="flex-shrink-0 px-2 py-1 text-xs font-bold rounded"
                                          style="color: #24504b; background-color: rgba(36, 80, 75, 0.2);">
                                          {{ hoatDong.ngay }}
                                    </div>
                                    <div class="flex-1">
                                          <p class="mb-1 text-sm font-semibold" style="color: #24504b;">{{
                                                hoatDong.hoatDong }}
                                          </p>
                                          <p class="flex items-center gap-1 text-xs"
                                                style="color: rgba(36, 80, 75, 0.7);">
                                                <i class="fas fa-user" style="color: rgba(36, 80, 75, 0.5);"></i>
                                                {{ hoatDong.nguoiThucHien }}
                                          </p>
                                    </div>
                              </div>
                        </div>
                  </div>

                  <div v-else class="flex flex-col items-center justify-center h-40 text-gray-400">
                        <i class="mb-2 text-3xl fas fa-inbox"></i>
                        <p class="text-sm">Chưa có lịch sử canh tác</p>
                  </div>
            </div>

            <!-- PHẦN 3: MÃ QR -->
            <div class="w-full lg:w-64 p-5 shadow-md rounded-xl" style="background-color: white;">
                  <div class="flex items-center gap-2 pb-3 mb-4 border-b-2" style="border-color: #24504b;">
                        <i class="text-lg fas fa-qrcode" style="color: #24504b;"></i>
                        <h3 class="text-sm font-bold" style="color: #24504b;">Mã QR Truy xuất</h3>
                  </div>

                  <div class="flex flex-col items-center gap-3">
                        <!-- QR Code (hiển thị thật với qrcode.vue) -->
                        <div class="relative flex justify-center">
                              <div class="relative">
                                    <!-- Glow effect -->
                                    <div class="absolute inset-0 transition-opacity duration-300 rounded-xl blur-lg opacity-20 hover:opacity-40"
                                          style="background: linear-gradient(to right, #24504b, #24504b);">
                                    </div>

                                    <!-- QR Card -->
                                    <div
                                          class="relative p-4 transition-all duration-300 bg-white shadow-lg rounded-xl hover:shadow-xl">
                                          <QrcodeVue :value="qrCodeUrl" :size="180" level="H" render-as="svg"
                                                foreground="#24504b" />
                                    </div>
                              </div>
                        </div>

                        <!-- Mã số -->
                        <div class="w-full text-center">
                              <p class="mb-1 text-xs" style="color: rgba(36, 80, 75, 0.6);">Mã số:</p>
                              <p class="px-4 py-2 text-lg font-bold border rounded"
                                    style="color: #24504b; border-color: #24504b; background-color: rgba(36, 80, 75, 0.1);">
                                    {{ props.selectedVung.maQR || props.selectedVung.ma }}
                              </p>
                        </div>

                        <!-- Link truy xuất -->
                        <a :href="`/truy-xuat/${props.selectedVung.maQR || props.selectedVung.ma}`" target="_blank"
                              class="flex items-center justify-center w-full gap-2 px-4 py-2 text-sm font-semibold text-center transition-colors rounded"
                              style="background-color: #24504b; color: #fbfced;"
                              @mouseover="$event.target.style.opacity = '0.9'"
                              @mouseout="$event.target.style.opacity = '1'">
                              <i class="fas fa-external-link-alt"></i>
                              Xem trang truy xuất
                        </a>

                        <!-- Hướng dẫn -->
                        <div class="w-full p-3 text-xs rounded"
                              style="background-color: rgba(36, 80, 75, 0.1); color: #24504b;">
                              <p class="flex items-center gap-1 mb-1 font-semibold">
                                    <i class="fas fa-info-circle"></i>
                                    Hướng dẫn:
                              </p>
                              <p>Quét mã QR để xem đầy đủ thông tin truy xuất nguồn gốc sản phẩm</p>
                        </div>
                  </div>
            </div>

      </div>

      <!-- No selection state -->
      <div v-else class="p-10 shadow-md rounded-xl" style="background-color: white;">
            <div class="flex flex-col items-center justify-center h-64">
                  <i class="mb-4 text-5xl" style="color: rgba(36, 80, 75, 0.3);"></i>
                  <p class="mb-2 text-base font-semibold" style="color: #24504b;">Chọn vùng trồng để xem chi tiết</p>
                  <p class="mb-4 text-sm" style="color: rgba(36, 80, 75, 0.6);">Nhấn vào bảng hoặc bản đồ để xem:</p>
                  <div class="grid grid-cols-3 gap-4 mt-2">
                        <div class="text-center">
                              <i class="mb-2 text-3xl fas fa-map-marked-alt" style="color: #24504b;"></i>
                              <p class="text-xs" style="color: rgba(36, 80, 75, 0.6);">Thông tin vùng</p>
                        </div>
                        <div class="text-center">
                              <i class="mb-2 text-3xl fas fa-clipboard-list" style="color: #24504b;"></i>
                              <p class="text-xs" style="color: rgba(36, 80, 75, 0.6);">Lịch sử canh tác</p>
                        </div>
                        <div class="text-center">
                              <i class="mb-2 text-3xl fas fa-qrcode" style="color: #24504b;"></i>
                              <p class="text-xs" style="color: rgba(36, 80, 75, 0.6);">Mã QR</p>
                        </div>
                  </div>
            </div>
      </div>
</template>

<style scoped>
/* Custom scrollbar for activity history */
.scrollbar-custom::-webkit-scrollbar {
      width: 6px;
}

.scrollbar-custom::-webkit-scrollbar-track {
      background: rgba(251, 252, 237, 0.5);
      border-radius: 10px;
}

.scrollbar-custom::-webkit-scrollbar-thumb {
      background: #24504b;
      border-radius: 10px;
}

.scrollbar-custom::-webkit-scrollbar-thumb:hover {
      background: rgba(36, 80, 75, 0.8);
}
</style>
