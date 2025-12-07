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
<style>.webgis-layout {
  display: flex;
  height: 100%;
  width: 100%;
  position: relative;
  background: #e2e8f0;
  /* Nền xám đệm dưới bản đồ */
}

/* Sidebar nổi lên trên bản đồ */
.sidebar {
  width: 340px;
  background: rgba(255, 255, 255, 0.95);
  /* Trắng đục */
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.08);
  /* Bóng đổ sang phải mượt mà */
}

.header-box {
  background: transparent;
  /* Bỏ nền xanh cũ */
  color: var(--text-main);
  padding: 25px 20px 15px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.header-box h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}

.list-container {
  padding: 20px;
  overflow-y: auto;
}

.list-item {
  list-style: none;
  padding: 16px;
  margin-bottom: 12px;
  background: white;
  border: 1px solid #f1f5f9;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Hiệu ứng khi di chuột vào vùng trồng */
.list-item:hover {
  transform: translateY(-2px);
  /* Nhấc nhẹ lên */
  box-shadow: var(--shadow-md);
  border-color: var(--accent-color);
}

.list-item.active {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  color: white;
  border: none;
  box-shadow: var(--shadow-lg);
}

.list-item strong {
  display: block;
  font-size: 0.9rem;
  margin-bottom: 2px;
}

.map-wrapper {
  flex-grow: 1;
  position: relative;
}
</style>
