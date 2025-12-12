import { ref, shallowRef } from "vue";
import L from "leaflet";

// Composable quản lý logic bản đồ Leaflet
export function useMapLogic() {
     // Instance bản đồ Leaflet (shallowRef để không track deep)
     const map = shallowRef(null);
     // Ref đến DOM element chứa bản đồ
     const mapContainer = ref(null);
     // Layer group chứa các điểm sâu bệnh
     const lopSauBenh = shallowRef(L.layerGroup());
     // Trạng thái chế độ xem hiện tại
     const cheDoXem = ref("hanh_chinh");

     // Khởi tạo bản đồ với tọa độ và mức zoom
     const initMap = (coordinates = [10.765, 106.66], zoom = 13) => {
          if (!mapContainer.value) return;

          // Tạo instance bản đồ trên element
          map.value = L.map(mapContainer.value, { zoomControl: false }).setView(
               coordinates,
               zoom
          );

          // Thêm control zoom ở góc dưới phải
          L.control.zoom({ position: "bottomright" }).addTo(map.value);

          // Thêm nền bản đồ CartoDB Positron (sáng, tối thiểu)
          L.tileLayer(
               "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
               {
                    attribution: "© CartoDB",
               }
          ).addTo(map.value);

          // Thêm layer sâu bệnh vào bản đồ
          lopSauBenh.value.addTo(map.value);
     };

     // Vẽ các marker (điểm) cho từng vùng trồng
     const vẽMarkerVùng = (danhSachVung) => {
          danhSachVung.forEach((vung) => {
               // Chọn màu dựa trên trạng thái vùng
               const color =
                    vung.trangThai === "active"
                         ? "#1b4332"
                         : vung.trangThai === "warning"
                         ? "#f59e0b"
                         : "#ef4444";

               // Tạo circle marker tại tọa độ vùng
               L.circleMarker(vung.toaDo, {
                    radius: 8,
                    fillColor: color,
                    color: "#fff",
                    weight: 2,
                    fillOpacity: 1,
               })
                    .bindPopup(`<b>${vung.ten}</b><br>Chủ hộ: ${vung.chu}`)
                    .addTo(map.value);
          });
     };

     // Bật chế độ xem sâu bệnh với nhiệt độ
     const batCheDoSauBenh = (diemNongSauBenh) => {
          cheDoXem.value = "sau_benh";
          // Xóa các layer cũ trước
          lopSauBenh.value.clearLayers();

          // Vẽ circle cho mỗi điểm sâu bệnh
          diemNongSauBenh.forEach((coord) => {
               L.circle(coord, {
                    color: "red",
                    fillColor: "#f03",
                    fillOpacity: 0.4,
                    radius: 300,
               }).addTo(lopSauBenh.value);
          });
     };

     // Bật chế độ xem hành chính (xóa layer sâu bệnh)
     const batCheDoHanhChinh = () => {
          cheDoXem.value = "hanh_chinh";
          lopSauBenh.value.clearLayers();
     };

     // Trả về các ref và function để dùng trong component
     return {
          map,
          mapContainer,
          lopSauBenh,
          cheDoXem,
          initMap,
          vẽMarkerVùng,
          batCheDoSauBenh,
          batCheDoHanhChinh,
     };
}
