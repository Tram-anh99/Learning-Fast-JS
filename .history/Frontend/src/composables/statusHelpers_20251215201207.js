/**
 * ========== COMPOSABLE HELPERS: statusHelpers.js ==========
 * Purpose: Centralized status mapping & helper functions
 * Features:
 *   - Convert status → badge (text, color, class)
 *   - Convert status → CSS class
 *   - Convert status → Display text (Tiếng Việt)
 *   - Mock data for testing & development
 */

// ========== STATUS MAPPING HELPERS ==========

/**
 * Lấy thông tin badge trạng thái vùng trồng
 * Map từ status value → display object (text, color, class)
 */
export function getStatusBadge(status) {
     const statusMap = {
          canh_tac: {
               text: "Đang canh tác",
               class: "bg-green-500",
               color: "#4caf50",
          },
          sau_benh: {
               text: "Cảnh báo dịch hại",
               class: "bg-red-500",
               color: "#ef5350",
          },
          thu_hoach: {
               text: "Đang thu hoạch",
               class: "bg-yellow-500",
               color: "#ffca28",
          },
          da_thu_hoach: {
               text: "Đã thu hoạch",
               class: "bg-blue-600",
               color: "#2563eb",
          },
          // Legacy status names (for backward compatibility)
          active: {
               text: "Đang hoạt động",
               class: "bg-green-500",
               color: "#4caf50",
          },
          warning: { text: "Cảnh báo", class: "bg-red-500", color: "#ef5350" },
          revoked: { text: "Đã thu hồi", class: "bg-gray-500", color: "#999" },
     };
     // Return matching status or default danger
     return (
          statusMap[status] || {
               text: "Không xác định",
               class: "bg-gray-500",
               color: "#999",
          }
     );
}

/**
 * Lấy class CSS Badge theo trạng thái (cho template)
 */
export function getClassTrangThai(status) {
     return getStatusBadge(status).class + " text-white";
}

/**
 * Lấy text hiển thị theo trạng thái
 */
export function getTextTrangThai(status) {
     return getStatusBadge(status).text;
}

/**
 * Lấy màu hex theo trạng thái
 * Shared with useMapLogic.getMapColor()
 */
export function getMapColor(status) {
     return getStatusBadge(status).color;
}

// ========== MOCK DATA ==========

/**
 * Mock data thống kê hệ thống
 * Sử dụng cho dashboard & stats widget
 */
export const mockDataThongKe = {
     tongVung: 124, // Tổng số vùng trồng được quản lý
     dienTich: "450 ha", // Tổng diện tích
     sanLuongDuKien: "1.200 tấn", // Sản lượng dự kiến
     canhBao: 5, // Số cảnh báo vi phạm
     maBiThuHoi: 2, // Số mã vùng bị thu hồi (VT-003, VT-005)
};

/**
 * Mock data danh sách vùng trồng
 * Sử dụng cho bản đồ & danh sách
 */
export const mockDataVung = [
     {
          id: 1,
          ma: "VT-001",
          ten: "HTX Xoài Mỹ Xương",
          chu: "Nguyễn Văn A",
          trangThai: "canh_tac",
          trangThaiMa: "hoat_dong",
          // 4 góc polygon (Tây Bắc, Đông Bắc, Đông Nam, Tây Nam)
          toaDo: [
               [10.759, 106.656],
               [10.759, 106.664],
               [10.765, 106.664],
               [10.765, 106.656],
          ],
          // Thông tin canh tác
          lichSuCanhTac: [
               { ngay: "2024-12-01", hoatDong: "Bón phân NPK", nguoiThucHien: "Nguyễn Văn A" },
               { ngay: "2024-11-15", hoatDong: "Phun thuốc trừ sâu", nguoiThucHien: "Nguyễn Văn A" },
               { ngay: "2024-11-01", hoatDong: "Tưới nước", nguoiThucHien: "Nguyễn Văn A" },
          ],
          // Mã QR để truy xuất
          maQR: "VT-001",
     },
     {
          id: 2,
          ma: "VT-002",
          ten: "Thanh Long VietGAP",
          chu: "Trần Thị B",
          trangThai: "sau_benh",
          trangThaiMa: "hoat_dong",
          // 4 góc polygon
          toaDo: [
               [10.768, 106.668],
               [10.768, 106.676],
               [10.772, 106.676],
               [10.772, 106.668],
          ],
          // Thông tin canh tác
          lichSuCanhTac: [
               { ngay: "2024-12-10", hoatDong: "Phát hiện sâu hại - Xử lý khẩn cấp", nguoiThucHien: "Trần Thị B" },
               { ngay: "2024-12-05", hoatDong: "Bón phân hữu cơ", nguoiThucHien: "Trần Thị B" },
               { ngay: "2024-11-20", hoatDong: "Tỉa cành", nguoiThucHien: "Trần Thị B" },
          ],
          maQR: "VT-002",
     },
     {
          id: 3,
          ma: "VT-003",
          ten: "Lúa Chất lượng cao",
          chu: "HTX Lúa Vàng",
          trangThai: "thu_hoach",
          trangThaiMa: "bi_thu_hoi",
          // 4 góc polygon
          toaDo: [
               [10.747, 106.648],
               [10.747, 106.656],
               [10.753, 106.656],
               [10.753, 106.648],
          ],
          lichSuCanhTac: [
               { ngay: "2024-12-14", hoatDong: "Thu hoạch lúa", nguoiThucHien: "HTX Lúa Vàng" },
               { ngay: "2024-11-30", hoatDong: "Phát hiện dư lượng thuốc vượt ngưỡng", nguoiThucHien: "Thanh tra" },
               { ngay: "2024-11-25", hoatDong: "Phun thuốc diệt cỏ", nguoiThucHien: "HTX Lúa Vàng" },
          ],
          maQR: "VT-003",
     },
     {
          id: 4,
          ma: "VT-004",
          ten: "Sầu Riêng Ri6",
          chu: "Lê Văn C",
          trangThai: "da_thu_hoach",
          trangThaiMa: "hoat_dong",
          // 4 góc polygon
          toaDo: [
               [10.777, 106.637],
               [10.777, 106.645],
               [10.781, 106.645],
               [10.781, 106.637],
          ],
          lichSuCanhTac: [
               { ngay: "2024-12-08", hoatDong: "Hoàn thành thu hoạch", nguoiThucHien: "Lê Văn C" },
               { ngay: "2024-11-28", hoatDong: "Đóng gói và vận chuyển", nguoiThucHien: "Lê Văn C" },
               { ngay: "2024-11-15", hoatDong: "Kiểm định chất lượng", nguoiThucHien: "Chi cục NN" },
          ],
          maQR: "VT-004",
     },
     {
          id: 5,
          ma: "VT-005",
          ten: "Tiêu đen Chất lượng",
          chu: "Võ Văn D",
          trangThai: "canh_tac",
          trangThaiMa: "bi_thu_hoi",
          // 4 góc polygon
          toaDo: [
               [10.758, 106.662],
               [10.758, 106.67],
               [10.762, 106.67],
               [10.762, 106.662],
          ],
     },
];

/**
 * Mock data điểm phát sinh sâu bệnh
 * Sử dụng cho layer sâu bệnh trên bản đồ
 */
export const mockDiemNongSauBenh = [
     [10.77, 106.67],
     [10.771, 106.671],
     [10.769, 106.669],
     [10.75, 106.65],
];
