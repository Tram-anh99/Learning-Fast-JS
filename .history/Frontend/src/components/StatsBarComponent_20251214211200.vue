<script setup>
/**
 * ========== COMPONENT: StatsBarComponent.vue ==========
 * Purpose: Thanh hiển thị các chỉ số thống kê chính - Hoạt động như bộ lọc
 * 
 * Features:
 *   - Hiển thị 4 card thống kê: Tổng vùng, Diện tích, Cảnh báo, Mã bị thu hồi
 *   - Bấm vào card để lọc dữ liệu
 *   - Icon & màu sắc phân biệt từng loại
 *   - Active state khi lọc được chọn
 * 
 * Props:
 *   - thongKe (Object): Chứa dữ liệu thống kê { tongVung, dienTich, canhBao, maBiThuHoi }
 * 
 * Emits:
 *   - filter: Phát ra sự kiện khi bấm vào filter với loại filter được chọn
 * 
 * Related Files:
 *   - src/views/QuanLyView.vue - Parent component
 */

import { ref } from 'vue';

// ========== STATE ==========
const activeFilter = ref(null); // 'all' | 'danger' | 'warning' | null

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

// ========== EMITS ==========
const emit = defineEmits(['filter']);

// ========== METHODS ==========
const handleFilterClick = (filterType) => {
      activeFilter.value = activeFilter.value === filterType ? null : filterType;
      emit('filter', activeFilter.value);
};
</script>

<template>
      <!-- ========== STATS BAR CONTAINER ========== -->
      <!-- Thanh hiển thị các thống kê chính - Hoạt động như bộ lọc -->
      <!-- flex = flex layout, gap-5 = khoảng cách giữa card là 20px -->
      <div class="flex gap-5">
            <!-- ========== CARD 1: Tổng số vùng trồng ========== -->
            <!-- Bấm để lọc theo tất cả vùng -->
            <div class="stat-card cursor-pointer transition-all" 
                  :class="{ 'ring-2 ring-green-500 scale-105': activeFilter === 'all' }"
                  @click="handleFilterClick('all')">
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
            <!-- Bấm để lọc theo diện tích -->
            <div class="stat-card cursor-pointer transition-all" 
                  :class="{ 'ring-2 ring-blue-500 scale-105': activeFilter === 'area' }"
                  @click="handleFilterClick('area')">
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
            <!-- Bấm để lọc theo cảnh báo -->
            <div class="stat-card cursor-pointer transition-all" 
                  :class="{ 'ring-2 ring-yellow-500 scale-105': activeFilter === 'warning' }"
                  @click="handleFilterClick('warning')">
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
            <!-- Số lượng mã vùng bị thu hồi -->
            <div class="stat-card">
                  <!-- Icon box: nền đỏ (danger color) -->
                  <div class="icon-box-danger">
                        <!-- Icon: biểu tượng ban/block -->
                        <i class="fas fa-ban"></i>
                  </div>
                  <!-- Nội dung text card -->
                  <div>
                        <!-- Tiêu đề: số mã bị thu hồi -->
                        <h3 class="stat-info-title">{{ thongKe.maBiThuHoi || 0 }}</h3>
                        <!-- Mô tả: "Mã bị thu hồi" -->
                        <p class="stat-info-desc">Mã bị thu hồi</p>
                  </div>
            </div>
      </div>
</template>
