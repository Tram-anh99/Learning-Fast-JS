<script setup>
/**
 * ========== COMPONENT: MapComponent.vue ==========
 * Purpose: Leaflet interactive map với polygon vùng trồng và layer controls
 * 
 * Features:
 *   - Hiển thị vùng trồng dưới dạng polygon trên bản đồ
 *   - Layer control: Hành chính, Sâu bệnh, Dư lượng thuốc
 *   - Tích hợp với useMapLogic composable
 * 
 * Props:
 *   - danhSachVung: Array - Danh sách vùng trồng để vẽ polygon
 *   - diemNongSauBenh: Array - Điểm dịch bệnh để hiển thị
 * 
 * Related Files:
 *   - src/composables/useMapLogic.js - Logic bản đồ
 *   - src/views/QuanLyView.vue - Parent component
 */

// ========== IMPORTS ==========
// Import onMounted hook từ Vue 3 Composition API
import { onMounted } from 'vue';
// Import composable chứa logic bản đồ (Leaflet)
import { useMapLogic } from '../composables/useMapLogic';

// ========== PROPS ==========
/**
 * Props nhận từ parent component
 * - danhSachVung: Danh sách vùng trồng với tọa độ polygon
 * - diemNongSauBenh: Danh sách điểm dịch bệnh trên bản đồ
 */
const props = defineProps({
      // danhSachVung: Array chứa các object vùng trồng { id, ten, toaDo }
      danhSachVung: { type: Array, required: true },
      // diemNongSauBenh: Array chứa các điểm dịch bệnh { lat, lng, type }
      diemNongSauBenh: { type: Array, required: true },
      // selectedVung: Vùng được chọn (để highlight)
      selectedVung: { type: Object, default: null }
});

// ========== EMITS ==========
const emit = defineEmits(['selectVung']);

// ========== STATE & METHODS FROM COMPOSABLE ==========
/**
 * Destructure state và methods từ useMapLogic composable
 * - mapContainer: ref để lưu DOM element bản đồ
 * - cheDoXem: current layer mode (hanh_chinh, sau_benh, phan_bon)
 * - batCheDoSauBenh: function mở layer sâu bệnh
 * - batCheDoHanhChinh: function mở layer hành chính
 * - initMap: function khởi tạo Leaflet map instance
 * - vẽMarkerVùng: function vẽ polygon cho các vùng
 */
const { mapContainer, cheDoXem, batCheDoSauBenh, batCheDoHanhChinh, initMap, vẽMarkerVùng } = useMapLogic();

// ========== LIFECYCLE ==========
/**
 * Hook: Khởi tạo bản đồ khi component mounted
 * - Gọi initMap() để tạo Leaflet instance
 * - Vẽ các polygon vùng trồng từ props.danhSachVung
 */
onMounted(() => {
      initMap();
      // Truyền callback để xử lý click event
      vẽMarkerVùng(props.danhSachVung, (vung) => {
            emit('selectVung', vung);
      });
});

// ========== HANDLERS ==========
/**
 * Handler: Mở layer sâu bệnh khi user nhấn button
 */
const handleBatCheDoSauBenh = () => batCheDoSauBenh(props.diemNongSauBenh);
</script>

<template>
      <!-- Map container: flex-[2] = chiếm 2 phần (lớn hơn biểu đồ) -->
      <!-- rounded-xl = border-radius 12px, overflow-hidden = clip content, shadow-md = shadow mờ -->
      <div class="flex-[2] relative rounded-xl overflow-hidden shadow-md border border-white">
            <!-- Leaflet map container: ref để Vue có thể lưu DOM element -->
            <!-- z-0 = layer thấp nhất, w-full h-full = 100% width & height -->
            <div ref="mapContainer" class="z-0 w-full h-full"></div>

            <!-- Layer control panel: floating button group ở góc trên phải -->
            <!-- absolute top-5 right-5 = vị trí cố định, z-50 = layer cao hơn map -->
            <div class="absolute top-5 right-5 z-50 bg-white p-2.5 rounded-lg shadow-lg flex flex-col gap-2 w-44">
                  <!-- Control panel header: tiêu đề "Lớp dữ liệu" -->
                  <!-- text-xs font-semibold = font chữ nhỏ, in đậm -->
                  <h4 class="m-0 text-xs font-semibold uppercase text-slate-600">
                        <!-- Icon: biểu tượng layer-group (nhiều lớp) -->
                        <i class="fas fa-layer-group"></i> Lớp dữ liệu
                  </h4>

                  <!-- Button 1: Layer Sâu bệnh (Mật độ dịch bệnh) -->
                  <!-- Toggle on/off heatmap dịch bệnh khi click -->
                  <button :class="{ 'map-control-btn-active': cheDoXem === 'sau_benh' }" @click="handleBatCheDoSauBenh"
                        class="map-control-btn">
                        <!-- Icon: biểu tượng nguy hiểm sinh học -->
                        <i class="fas fa-biohazard"></i> Mật độ Sâu bệnh
                  </button>

                  <!-- Button 2: Layer Dư lượng thuốc (Phân tích hóa chất) -->
                  <button :class="{ 'map-control-btn-active': cheDoXem === 'phan_bon' }" class="map-control-btn">
                        <!-- Icon: biểu tượng bình đựng -->
                        <i class="fas fa-flask"></i> Dư lượng Thuốc
                  </button>
            </div>
      </div>
</template>
