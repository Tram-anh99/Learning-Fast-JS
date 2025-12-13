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
import L from "leaflet"; // Leaflet - thư viện bản đồ interactiveMap

// ========== STATE & REFS ==========
// Mảng dữ liệu gốc chứa tất cả vùng trồng
export const danhSachGoc = ref([
     {
          id: 1, // ID duy nhất
          ma: "VT-001", // Mã vùng trồng
          ten: "Xoài Cát Hòa Lộc", // Tên sản phẩm
          dienTich: "5ha", // Diện tích vùng
          trangThai: "canh_tac", // Trạng thái (canh_tac, thu_hoach, da_thu_hoach)
          chungNhan: "VietGAP", // Chứng nhận (VietGAP, GlobalGAP, etc)
          anh: "https://images.unsplash.com/photo-1553279768-865429fa0078?q=80&w=1000&auto=format&fit=crop", // URL ảnh
          toaDo: [ // Tọa độ polygon của vùng trồng
               [10.762, 106.66],
               [10.77, 106.67],
               [10.76, 106.67],
          ],
          nhatKy: [ // Nhật ký hoạt động canh tác
               {
                    ngay: "10/12/2024", // Ngày hoạt động
                    hoatDong: "Bón phân hữu cơ", // Tên hoạt động
                    chiTiet: "Bón lót 50kg phân vi sinh", // Chi tiết hoạt động
               },
               {
                    ngay: "01/12/2024",
                    hoatDong: "Tỉa cành",
                    chiTiet: "Tỉa cành tạo tán sau thu hoạch vụ trước",
               },
          ],
     },
     // ... các vùng trồng khác
]);

// Trạng thái bộ lọc hiện tại (all, canh_tac, thu_hoach, da_thu_hoach)
export const boLocHienTai = ref("all");
// Vùng trồng đang xem chi tiết (null khi hiển thị danh sách)
export const vungDangXem = ref(null);
// Keyword tìm kiếm
export const searchQuery = ref("");
// Hiển thị QR modal hay không
export const showQR = ref(false);
// Giá trị QR link để chia sẻ
export const qrLink = ref("");

// Instance bản đồ Leaflet
export const map = shallowRef(null);
// Ref container HTML chứa bản đồ
export const mapContainer = ref(null);
// Layer group chứa các polygon vùng trồng
export const layerGroup = shallowRef(null);

// ========== COMPUTED PROPERTIES ==========

/**
 * Lọc danh sách theo trạng thái
 * Nếu boLocHienTai = 'all' thì return toàn bộ danh sách
 * Ngược lại filter chỉ lấy những vùng có trạng thái trùng khớp
 */
export const danhSachHienThi = computed(() => {
     if (boLocHienTai.value === "all") return danhSachGoc.value;
     return danhSachGoc.value.filter((v) => v.trangThai === boLocHienTai.value);
});

/**
 * Lọc danh sách theo từ khóa tìm kiếm
 * Tìm kiếm trên tên vùng (ten) hoặc mã vùng (ma)
 * Không phân biệt hoa thường (toLowerCase)
 */
export const danhSachTimKiem = computed(() => {
     // Nếu không có từ khóa tìm kiếm thì return danh sách đã lọc theo trạng thái
     if (!searchQuery.value) return danhSachHienThi.value;

     const keyword = searchQuery.value.toLowerCase();
     // Filter danh sách theo từ khóa
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
