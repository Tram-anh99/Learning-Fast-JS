<script setup>
import { ref } from 'vue';
import BanDo from './components/BanDo.vue';

// 1. Dữ liệu (Đã thêm tọa độ để vẽ)
const danhSachVung = ref([
  {
    id: 1,
    maSo: 'VT-001',
    ten: 'Xoài Cát Hòa Lộc',
    toaDo: [
      [10.762, 106.660],
      [10.770, 106.670],
      [10.760, 106.670]
    ]
  },
  {
    id: 2,
    maSo: 'VT-002',
    ten: 'Thanh Long',
    // Vùng này thử tạo tọa độ khác một chút
    toaDo: [
      [10.780, 106.680],
      [10.790, 106.690],
      [10.780, 106.690]
    ]
  }
]);

const chonVung = (vung) => {
  console.log("Đã chọn:", vung.ten);
};
</script>

<template>
  <div class="webgis-layout">

    <aside class="sidebar">
      <div class="header-box">
        <h2>🌱 WebGIS Vùng Trồng</h2>
      </div>

      <div class="list-container">
        <ul>
          <li v-for="vung in danhSachVung" :key="vung.id" @click="chonVung(vung)" class="list-item">
            <strong>{{ vung.maSo }}</strong> - {{ vung.ten }}
          </li>
        </ul>
      </div>
    </aside>

    <main class="map-wrapper">
      <BanDo :duLieuDauVao="danhSachVung" />
    </main>

  </div>
</template>

<style>
/* CSS BẮT BUỘC ĐỂ CHIA 2 CỘT */
body {
  margin: 0;
  padding: 0;
}

.webgis-layout {
  display: flex;
  /* Xếp hàng ngang */
  height: 100vh;
  /* Cao full màn hình */
  width: 100vw;
  /* Rộng full màn hình */
  overflow: hidden;
  /* Ẩn thanh cuộn thừa */
}

.sidebar {
  width: 300px;
  /* Cố định rộng 300px */
  background: #f8f9fa;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  /* Đè lên trên để không bị che */
}

.header-box {
  background: #42b883;
  color: white;
  padding: 15px;
  text-align: center;
}

.list-container {
  padding: 10px;
  overflow-y: auto;
}

.list-item {
  background: white;
  padding: 10px;
  margin-bottom: 8px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  list-style: none;
}

.list-item:hover {
  background-color: #e9ecef;
}

ul {
  padding: 0;
  margin: 0;
}

.map-wrapper {
  flex-grow: 1;
  /* Chiếm hết phần còn lại */
  position: relative;
}
</style>