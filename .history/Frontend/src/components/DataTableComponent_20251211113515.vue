<script setup>
import { getStatusBadge } from '../composables/statusHelpers';

// Props nhận danh sách vùng từ component cha
defineProps({
  danhSachVung: {
    type: Array,
    required: true
  }
});
</script>

<template>
  <!-- Panel chứa bảng danh sách vùng trồng -->
  <div class="admin-panel">
    <!-- Header với tiêu đề và nút xuất báo cáo -->
    <div class="panel-header">
      <h3>Danh sách Vùng trồng & Giám sát</h3>
      <button class="btn-export"><i class="fas fa-file-export"></i> Xuất báo cáo</button>
    </div>
    
    <!-- Container bảng có scroll nếu có nhiều dòng -->
    <div class="table-container">
      <table>
        <!-- Header bảng -->
        <thead>
          <tr>
            <th>Mã số</th>
            <th>Tên vùng</th>
            <th>Chủ hộ</th>
            <th>Trạng thái</th>
            <th>Thao tác</th>
          </tr>
        </thead>
        
        <!-- Body bảng - duyệt qua từng vùng -->
        <tbody>
          <tr v-for="vung in danhSachVung" :key="vung.id">
            <!-- Mã số vùng trồng -->
            <td><strong>{{ vung.ma }}</strong></td>
            
            <!-- Tên vùng -->
            <td>{{ vung.ten }}</td>
            
            <!-- Chủ hộ / người quản lý -->
            <td>{{ vung.chu }}</td>
            
            <!-- Trạng thái với badge màu -->
            <td>
              <span :class="['status-badge', getStatusBadge(vung.trangThai).class]">
                {{ getStatusBadge(vung.trangThai).text }}
              </span>
            </td>
            
            <!-- Các nút thao tác (chỉnh sửa, cảnh báo) -->
            <td>
              <button class="btn-action edit" title="Chỉnh sửa"><i class="fas fa-edit"></i></button>
              <button class="btn-action warn" title="Cảnh báo"><i class="fas fa-bell"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* Panel chính - flex 1.5 */
.admin-panel {
  flex: 1.5;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Header của panel */
.panel-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Tiêu đề panel */
.panel-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1e293b;
}

/* Nút xuất báo cáo */
.btn-export {
  background: #1b4332;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
}

/* Container bảng - có scroll nếu cần */
.table-container {
  overflow-y: auto;
  flex-grow: 1;
}

/* Bảng */
table {
  width: 100%;
  border-collapse: collapse;
}

/* Header cột bảng - sticky top */
th {
  text-align: left;
  padding: 12px 20px;
  background: #f8fafc;
  color: #64748b;
  font-weight: 600;
  font-size: 0.85rem;
  position: sticky;
  top: 0;
}

/* Ô dữ liệu */
td {
  padding: 12px 20px;
  border-bottom: 1px solid #f1f5f9;
  color: #333;
  font-size: 0.9rem;
}

/* Highlight khi hover dòng */
tr:hover {
  background: #f8fafc;
}

/* Badge hiển thị trạng thái */
.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

/* Màu badge - hoạt động (xanh) */
.badge-active {
  background: #d1fae5;
  color: #065f46;
}

/* Màu badge - cảnh báo (vàng) */
.badge-warning {
  background: #fef3c7;
  color: #92400e;
}

/* Màu badge - đã thu hồi (đỏ) */
.badge-danger {
  background: #fee2e2;
  color: #991b1b;
}

/* Nút thao tác (nhỏ) */
.btn-action {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 5px;
}

/* Nút chỉnh sửa (xanh) */
.btn-action.edit {
  background: #e0f2fe;
  color: #0284c7;
}

/* Nút cảnh báo (cam) */
.btn-action.warn {
  background: #ffedd5;
  color: #ea580c;
}
</style>
