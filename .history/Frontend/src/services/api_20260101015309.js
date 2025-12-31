"""
========== Frontend API Service ==========
File: Frontend/src/services/api.js
Mục đích: Quản lý tất cả API calls từ Frontend đến Backend
Kết nối với: Backend FastAPI (http://localhost:8000)
===========================================
"""

/**
 * BASE API CONFIGURATION
 * Cấu hình địa chỉ gốc của Backend API
 * 
 * Development: http://localhost:8000/api
 * Production: Thay đổi thành domain thực
 */
const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Helper function để xử lý HTTP errors
 * 
 * @param {Response} response - Fetch API response object
 * @returns {Response} - Original response nếu OK
 * @throws {Error} - Throw error với message từ backend nếu có lỗi
 */
async function handleResponse(response) {
  // Kiểm tra response.ok (status 200-299)
  if (!response.ok) {
    // Cố gắng lấy error message từ backend
    try {
      const errorData = await response.json();
      throw new Error(errorData.detail || errorData.message || 'API request failed');
    } catch (e) {
      // Nếu không parse được JSON, dùng statusText
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
  }
  return response;
}

/**
 * ============================================
 * HEALTH & SYSTEM APIs
 * ============================================
 */

/**
 * Kiểm tra trạng thái Backend và Database
 * 
 * Endpoint: GET /api/health
 * 
 * @returns {Promise<Object>} Health status object
 *   {
 *     status: "healthy",
 *     database_connected: true,
 *     total_tables: 18,
 *     schema: "nongsan"
 *   }
 */
export async function getHealthStatus() {
  const response = await fetch(`${API_BASE_URL}/health`);
  await handleResponse(response);
  return await response.json();
}

/**
 * ============================================
 * FARMS APIs (Vùng Trồng - MSVT)
 * ============================================
 */

/**
 * Lấy danh sách vùng trồng với pagination và filter
 * 
 * Endpoint: GET /api/farms
 * 
 * @param {Object} params - Query parameters
 * @param {number} params.skip - Số record bỏ qua (default: 0)
 * @param {number} params.limit - Số record tối đa (default: 100)
 * @param {string} params.search - Tìm kiếm theo mã/tên vùng
 * @param {number} params.trang_thai_id - Filter theo trạng thái
 * 
 * @returns {Promise<Object>} Paginated farms data
 *   {
 *     total: 150,
 *     skip: 0,
 *     limit: 100,
 *     data: [...]
 *   }
 */
export async function getFarms(params = {}) {
  // Build query string từ params object
  const queryParams = new URLSearchParams();
  
  // Thêm các params vào query string nếu có giá trị
  if (params.skip !== undefined) queryParams.append('skip', params.skip);
  if (params.limit !== undefined) queryParams.append('limit', params.limit);
  if (params.search) queryParams.append('search', params.search);
  if (params.trang_thai_id) queryParams.append('trang_thai_id', params.trang_thai_id);
  
  // Gọi API với query string
  const response = await fetch(`${API_BASE_URL}/farms?${queryParams.toString()}`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy chi tiết một vùng trồng theo ID
 * 
 * Endpoint: GET /api/farms/{id}
 * 
 * @param {number} id - Farm ID
 * @returns {Promise<Object>} Farm detail object with relationships
 *   {
 *     id, ma_vung, ten_vung, dia_chi, dien_tich_ha,
 *     chu_vung: {...},
 *     trang_thai: {...},
 *     toa_do: [...]
 *   }
 */
export async function getFarmById(id) {
  const response = await fetch(`${API_BASE_URL}/farms/${id}`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Tìm vùng trồng theo mã MSVT
 * 
 * Endpoint: GET /api/farms/by-code/{ma_vung}
 * 
 * @param {string} maVung - Mã MSVT (vd: "MSVT2024001")
 * @returns {Promise<Object>} Farm basic info
 */
export async function getFarmByCode(maVung) {
  const response = await fetch(`${API_BASE_URL}/farms/by-code/${maVung}`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Tạo vùng trồng mới
 * 
 * Endpoint: POST /api/farms
 * 
 * @param {Object} farmData - Farm data object
 * @param {string} farmData.ma_vung - Mã MSVT (bắt buộc, unique)
 * @param {string} farmData.ten_vung - Tên vùng trồng (bắt buộc)
 * @param {string} farmData.dia_chi - Địa chỉ
 * @param {number} farmData.dien_tich_ha - Diện tích (hecta)
 * @param {string} farmData.ngay_cap_ma - Ngày cấp mã (YYYY-MM-DD)
 * @param {string} farmData.ngay_het_han - Ngày hết hạn (YYYY-MM-DD)
 * @param {number} farmData.chu_vung_id - ID chủ vùng
 * @param {number} farmData.trang_thai_id - ID trạng thái
 * @param {Array} farmData.toa_do - Mảng tọa độ polygon [{latitude, longitude, thu_tu}]
 * 
 * @returns {Promise<Object>} Created farm object
 */
export async function createFarm(farmData) {
  const response = await fetch(`${API_BASE_URL}/farms`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(farmData)
  });
  await handleResponse(response);
  return await response.json();
}

/**
 * Cập nhật thông tin vùng trồng
 * 
 * Endpoint: PUT /api/farms/{id}
 * 
 * @param {number} id - Farm ID
 * @param {Object} farmData - Farm data object (same as createFarm)
 * @returns {Promise<Object>} Updated farm object
 */
export async function updateFarm(id, farmData) {
  const response = await fetch(`${API_BASE_URL}/farms/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(farmData)
  });
  await handleResponse(response);
  return await response.json();
}

/**
 * Xóa vùng trồng
 * 
 * Endpoint: DELETE /api/farms/{id}
 * 
 * @param {number} id - Farm ID
 * @returns {Promise<Object>} Success message
 */
export async function deleteFarm(id) {
  const response = await fetch(`${API_BASE_URL}/farms/${id}`, {
    method: 'DELETE'
  });
  await handleResponse(response);
  return await response.json();
}

/**
 * ============================================
 * CHARTS & STATISTICS APIs
 * ============================================
 */

/**
 * Lấy thống kê tổng quan cho dashboard
 * 
 * Endpoint: GET /api/charts/dashboard-stats
 * 
 * @returns {Promise<Object>} Dashboard statistics
 *   {
 *     total_farms: 150,
 *     active_farms: 142,
 *     total_area_ha: 1250.75,
 *     total_production: 5420.30,
 *     recent_activities: 87
 *   }
 */
export async function getDashboardStats() {
  const response = await fetch(`${API_BASE_URL}/charts/dashboard-stats`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy dữ liệu cho biểu đồ thị trường xuất khẩu (Pie Chart)
 * 
 * Endpoint: GET /api/charts/export-markets
 * 
 * @returns {Promise<Object>} Chart.js compatible data
 *   {
 *     labels: ["Trung Quốc", "Hoa Kỳ", ...],
 *     datasets: [{
 *       data: [35, 25, ...],
 *       backgroundColor: ["#FF6384", ...]
 *     }]
 *   }
 */
export async function getExportMarketsChart() {
  const response = await fetch(`${API_BASE_URL}/charts/export-markets`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy dữ liệu cho biểu đồ sản lượng cây trồng (Bar Chart)
 * 
 * Endpoint: GET /api/charts/crop-production
 * 
 * @returns {Promise<Object>} Chart.js compatible data
 */
export async function getCropProductionChart() {
  const response = await fetch(`${API_BASE_URL}/charts/crop-production`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy dữ liệu cho biểu đồ xu hướng năng suất (Line Chart)
 * 
 * Endpoint: GET /api/charts/productivity-trend
 * 
 * @param {number} years - Số năm lấy dữ liệu (default: 5)
 * @returns {Promise<Object>} Chart.js compatible data
 */
export async function getProductivityTrendChart(years = 5) {
  const response = await fetch(`${API_BASE_URL}/charts/productivity-trend?years=${years}`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy dữ liệu phân bổ trạng thái vùng trồng
 * 
 * Endpoint: GET /api/charts/farm-status
 * 
 * @returns {Promise<Object>} Chart.js compatible data
 */
export async function getFarmStatusChart() {
  const response = await fetch(`${API_BASE_URL}/charts/farm-status`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy dữ liệu timeline hoạt động canh tác
 * 
 * Endpoint: GET /api/charts/activity-timeline
 * 
 * @param {number} days - Số ngày lấy dữ liệu (default: 30)
 * @returns {Promise<Object>} Chart.js compatible data
 */
export async function getActivityTimeline(days = 30) {
  const response = await fetch(`${API_BASE_URL}/charts/activity-timeline?days=${days}`);
  await handleResponse(response);
  return await response.json();
}

/**
 * ============================================
 * DIARY APIs (Nhật Ký Canh Tác)
 * ============================================
 */

/**
 * Lấy danh sách nhật ký canh tác với filter
 * 
 * Endpoint: GET /api/diary
 * 
 * @param {Object} params - Query parameters
 * @param {number} params.skip - Số record bỏ qua
 * @param {number} params.limit - Số record tối đa
 * @param {number} params.vung_trong_id - Filter theo vùng trồng
 * @param {number} params.loai_hoat_dong_id - Filter theo loại hoạt động
 * @param {string} params.from_date - Từ ngày (YYYY-MM-DD)
 * @param {string} params.to_date - Đến ngày (YYYY-MM-DD)
 * 
 * @returns {Promise<Object>} Paginated diary entries
 */
export async function getDiaryEntries(params = {}) {
  const queryParams = new URLSearchParams();
  
  if (params.skip !== undefined) queryParams.append('skip', params.skip);
  if (params.limit !== undefined) queryParams.append('limit', params.limit);
  if (params.vung_trong_id) queryParams.append('vung_trong_id', params.vung_trong_id);
  if (params.loai_hoat_dong_id) queryParams.append('loai_hoat_dong_id', params.loai_hoat_dong_id);
  if (params.from_date) queryParams.append('from_date', params.from_date);
  if (params.to_date) queryParams.append('to_date', params.to_date);
  
  const response = await fetch(`${API_BASE_URL}/diary?${queryParams.toString()}`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy chi tiết một nhật ký
 * 
 * Endpoint: GET /api/diary/{id}
 * 
 * @param {number} id - Diary entry ID
 * @returns {Promise<Object>} Diary entry detail
 */
export async function getDiaryById(id) {
  const response = await fetch(`${API_BASE_URL}/diary/${id}`);
  await handleResponse(response);
  return await response.json();
}

/**
 * Tạo nhật ký canh tác mới
 * 
 * Endpoint: POST /api/diary
 * 
 * @param {Object} entryData - Diary entry data
 * @param {number} entryData.vung_trong_id - ID vùng trồng (bắt buộc)
 * @param {number} entryData.loai_hoat_dong_id - ID loại hoạt động
 * @param {string} entryData.ngay_thuc_hien - Ngày thực hiện (YYYY-MM-DD)
 * @param {string} entryData.mo_ta - Mô tả
 * @param {number} entryData.phan_bon_id - ID phân bón (nếu có)
 * @param {number} entryData.thuoc_bvtv_id - ID thuốc BVTV (nếu có)
 * @param {number} entryData.luong_su_dung - Lượng sử dụng
 * @param {string} entryData.don_vi - Đơn vị (kg, lít, etc.)
 * @param {string} entryData.nguoi_thuc_hien - Người thực hiện
 * 
 * @returns {Promise<Object>} Created diary entry
 */
export async function createDiaryEntry(entryData) {
  const response = await fetch(`${API_BASE_URL}/diary`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(entryData)
  });
  await handleResponse(response);
  return await response.json();
}

/**
 * Cập nhật nhật ký
 * 
 * Endpoint: PUT /api/diary/{id}
 * 
 * @param {number} id - Diary entry ID
 * @param {Object} entryData - Diary entry data (same as createDiaryEntry)
 * @returns {Promise<Object>} Updated diary entry
 */
export async function updateDiaryEntry(id, entryData) {
  const response = await fetch(`${API_BASE_URL}/diary/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(entryData)
  });
  await handleResponse(response);
  return await response.json();
}

/**
 * Xóa nhật ký
 * 
 * Endpoint: DELETE /api/diary/{id}
 * 
 * @param {number} id - Diary entry ID
 * @returns {Promise<Object>} Success message
 */
export async function deleteDiaryEntry(id) {
  const response = await fetch(`${API_BASE_URL}/diary/${id}`, {
    method: 'DELETE'
  });
  await handleResponse(response);
  return await response.json();
}

/**
 * Lấy danh sách loại hoạt động canh tác
 * 
 * Endpoint: GET /api/diary/activity-types
 * 
 * @returns {Promise<Array>} Array of activity types
 *   [{id, ma_loai, ten_loai, nhom, icon}]
 */
export async function getActivityTypes() {
  const response = await fetch(`${API_BASE_URL}/diary/activity-types/`);
  await handleResponse(response);
  return await response.json();
}

/**
 * ============================================
 * DEFAULT EXPORT
 * Xuất tất cả functions để dùng trong components
 * ============================================
 */
export default {
  // Health
  getHealthStatus,
  
  // Farms
  getFarms,
  getFarmById,
  getFarmByCode,
  createFarm,
  updateFarm,
  deleteFarm,
  
  // Charts
  getDashboardStats,
  getExportMarketsChart,
  getCropProductionChart,
  getProductivityTrendChart,
  getFarmStatusChart,
  getActivityTimeline,
  
  // Diary
  getDiaryEntries,
  getDiaryById,
  createDiaryEntry,
  updateDiaryEntry,
  deleteDiaryEntry,
  getActivityTypes
};
