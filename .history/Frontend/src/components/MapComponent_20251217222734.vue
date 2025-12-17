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
      selectedVung: { type: Object, default: null },
      // cheDoXem: Chế độ xem bản đồ (hanh_chinh, sau_benh, phan_bon)
      cheDoXem: { type: String, default: 'hanh_chinh' }
});

// ========== EMITS ==========
const emit = defineEmits(['selectVung']);

// ========== STATE & METHODS FROM COMPOSABLE ==========
/**
 * Destructure state và methods từ useMapLogic composable
 * - mapContainer: ref để lưu DOM element bản đồ
 * - cheDoXem: current layer mode (sau_benh, phan_bon)
 * - batCheDoSauBenh: function toggle layer sâu bệnh
 * - initMap: function khởi tạo Leaflet map instance
 * - vẽMarkerVùng: function vẽ polygon cho các vùng
 */
const { mapContainer, cheDoXem, batCheDoSauBenh, initMap, vẽMarkerVùng } = useMapLogic();

// ========== LIFECYCLE ==========
/**
 * Hook: Khởi tạo bản đồ khi component mounted
 * - Gọi initMap() để tạo Leaflet instance
 * - Vẽ các polygon vùng trồng từ props.danhSachVung
 */
onMounted(() => {
      console.log('[MapComponent] onMounted - Initializing map');
      console.log('[MapComponent] danhSachVung:', props.danhSachVung);
      console.log('[MapComponent] mapContainer ref:', mapContainer.value);
      console.log('[MapComponent] cheDoXem prop:', props.cheDoXem);

      // Gọi initMap với mode 'dashboard'
      console.log('[MapComponent] Calling initMap with mode: dashboard');
      initMap('dashboard');

      console.log('[MapComponent] Map initialized, drawing polygons...');
      // Truyền callback để xử lý click event
      vẽMarkerVùng(props.danhSachVung, (vung) => {
            console.log('[MapComponent] Polygon clicked:', vung);
            emit('selectVung', vung);
      });

      console.log('[MapComponent] Polygons drawn');
});

// ========== HANDLERS ==========
/**
 * Handler: Toggle layer sâu bệnh khi user nhấn button
 */
const handleBatCheDoSauBenh = () => batCheDoSauBenh(props.diemNongSauBenh);
</script>

<template>
      <!-- Map container: flex-[2] = chiếm 2 phần (lớn hơn biểu đồ) -->
      <!-- rounded-xl = border-radius 12px, overflow-hidden = clip content, shadow-md = shadow mờ -->
      <!-- Responsive: min-height 250px trên mobile, 400px trên desktop -->
      <div class="flex-[2] relative rounded-xl overflow-hidden shadow-md min-h-[250px] sm:min-h-[300px] lg:min-h-[400px] h-full"
            style="background-color: #e0e0e0;">
            <!-- Leaflet map container: ref để Vue có thể lưu DOM element -->
            <!-- z-0 = layer thấp nhất, w-full h-full = 100% width & height -->
            <div ref="mapContainer" class="z-0 w-full h-full absolute inset-0"></div>
      </div>
</template>
<style scoped>
/* Styles removed - layer control now in separate component */
</style>