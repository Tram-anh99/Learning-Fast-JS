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

// CSS scrollbar custom - Dùng cho các element có scroll
import '../assets/styles/scrollbar.css';

// ========== IMPORTS: Components ==========
// Thành phần thanh thống kê hiển thị số liệu tổng quát hệ thống
import StatsBarComponent from '../components/StatsBarComponent.vue';

// Thành phần bản đồ tương tác sử dụng Leaflet library
import MapComponent from '../components/MapComponent.vue';

// Thành phần bảng danh sách vùng trồng với sắp xếp/lọc
import DataTableComponent from '../components/DataTableComponent.vue';

// Thành phần biểu đồ tròn (Pie Chart) - Thị trường xuất khẩu
import PieChartComponent from '../components/PieChartComponent.vue';

// Thành phần biểu đồ cột (Bar Chart) - Năng suất cây trồng
import BarChartComponent from '../components/BarChartComponent.vue';

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
      <!-- ========== MAIN CONTAINER ========== -->
      <!-- Layout chính: Toàn màn hình với scroll support -->
      <!-- min-h-screen: Tối thiểu chiều cao viewport -->
      <!-- flex flex-col: Bố cục dọc (các phần xếp từ trên xuống) -->
      <!-- p-5: Padding 20px xung quanh -->
      <!-- gap-5: Khoảng cách 20px giữa các phần -->
      <!-- overflow-y-auto: Cho phép cuộn dọc khi nội dung vượt quá màn hình -->
      <!-- scrollbar-custom: Thanh cuộn đẹp với màu xanh lá -->
      <div class="flex flex-col gap-5 p-5 bg-slate-100 overflow-y-auto scrollbar-custom w-full h-full">

            <!-- ========== SECTION 1: STATS BAR ========== -->
            <!-- Thanh thống kê ở trên cùng - Chiều cao tự động, fixed layout -->
            <!-- Props:
         - :thongKe - Dữ liệu thống kê hệ thống (tongVung, dienTich, canhBao)
         Output: 3 stat cards hiển thị các chỉ số chính
    -->
            <StatsBarComponent :thongKe="thongKe" />

            <!-- ========== SECTION 2: PIE CHART & MAP ========== -->
            <!-- Khu vực giữa (trên): Biểu đồ tròn (trái) & Bản đồ (phải) -->
            <!-- h-80: Fixed height 320px (20rem) -->
            <!-- gap-5: Khoảng cách 20px giữa biểu đồ tròn và bản đồ -->
            <div class="flex h-80 gap-5">

                  <!-- ========== PIE CHART SECTION ========== -->
                  <!-- Biểu đồ tròn bên trái: Phân bổ thị trường xuất khẩu -->
                  <!-- flex-1: Chiếm 1 phần của flex space -->
                  <!-- min-w-[300px]: Chiều rộng tối thiểu 300px để responsive trên màn hình nhỏ -->
                  <div class="flex-1 min-w-[300px] bg-white border border-white shadow-md rounded-xl p-4 overflow-hidden">
                        <!-- Component biểu đồ tròn -->
                        <PieChartComponent />
                  </div>

                  <!-- ========== MAP SECTION ========== -->
                  <!-- Bản đồ bên phải: Leaflet map với polygon vùng trồng -->
                  <!-- flex-[1.5]: Chiếm 1.5 phần của flex space (rộng hơn biểu đồ tròn) -->
                  <!-- Props:
           - :danhSachVung - Danh sách vùng trồng để render polygon trên bản đồ
           - :diemNongSauBenh - Điểm dịch bệnh/rủi ro để hiển thị marker
      -->
                  <MapComponent :danhSachVung="danhSachVung" :diemNongSauBenh="mockDiemNongSauBenh" />
            </div>

            <!-- ========== SECTION 3: BAR CHART ========== -->
            <!-- Biểu đồ cột: Năng suất cây trồng - hiển thị hết nội dung -->
            <!-- h-96: Fixed height 384px (24rem) - tăng từ h-72 để hiển thị hết -->
            <div class="bg-white border border-white shadow-md rounded-xl p-4 h-96 overflow-hidden">
                  <!-- Component biểu đồ cột -->
                  <BarChartComponent />
            </div>

            <!-- ========== SECTION 4: DATA TABLE ========== -->
            <!-- Bảng danh sách vùng - hiển thị hết nội dung -->
            <!-- h-96: Fixed height 384px (24rem) - tăng từ h-80 để hiển thị hết dòng và có thanh cuộn -->
            <!-- Props:
         - :danhSachVung - Danh sách vùng trồng để render trong bảng
         Features: Sắp xếp theo cột, lọc, chỉnh sửa inline
    -->
            <DataTableComponent :danhSachVung="danhSachVung" />
      </div>
</template>
