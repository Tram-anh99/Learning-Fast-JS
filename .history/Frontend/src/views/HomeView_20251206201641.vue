<script setup>
import { ref } from 'vue';

// SỬA LỖI ĐƯỜNG DẪN: Thêm dấu chấm "." thành ".."
// Nghĩa là: Đi lùi ra thư mục cha, rồi mới vào components
import BanDo from '../components/BanDo.vue'; 

// (Đã xóa dòng import FormNhaNong thừa đi rồi)

// Dữ liệu danh sách vùng trồng
const danhSachVung = ref([
  { 
    id: 1, 
    maSo: 'VT-001', 
    ten: 'Xoài Cát Hòa Lộc',
    trangThai: 'canh_tac',
    toaDo: [[10.762, 106.660], [10.770, 106.670], [10.760, 106.670]]
  },
  { 
    id: 2, 
    maSo: 'VT-002', 
    ten: 'Thanh Long Ruột Đỏ',
    trangThai: 'sau_benh',
    toaDo: [[10.780, 106.680], [10.790, 106.690], [10.780, 106.690]]
  },
  {
    id: 3, 
    maSo: 'VT-003', 
    ten: 'Lúa ST25',
    trangThai: 'thu_hoach',
    toaDo: [[10.750, 106.640], [10.755, 106.650], [10.745, 106.650]]
  }
]);

const vungDangChon = ref(null);

const chonVung = (vung) => {
  vungDangChon.value = vung;
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
          <li 
            v-for="vung in danhSachVung" 
            :key="vung.id"
            @click="chonVung(vung)"
            class="list-item"
            :class="{ 'active': vungDangChon?.id === vung.id }"
          >
            <strong>{{ vung.maSo }}</strong> - {{ vung.ten }}
          </li>
        </ul>
      </div>
    </aside>

    <main class="map-wrapper">
      <BanDo 
        :duLieuDauVao="danhSachVung" 
        :vungCanZoom="vungDangChon"
      />
    </main>
    
    </div>
</template>

<style>
/* Copy nguyên CSS cũ từ App.vue sang đây */
/* Để đảm bảo giao diện không bị vỡ */
.webgis-layout {
  display: flex;
  height: calc(100vh - 60px); /* Trừ đi 60px của thanh Menu ở trên cùng */
  width: 100vw;
  overflow: hidden;
  position: relative;
}

.sidebar {
  width: 300px;
  background-color: #f8f9fa;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.header-box {
  background-color: #42b883;
  color: white;
  padding: 15px;
  text-align: center;
}

.list-container {
  padding: 10px;
  overflow-y: auto;
}

.list-item {
  list-style: none;
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: 0.2s;
}

.list-item:hover {
  background-color: #e2e6ea;
  padding-left: 20px;
}

.list-item.active {
  background-color: #42b883;
  color: white;
}

ul { padding: 0; margin: 0; }

.map-wrapper {
  flex-grow: 1;
  position: relative;
  background-color: #e0e0e0;
}
</style>