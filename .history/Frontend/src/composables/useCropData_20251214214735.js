/**
 * ========== COMPOSABLE: useCropData.js ==========
 * Purpose: Quản lý dữ liệu chi tiết loại cây và thị trường xuất khẩu
 *
 * Features:
 *   - Dữ liệu loại cây chi tiết cho từng vùng (1 vùng có thể có nhiều cây)
 *   - Thị trường xuất khẩu cho từng loại cây
 *   - Hàm lấy dữ liệu loại cây theo vùng
 *   - Hàm lấy dữ liệu xuất khẩu theo vùng
 */

/**
 * ========== CROP DETAIL DATA ==========
 * Dữ liệu chi tiết loại cây trong từng vùng
 *
 * Structure:
 *   - id: ID duy nhất của record
 *   - maVung: Mã vùng (VT-001, VT-002, ...)
 *   - tenCay: Tên loại cây (Xoài, Thanh Long, ...)
 *   - dienTich: Diện tích trồng (ha)
 *   - namTrau: Năm trồng
 *   - nangSuat: Năng suất (tạ/ha)
 *   - thiBruongXuatKhau: Thị trường xuất khẩu (array: ['Trung Quốc', 'Hoa Kỳ'])
 *   - giaXuat: Giá xuất khẩu (USD/kg)
 */
export const mockCropDetails = [
     // VT-001: HTX Xoài Mỹ Xương
     {
          id: 1,
          maVung: "VT-001",
          tenCay: "Xoài Mỹ Xương",
          dienTich: 8.5,
          namTrau: 2019,
          nangSuat: 42.3,
          thiBruongXuatKhau: ["Trung Quốc", "Hoa Kỳ"],
          giaXuat: 0.85,
     },
     {
          id: 2,
          maVung: "VT-001",
          tenCay: "Nhãn",
          dienTich: 3.2,
          namTrau: 2021,
          nangSuat: 28.5,
          thiBruongXuatKhau: ["Trung Quốc"],
          giaXuat: 0.65,
     },

     // VT-002: Thanh Long VietGAP
     {
          id: 3,
          maVung: "VT-002",
          tenCay: "Thanh Long Đỏ",
          dienTich: 12.0,
          namTrau: 2020,
          nangSuat: 35.8,
          thiBruongXuatKhau: ["Trung Quốc", "Hoa Kỳ", "Châu Âu"],
          giaXuat: 1.2,
     },
     {
          id: 4,
          maVung: "VT-002",
          tenCay: "Thanh Long Trắng",
          dienTich: 6.5,
          namTrau: 2021,
          nangSuat: 32.1,
          thiBruongXuatKhau: ["Trung Quốc", "Châu Âu"],
          giaXuat: 1.0,
     },

     // VT-003: Lúa Chất lượng cao
     {
          id: 5,
          maVung: "VT-003",
          tenCay: "Lúa Jasmine",
          dienTich: 15.0,
          namTrau: 2022,
          nangSuat: 58.5,
          thiBruongXuatKhau: ["Trung Quốc", "ASEAN"],
          giaXuat: 0.45,
     },
     {
          id: 6,
          maVung: "VT-003",
          tenCay: "Lúa Thơm",
          dienTich: 10.0,
          namTrau: 2022,
          nangSuat: 55.2,
          thiBruongXuatKhau: ["Trung Quốc", "Hoa Kỳ"],
          giaXuat: 0.55,
     },

     // VT-004: Sầu Riêng Ri6
     {
          id: 7,
          maVung: "VT-004",
          tenCay: "Sầu Riêng Ri6",
          dienTich: 7.0,
          namTrau: 2018,
          nangSuat: 28.5,
          thiBruongXuatKhau: ["Trung Quốc"],
          giaXuat: 2.5,
     },
     {
          id: 8,
          maVung: "VT-004",
          tenCay: "Sầu Riêng Musang King",
          dienTich: 5.5,
          namTrau: 2020,
          nangSuat: 30.2,
          thiBruongXuatKhau: ["Trung Quốc", "Hoa Kỳ"],
          giaXuat: 3.2,
     },

     // VT-005: Tiêu đen Chất lượng
     {
          id: 9,
          maVung: "VT-005",
          tenCay: "Tiêu đen",
          dienTich: 4.5,
          namTrau: 2019,
          nangSuat: 22.5,
          thiBruongXuatKhau: ["Trung Quốc", "Châu Âu", "Hoa Kỳ"],
          giaXuat: 3.8,
     },
     {
          id: 10,
          maVung: "VT-005",
          tenCay: "Tiêu trắng",
          dienTich: 2.0,
          namTrau: 2021,
          nangSuat: 18.5,
          thiBruongXuatKhau: ["Châu Âu", "Hoa Kỳ"],
          giaXuat: 2.8,
     },
];

