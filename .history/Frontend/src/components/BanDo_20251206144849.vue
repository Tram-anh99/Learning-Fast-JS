<script setup>
import { onMounted } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// 1. KHAI BÁO NHẬN DỮ LIỆU (PROPS)
// "Tôi là bản đồ, tôi chờ cha gửi xuống một cục tên là 'duLieuDauVao'"
const props = defineProps(['duLieuDauVao']);

onMounted(() => {
  const map = L.map('map-container').setView([10.762, 106.660], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // 2. DUYỆT QUA DỮ LIỆU ĐƯỢC GỬI XUỐNG ĐỂ VẼ
  // props.duLieuDauVao chính là danh sách từ App.vue gửi sang
  if (props.duLieuDauVao) {
    
    // Dùng vòng lặp (giống Python) để vẽ tất cả các vùng
    props.duLieuDauVao.forEach(vung => {
      
      // Chỉ vẽ nếu có tọa độ (mảng không rỗng)
      if (vung.toaDo && vung.toaDo.length > 0) {
        
        const polygon = L.polygon(vung.toaDo, {
          color: 'red',
          fillColor: '#f03',
          fillOpacity: 0.5
        }).addTo(map);

        // Bind popup lấy thông tin từ dữ liệu thật
        polygon.bindPopup(`<b>${vung.ten}</b><br>Mã: ${vung.maSo}`);
      }
      
    });
  }
});
</script>