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
  <!-- Thanh hiển thị các thống kê chính -->
  <div class="stats-bar">
    <!-- Card 1: Tổng số vùng trồng -->
    <div class="stat-card">
      <div class="icon-box green"><i class="fas fa-layer-group"></i></div>
      <div class="stat-info">
        <h3>{{ thongKe.tongVung }}</h3>
        <p>Mã số vùng trồng</p>
      </div>
    </div>
    
    <!-- Card 2: Tổng diện tích -->
    <div class="stat-card">
      <div class="icon-box blue"><i class="fas fa-ruler-combined"></i></div>
      <div class="stat-info">
        <h3>{{ thongKe.dienTich }}</h3>
        <p>Tổng diện tích</p>
      </div>
    </div>
    
    <!-- Card 3: Cảnh báo vi phạm -->
    <div class="stat-card">
      <div class="icon-box yellow"><i class="fas fa-exclamation-triangle"></i></div>
      <div class="stat-info">
        <h3>{{ thongKe.canhBao }}</h3>
        <p>Cảnh báo vi phạm</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Container chứa các thẻ thống kê - dùng flexbox xếp hàng */
.stats-bar {
  display: flex;
  gap: 20px;
}

/* Mỗi thẻ thống kê */
.stat-card {
  flex: 1;
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 15px;
}

/* Hộp icon với nền màu */
.icon-box {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  color: white;
}

/* Các màu nền cho icon */
.icon-box.green {
  background: #10b981;
}

.icon-box.blue {
  background: #3b82f6;
}

.icon-box.yellow {
  background: #f59e0b;
}

/* Tiêu đề số thống kê */
.stat-info h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #1e293b;
}

/* Mô tả dưới tiêu đề */
.stat-info p {
  margin: 0;
  color: #64748b;
  font-size: 0.9rem;
}
</style>