/**
 * ========== FUNCTION: Lấy danh sách loại cây theo vùng ==========
 * @param {string} maVung - Mã vùng (VT-001, VT-002, ...)
 * @returns {Array} Danh sách loại cây trong vùng
 */
export function getCropsByZone(maVung) {
     return mockCropDetails.filter((crop) => crop.maVung === maVung);
}

/**
 * ========== FUNCTION: Lấy tổng diện tích cây trồng theo vùng ==========
 * @param {string} maVung - Mã vùng
 * @returns {Number} Tổng diện tích (ha)
 */
export function getTotalAreaByZone(maVung) {
     const crops = getCropsByZone(maVung);
     return crops.reduce((sum, crop) => sum + crop.dienTich, 0);
}

/**
 * ========== FUNCTION: Lấy danh sách thị trường xuất khẩu theo vùng ==========
 * @param {string} maVung - Mã vùng
 * @returns {Array} Danh sách thị trường (không trùng lặp)
 */
export function getMarketsbyZone(maVung) {
     const crops = getCropsByZone(maVung);
     const markets = new Set();
     crops.forEach((crop) => {
          crop.thiBruongXuatKhau.forEach((market) => markets.add(market));
     });
     return Array.from(markets);
}

/**
 * ========== FUNCTION: Lấy dữ liệu cây để vẽ biểu đồ bar chart ==========
 * Tính tổng năng suất theo loại cây (tất cả vùng)
 * @returns {Array} Danh sách {tenCay, nangSuat, dienTich}
 */
export function getCropProductivityData() {
     const cropMap = {};

     mockCropDetails.forEach((crop) => {
          if (!cropMap[crop.tenCay]) {
               cropMap[crop.tenCay] = {
                    tenCay: crop.tenCay,
                    nangSuat: crop.nangSuat,
                    dienTich: crop.dienTich,
                    count: 1,
               };
          } else {
               // Nếu loại cây có nhiều lần, lấy trung bình năng suất
               cropMap[crop.tenCay].nangSuat =
                    (cropMap[crop.tenCay].nangSuat + crop.nangSuat) / 2;
               cropMap[crop.tenCay].dienTich += crop.dienTich;
               cropMap[crop.tenCay].count += 1;
          }
     });

     return Object.values(cropMap).sort((a, b) => b.nangSuat - a.nangSuat);
}

/**
 * ========== FUNCTION: Lấy dữ liệu xuất khẩu theo thị trường ==========
 * Tính tổng giá trị xuất khẩu theo thị trường (thị trường nào có cây gì)
 * @returns {Array} Danh sách {market, value, cropCount}
 */
export function getExportMarketData() {
     const marketMap = {};

     mockCropDetails.forEach((crop) => {
          crop.thiBruongXuatKhau.forEach((market) => {
               if (!marketMap[market]) {
                    marketMap[market] = {
                         market: market,
                         value: 0,
                         crops: [],
                    };
               }
               // Tính giá trị xuất khẩu = diện tích * năng suất * giá xuất khẩu
               const exportValue = crop.dienTich * crop.nangSuat * crop.giaXuat;
               marketMap[market].value += exportValue;

               // Thêm loại cây vào list (không trùng)
               if (
                    !marketMap[market].crops.some(
                         (c) => c.tenCay === crop.tenCay
                    )
               ) {
                    marketMap[market].crops.push({
                         tenCay: crop.tenCay,
                         giaXuat: crop.giaXuat,
                    });
               }
          });
     });

     return Object.values(marketMap)
          .sort((a, b) => b.value - a.value)
          .map((m) => ({
               market: m.market,
               value: Math.round(m.value),
               cropCount: m.crops.length,
          }));
}

/**
 * ========== FUNCTION: Lấy danh sách tất cả loại cây ==========
 * @returns {Array} Danh sách loại cây (không trùng lặp)
 */
export function getAllCrops() {
     const crops = new Set();
     mockCropDetails.forEach((crop) => crops.add(crop.tenCay));
     return Array.from(crops).sort();
}

/**
 * ========== FUNCTION: Lấy danh sách tất cả thị trường ==========
 * @returns {Array} Danh sách thị trường (không trùng lặp)
 */
export function getAllMarkets() {
     const markets = new Set();
     mockCropDetails.forEach((crop) => {
          crop.thiBruongXuatKhau.forEach((market) => markets.add(market));
     });
     return Array.from(markets).sort();
}
