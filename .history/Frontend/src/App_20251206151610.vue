<script setup>
import { ref } from 'vue';
import BanDo from './components/BanDo.vue';

// ... (Phần dữ liệu danhSachVung giữ nguyên như cũ) ...
const danhSachVung = ref([
  { 
    id: 1, 
    maSo: 'VT-001', 
    ten: 'Xoài Cát Chu', 
    toaDo: [[10.762, 106.660], [10.770, 106.670], [10.760, 106.670]]
  },
  { 
    id: 2, 
    maSo: 'VT-002', 
    ten: 'Thanh Long',
    toaDo: [[10.780, 106.680], [10.790, 106.690], [10.780, 106.690]]
  }
]);

// 1. Tạo biến để lưu vùng đang được chọn (Ban đầu chưa chọn gì nên là null)
const vungDangChon = ref(null);

// 2. Khi click vào danh sách, gán vùng đó vào biến này
const chonVung = (vung) => {
  console.log("Đang bay tới:", vung.ten);
  vungDangChon.value = vung; 
};
</script>

<template>
  <div class="webgis-layout">
    <aside class="sidebar">
      <div class="header-box"><h2>🌱 WebGIS Vùng Trồng</h2></div>
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
/* ...Giữ nguyên CSS cũ... */

/* Thêm CSS cho dòng đang được chọn */
.list-item.active {
  background-color: #42b883; /* Màu xanh Vue */
  color: white;
  font-weight: bold;
}
</style>