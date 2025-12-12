/**
 * ========== COMPOSABLE: useHome.js ==========
 * Purpose: Logic cho trang Home (Tra cứu Nông sản)
 * Features: Quản lý dữ liệu vùng trồng, bộ lọc, QR modal
 * Related Files:
 *   - src/views/HomeView.vue (Main view)
 *   - src/components/HomeListItem.vue (Item trong danh sách)
 *   - src/components/HomeDetailView.vue (Chi tiết vùng)
 *   - src/components/HomeQRModal.vue (Modal QR code)
 *   - src/assets/styles/tailwind.css (Global styles)
 */

import { ref, computed, onMounted, shallowRef } from "vue";
import L from "leaflet";

// ========== STATE & REFS ==========
export const danhSachGoc = ref([
     {
          id: 1,
          ma: "VT-001",
          ten: "Xoài Cát Hòa Lộc",
          dienTich: "5ha",
          trangThai: "canh_tac",
          chungNhan: "VietGAP",
          anh: "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=1000&auto=format&fit=crop",
          toaDo: [
               [10.762, 106.66],
               [10.77, 106.67],
               [10.76, 106.67],
          ],
          nhatKy: [
               {
                    ngay: "10/12/2024",
                    hoatDong: "Bón phân hữu cơ",
                    chiTiet: "Bón lót 50kg phân vi sinh",
               },
               {
                    ngay: "01/12/2024",
                    hoatDong: "Tỉa cành",
                    chiTiet: "Tỉa cành tạo tán sau thu hoạch vụ trước",
               },
          ],
     },
     {
          id: 2,
          ma: "VT-002",
          ten: "Thanh Long Ruột Đỏ",
          dienTich: "3.2ha",
          trangThai: "canh_tac",
          chungNhan: "GlobalGAP",
          anh: "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?q=80&w=1000&auto=format&fit=crop",
          toaDo: [
               [10.78, 106.68],
               [10.79, 106.69],
               [10.78, 106.69],
          ],
          nhatKy: [
               {
                    ngay: "05/12/2024",
                    hoatDong: "Cảnh báo",
                    chiTiet: "Phát hiện nấm tắc kè, đã phun thuốc sinh học",
               },
          ],
     },
     {
          id: 3,
          ma: "VT-003",
          ten: "Lúa ST25",
          dienTich: "10ha",
          trangThai: "thu_hoach",
          chungNhan: "OCOP 4 Sao",
          anh: "https://images.unsplash.com/photo-1536617621572-1d5f1e6269a0?q=80&w=1000&auto=format&fit=crop",
          toaDo: [
               [10.75, 106.64],
               [10.758, 106.66],
               [10.742, 106.66],
          ],
          nhatKy: [
               {
                    ngay: "07/12/2024",
                    hoatDong: "Thu hoạch",
                    chiTiet: "Bắt đầu gặt đợt 1, năng suất tốt",
               },
               {
                    ngay: "20/09/2024",
                    hoatDong: "Gieo sạ",
                    chiTiet: "Sạ giống xác nhận cấp 1",
               },
          ],
     },
     {
          id: 4,
          ma: "VT-004",
          ten: "Cà phê Robusta",
          dienTich: "7.5ha",
          trangThai: "da_thu_hoach",
          chungNhan: "4C Certified",
          anh: "https://images.unsplash.com/photo-1559056199-641a0ac8b3f2?q=80&w=1000&auto=format&fit=crop",
          toaDo: [
               [10.7, 106.65],
               [10.71, 106.66],
               [10.7, 106.66],
          ],
          nhatKy: [
               {
                    ngay: "03/12/2024",
                    hoatDong: "Sơ chế",
                    chiTiet: "Hoàn thành sơ chế, chuẩn bị xuất khẩu",
               },
               {
                    ngay: "28/11/2024",
                    hoatDong: "Thu hoạch hoàn tất",
                    chiTiet: "Kết thúc mùa thu hoạch, năng suất 1.2 tấn/ha",
               },
          ],
     },
]);

export const boLocHienTai = ref("all");
export const vungDangXem = ref(null);
export const searchQuery = ref("");
export const showQR = ref(false);
export const qrLink = ref("");

