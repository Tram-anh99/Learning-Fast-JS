<script setup>
/**
 * ========== VIEW: QuanLyView.vue ==========
 * Mục đích: Trang Quản lý vùng trồng - Dashboard với thống kê, bản đồ tương tác và bảng dữ liệu
 * 
 * Kiến trúc:
 *   - Thành phần con:
 *     • StatsBarComponent.vue - Thanh thống kê hệ thống (số vùng, diện tích, cảnh báo)
 *     • MapComponent.vue - Bản đồ Leaflet tương tác với polygon vùng trồng
 *     • DataTableComponent.vue - Bảng danh sách vùng với thông tin chi tiết
 *     • ChartsComponent.vue - Biểu đồ thống kê (pie chart xuất khẩu, bar chart năng suất)
 *   - Styling: src/assets/styles/tailwind.css (Tailwind utilities toàn cục)
 *   - Thư viện: Leaflet (bản đồ), Chart.js (biểu đồ)
 * 
 * Tính năng:
 *   - Hiển thị thống kê tổng quát hệ thống (số vùng, diện tích, số vùng cảnh báo)
 *   - Bản đồ tương tác hiển thị vị trí các vùng trồng dưới dạng polygon
 *   - Lớp bản đồ có thể chuyển đổi (ảnh vệ tinh hoặc bản đồ đường phố)
 *   - Biểu đồ phân tích: Thị trường xuất khẩu (pie) và năng suất cây trồng (bar)
 *   - Bảng danh sách vùng có thể sắp xếp, lọc, chỉnh sửa
 */

// ========== IMPORTS ==========
// ref: Vue 3 Composition API hook để tạo reactive state
import { ref } from 'vue';

// CSS từ Leaflet (bản đồ) - Cần thiết để hiển thị bản đồ chính xác
import 'leaflet/dist/leaflet.css';

// ========== IMPORTS: Components ==========
// Thành phần thanh thống kê hiển thị số liệu tổng quát hệ thống
import StatsBarComponent from '../components/StatsBarComponent.vue';

// Thành phần bản đồ tương tác sử dụng Leaflet library
import MapComponent from '../components/MapComponent.vue';

// Thành phần bảng danh sách vùng trồng với sắp xếp/lọc
import DataTableComponent from '../components/DataTableComponent.vue';

// Thành phần biểu đồ thống kê sử dụng Chart.js library
import ChartsComponent from '../components/ChartsComponent.vue';

// ========== IMPORTS: Composables & Mock Data ==========
// Dữ liệu giả lập: Thống kê, danh sách vùng, điểm dịch bệnh
import { mockDataThongKe, mockDataVung, mockDiemNongSauBenh } from '../composables/statusHelpers';

// ========== STATE ==========
/**
 * thongKe: Dữ liệu thống kê hệ thống
 * Type: Ref<Object>
 * Structure: {tongVung, dienTich, canhBao, ...}
 * 
 * Thông tin chi tiết:
 *   - tongVung: Tổng số vùng trồng
 *   - dienTich: Tổng diện tích canh tác (hectare)
 *   - canhBao: Số vùng cần cảnh báo (sâu bệnh, dư lượng thuốc, v.v.)
 *   - các chỉ số khác: Năng suất, chất lượng, chi phí, v.v.
 * 
 * Ứng dụng:
 *   - Render trong StatsBarComponent ở đầu trang
 *   - Cập nhật thực thời từ API (hiện tại dùng mock data)
 */
const thongKe = ref(mockDataThongKe);

// ========== DATA ==========
/**
 * danhSachVung: Danh sách tất cả vùng trồng được quản lý
 * Type: Ref<Array>
 * Structure: Array<{id, ma, ten, dienTich, trangThai, chungNhan, anh, toaDo, nhatKy}>
 * 
 * Thông tin chi tiết mỗi vùng:
 *   - id: Định danh duy nhất (e.g., 'vung-001')
 *   - ma: Mã số vùng trồng (e.g., 'VT-001') - Dùng trên bản đồ WebGIS
 *   - ten: Tên vùng trồng (e.g., "Vùng Lúa Tây Đô - Khu A")
 *   - dienTich: Diện tích canh tác (hectare)
 *   - trangThai: Trạng thái hiện tại ('Đang canh tác', 'Thu hoạch', 'Nghỉ đất', v.v.)
 *   - chungNhan: Chứng chỉ góp nhặn (e.g., 'VietGAP', 'GlobalGAP', 'Organic')
 *   - anh: URL ảnh đại diện vùng
 *   - toaDo: Mảng tọa độ GPS để vẽ polygon trên bản đồ
 *   - nhatKy: Mảng các hoạt động canh tác đã thực hiện
 * 
 * Ứng dụng:
 *   - Render các marker/polygon trên bản đồ (MapComponent)
 *   - Render dòng dữ liệu trong bảng (DataTableComponent)
 *   - Cơ sở dữ liệu chính của quản lý vùng trồng
 */
const danhSachVung = ref(mockDataVung);

// ========== METHODS ==========
// TODO: Thêm các phương thức sau khi tích hợp API:
// - editVung(id): Chỉnh sửa thông tin vùng trồng
// - deleteVung(id): Xóa vùng trồng khỏi hệ thống
// - exportData(): Xuất dữ liệu ra file CSV/Excel
// - importData(file): Nhập dữ liệu từ file tải lên
// - filterByStatus(status): Lọc vùng theo tình trạng canh tác
// - updateStats(): Cập nhật thống kê từ API
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
