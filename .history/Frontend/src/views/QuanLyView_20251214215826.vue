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

// Thành phần biểu đồ đường (Line Chart) - Mối quan hệ thị trường & loại cây
import LineChartComponent from '../components/LineChartComponent.vue';

// Thành phần chi tiết loại cây cho vùng được chọn
import CropDetailsComponent from '../components/CropDetailsComponent.vue';

// ========== IMPORTS: Composables & Mock Data ==========
// Dữ liệu giả lập: Thống kê, danh sách vùng, điểm dịch bệnh
import { mockDataThongKe, mockDataVung, mockDiemNongSauBenh } from '../composables/statusHelpers';

// ========== STATE ==========
/**
 * thongKe: Dữ liệu thống kê hệ thống
 * Type: Ref<Object>
 */
const thongKe = ref(mockDataThongKe);

/**
 * danhSachVung: Danh sách tất cả vùng trồng được quản lý
 * Type: Ref<Array>
 */
const danhSachVung = ref(mockDataVung);

/**
 * selectedVung: Vùng được chọn từ bản đồ, bảng, hoặc biểu đồ
 * Type: Ref<Object|null>
 * Dùng để highlight/focus vùng trên các component khác
 */
const selectedVung = ref(null);

// ========== METHODS ==========
/**
 * Xử lý khi bấm vào row trong bảng danh sách
 */
const handleSelectVungFromTable = (vung) => {
      console.log("📍 QuanLyView - Table selected vung:", vung);
      selectedVung.value = vung;
      console.log("📍 QuanLyView - selectedVung.value updated:", selectedVung.value);
      // Có thể scroll tới vùng trên bản đồ hoặc highlight
};

/**
 * Xử lý khi bấm vào polygon trên bản đồ
 */
const handleSelectVungFromMap = (vung) => {
      console.log("🗺️ QuanLyView - Map selected vung:", vung);
      selectedVung.value = vung;
      console.log("🗺️ QuanLyView - selectedVung.value updated:", selectedVung.value);
      // Có thể highlight row trong bảng hoặc update biểu đồ
};

/**
 * Clear selection
 */
const clearSelection = () => {
      selectedVung.value = null;
};

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
      <!-- Layout chính: Chiếm toàn màn hình với scroll support -->
      <!-- h-screen: Chiều cao bằng viewport height -->
      <!-- flex flex-col: Bố cục dọc (các phần xếp từ trên xuống) -->
      <!-- p-5: Padding 20px xung quanh -->
      <!-- gap-5: Khoảng cách 20px giữa các phần -->
      <!-- overflow-y-auto: Cho phép cuộn dọc khi nội dung vượt quá màn hình -->
      <!-- scrollbar-custom: Thanh cuộn đẹp với màu xanh lá -->
      <div class="flex flex-col w-full h-screen gap-5 p-5 pb-[80px] overflow-y-auto bg-slate-100 scrollbar-custom">

            <!-- ========== SECTION 1: STATS BAR ========== -->
            <!-- Thanh thống kê ở trên cùng - Chiều cao tự động -->
            <!-- Props:
         - :thongKe - Dữ liệu thống kê hệ thống (tongVung, dienTich, canhBao)
         Output: 3 stat cards hiển thị các chỉ số chính
    -->
            <StatsBarComponent :thongKe="thongKe" />

            <!-- ========== SECTION 2: PIE CHART & MAP ========== -->
            <!-- Khu vực: Biểu đồ tròn (trái) & Bản đồ (phải) -->
            <!-- Chiều cao tự động theo nội dung -->
            <!-- gap-5: Khoảng cách 20px giữa biểu đồ tròn và bản đồ -->
            <div class="flex gap-5 min-h-[400px]">

                  <!-- ========== PIE CHART SECTION ========== -->
                  <!-- Biểu đồ tròn bên trái: Phân bổ thị trường xuất khẩu -->
                  <!-- w-1/3: Chiều rộng 33% (nhỏ hơn) -->
                  <div class="w-1/3 bg-white border border-white shadow-md rounded-xl p-4">
                        <!-- Component biểu đồ tròn -->
                        <PieChartComponent />
                  </div>

                  <!-- ========== MAP SECTION ========== -->
                  <!-- Bản đồ bên phải: Leaflet map với polygon vùng trồng -->
                  <!-- flex-1: Chiếm không gian còn lại (rộng hơn) -->
                  <!-- Props:
           - :danhSachVung - Danh sách vùng trồng để render polygon trên bản đồ
           - :diemNongSauBenh - Điểm dịch bệnh/rủi ro để hiển thị marker
           - :selectedVung - Vùng được chọn (highlight trên bản đồ)
      Events:
           - @selectVung - Phát ra khi bấm vào polygon
      -->
                  <MapComponent :danhSachVung="danhSachVung" :diemNongSauBenh="mockDiemNongSauBenh"
                        :selectedVung="selectedVung" @selectVung="handleSelectVungFromMap" />
            </div>

            <!-- ========== SECTION 3: BAR CHART & LINE CHART ========== -->
            <!-- Khu vực: Biểu đồ cột (trái) & Biểu đồ đường (phải) -->
            <!-- gap-5: Khoảng cách 20px giữa hai biểu đồ -->
            <div class="flex gap-5 min-h-[450px]">

                  <!-- ========== BAR CHART SECTION ========== -->
                  <!-- Biểu đồ cột bên trái: Năng suất cây trồng -->
                  <!-- w-1/3: Chiều rộng 33% -->
                  <div class="w-1/3 bg-white border border-white shadow-md rounded-xl p-4">
                        <!-- Component biểu đồ cột -->
                        <BarChartComponent />
                  </div>

                  <!-- ========== LINE CHART SECTION ========== -->
                  <!-- Biểu đồ đường bên phải: Mối quan hệ thị trường & loại cây -->
                  <!-- flex-1: Chiếm không gian còn lại (rộng hơn) -->
                  <div class="flex-1 bg-white border border-white shadow-md rounded-xl p-4">
                        <!-- Component biểu đồ đường -->
                        <LineChartComponent />
                  </div>

            </div>

            <!-- ========== SECTION 4: CROP DETAILS ========== -->
            <!-- Chi tiết loại cây của vùng được chọn -->
            <!-- Hiển thị danh sách loại cây, diện tích, năng suất, thị trường xuất khẩu -->
            <CropDetailsComponent :selectedVung="selectedVung.value" />

            <!-- ========== SECTION 5: DATA TABLE ========== -->
            <!-- Bảng danh sách vùng -->
            <!-- Chiều cao tự động theo nội dung -->
            <!-- Props:
         - :danhSachVung - Danh sách vùng trồng để render trong bảng
         - :selectedVung - Vùng được chọn (highlight row)
         Events:
         - @selectVung - Phát ra khi bấm vào row
         Features: Sắp xếp theo cột, lọc, chỉnh sửa inline
    -->
            <DataTableComponent :danhSachVung="danhSachVung" :selectedVung="selectedVung"
                  @selectVung="handleSelectVungFromTable" />

            <!-- ========== FOOTER ========== -->
            <footer class="mt-8 pt-6 pb-4 border-t border-gray-200 text-center text-gray-600 text-sm">
                  <p>&copy; 2024 Hệ thống Quản lý Nông nghiệp. Phát triển bởi <span
                              class="font-semibold text-gray-800">Dev Team</span></p>
                  <p class="mt-2 text-xs text-gray-500">Cập nhật lần cuối: <span class="font-medium">{{ new
                        Date().toLocaleDateString('vi-VN') }}</span></p>
            </footer>
      </div>
</template>
