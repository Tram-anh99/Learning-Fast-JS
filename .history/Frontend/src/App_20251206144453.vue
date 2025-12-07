<script setup>
import { ref } from 'vue';
import BanDo from './components/BanDo.vue';

// 1. Giả lập dữ liệu danh sách vùng trồng (Sau này sẽ lấy từ API Python)
const danhSachVung = ref([
  { id: 1, maSo: 'VT-001', ten: 'Xoài Cát Chu', dienTich: 5000 },
  { id: 2, maSo: 'VT-002', ten: 'Thanh Long Ruột Đỏ', dienTich: 3200 },
  { id: 3, maSo: 'VT-003', ten: 'Sầu Riêng Ri6', dienTich: 8500 },
]);

// Hàm xử lý khi click vào danh sách
const chonVung = (vung) => {
  alert(`Bạn vừa chọn vùng: ${vung.ten}\n(Sau này click vào đây bản đồ sẽ zoom tới đó)`);
};
</script>

<template>
  <div class="webgis-layout">
    <aside class="sidebar">
      <div class="header-box">
        <h2>🌱 Quản lý Vùng Trồng</h2>
      </div>

      <div class="list-container">
        <h3>Danh sách ({{ danhSachVung.length }})</h3>

        <ul>
          <li v-for="vung in danhSachVung" :key="vung.id" @click="chonVung(vung)" class="list-item">
            <strong>{{ vung.maSo }}</strong> - {{ vung.ten }}
          </li>
        </ul>
      </div>
    </aside>

    <main class="map-wrapper">
      <BanDo />
    </main>
  </div>
</template>

<style>
/* Reset mặc định của trình duyệt */
body {
  margin: 0;
  padding: 0;
}

/* Bố cục chia 2 cột: Sidebar cố định, Map co giãn */
.webgis-layout {
  display: flex;
  /* Dùng Flexbox để chia cột */
  height: 100vh;
  /* Chiều cao full màn hình */
  width: 100vw;
}

/* Sidebar bên trái */
.sidebar {
  width: 300px;
  /* Rộng cố định 300px */
  background-color: #f8f9fa;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
}

.header-box {
  padding: 20px;
  background-color: #42b883;
  color: white;
}

.list-container {
  padding: 10px;
  overflow-y: auto;
  /* Cho phép cuộn nếu danh sách dài */
}

/* Style cho từng dòng trong danh sách */
.list-item {
  background: white;
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  list-style: none;
  /* Bỏ dấu chấm tròn đầu dòng */
  transition: 0.2s;
}

.list-item:hover {
  background-color: #e2e6ea;
  transform: translateX(5px);
  /* Hiệu ứng đẩy nhẹ sang phải */
}

ul {
  padding: 0;
}

/* Phần bao quanh bản đồ */
.map-wrapper {
  flex-grow: 1;
  /* Chiếm hết phần diện tích còn lại */
  position: relative;
}
</style>