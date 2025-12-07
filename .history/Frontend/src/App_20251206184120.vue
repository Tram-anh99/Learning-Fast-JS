<script setup>
// --- PHẦN 1: IMPORT ---
import { ref } from 'vue';
import BanDo from './components/BanDo.vue';
import FormNhaNong from './components/FormNhaNong.vue'; // [MỚI] Import Form

// --- PHẦN 2: DỮ LIỆU ---
// Dữ liệu danh sách vùng trồng (Code cũ)
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

// Hàm chọn vùng để zoom (Code cũ)
const chonVung = (vung) => {
  vungDangChon.value = vung;
};

// --- PHẦN 3: LOGIC FORM MỚI ---
const hienForm = ref(false); // Biến bật tắt form

// Hàm xử lý khi bấm nút Lưu ở Form
const xuLyLuuDuLieu = (duLieuMoi) => {
  console.log("Dữ liệu nhận được:", duLieuMoi);

  // Thêm vùng mới vào danh sách
  danhSachVung.value.push({
    id: Date.now(),
    maSo: 'VT-NEW',
    ten: duLieuMoi.tenVung,
    trangThai: duLieuMoi.trangThai,
    toaDo: [] // Tạm thời chưa có tọa độ
  });

  hienForm.value = false; // Đóng form
  alert("Đã thêm vùng mới thành công!");
};
</script>

<template>
  <div class="webgis-layout">

    <aside class="sidebar">
      <div class="header-box">
        <h2>🌱 WebGIS Vùng Trồng</h2>
        <button class="btn-them-moi" @click="hienForm = true">+ Thêm Nhật Ký</button>
      </div>

      <div class="list-container">
        <ul>
          <li v-for="vung in danhSachVung" :key="vung.id" @click="chonVung(vung)" class="list-item"
            :class="{ 'active': vungDangChon?.id === vung.id }">
            <strong>{{ vung.maSo }}</strong> - {{ vung.ten }}
          </li>
        </ul>
      </div>
    </aside>

    <main class="map-wrapper">
      <BanDo :duLieuDauVao="danhSachVung" :vungCanZoom="vungDangChon" />
    </main>

    <FormNhaNong v-if="hienForm" @dong-form="hienForm = false" @luu-du-lieu="xuLyLuuDuLieu" />

  </div>
</template>

<style>
/* --- GIỮ NGUYÊN CSS CŨ --- */
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.webgis-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
  /* Thêm cái này để Form đè lên đúng vị trí */
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

ul {
  padding: 0;
  margin: 0;
}

.map-wrapper {
  flex-grow: 1;
  position: relative;
  background-color: #e0e0e0;
}

/* --- [MỚI] CSS CHO NÚT BẤM --- */
.btn-them-moi {
  margin-top: 10px;
  background: white;
  color: #42b883;
  border: none;
  padding: 8px 15px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: bold;
  width: 100%;
  transition: 0.2s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.btn-them-moi:hover {
  background: #e6f7ef;
  transform: translateY(-2px);
}
</style>