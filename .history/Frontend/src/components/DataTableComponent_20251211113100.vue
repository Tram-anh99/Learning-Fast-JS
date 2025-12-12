<script setup>
import { getStatusBadge } from '../composables/statusHelpers';

defineProps({
  danhSachVung: {
    type: Array,
    required: true
  }
});
</script>

<template>
  <div class="admin-panel">
    <div class="panel-header">
      <h3>Danh sách Vùng trồng & Giám sát</h3>
      <button class="btn-export"><i class="fas fa-file-export"></i> Xuất báo cáo</button>
    </div>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Mã số</th>
            <th>Tên vùng</th>
            <th>Chủ hộ</th>
            <th>Trạng thái</th>
            <th>Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vung in danhSachVung" :key="vung.id">
            <td><strong>{{ vung.ma }}</strong></td>
            <td>{{ vung.ten }}</td>
            <td>{{ vung.chu }}</td>
            <td>
              <span :class="['status-badge', getStatusBadge(vung.trangThai).class]">
                {{ getStatusBadge(vung.trangThai).text }}
              </span>
            </td>
            <td>
              <button class="btn-action edit"><i class="fas fa-edit"></i></button>
              <button class="btn-action warn"><i class="fas fa-bell"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.admin-panel {
  flex: 1.5;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: 15px 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1e293b;
}

.btn-export {
  background: #1b4332;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
}

.table-container {
  overflow-y: auto;
  flex-grow: 1;
}

table {
  width: 100%;
  border-collapse: collapse;
}

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

td {
  padding: 12px 20px;
  border-bottom: 1px solid #f1f5f9;
  color: #333;
  font-size: 0.9rem;
}

tr:hover {
  background: #f8fafc;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-active {
  background: #d1fae5;
  color: #065f46;
}

.badge-warning {
  background: #fef3c7;
  color: #92400e;
}

.badge-danger {
  background: #fee2e2;
  color: #991b1b;
}

.btn-action {
  width: 30px;
  height: 30px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-right: 5px;
}

.btn-action.edit {
  background: #e0f2fe;
  color: #0284c7;
}

.btn-action.warn {
  background: #ffedd5;
  color: #ea580c;
}
</style>
