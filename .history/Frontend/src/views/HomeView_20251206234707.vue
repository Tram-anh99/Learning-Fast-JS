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
/* 1. Layout chính: Cho phép các phần tử xếp chồng lên nhau */
.webgis-layout {
  position: relative;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

/* 2. Bản đồ: Tràn đầy màn hình, nằm dưới cùng */
.map-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  /* Lớp dưới cùng */
}

/* 3. Sidebar: NỔI LÊN TRÊN bản đồ (Floating) */
.sidebar {
  position: absolute;
  top: 20px;
  /* Cách lề trên */
  left: 20px;
  /* Cách lề trái */
  bottom: 20px;
  /* Cách lề dưới (để tạo khoảng hở đẹp) */
  width: 340px;

  /* HIỆU ỨNG KÍNH MỜ (Đã chỉnh lại độ trong suốt để thấy map bên dưới) */
  background: rgba(255, 255, 255, 0.7);
  /* Trắng trong suốt 70% */
  backdrop-filter: blur(15px);
  /* Làm mờ bản đồ bên dưới */
  -webkit-backdrop-filter: blur(15px);

  border-radius: 16px;
  /* Bo tròn các góc */
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  /* Bóng đổ sâu */
  border: 1px solid rgba(255, 255, 255, 0.4);
  /* Viền kính sáng */

  display: flex;
  flex-direction: column;
  z-index: 1000;
  /* Nằm đè lên trên bản đồ */
}

/* Header trong suốt */
.header-box {
  background: transparent;
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.header-box h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 800;
  color: var(--primary-dark);
  /* Dùng màu xanh đậm đã khai báo */
  text-transform: uppercase;
}

.list-container {
  padding: 15px;
  overflow-y: auto;
  /* Scrollbar ẩn cho đẹp */
  scrollbar-width: thin;
}

/* Item danh sách */
.list-item {
  /* Nền trắng đục hơn sidebar một chút để đọc chữ rõ */
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(5px);
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;

  list-style: none;
}

.list-item:hover {
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.list-item.active {
  /* Màu xanh Gradient cho cái đang chọn */
  background: linear-gradient(135deg, var(--primary-main), var(--primary-dark));
  color: white;
  border: none;
}
</style>