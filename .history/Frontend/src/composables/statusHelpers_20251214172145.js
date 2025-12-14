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
          toaDo: [10.762, 106.66],
     },
     {
          id: 2,
          ma: "VT-002",
          ten: "Thanh Long VietGAP",
          chu: "Trần Thị B",
          trangThai: "sau_benh",
          toaDo: [10.77, 106.67],
     },
     {
          id: 3,
          ma: "VT-003",
          ten: "Lúa Chất lượng cao",
          chu: "HTX Lúa Vàng",
          trangThai: "thu_hoach",
          toaDo: [10.75, 106.65],
     },
     {
          id: 4,
          ma: "VT-004",
          ten: "Sầu Riêng Ri6",
          chu: "Lê Văn C",
          trangThai: "da_thu_hoach",
          toaDo: [10.78, 106.64],
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
