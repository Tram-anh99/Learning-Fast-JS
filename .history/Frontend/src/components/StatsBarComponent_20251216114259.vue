<script setup>
/**
 * ========== COMPONENT: StatsBarComponent.vue ==========
 * Purpose: Thanh hiển thị các chỉ số thống kê chính
 * 
 * Features:
 *   - Hiển thị 4 card thống kê: Tổng vùng, Diện tích, Cảnh báo, Mã bị thu hồi
 *   - Icon & màu sắc phân biệt từng loại
 * 
 * Props:
 *   - thongKe (Object): Chứa dữ liệu thống kê { tongVung, dienTich, canhBao, maBiThuHoi }
 * 
 * Related Files:
 *   - src/views/QuanLyView.vue - Parent component
 */

// ========== PROPS ==========
/**
 * Props nhận dữ liệu thống kê từ component cha
 * Object chứa 4 trường: tongVung, dienTich, canhBao, maBiThuHoi
 */
defineProps({
      // thongKe: Object chứa dữ liệu thống kê hệ thống
      thongKe: {
            type: Object,
            required: true
      }
});
</script>

<template>
      <!-- ========== STATS BAR CONTAINER ========== -->
      <!-- Thanh hiển thị các thống kê chính -->
      <!-- Responsive: Grid 1 cột trên mobile, 2 cột trên tablet, 4 cột trên desktop -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <!-- ========== CARD 1: Tổng số vùng trồng ========== -->
            <div class="stat-card">
                  <!-- Icon box: nền xanh lá (success color) -->
                  <div class="icon-box-success">
                        <i class="fas fa-layer-group"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <h3 class="stat-info-title">{{ thongKe.tongVung }}</h3>
                        <p class="stat-info-desc">Mã số vùng trồng</p>
                  </div>
            </div>

            <!-- ========== CARD 2: Tổng diện tích canh tác ========== -->
            <div class="stat-card">
                  <!-- Icon box: nền xanh da trời (primary color) -->
                  <div class="icon-box-primary">
                        <i class="fas fa-ruler-combined"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <h3 class="stat-info-title">{{ thongKe.dienTich }}</h3>
                        <p class="stat-info-desc">Tổng diện tích</p>
                  </div>
            </div>

            <!-- ========== CARD 3: Cảnh báo vi phạm ========== -->
            <div class="stat-card">
                  <!-- Icon box: nền vàng/cam (warning color) -->
                  <div class="icon-box-warning">
                        <i class="fas fa-exclamation-triangle"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <h3 class="stat-info-title">{{ thongKe.canhBao }}</h3>
                        <p class="stat-info-desc">Cảnh báo vi phạm</p>
                  </div>
            </div>

            <!-- ========== CARD 4: Mã bị thu hồi ========== -->
            <div class="stat-card">
                  <!-- Icon box: nền đỏ (danger color) -->
                  <div class="icon-box-danger">
                        <i class="fas fa-ban"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <h3 class="stat-info-title">{{ thongKe.maBiThuHoi || 0 }}</h3>
                        <p class="stat-info-desc">Mã bị thu hồi</p>
                  </div>
            </div>
      </div>
</template>
