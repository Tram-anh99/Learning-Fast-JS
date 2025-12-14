/**
 * ========== COMPOSABLE: useCharts.js ==========
 * Purpose: Quản lý dữ liệu và logic cho các biểu đồ thống kê trong QuanLyView
 * 
 * Features:
 *   - Dữ liệu pie chart (thị trường xuất khẩu)
 *   - Dữ liệu bar chart (sản lượng cây trồng)
 *   - Dữ liệu line chart (xu hướng theo thời gian)
 *   - Hàm tính toán gradient conic cho pie chart
 *   - Hàm API integration để lấy data thực tế
 */

import { ref, computed } from 'vue';

/**
 * ========== EXPORT CHART MARKET DATA ==========
 * Dữ liệu biểu đồ tròn phân bổ thị trường xuất khẩu
 * 
 * Structure:
 *   - label: Tên thị trường (Trung Quốc, Hoa Kỳ, Châu Âu, ...)
 *   - value: Tỉ lệ phần trăm (%)
 *   - color: Mã màu hex (dùng cho conic-gradient)
 */
const exportData = ref([
  { label: 'Trung Quốc', value: 45, color: '#ef4444' },   // red-500
  { label: 'Hoa Kỳ', value: 25, color: '#3b82f6' },       // blue-500
  { label: 'Châu Âu', value: 20, color: '#10b981' },      // emerald-500
  { label: 'Khác', value: 10, color: '#f59e0b' },         // amber-500
]);

/**
 * ========== CROP PRODUCTION DATA ==========
 * Dữ liệu biểu đồ cột sản lượng theo loại cây
 * 
 * Structure:
 *   - label: Tên cây trồng (Lúa, Xoài, Thanh Long, ...)
 *   - value: Giá trị sản lượng (%)
 *   - color: Tailwind class color (bg-yellow-400, bg-green-500, ...)
 */
const cropData = ref([
  { label: 'Lúa', value: 85, color: 'bg-yellow-400' },
  { label: 'Xoài', value: 65, color: 'bg-green-500' },
  { label: 'Thanh Long', value: 45, color: 'bg-red-500' },
  { label: 'Sầu Riêng', value: 30, color: 'bg-orange-400' },
]);

/**
 * ========== PRODUCTIVITY TREND DATA ==========
 * Dữ liệu line chart xu hướng năng suất theo tháng
 * 
 * Structure:
 *   - month: Tháng (T1, T2, T3, ...)
 *   - productivity: Năng suất (tấn/hectare)
 *   - quality: Chất lượng (điểm 1-10)
 */
const productivityTrendData = ref([
  { month: 'T1', productivity: 4.2, quality: 7.5 },
  { month: 'T2', productivity: 5.1, quality: 7.8 },
  { month: 'T3', productivity: 4.8, quality: 7.6 },
  { month: 'T4', productivity: 5.5, quality: 8.0 },
  { month: 'T5', productivity: 5.9, quality: 8.2 },
  { month: 'T6', productivity: 5.3, quality: 8.1 },
]);

/**
 * ========== COMPUTED: Pie Chart Gradient Style ==========
 * Tính toán conic-gradient style cho biểu đồ tròn
 * 
 * Logic:
 *   1. Loop qua từng segment của exportData
 *   2. Tính góc bắt đầu và góc kết thúc dựa vào tỉ lệ %
 *   3. Tạo chuỗi gradient: "color start deg end deg"
 *   4. Trả về object style {background: 'conic-gradient(...)'}
 * 
 * Example:
 *   Nếu Trung Quốc = 45%, kết quả: "red 0deg 162deg"
 *   Nếu Hoa Kỳ = 25%, kết quả: "blue 162deg 252deg"
 */
const pieChartStyle = computed(() => {
  let currentAngle = 0;
  const gradientParts = exportData.value.map(item => {
    const start = currentAngle;
    const end = currentAngle + (item.value / 100) * 360;
    currentAngle = end;
    return `${item.color} ${start}deg ${end}deg`;
  });
  return {
    background: `conic-gradient(${gradientParts.join(', ')})`
  };
});

/**
 * ========== COMPUTED: Total Export Value ==========
 * Tính tổng giá trị phần trăm (kiểm tra hợp lệ = 100%)
 */
const totalExportValue = computed(() => {
  return exportData.value.reduce((sum, item) => sum + item.value, 0);
});

