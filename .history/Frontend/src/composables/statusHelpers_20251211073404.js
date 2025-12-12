export function getStatusBadge(status) {
  const statusMap = {
    'active': { text: 'Đang hoạt động', class: 'badge-active' },
    'warning': { text: 'Cảnh báo', class: 'badge-warning' },
    'revoked': { text: 'Đã thu hồi', class: 'badge-danger' }
  };
  return statusMap[status] || { text: 'Không xác định', class: 'badge-danger' };
}

export const mockDataThongKe = {
  tongVung: 124,
  dienTich: '450 ha',
  sanLuongDuKien: '1.200 tấn',
  canhBao: 5
};

export const mockDataVung = [
  { id: 1, ma: 'VT-001', ten: 'HTX Xoài Mỹ Xương', chu: 'Nguyễn Văn A', trangThai: 'active', toaDo: [10.762, 106.660] },
  { id: 2, ma: 'VT-002', ten: 'Thanh Long VietGAP', chu: 'Trần Thị B', trangThai: 'warning', toaDo: [10.770, 106.670] },
  { id: 3, ma: 'VT-003', ten: 'Lúa Chất lượng cao', chu: 'HTX Lúa Vàng', trangThai: 'revoked', toaDo: [10.750, 106.650] },
  { id: 4, ma: 'VT-004', ten: 'Sầu Riêng Ri6', chu: 'Lê Văn C', trangThai: 'active', toaDo: [10.780, 106.640] }
];

export const mockDiemNongSauBenh = [
  [10.770, 106.670],
  [10.771, 106.671],
  [10.769, 106.669],
  [10.750, 106.650]
];
