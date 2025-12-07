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

  </div>
</template>

<style>
.webgis-layout {
  display: flex;
  height: 100%;
  width: 100%;
  position: relative;
  background-color: var(--grey-bg);
}

.sidebar {
  width: 320px;
  background-color: var(--grey-sidebar);
  /* Nền trắng */
  border-right: 1px solid var(--grey-border);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
}

.header-box {
  background-color: white;
  padding: 20px;
  border-bottom: 2px solid var(--grey-bg);
}

.header-box h2 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary-dark);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.list-container {
  padding: 15px;
  overflow-y: auto;
  background-color: #f8fafc;
  flex-grow: 1;
}

/* Item danh sách phong cách KHỐI (Block) */
.list-item {
  list-style: none;
  padding: 15px;
  margin-bottom: 8px;

  background-color: white;
  border: 1px solid var(--grey-border);
  border-left: 4px solid transparent;
  /* Chuẩn bị sẵn viền trái */
  border-radius: 4px;

  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.list-item:hover {
  border-color: var(--primary-light);
  transform: translateX(3px);
}

/* KHI ĐƯỢC CHỌN -> BIẾN HÌNH */
.list-item.active {
  background-color: var(--primary-dark);
  /* Nền xanh thẫm */
  color: white;
  border-color: var(--primary-dark);
  border-left-color: #74c69d;
  /* Viền trái màu xanh sáng nổi bật */
}

/* Sửa lại text bên trong item cho đẹp */
.list-item strong {
  display: block;
  font-size: 0.95rem;
  margin-bottom: 3px;
}

.map-wrapper {
  flex-grow: 1;
  position: relative;
}
</style>.webgis-layout {
display: flex;
height: 100%;
width: 100%;
position: relative;
/* Không cần background ở đây nữa vì đã có background body */
}

/* Sidebar phong cách FROSTED MINT GLASS */
.sidebar {
width: 340px;

/* Màu trắng pha xanh ngọc, trong suốt nhiều hơn */
background: rgba(236, 253, 245, 0.6);
backdrop-filter: blur(20px);
/* Blur mạnh để làm mờ bản đồ phía dưới nếu bị che */
-webkit-backdrop-filter: blur(20px);
border-right: 1px solid rgba(255, 255, 255, 0.6);

display: flex;
flex-direction: column;
z-index: 1000;
box-shadow: 10px 0 30px rgba(0, 0, 0, 0.05);
/* Bóng đổ mềm */
}

.header-box {
background: rgba(16, 185, 129, 0.1);
/* Đầu đề hơi xanh nhẹ */
padding: 25px 20px;
border-bottom: 1px solid rgba(255, 255, 255, 0.5);
}

.header-box h2 {
margin: 0;
font-size: 1.4rem;
color: #065f46;
text-shadow: 0 1px 0 rgba(255, 255, 255, 0.8);
}

.list-container {
padding: 20px;
overflow-y: auto;
}

/* Item danh sách kiểu GIỌT NƯỚC */
.list-item {
list-style: none;
padding: 16px;
margin-bottom: 12px;

/* Nền trong suốt nhẹ */
background: rgba(255, 255, 255, 0.6);
border: 1px solid rgba(255, 255, 255, 0.8);
border-radius: 16px;

cursor: pointer;
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
display: flex;
align-items: center;
gap: 12px;
}

.list-item:hover {
background: rgba(255, 255, 255, 0.9);
transform: scale(1.02) translateX(5px);
box-shadow: 0 10px 20px rgba(5, 150, 105, 0.1);
/* Bóng xanh khi hover */
}

.list-item.active {
/* Gradient xanh ngọc rực rỡ cho cái đang chọn */
background: linear-gradient(135deg, #10b981 0%, #059669 100%);
color: white;
border: none;
box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4);
/* Glow effect */
}

.list-item strong {
font-size: 1rem;
}

.map-wrapper {
flex-grow: 1;
position: relative;
}
</style>