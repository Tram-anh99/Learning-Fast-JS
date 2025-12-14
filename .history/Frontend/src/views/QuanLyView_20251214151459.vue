<script setup>
/**
 * ========== VIEW: QuanLyView.vue ==========
 * Purpose: Trang quản lý vùng trồng - Dashboard với thống kê, bản đồ và bảng dữ liệu
 * 
 * Architecture:
 *   - Components:
 *     • StatsBarComponent.vue - Thanh thống kê (số vùng, diện tích, v.v.)
 *     • MapComponent.vue - Bản đồ tương tác với polygon vùng trồng
 *     • DataTableComponent.vue - Bảng danh sách vùng với các chỉ số
 *     • ChartsComponent.vue - Biểu đồ thống kê
 *   - Styling: src/assets/styles/tailwind.css (Global utilities)
 *   - Libraries: Leaflet, Chart.js
 * 
 * Features:
 *   - Thống kê tổng quát hệ thống
 *   - Bản đồ tương tác hiển thị các vùng trồng
 *   - Biểu đồ phân tích dữ liệu
 *   - Bảng danh sách vùng trồng có thể sắp xếp và lọc
 */

// ========== IMPORTS ==========
// Import reactive ref từ Vue 3 Composition API
import { ref } from 'vue';

// Import CSS từ Leaflet (bản đồ)
import 'leaflet/dist/leaflet.css';

// ========== IMPORTS: Components ==========
// Thành phần thanh thống kê hiển thị số liệu hệ thống
import StatsBarComponent from '../components/StatsBarComponent.vue';

// Thành phần bản đồ tương tác (Leaflet)
import MapComponent from '../components/MapComponent.vue';

// Thành phần bảng danh sách vùng trồng với sắp xếp/lọc
import DataTableComponent from '../components/DataTableComponent.vue';

// Thành phần biểu đồ thống kê (Chart.js)
import ChartsComponent from '../components/ChartsComponent.vue';

// ========== IMPORTS: Composables & Mock Data ==========
// Import dữ liệu giả lập từ composable statusHelpers
import { mockDataThongKe, mockDataVung, mockDiemNongSauBenh } from '../composables/statusHelpers';

// ========== STATE ==========
/**
 * Dữ liệu thống kê hệ thống
 * - Số lượng vùng trồng
 * - Tổng diện tích canh tác
 * - Số vùng theo tình trạng (Đang canh tác, Thu hoạch, Nghỉ đất, v.v.)
 * - Các chỉ số khác (năng suất, chất lượng, v.v.)
 */
const thongKe = ref(mockDataThongKe);

// ========== DATA ==========
/**
 * Danh sách vùng trồng được quản lý
 * - id: ID duy nhất của vùng
 * - ma: Mã số vùng trồng (VT-001, VT-002, v.v.)
 * - ten: Tên vùng trồng
 * - dienTich: Diện tích (hectare)
 * - trangThai: Trạng thái canh tác
 * - chungNhan: Chứng chỉ (VietGAP, GlobalGAP, v.v.)
 * - anh: URL hình ảnh vùng
 * - toaDo: Tọa độ GPS (polygon) cho bản đồ
 * - nhatKy: Lịch sử hoạt động canh tác
 */
const danhSachVung = ref(mockDataVung);

// ========== METHODS ==========
// TODO: Các phương thức có thể thêm sau:
// - editVung(id) - Chỉnh sửa thông tin vùng
// - deleteVung(id) - Xóa vùng trồng
// - exportData() - Xuất dữ liệu ra CSV/Excel
// - importData(file) - Nhập dữ liệu từ file
// - filterByStatus(status) - Lọc vùng theo tình trạng
</script>

<template>
      <!-- Container layout chính - Position absolute toàn màn hình, Flex column -->
      <div class="absolute inset-0 bg-slate-100 flex flex-col p-5 gap-5">

            <!-- 1. Thanh thống kê ở trên cùng - Chiều cao cố định -->
            <!-- Props: :thongKe - Dữ liệu thống kê hệ thống -->
            <StatsBarComponent :thongKe="thongKe" />

            <!-- 2. Khu vực giữa: Biểu đồ & Bản đồ - Flex row, chiếm phần còn lại của không gian -->
            <div class="flex flex-[2] gap-5 min-h-0">

                  <!-- 2.1 Biểu đồ bên trái - Chiếm 1 phần của flex -->
                  <!-- min-w-[300px] - Chiều rộng tối thiểu 300px để responsive -->
                  <div class="flex-1 min-w-[300px]">
                        <!-- Thành phần biểu đồ thống kê (Chart.js) -->
                        <ChartsComponent />
                  </div>

                  <!-- 2.2 Bản đồ bên phải - Chiếm 2 phần của flex (lớn hơn biểu đồ) -->
                  <!-- Props:
           - :danhSachVung - Danh sách vùng trồng để hiển thị trên bản đồ
           - :diemNongSauBenh - Điểm dịch bệnh trên bản đồ
      -->
                  <MapComponent :danhSachVung="danhSachVung" :diemNongSauBenh="mockDiemNongSauBenh" />

            </div>

            <!-- 3. Bảng danh sách vùng ở dưới - Chiều cao cố định -->
            <!-- Props: :danhSachVung - Danh sách vùng trồng để hiển thị trong bảng -->
            <DataTableComponent :danhSachVung="danhSachVung" />

      </div>
</template>