/**
 * ========== COMPUTED: Crops sorted by production ==========
 * Sắp xếp cây trồng theo sản lượng (cao nhất trước)
 */
const sortedCropData = computed(() => {
  return [...cropData.value].sort((a, b) => b.value - a.value);
});

/**
 * ========== FUNCTION: Add new export market ==========
 * Thêm thị trường xuất khẩu mới
 * 
 * @param {Object} newMarket - {label, value, color}
 * Example: addExportMarket({label: 'Việt Nam', value: 5, color: '#fbbf24'})
 */
const addExportMarket = (newMarket) => {
  // Kiểm tra xem thị trường đã tồn tại chưa
  const exists = exportData.value.some(m => m.label === newMarket.label);
  if (!exists && newMarket.value > 0) {
    exportData.value.push(newMarket);
    // Cập nhật nếu vượt quá 100%
    if (totalExportValue.value > 100) {
      const excess = totalExportValue.value - 100;
      const lastItem = exportData.value[exportData.value.length - 2];
      if (lastItem) {
        lastItem.value -= excess;
      }
    }
  }
};

/**
 * ========== FUNCTION: Update export data from API ==========
 * Lấy dữ liệu biểu đồ từ server
 * 
 * Note: Hiện tại dùng mock data, sau tích hợp API thay thế
 * 
 * @returns {Promise}
 * Example: const data = await fetchExportData()
 */
const fetchExportData = async () => {
  try {
    // TODO: Thay bằng API call thực tế
    // const response = await fetch('/api/charts/export-markets');
    // const data = await response.json();
    // exportData.value = data;
    
    console.log('📊 Fetching export market data...');
    return exportData.value;
  } catch (error) {
    console.error('❌ Error fetching export data:', error);
  }
};

/**
 * ========== FUNCTION: Update crop production data from API ==========
 * Lấy dữ liệu sản lượng cây trồng từ server
 * 
 * @returns {Promise}
 */
const fetchCropData = async () => {
  try {
    // TODO: Thay bằng API call thực tế
    // const response = await fetch('/api/charts/crop-production');
    // const data = await response.json();
    // cropData.value = data;
    
    console.log('📊 Fetching crop production data...');
    return cropData.value;
  } catch (error) {
    console.error('❌ Error fetching crop data:', error);
  }
};

/**
 * ========== FUNCTION: Update productivity trend from API ==========
 * Lấy dữ liệu xu hướng năng suất
 * 
 * @returns {Promise}
 */
const fetchProductivityTrend = async () => {
  try {
    // TODO: Thay bằng API call thực tế
    // const response = await fetch('/api/charts/productivity-trend');
    // const data = await response.json();
    // productivityTrendData.value = data;
    
    console.log('📊 Fetching productivity trend data...');
    return productivityTrendData.value;
  } catch (error) {
    console.error('❌ Error fetching productivity trend:', error);
  }
};

/**
 * ========== FUNCTION: Get highest producing crop ==========
 * Tìm cây trồng có sản lượng cao nhất
 * 
 * @returns {Object} Cây trồng với sản lượng cao nhất
 */
const getTopCrop = () => {
  return sortedCropData.value[0] || null;
};

/**
 * ========== FUNCTION: Get market share for specific market ==========
 * Lấy tỉ lệ thị trường cho một thị trường cụ thể
 * 
 * @param {String} marketLabel - Tên thị trường
 * @returns {Number} Tỉ lệ %
 */
const getMarketShare = (marketLabel) => {
  const market = exportData.value.find(m => m.label === marketLabel);
  return market ? market.value : 0;
};

/**
 * ========== FUNCTION: Get average productivity ==========
 * Tính năng suất trung bình
 * 
 * @returns {Number} Năng suất trung bình
 */
const getAverageProductivity = () => {
  if (productivityTrendData.value.length === 0) return 0;
  const total = productivityTrendData.value.reduce(
    (sum, item) => sum + item.productivity, 
    0
  );
  return (total / productivityTrendData.value.length).toFixed(2);
};

export {
  // Data refs
  exportData,
  cropData,
  productivityTrendData,
  
  // Computed
  pieChartStyle,
  totalExportValue,
  sortedCropData,
  
  // Functions
  addExportMarket,
  fetchExportData,
  fetchCropData,
  fetchProductivityTrend,
  getTopCrop,
  getMarketShare,
  getAverageProductivity,
};
