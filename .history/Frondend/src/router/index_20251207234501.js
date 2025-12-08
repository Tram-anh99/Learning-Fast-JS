import { createRouter, createWebHistory } from "vue-router";
// Import 2 trang chính của chúng ta
import HomeView from "../views/HomeView.vue"; // Trang này để Bản đồ
import QuanLyView from "../views/QuanLyView.vue"; // Trang này để Quản lý

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
               path: "/quan-ly",
               name: "quan-ly",
               component: QuanLyView,
          },
     ],
});

export default router;
