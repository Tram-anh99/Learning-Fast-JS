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

// Thành phần điều khiển lớp dữ liệu bản đồ
import MapLayerControl from '../components/MapLayerControl.vue';

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
      selectedVung.value = vung;
};

/**
 * Xử lý khi bấm vào polygon trên bản đồ
 */
const handleSelectVungFromMap = (vung) => {
      selectedVung.value = vung;
};

/**
 * Clear selection
 */
const clearSelection = () => {
      selectedVung.value = null;
};

/**
 * Chế độ xem bản đồ
 */
const cheDoXem = ref('hanh_chinh');

/**
 * Toggle layer sâu bệnh
 */
const handleToggleSauBenh = () => {
      cheDoXem.value = cheDoXem.value === 'sau_benh' ? 'hanh_chinh' : 'sau_benh';
};

/**
 * Toggle layer dư lượng thuốc
 */
const handleToggleDuLuongThuoc = () => {
      cheDoXem.value = cheDoXem.value === 'phan_bon' ? 'hanh_chinh' : 'phan_bon';
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
      <div class="flex flex-col w-full h-screen gap-4 sm:gap-5 p-3 sm:p-5 pb-[80px] overflow-y-auto scrollbar-custom"
            style="background-color: #fbfced;">

            <!-- ========== SECTION 1: STATS BAR ========== -->
            <!-- Thanh thống kê ở trên cùng - Chiều cao tự động -->
            <!-- Props:
         - :thongKe - Dữ liệu thống kê hệ thống (tongVung, dienTich, canhBao)
         Output: 3 stat cards hiển thị các chỉ số chính
    -->
            <StatsBarComponent :thongKe="thongKe" />

            <!-- ========== INSIGHT PANEL ========== -->
            <!-- Panel hướng dẫn ra quyết định - giải thích mối liên hệ giữa các biểu đồ -->
            <div class="bg-gradient-to-r from-[#24504b] to-[#1a3d39] text-white p-3 sm:p-4 rounded-xl shadow-lg">
                  <div class="flex items-start gap-3">
                        <i class="fas fa-lightbulb text-yellow-300 text-lg sm:text-xl flex-shrink-0 mt-0.5"></i>
                        <div class="text-xs sm:text-sm">
                              <p class="font-bold mb-1">💡 Hỗ trợ ra quyết định:</p>
                              <p class="opacity-90 leading-relaxed">
                                    <span class="font-semibold text-yellow-200">Biểu đồ tròn</span> cho thấy thị trường nào đang mang lại giá trị cao nhất → 
                                    <span class="font-semibold text-green-200">Biểu đồ cột</span> cho biết cây nào có năng suất tốt → 
                                    <span class="font-semibold text-blue-200">Biểu đồ đường</span> thể hiện cây nào phù hợp với thị trường nào để tối ưu lợi nhuận.
                              </p>
                        </div>
                  </div>
            </div>

            <!-- ========== SECTION 2: PIE CHART & MAP & LAYER CONTROL ========== -->
            <!-- Khu vực: Biểu đồ tròn (trái) & Bản đồ (giữa) & Layer Control (phải) -->
            <!-- Responsive: Dọc trên mobile, ngang trên desktop -->
            <!-- Mobile 6 inch: h-[280px], Tablet+: h-[400px] -->
            <div class="flex flex-col lg:flex-row gap-4 sm:gap-5">

                  <!-- ========== PIE CHART SECTION ========== -->
                  <!-- Biểu đồ tròn: Full width trên mobile, 25% trên desktop -->
                  <div class="w-full lg:w-1/4 p-3 sm:p-4 shadow-md rounded-xl h-[280px] sm:h-[350px] lg:h-[400px]" style="background-color: white;">
                        <!-- Component biểu đồ tròn -->
                        <PieChartComponent />
                  </div>

                  <!-- ========== MAP SECTION ========== -->
                  <!-- Bản đồ: Full width trên mobile, flex-1 trên desktop -->
                  <div class="w-full lg:flex-1 h-[280px] sm:h-[350px] lg:h-[400px]">
                        <MapComponent :danhSachVung="danhSachVung" :diemNongSauBenh="mockDiemNongSauBenh"
                              :selectedVung="selectedVung" :cheDoXem="cheDoXem" @selectVung="handleSelectVungFromMap" />
                  </div>

                  <!-- ========== LAYER CONTROL SECTION ========== -->
                  <!-- Panel điều khiển: Full width trên mobile, cố định 224px trên desktop -->
                  <div class="w-full lg:w-56">
                        <MapLayerControl :cheDoXem="cheDoXem" @toggleSauBenh="handleToggleSauBenh"
                              @toggleDuLuongThuoc="handleToggleDuLuongThuoc" />
                  </div>
            </div>

            <!-- ========== SECTION 3: BAR CHART & LINE CHART ========== -->
            <!-- Khu vực: Biểu đồ cột (trái) & Biểu đồ đường (phải) -->
            <!-- Responsive: Dọc trên mobile/tablet, ngang trên desktop -->
            <!-- Mobile 6 inch: h-[320px], Tablet+: h-[450px] -->
            <div class="flex flex-col md:flex-row gap-4 sm:gap-5">

                  <!-- ========== BAR CHART SECTION ========== -->
                  <!-- Biểu đồ cột: Full width trên mobile, 40% trên desktop -->
                  <div class="w-full md:w-2/5 p-3 sm:p-4 shadow-md rounded-xl h-[320px] sm:h-[380px] md:h-[450px]" style="background-color: white;">
                        <!-- Component biểu đồ cột -->
                        <BarChartComponent />
                  </div>

                  <!-- ========== LINE CHART SECTION ========== -->
                  <!-- Biểu đồ đường: Full width trên mobile, 60% trên desktop -->
                  <div class="w-full md:flex-1 p-3 sm:p-4 shadow-md rounded-xl h-[320px] sm:h-[380px] md:h-auto" style="background-color: white;">
                        <!-- Component biểu đồ đường -->
                        <LineChartComponent />
                  </div>

            </div>

            <!-- ========== SECTION 4: CROP DETAILS ========== -->
            <!-- Chi tiết loại cây của vùng được chọn -->
            <!-- Hiển thị danh sách loại cây, diện tích, năng suất, thị trường xuất khẩu -->
            <CropDetailsComponent :selectedVung="selectedVung" />

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
            <footer class="pt-6 pb-4 mt-8 text-sm text-center text-gray-600 border-t border-gray-200">
                  <p>&copy; 2024 Hệ thống Quản lý Nông nghiệp. Phát triển bởi <span
                              class="font-semibold text-gray-800">Dev Team</span></p>
                  <p class="mt-2 text-xs text-gray-500">Cập nhật lần cuối: <span class="font-medium">{{ new
                        Date().toLocaleDateString('vi-VN') }}</span></p>
            </footer>
      </div>
</template>
