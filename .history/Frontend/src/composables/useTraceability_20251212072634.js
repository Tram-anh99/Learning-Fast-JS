import { ref, computed } from 'vue';

// Composable quản lý logic trang truy xuất
export function useTraceability() {
  // Biến điều khiển bật/tắt modal QR
  const showQR = ref(false);

  // Tính toán giá trị QR code dựa trên URL hiện tại
  const qrValue = computed(() => {
    // Lấy đường dẫn hiện tại của trình duyệt
    return window.location.href;
    
    // Hoặc có thể customize theo route params:
    // return `https://your-domain.com/truy-xuat/${route.params.id}`;
  });

  // Hàm mở modal QR
  const openQR = () => {
    showQR.value = true;
  };

  // Hàm đóng modal QR
  const closeQR = () => {
    showQR.value = false;
  };

  // Trả về các state và function
  return {
    showQR,
    qrValue,
    openQR,
    closeQR
  };
}