export const map = shallowRef(null);
export const mapContainer = ref(null);
export const layerGroup = shallowRef(null);
export const selectedLayer = ref("satellite"); // Lớp bản đồ được chọn
export const tileLayers = shallowRef({}); // Lưu các tile layers

// ========== COMPUTED PROPERTIES ==========

/**
 * Lọc danh sách theo trạng thái
 */
export const danhSachHienThi = computed(() => {
     if (boLocHienTai.value === "all") return danhSachGoc.value;
     return danhSachGoc.value.filter((v) => v.trangThai === boLocHienTai.value);
});

/**
 * Lọc danh sách theo từ khóa tìm kiếm
 */
export const danhSachTimKiem = computed(() => {
     if (!searchQuery.value) return danhSachHienThi.value;

     const keyword = searchQuery.value.toLowerCase();
     return danhSachHienThi.value.filter(
          (item) =>
               item.ten.toLowerCase().includes(keyword) ||
               item.ma.toLowerCase().includes(keyword)
     );
});

// ========== HELPER FUNCTIONS ==========

/**
 * Lấy class CSS theo trạng thái
 */
export const getClassTrangThai = (tt) => {
     const classes = {
          canh_tac: "bg-green-500",
          sau_benh: "bg-red-500",
          thu_hoach: "bg-yellow-500",
          da_thu_hoach: "bg-blue-600",
     };
     return classes[tt] || "bg-gray-500";
};

/**
 * Lấy màu bản đồ theo trạng thái
 */
export const getMapColor = (tt) => {
     const colors = {
          canh_tac: "#4caf50",
          sau_benh: "#ef5350",
          thu_hoach: "#ffca28",
          da_thu_hoach: "#2563eb",
     };
     return colors[tt] || "#999";
};

/**
 * Lấy text hiển thị từ trạng thái
 */
export const getTextTrangThai = (tt) => {
     const texts = {
          canh_tac: "Đang canh tác",
          sau_benh: "Cảnh báo dịch hại",
          thu_hoach: "Đang thu hoạch",
          da_thu_hoach: "Đã thu hoạch",
     };
     return texts[tt] || "Không xác định";
};

// ========== INTERACTIVE FUNCTIONS ==========

/**
 * Chọn vùng để xem chi tiết
 */
export const chonVung = (vung) => {
     if (map.value && vung.toaDo) {
          const polygon = L.polygon(vung.toaDo);
          map.value.flyTo(polygon.getBounds().getCenter(), 16, {
               duration: 1.2,
          });
     }
     vungDangXem.value = vung;
};

/**
 * Quay lại danh sách
 */
export const quayLaiDanhSach = () => {
     vungDangXem.value = null;
     if (map.value) {
          map.value.flyTo([10.762, 106.66], 13, { duration: 1 });
     }
};

/**
 * Vẽ lại bản đồ
 */
export const veLaiBanDo = () => {
     if (!map.value || !layerGroup.value) return;
     layerGroup.value.clearLayers();

     danhSachTimKiem.value.forEach((vung) => {
          if (vung.toaDo) {
               const mauSac = getMapColor(vung.trangThai);
               const poly = L.polygon(vung.toaDo, {
                    color: mauSac,
                    fillColor: mauSac,
                    fillOpacity: 0.6,
                    weight: 2,
               }).addTo(layerGroup.value);

               poly.on("click", () => chonVung(vung));
          }
     });
};

/**
 * Mở Modal QR code
 */
export const openQRModal = (maSanPham) => {
     qrLink.value = `${window.location.origin}/truy-xuat/${maSanPham}`;
     showQR.value = true;
};

/**
 * Đóng Modal QR code
 */
export const closeQRModal = () => {
     showQR.value = false;
     qrLink.value = "";
};

// ========== MAP INITIALIZATION ==========

/**
 * Khởi tạo bản đồ Leaflet
 */
export const initMap = () => {
     if (!mapContainer.value) return;

     map.value = L.map(mapContainer.value, { zoomControl: false }).setView(
          [10.762, 106.66],
          13
     );

     L.control.zoom({ position: "bottomright" }).addTo(map.value);

     // Tile layer: Ảnh vệ tinh
     L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          {
               maxZoom: 19,
          }
     ).addTo(map.value);

     // Tile layer: Ranh giới hành chính
     L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
     ).addTo(map.value);

     layerGroup.value = L.layerGroup().addTo(map.value);
     veLaiBanDo();
};
