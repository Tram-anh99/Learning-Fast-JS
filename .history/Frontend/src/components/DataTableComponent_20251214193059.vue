<script setup>
/**
 * ========== COMPONENT: DataTableComponent.vue ==========
 * Purpose: Hiển thị bảng danh sách vùng trồng với scroll custom
 * 
 * Features:
 *   - Scrollable table with custom scrollbar styling
 *   - Status badges for cultivation status
 *   - Action buttons (Edit, Alert)
 *   - Export report functionality
 * 
 * Props:
 *   - danhSachVung: Array of farm zones (id, ma, ten, chu, trangThai)
 */

import { getStatusBadge } from '../composables/statusHelpers';

defineProps({
      danhSachVung: { type: Array, required: true }
});
</script>

<template>
      <div class="panel flex flex-col flex-[3] overflow-hidden">
            <div class="panel-header">
                  <h3 class="panel-title">Danh sách Vùng trồng & Giám sát</h3>
                  <button class="btn-primary">
                        <i class="fas fa-file-export"></i> Xuất báo cáo
                  </button>
            </div>

            <!-- Scrollable table container with custom scrollbar -->
            <div class="overflow-y-auto flex-grow scrollbar-custom">
                  <table class="w-full border-collapse">
                        <thead class="sticky top-0 z-10 bg-white shadow-sm">
                              <tr>
                                    <th class="table-header">Mã số</th>
                                    <th class="table-header">Tên vùng</th>
                                    <th class="table-header">Chủ hộ</th>
                                    <th class="table-header">Trạng thái</th>
                                    <th class="table-header">Thao tác</th>
                              </tr>
                        </thead>
                        <tbody>
                              <tr v-for="vung in danhSachVung" :key="vung.id" class="table-row-hover">
                                    <td class="table-cell"><strong>{{ vung.ma }}</strong></td>
                                    <td class="table-cell">{{ vung.ten }}</td>
                                    <td class="table-cell">{{ vung.chu }}</td>
                                    <td class="table-cell">
                                          <span :class="`badge-${getStatusBadge(vung.trangThai).class.split('-')[1]}`">
                                                {{ getStatusBadge(vung.trangThai).text }}
                                          </span>
                                    </td>
                                    <td class="table-cell space-x-1">
                                          <button class="btn-primary-sm"><i class="fas fa-edit"></i></button>
                                          <button class="btn-primary-warn"><i class="fas fa-bell"></i></button>
                                    </td>
                              </tr>
                        </tbody>
                  </table>
            </div>
      </div>
</template>
