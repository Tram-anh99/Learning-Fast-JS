<script setup>
// Props nhận dữ liệu thống kê từ component cha
defineProps({
  thongKe: {
    type: Object,
    required: true
  }
});
</script>

<template>
  <!-- Thanh hiển thị các thống kê chính - flex row -->
  <div class="flex gap-5">
    <!-- Card 1: Tổng số vùng trồng -->
    <div class="stat-card">
      <div class="icon-box-success">
        <i class="fas fa-layer-group"></i>
      </div>
      <div>
        <h3 class="stat-info-title">{{ thongKe.tongVung }}</h3>
        <p class="stat-info-desc">Mã số vùng trồng</p>
      </div>
    </div>
    
    <!-- Card 2: Tổng diện tích -->
    <div class="stat-card">
      <div class="icon-box-primary">
        <i class="fas fa-ruler-combined"></i>
      </div>
      <div>
        <h3 class="stat-info-title">{{ thongKe.dienTich }}</h3>
        <p class="stat-info-desc">Tổng diện tích</p>
      </div>
    </div>
    
    <!-- Card 3: Cảnh báo vi phạm -->
    <div class="stat-card">
      <div class="icon-box-warning">
        <i class="fas fa-exclamation-triangle"></i>
      </div>
      <div>
        <h3 class="stat-info-title">{{ thongKe.canhBao }}</h3>
        <p class="stat-info-desc">Cảnh báo vi phạm</p>
      </div>
    </div>
  </div>
</template>

