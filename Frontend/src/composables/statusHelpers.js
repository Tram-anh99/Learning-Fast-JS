// Lấy thông tin badge trạng thái vùng trồng
export function getStatusBadge(status) {
     const statusMap = {
          active: { text: "Đang hoạt động", class: "badge-active" },
          warning: { text: "Cảnh báo", class: "badge-warning" },
          revoked: { text: "Đã thu hồi", class: "badge-danger" },
     };
     // Trả về status tương ứng hoặc mặc định là danger
     return (
          statusMap[status] || { text: "Không xác định", class: "badge-danger" }
     );
}

// Mock data thống kê hệ thống
export const mockDataThongKe = {
     tongVung: 124, // Tổng số vùng trồng được quản lý
     dienTich: "450 ha", // Tổng diện tích
     sanLuongDuKien: "1.200 tấn", // Sản lượng dự kiến
     canhBao: 5, // Số cảnh báo vi phạm
};

// Mock data danh sách vùng trồng
export const mockDataVung = [
     {
          id: 1,
          ma: "VT-001", // Mã số vùng
          ten: "HTX Xoài Mỹ Xương", // Tên vùng trồng
          chu: "Nguyễn Văn A", // Chủ hộ
          trangThai: "active", // Trạng thái: active/warning/revoked
          toaDo: [10.762, 106.66], // [latitude, longitude]
     },
     {
          id: 2,
          ma: "VT-002",
          ten: "Thanh Long VietGAP",
          chu: "Trần Thị B",
          trangThai: "warning",
          toaDo: [10.77, 106.67],
     },
     {
          id: 3,
          ma: "VT-003",
          ten: "Lúa Chất lượng cao",
          chu: "HTX Lúa Vàng",
          trangThai: "revoked",
          toaDo: [10.75, 106.65],
     },
     {
          id: 4,
          ma: "VT-004",
          ten: "Sầu Riêng Ri6",
          chu: "Lê Văn C",
          trangThai: "active",
          toaDo: [10.78, 106.64],
     },
];

// Mock data điểm phát sinh sâu bệnh (nhiệt độ)
export const mockDiemNongSauBenh = [
     [10.77, 106.67], // Tập trung ở vùng 2
     [10.771, 106.671], // Gần vùng 2
     [10.769, 106.669], // Gần vùng 2
     [10.75, 106.65], // Vùng 3 lẻ tẻ
];
