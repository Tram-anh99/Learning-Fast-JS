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
/* src/views/HomeView.vue */

/* ... */

/* SỬA ĐOẠN NÀY: Sidebar hiệu ứng kính mờ trong suốt */
.sidebar {
  width: 320px;
  
  /* 1. Nền trắng có độ trong suốt (Alpha = 0.75) */
  background-color: rgba(255, 255, 255, 0.75);
  
  /* 2. HIỆU ỨNG KÍNH MỜ (Làm mờ hậu cảnh phía sau) */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px); /* Hỗ trợ Safari trên Mac */
  
  /* Viền và bóng đổ nhẹ nhàng hơn */
  border-right: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 5px 0 15px rgba(0, 0, 0, 0.05);
  
  display: flex; flex-direction: column; z-index: 1000;
}

/* Header bên trong cũng phải trong suốt */
.header-box {
  background-color: transparent; /* Không màu nền */
  padding: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05); /* Viền mờ */
}

.header-box h2 {
  /* ... giữ nguyên ... */
  margin: 0; font-size: 1.2rem; font-weight: 700; color: var(--primary-dark);
  text-transform: uppercase; letter-spacing: 0.5px;
}

/* Container danh sách cũng trong suốt */
.list-container {
  padding: 15px;
  overflow-y: auto;
  background-color: transparent; /* Không màu nền */
  flex-grow: 1;
}

/* Item danh sách: Làm cho chúng nổi lên trên nền kính */
.list-item {
  /* ... */
  /* Nền item trắng đục hơn một chút để dễ đọc chữ */
  background-color: rgba(255, 255, 255, 0.85);
  /* ... giữ nguyên các thuộc tính khác ... */
  list-style: none; padding: 15px; margin-bottom: 8px;
  border: 1px solid var(--grey-border); border-left: 4px solid transparent;
  border-radius: 4px; cursor: pointer; transition: all 0.2s;
  display: flex; align-items: center; justify-content: space-between;
}

/* ... (Các phần còn lại giữ nguyên) ... */

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
</style>