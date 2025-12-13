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

// Tile layers - lưu các layer khác nhau
export const tileLayers = shallowRef({
     satellite: null,
     street: null,
});
// Lớp hiện tại đang hiển thị
export const currentLayer = ref("satellite");

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
 * Xóa các polygon cũ và thêm polygon mới cho từng vùng trồng
 */
export const veLaiBanDo = () => {
     if (!map.value || !layerGroup.value) return;
     // Xóa tất cả các layer cũ
     layerGroup.value.clearLayers();

     // Lặp qua từng vùng trong danh sách tìm kiếm
     danhSachTimKiem.value.forEach((vung) => {
          if (vung.toaDo) {
               // Lấy màu theo trạng thái
               const mauSac = getMapColor(vung.trangThai);
               // Tạo polygon
               const poly = L.polygon(vung.toaDo, {
                    color: mauSac, // Màu viền
                    fillColor: mauSac, // Màu fill
                    fillOpacity: 0.6, // Độ trong suốt
                    weight: 2, // Độ dày viền
               }).addTo(layerGroup.value);

               // Click vào polygon để xem chi tiết
               poly.on("click", () => chonVung(vung));
          }
     });
};

/**
 * Mở Modal QR code
 * Tạo link truy xuất từ mã sản phẩm
 */
export const openQRModal = (maSanPham) => {
     // Tạo URL cho QR code
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
 * - Tạo instance Leaflet map
 * - Set toạ độ mặc định (Mekong Delta)
 * - Thêm tile layer ảnh vệ tinh
 * - Thêm tile layer ranh giới hành chính
 * - Tạo layer group để chứa các polygon vùng trồng
 * - Vẽ bản đồ với danh sách hiện tại
 */
export const initMap = () => {
     // Kiểm tra container có được ref không
     if (!mapContainer.value) return;

     // Tạo instance map với toạ độ center [10.762, 106.66] (Mekong Delta)
     // Zoom level 13
     // zoomControl: false để tự custom vị trí control
     map.value = L.map(mapContainer.value, { zoomControl: false }).setView(
          [10.762, 106.66],
          13
     );

     // Thêm zoom control ở góc dưới bên phải
     L.control.zoom({ position: "bottomright" }).addTo(map.value);

     // Thêm Tile layer ảnh vệ tinh từ ArcGIS
     L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          {
               maxZoom: 19, // Zoom tối đa
          }
     ).addTo(map.value);

     // Thêm Tile layer ranh giới hành chính từ ArcGIS
     // Dùng để hiển thị đường biên giữa các vùng
     L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
     ).addTo(map.value);

     // Tạo layer group để chứa các polygon vùng trồng
     // Làm riêng để dễ clear khi lọc dữ liệu
     layerGroup.value = L.layerGroup().addTo(map.value);

     // Vẽ các polygon lên bản đồ
     veLaiBanDo();
};
