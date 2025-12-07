<script setup>
import { ref } from 'vue';

// Dữ liệu mẫu (Sau này lấy từ Database)
const danhSachNhatKy = ref([
      { id: 1, ngay: '2024-03-28', hoatDong: 'Bón phân', chiTiet: 'Phân hữu cơ vi sinh (50kg)', vung: 'Vườn Xoài A1', trangThai: 'Hoàn thành' },
      { id: 2, ngay: '2024-03-25', hoatDong: 'Phun thuốc', chiTiet: 'Trừ sâu sinh học (2L)', vung: 'Thanh Long B2', trangThai: 'Đang xử lý' }
]);

// Biến quản lý đóng mở Modal thêm mới
const hienModal = ref(false);
</script>

<template>
      <div class="admin-page">
            <div class="page-header">
                  <div>
                        <h2>🚜 Quản lý Canh tác</h2>
                        <p>Theo dõi quy trình và nhật ký hoạt động</p>
                  </div>
                  <button class="btn-primary" @click="hienModal = true">+ Thêm hoạt động mới</button>
            </div>

            <div class="stats-grid">
                  <div class="card">
                        <h3>12</h3>
                        <span>Vùng trồng</span>
                  </div>
                  <div class="card">
                        <h3>5</h3>
                        <span>Đang thu hoạch</span>
                  </div>
                  <div class="card warning">
                        <h3>2</h3>
                        <span>Cảnh báo sâu bệnh</span>
                  </div>
            </div>

            <div class="table-container">
                  <table>
                        <thead>
                              <tr>
                                    <th>Ngày thực hiện</th>
                                    <th>Hoạt động</th>
                                    <th>Chi tiết</th>
                                    <th>Vùng trồng</th>
                                    <th>Trạng thái</th>
                                    <th>Thao tác</th>
                              </tr>
                        </thead>
                        <tbody>
                              <tr v-for="item in danhSachNhatKy" :key="item.id">
                                    <td>{{ item.ngay }}</td>
                                    <td><span class="badge" :class="item.hoatDong">{{ item.hoatDong }}</span></td>
                                    <td>{{ item.chiTiet }}</td>
                                    <td><b>{{ item.vung }}</b></td>
                                    <td>
                                          <span class="status-dot"
                                                :class="item.trangThai === 'Hoàn thành' ? 'green' : 'orange'"></span>
                                          {{ item.trangThai }}
                                    </td>
                                    <td>
                                          <button class="btn-icon">✏️</button>
                                          <button class="btn-icon">🗑</button>
                                    </td>
                              </tr>
                        </tbody>
                  </table>
            </div>

            <div v-if="hienModal" class="modal-placeholder">
                  <div class="modal-content">
                        <h3>Form nhập liệu sẽ hiện ở đây</h3>
                        <button @click="hienModal = false">Đóng</button>
                  </div>
            </div>
      </div>
</template>

<style scoped>
/* CSS GIAO DIỆN ADMIN HIỆN ĐẠI (Clean UI) */
.admin-page {
      padding: 30px;
      background-color: #f5f7fa;
      min-height: 100vh;
}

.page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
}

.page-header h2 {
      margin: 0;
      color: #2c3e50;
}

.page-header p {
      margin: 5px 0 0;
      color: #7f8c8d;
}

.btn-primary {
      background: #42b883;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 8px;
      font-weight: bold;
      cursor: pointer;
      transition: 0.2s;
      box-shadow: 0 4px 6px rgba(66, 184, 131, 0.2);
}

.btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 8px rgba(66, 184, 131, 0.3);
}

/* Stats Cards */
.stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 30px;
}

.card {
      background: white;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
      text-align: center;
}

.card h3 {
      font-size: 2rem;
      margin: 0;
      color: #42b883;
}

.card.warning h3 {
      color: #e74c3c;
}

.card span {
      color: #7f8c8d;
      font-size: 0.9rem;
}

/* Table Styles */
.table-container {
      background: white;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
      overflow: hidden;
}

table {
      width: 100%;
      border-collapse: collapse;
}

th {
      background: #f8f9fa;
      padding: 15px;
      text-align: left;
      font-weight: 600;
      color: #666;
}

td {
      padding: 15px;
      border-bottom: 1px solid #eee;
      color: #333;
}

tr:last-child td {
      border-bottom: none;
}

tr:hover {
      background-color: #fafafa;
}

.badge {
      padding: 5px 10px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 500;
}

.btn-icon {
      background: none;
      border: none;
      cursor: pointer;
      opacity: 0.6;
      font-size: 1.1rem;
}

.btn-icon:hover {
      opacity: 1;
      transform: scale(1.1);
}

.status-dot {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      margin-right: 5px;
}

.green {
      background: #2ecc71;
}

.orange {
      background: #f1c40f;
}

/* Modal tạm */
.modal-placeholder {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      justify-content: center;
      align-items: center;
}

.modal-content {
      background: white;
      padding: 30px;
      border-radius: 10px;
}
</style>