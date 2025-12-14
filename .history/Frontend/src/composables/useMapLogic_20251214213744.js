/**
 * ========== COMPOSABLE: useMapLogic.js ==========
 * Purpose: Quản lý logic bản đồ Leaflet - hỗ trợ cả Home view & Dashboard
 *
 * Features:
 *   - Khởi tạo bản đồ với 2 mode: 'home' (ArcGIS tiles) & 'dashboard' (CartoDB)
 *   - Vẽ polygon vùng trồng & circle markers
 *   - Quản lý layer sâu bệnh, hành chính
 *   - Zoom control & tile layer switching
 *
 * Related Files:
 *   - src/composables/useHome.js (sử dụng mode 'home')
 *   - src/components/MapComponent.vue (sử dụng mode 'dashboard')
 */

import { ref, shallowRef } from "vue";
import L from "leaflet";

/**
 * ========== COMPOSABLE FUNCTION ==========
 * Trả về tất cả state & methods để quản lý bản đồ
 */
export function useMapLogic() {
     // ========== STATE & REFS ==========

     // Instance bản đồ Leaflet (shallowRef để không track deep changes)
     const map = shallowRef(null);

     // Ref đến DOM element #map-container - nơi Leaflet mount
     const mapContainer = ref(null);

     // Layer group chứa các circle markers cho điểm sâu bệnh
     const lopSauBenh = shallowRef(L.layerGroup());

     // Layer group chứa các polygon vùng trồng (cho mode home)
     const layerGroup = shallowRef(null);

     // Trạng thái chế độ xem hiện tại: 'hanh_chinh' | 'sau_benh'
     const cheDoXem = ref("hanh_chinh");

     // Lưu tile layers khác nhau { satellite, street }
     const tileLayers = shallowRef({
          satellite: null,
          street: null,
     });

     // Layer hiện tại đang hiển thị
     const currentLayer = ref("satellite");

     // ========== HELPER: Lấy màu theo trạng thái vùng ==========
     /**
      * Map từ trạng thái vùng → màu hex để vẽ polygon
      * Dùng chung cho cả 2 mode (home & dashboard)
      * @param {string} trangThai - canh_tac | sau_benh | thu_hoach | da_thu_hoach
      * @returns {string} hex color (vd: "#4caf50")
      */
     const getMapColor = (trangThai) => {
          const colors = {
               canh_tac: "#4caf50", // Xanh lá
               sau_benh: "#ef5350", // Đỏ
               thu_hoach: "#ffca28", // Vàng
               da_thu_hoach: "#2563eb", // Xanh dương
          };
          return colors[trangThai] || "#999";
     };

     // ========== MAIN: Khởi tạo bản đồ ==========
     /**
      * Khởi tạo Leaflet map instance
      * Hỗ trợ 2 mode: 'home' (sidebar map) & 'dashboard' (full map)
      *
      * Mode 'home':
      *   - Tiles: ArcGIS Satellite + Street + Boundaries
      *   - Phục vụ HomeView.vue
      *
      * Mode 'dashboard':
      *   - Tiles: CartoDB Positron (single tile)
      *   - Phục vụ MapComponent.vue trong QuanLyView
      *
      * @param {string} mode - 'home' | 'dashboard' (mặc định: 'dashboard')
      * @param {Array} coordinates - [lat, lng] (mặc định: [10.765, 106.66])
      * @param {number} zoom - zoom level (mặc định: 13)
      */
     const initMap = (
          mode = "dashboard",
          coordinates = [10.765, 106.66],
          zoom = 13
     ) => {
          // Kiểm tra container DOM tồn tại
          if (!mapContainer.value) return;

          // Tạo instance map Leaflet
          map.value = L.map(mapContainer.value, { zoomControl: false }).setView(
               coordinates,
               zoom
          );

          // Thêm zoom control ở góc dưới phải
          L.control.zoom({ position: "bottomright" }).addTo(map.value);

          if (mode === "home") {
               // ========== MODE HOME: ArcGIS Tiles ==========

               // Tile 1: Satellite (ảnh vệ tinh)
               tileLayers.value.satellite = L.tileLayer(
                    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                    {
                         maxZoom: 19,
                         attribution: "Tiles &copy; Esri",
                    }
               );

               // Tile 2: Street (bản đồ đường phố)
               tileLayers.value.street = L.tileLayer(
                    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                    {
                         maxZoom: 19,
                         attribution: "© OpenStreetMap contributors",
                    }
               );

               // Thêm Satellite layer mặc định vào map
               tileLayers.value.satellite.addTo(map.value);

               // Tile 3: Ranh giới hành chính (overlay)
               L.tileLayer(
                    "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
               ).addTo(map.value);

               // Tạo layer group để chứa polygon vùng trồng (dễ xóa/update)
               layerGroup.value = L.layerGroup().addTo(map.value);
          } else {
               // ========== MODE DASHBOARD: CartoDB Positron ==========

               // Tile: CartoDB Positron (light, minimal)
               L.tileLayer(
                    "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                    {
                         attribution: "© CartoDB",
                    }
               ).addTo(map.value);
          }

          // Thêm layer sâu bệnh vào map (có thể ẩn ban đầu)
          lopSauBenh.value.addTo(map.value);
     };

     // ========== LAYER MANAGEMENT: Vẽ vùng trồng ==========
     /**
      * Vẽ polygon cho từng vùng trồng
      * Dùng cho mode 'home' (sidebar map) - vẽ từng polygon cho mỗi vùng
      * @param {Array} danhSachVung - danh sách vùng { id, ten, trangThai, toaDo }
      */
     const veLaiBanDo = (danhSachVung) => {
          if (!map.value || !layerGroup.value) return;

          // Xóa tất cả layer cũ
          layerGroup.value.clearLayers();

          // Lặp qua từng vùng & vẽ polygon
          danhSachVung.forEach((vung) => {
               if (vung.toaDo) {
                    // Lấy màu theo trạng thái
                    const mauSac = getMapColor(vung.trangThai);

                    // Vẽ polygon với tọa độ vùng
                    const poly = L.polygon(vung.toaDo, {
                         color: mauSac, // Màu viền
                         fillColor: mauSac, // Màu nền
                         fillOpacity: 0.6, // Độ trong suốt
                         weight: 2, // Độ dày viền
                    }).addTo(layerGroup.value);

                    // Thêm popup khi click
                    poly.bindPopup(`<b>${vung.ten}</b><br>Chủ hộ: ${vung.chu}`);
               }
          });
     };

     /**
      * Vẽ circle markers cho từng vùng (dashboard view)
      * Dùng cho mode 'dashboard' (MapComponent) - vẽ circle markers thay vì polygon
      * @param {Array} danhSachVung - danh sách vùng với toaDo (center point)
      */
     const vẽMarkerVùng = (danhSachVung) => {
          if (!map.value) return;

          danhSachVung.forEach((vung) => {
               // Chọn màu dựa trên trạng thái
               const color = getMapColor(vung.trangThai);

               // Nếu toaDo là array 4 góc (polygon), vẽ polygon thay vì circle
               if (vung.toaDo && Array.isArray(vung.toaDo) && vung.toaDo.length === 4) {
                    // Vẽ polygon với 4 góc
                    L.polygon(vung.toaDo, {
                         color: color, // Màu viền
                         fillColor: color, // Màu nền
                         fillOpacity: 0.6, // Độ trong suốt
                         weight: 2, // Độ dày viền
                    })
                         .bindPopup(`<b>${vung.ten}</b><br>Chủ hộ: ${vung.chu}<br>Mã: ${vung.ma}`)
                         .addTo(map.value);
               } else if (vung.toaDo && vung.toaDo.length === 2) {
                    // Nếu chỉ có 1 point (tâm), vẽ circle marker
                    L.circleMarker(vung.toaDo, {
                         radius: 8,
                         fillColor: color,
                         color: "#fff",
                         weight: 2,
                         fillOpacity: 1,
                    })
                         .bindPopup(`<b>${vung.ten}</b><br>Chủ hộ: ${vung.chu}<br>Mã: ${vung.ma}`)
                         .addTo(map.value);
               }
          });
     };

     // ========== VIEW MODE: Quản lý layer hiển thị ==========
     /**
      * Bật chế độ xem "sâu bệnh"
      * Hiển thị circle markers cho các điểm dịch bệnh
      * @param {Array} diemNongSauBenh - danh sách điểm bệnh [lat, lng]
      */
     const batCheDoSauBenh = (diemNongSauBenh) => {
          cheDoXem.value = "sau_benh";
          // Xóa layer cũ trước đó
          lopSauBenh.value.clearLayers();

          // Vẽ circle (heatmap) cho mỗi điểm dịch bệnh
          diemNongSauBenh.forEach((coord) => {
               L.circle(coord, {
                    color: "red",
                    fillColor: "#f03",
                    fillOpacity: 0.4,
                    radius: 300, // 300m radius
               }).addTo(lopSauBenh.value);
          });
     };

     /**
      * Bật chế độ xem "hành chính"
      * Ẩn layer sâu bệnh, chỉ hiển thị polygon/marker vùng trồng
      */
     const batCheDoHanhChinh = () => {
          cheDoXem.value = "hanh_chinh";
          // Xóa các circle bệnh
          lopSauBenh.value.clearLayers();
     };

     /**
      * Thay đổi tile layer (cho mode home)
      * Chuyển đổi giữa Satellite & Street view
      * @param {string} layer - 'satellite' | 'street'
      */
     const changeTileLayer = (layer) => {
          if (!map.value || !tileLayers.value[layer]) return;

          // Xóa layer hiện tại khỏi map
          map.value.removeLayer(tileLayers.value[currentLayer.value]);

          // Thêm layer mới
          tileLayers.value[layer].addTo(map.value);

          // Update trạng thái
          currentLayer.value = layer;
     };

     // ========== RETURN EXPORTS ==========
     return {
          // State
          map,
          mapContainer,
          lopSauBenh,
          layerGroup,
          cheDoXem,
          tileLayers,
          currentLayer,

          // Methods
          initMap,
          veLaiBanDo,
          vẽMarkerVùng,
          batCheDoSauBenh,
          batCheDoHanhChinh,
          changeTileLayer,
          getMapColor,
     };
}
