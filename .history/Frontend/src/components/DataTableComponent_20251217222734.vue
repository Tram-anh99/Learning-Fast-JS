<script setup>
/**
 * ========== COMPONENT: DataTableComponent.vue ==========
 * Purpose: Hiển thị bảng danh sách vùng trồng với scroll custom & tương tác
 * 
 * Features:
 *   - Scrollable table with custom scrollbar styling
 *   - Status badges for cultivation status
 *   - Action buttons (Edit, Alert)
 *   - Export report functionality
 *   - Interactive selection with highlight
 * 
 * Props:
 *   - danhSachVung: Array of farm zones (id, ma, ten, chu, trangThai)
 *   - selectedVung: Currently selected zone (for highlighting)
 * 
 * Emits:
 *   - selectVung: Fired when user clicks on a row
 */

import { getStatusBadge } from '../composables/statusHelpers';

defineProps({
      danhSachVung: { type: Array, required: true },
      selectedVung: { type: Object, default: null }
});

defineEmits(['selectVung']);
</script>

<template>
      <div class="panel flex flex-col min-h-[280px] sm:min-h-[350px] max-h-[500px] sm:max-h-[600px] overflow-hidden">
            <div class="panel-header flex-shrink-0 px-3 sm:px-6 py-3 sm:py-5">
                  <h3 class="panel-title text-sm sm:text-lg">Danh sách Vùng trồng</h3>
                  <button class="btn-primary text-xs sm:text-sm px-2 sm:px-4 py-1.5 sm:py-2.5">
                        <i class="fas fa-file-export"></i> <span class="hidden sm:inline">Xuất báo cáo</span>
                  </button>
            </div>

            <!-- Scrollable table container with custom scrollbar -->
            <div class="overflow-auto flex-grow scrollbar-custom">
                  <table class="w-full border-collapse min-w-[500px]">
                        <thead class="sticky top-0 z-10 bg-white shadow-sm">
                              <tr>
                                    <th class="table-header text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3">Mã số</th>
                                    <th class="table-header text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3">Tên vùng</th>
                                    <th class="table-header text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3 hidden md:table-cell">Chủ hộ</th>
                                    <th class="table-header text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3 hidden sm:table-cell">Mã</th>
                                    <th class="table-header text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3">Trạng thái</th>
                                    <th class="table-header text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3">Thao tác</th>
                              </tr>
                        </thead>
                        <tbody>
                              <tr v-for="vung in danhSachVung" :key="vung.id"
                                    class="table-row-hover cursor-pointer transition-all"
                                    :class="{ 'bg-blue-100 border-l-4 border-blue-500': selectedVung?.id === vung.id }"
                                    @click="$emit('selectVung', vung)">
                                    <td class="table-cell text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3"><strong>{{ vung.ma }}</strong></td>
                                    <td class="table-cell text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3">{{ vung.ten }}</td>
                                    <td class="table-cell text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3 hidden md:table-cell">{{ vung.chu }}</td>
                                    <td class="table-cell text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3 hidden sm:table-cell">
                                          <span
                                                :class="vung.trangThaiMa === 'bi_thu_hoi' ? 'badge-danger' : 'badge-success'"
                                                class="text-[10px] sm:text-xs px-1.5 sm:px-3 py-0.5 sm:py-1.5">
                                                {{ vung.trangThaiMa === 'bi_thu_hoi' ? 'Thu hồi' : 'HĐ' }}
                                          </span>
                                    </td>
                                    <td class="table-cell text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3">
                                          <span :class="`badge-${getStatusBadge(vung.trangThai).class.split('-')[1]}`"
                                                class="text-[10px] sm:text-xs px-1.5 sm:px-3 py-0.5 sm:py-1.5">
                                                {{ getStatusBadge(vung.trangThai).text }}
                                          </span>
                                    </td>
                                    <td class="table-cell text-xs sm:text-sm px-2 sm:px-5 py-2 sm:py-3 space-x-1">
                                          <button class="btn-primary-sm w-7 h-7 sm:w-9 sm:h-9"><i class="fas fa-edit text-xs"></i></button>
                                          <button class="btn-primary-warn w-7 h-7 sm:w-9 sm:h-9"><i class="fas fa-bell text-xs"></i></button>
                                    </td>
                              </tr>
                        </tbody>
                  </table>
            </div>
      </div>
</template>
