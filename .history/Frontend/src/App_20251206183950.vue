<script setup>
import { ref } from 'vue';
import BanDo from './components/BanDo.vue';
import FormNhaNong from './components/FormNhaNong.vue';

// Dữ liệu mẫu (Có tọa độ để test)
const danhSachVung = ref([
  {
    id: 1,
    maSo: 'VT-001',
    ten: 'Xoài Cát Hòa Lộc',
    trangThai: 'canh_tac', // <--- Thêm cái này (Màu xanh)
    toaDo: [[10.762, 106.660], [10.770, 106.670], [10.760, 106.670]]
  },
  {
    id: 2,
    maSo: 'VT-002',
    ten: 'Thanh Long Ruột Đỏ',
    trangThai: 'sau_benh', // <--- Thêm cái này (Màu đỏ)
    toaDo: [[10.780, 106.680], [10.790, 106.690], [10.780, 106.690]]
  },
  {
    id: 3,
    maSo: 'VT-003',
    ten: 'Lúa ST25',
    trangThai: 'thu_hoach', // <--- Thêm cái này (Màu vàng)
    toaDo: [[10.750, 106.640], [10.755, 106.650], [10.745, 106.650]]
  }
]);

const vungDangChon = ref(null);

const chonVung = (vung) => {
  vungDangChon.value = vung;
};

// Biến kiểm soát việc hiện form
const hienForm = ref(false);

// Hàm nhận dữ liệu khi Form bấm nút Lưu
const xuLyLuuDuLieu = (duLieuMoi) => {
  console.log("Dữ liệu nhận được từ Form:", duLieuMoi);

  // Tạm thời thêm giả vào danh sách (để thấy hiệu ứng)
  // Lưu ý: Tọa độ đang để rỗng, sau này ta sẽ tính sau
  danhSachVung.value.push({
    id: Date.now(),
    maSo: 'VT-NEW',
    ten: duLieuMoi.tenVung,
    trangThai: duLieuMoi.trangThai,
    toaDo: []
  });

  // Đóng form
  hienForm.value = false;
  alert("Đã lưu thành công! (Hiện tại chỉ lưu tạm trên trình duyệt)");
};
</script>

<template>
  <div class="app-root">
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
      <FormNhaNong v-if="hienForm" @dong-form="hienForm = false" @luu-du-lieu="xuLyLuuDuLieu" />
    </div>


  </div>

</template>

<style>
/* --- PHẦN CSS QUAN TRỌNG NÀY ĐANG BỊ THIẾU Ở MÁY BẠN --- */

/* 1. Xóa lề mặc định của trình duyệt */
body {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 2. Chia bố cục 2 cột (Sidebar - Map) */
.webgis-layout {
  display: flex;
  /* Xếp hàng ngang */
  height: 100vh;
  /* Cao 100% màn hình */
  width: 100vw;
  /* Rộng 100% màn hình */
  overflow: hidden;
  /* Không cho cuộn trang chính */
}

/* 3. Trang trí Sidebar */
.sidebar {
  width: 300px;
  /* Cố định chiều rộng */
  background-color: #f8f9fa;
  /* Màu xám nhạt */
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
  /* Cho phép cuộn danh sách */
}

.list-item {
  list-style: none;
  /* Bỏ dấu chấm tròn đầu dòng */
  padding: 12px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: 0.2s;
}

.list-item:hover {
  background-color: #e2e6ea;
  padding-left: 20px;
  /* Hiệu ứng đẩy chữ */
}

.list-item.active {
  background-color: #42b883;
  color: white;
}

ul {
  padding: 0;
  margin: 0;
}

/* 4. Khung chứa bản đồ */
.map-wrapper {
  flex-grow: 1;
  /* Chiếm hết phần còn lại */
  position: relative;
  background-color: #e0e0e0;
  /* Màu nền tạm để biết khung có hiện ko */
}

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
}

.btn-them-moi:hover {
  background: #e6f7ef;
  transform: scale(1.05);
}
</style>