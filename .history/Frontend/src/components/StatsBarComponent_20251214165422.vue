<script setup>
/**
 * ========== COMPONENT: StatsBarComponent.vue ==========
 * Purpose: Thanh hiển thị các chỉ số thống kê chính cho dashboard
 * 
 * Features:
 *   - Hiển thị 3 card thống kê: Tổng vùng, Diện tích, Cảnh báo
 *   - Icon & màu sắc phân biệt từng loại
 *   - Responsive layout
 * 
 * Props:
 *   - thongKe (Object): Chứa dữ liệu thống kê { tongVung, dienTich, canhBao }
 * 
 * Related Files:
 *   - src/views/QuanLyView.vue - Parent component
 */

// ========== PROPS ==========
/**
 * Props nhận dữ liệu thống kê từ component cha
 * Object chứa 3 trường: tongVung, dienTich, canhBao
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
      <!-- Thanh hiển thị các thống kê chính - flex row -->
      <!-- flex = flex layout, gap-5 = khoảng cách giữa 3 card là 20px -->
      <div class="flex gap-5">
            <!-- ========== CARD 1: Tổng số vùng trồng ========== -->
            <!-- stat-card = custom CSS class (styling & layout) -->
            <div class="stat-card">
                  <!-- Icon box: nền xanh lá (success color) -->
                  <!-- icon-box-success = custom CSS class với background xanh -->
                  <div class="icon-box-success">
                        <!-- Icon: biểu tượng layers (nhiều lớp) -->
                        <i class="fas fa-layer-group"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <!-- Tiêu đề: số lượng vùng trồng -->
                        <!-- stat-info-title = custom CSS class: font lớn, đậm, màu sẫm -->
                        <h3 class="stat-info-title">{{ thongKe.tongVung }}</h3>
                        <!-- Mô tả: "Mã số vùng trồng" -->
                        <!-- stat-info-desc = custom CSS class: font nhỏ, màu nhạt -->
                        <p class="stat-info-desc">Mã số vùng trồng</p>
                  </div>
            </div>

            <!-- ========== CARD 2: Tổng diện tích canh tác ========== -->
            <!-- Hiển thị diện tích tổng cộng tất cả vùng trồng -->
            <div class="stat-card">
                  <!-- Icon box: nền xanh da trời (primary color) -->
                  <!-- icon-box-primary = custom CSS class với background xanh da trời -->
                  <div class="icon-box-primary">
                        <!-- Icon: biểu tượng ruler (thước đo) -->
                        <i class="fas fa-ruler-combined"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <!-- Tiêu đề: tổng diện tích (ha) -->
                        <h3 class="stat-info-title">{{ thongKe.dienTich }}</h3>
                        <!-- Mô tả: "Tổng diện tích" -->
                        <p class="stat-info-desc">Tổng diện tích</p>
                  </div>
            </div>

            <!-- ========== CARD 3: Cảnh báo vi phạm ========== -->
            <!-- Số lượng vi phạm / cảnh báo hệ thống -->
            <div class="stat-card">
                  <!-- Icon box: nền vàng/cam (warning color) -->
                  <!-- icon-box-warning = custom CSS class với background vàng/cam -->
                  <div class="icon-box-warning">
                        <!-- Icon: biểu tượng dấu cảnh báo (exclamation) -->
                        <i class="fas fa-exclamation-triangle"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <!-- Tiêu đề: số cảnh báo -->
                        <h3 class="stat-info-title">{{ thongKe.canhBao }}</h3>
                        <!-- Mô tả: "Cảnh báo vi phạm" -->
                        <p class="stat-info-desc">Cảnh báo vi phạm</p>
                  </div>
            </div>
      </div>
</template>
