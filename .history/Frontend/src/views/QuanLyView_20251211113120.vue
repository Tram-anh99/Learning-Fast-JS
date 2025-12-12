<script setup>
import { ref } from 'vue';
import 'leaflet/dist/leaflet.css';
import StatsBarComponent from '../components/StatsBarComponent.vue';
import MapComponent from '../components/MapComponent.vue';
import DataTableComponent from '../components/DataTableComponent.vue';
import { mockDataThongKe, mockDataVung, mockDiemNongSauBenh } from '../composables/statusHelpers';

// Dữ liệu
const thongKe = ref(mockDataThongKe);
const danhSachVung = ref(mockDataVung);
</script>

<template>
  <div class="admin-container">
    <StatsBarComponent :thongKe="thongKe" />
    <MapComponent :danhSachVung="danhSachVung" :diemNongSauBenh="mockDiemNongSauBenh" />
    <DataTableComponent :danhSachVung="danhSachVung" />
  </div>
</template>

<style scoped>
.admin-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #f1f5f9;
      display: flex;
      flex-direction: column;
      padding: 20px;
      box-sizing: border-box;
      gap: 20px;
}

.stats-bar {
      display: flex;
      gap: 20px;
}

.stat-card {
      flex: 1;
      background: white;
      padding: 15px 20px;
      border-radius: 12px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
      display: flex;
      align-items: center;
      gap: 15px;
}

.icon-box {
      width: 50px;
      height: 50px;
      border-radius: 10px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 1.5rem;
      color: white;
}

.icon-box.green {
      background: #10b981;
}

.icon-box.blue {
      background: #3b82f6;
}

.icon-box.yellow {
      background: #f59e0b;
}

.stat-info h3 {
      margin: 0;
      font-size: 1.5rem;
      color: #1e293b;
}

.stat-info p {
      margin: 0;
      color: #64748b;
      font-size: 0.9rem;
}

.map-section {
      flex: 2;
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
      border: 1px solid white;
}

.map-view {
      width: 100%;
      height: 100%;
      z-index: 0;
}

.map-controls {
      position: absolute;
      top: 20px;
      right: 20px;
      z-index: 1000;
      background: white;
      padding: 10px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      display: flex;
      flex-direction: column;
      gap: 8px;
      width: 180px;
}

.map-controls h4 {
      margin: 0 0 5px 0;
      font-size: 0.85rem;
      color: #64748b;
      text-transform: uppercase;
}

.map-controls button {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      padding: 8px;
      border-radius: 6px;
      text-align: left;
      cursor: pointer;
      font-size: 0.9rem;
      color: #333;
      transition: all 0.2s;
}

.map-controls button:hover {
      background: #e2e6ea;
}

.map-controls button.active {
      background: #1b4332;
      color: white;
      border-color: #1b4332;
}

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