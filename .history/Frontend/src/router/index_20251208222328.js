import { createRouter, createWebHistory } from "vue-router";
// Import 2 trang chính của chúng ta
import HomeView from "../views/HomeView.vue"; // Trang này để Bản đồ
import QuanLyView from "../views/QuanLyView.vue"; // Trang này để Quản lý
import DiaryPage from "@/views/DiaryPage.vue"; // Trang Nhật ký canh tác
import TraceabilityPage from "../views/TraceabilityPage.vue"; // Trang truy xuất nguồn gốc
const router = createRouter({
     history: createWebHistory(import.meta.env.BASE_URL),
     routes: [
          {
               path: "/",
               name: "home",
               component: HomeView,
          },
          {
               path: "/quan-ly",
               name: "quan-ly",
               component: QuanLyView,
          },
          {
               path: "/nhat-ky-canh-tac",
               name: "nhat-ky-canh-tac",
               component: DiaryPage,
          },
          // Route động cho khách quét QR
          // :id là mã số của lô trồng/sản phẩm
          {
               path: "/truy-xuat/:id",
               name: "Traceability",
               component: TraceabilityPage,
          },
     ],
});

export default router;
