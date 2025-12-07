<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="app-container">
    <header class="navbar">
      <div class="logo">🌱 VN-AgriTrace</div>
      <nav>
        <RouterLink to="/" class="nav-link">🌏 Bản đồ Vùng trồng</RouterLink>
        <RouterLink to="/quan-ly" class="nav-link">🚜 Quản lý Canh tác</RouterLink>
      </nav>
      <div class="user-info">
        👤 Xin chào, Nhà nông
      </div>
    </header>

    <div class="content-area">
      <RouterView />
    </div>
  </div>
</template>

<style>
.navbar {
  height: 70px;
  /* Cao hơn chút cho thoáng */

  /* HIỆU ỨNG KÍNH MỜ (Glassmorphism) */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);

  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 2000;
  box-sizing: border-box;
}

/* IMPORT FONT CHỮ HIỆN ĐẠI (Inter) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* BẢNG MÀU CHUẨN (Emerald Palette) */
  --primary-color: #059669;
  /* Xanh lá đậm chủ đạo */
  --primary-hover: #047857;
  /* Xanh khi di chuột */
  --accent-color: #10b981;
  /* Xanh sáng điểm nhấn */
  --bg-color: #f0fdf4;
  /* Nền xanh siêu nhạt */
  --text-main: #1e293b;
  /* Chữ màu xám đen (dễ đọc hơn đen tuyền) */
  --text-light: #64748b;
  /* Chữ phụ */
  --white: #ffffff;
  --danger: #ef4444;
  --warning: #f59e0b;

  /* HIỆU ỨNG GÓC BO & BÓNG ĐỔ (Shadow) */
  --radius: 16px;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  /* Font chữ sạch, hiện đại */
  background-color: var(--bg-color);
  color: var(--text-main);
  -webkit-font-smoothing: antialiased;
  /* Làm mượt chữ trên Mac */
}

#app {
  width: 100%;
  height: 100%;
  display: block;
  max-width: none;
  margin: 0;
  padding: 0;
}

/* Scrollbar đẹp hơn */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.nav-link {
  color: var(--text-light);
  text-decoration: none;
  margin: 0 20px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  padding: 8px 12px;
  border-radius: 8px;
}

.nav-link:hover {
  color: var(--primary-color);
  background: rgba(16, 185, 129, 0.1);
  /* Nền xanh nhạt khi di chuột */
}

.nav-link.router-link-active {
  color: var(--primary-color);
  background: rgba(16, 185, 129, 0.15);
}

.user-info {
  font-weight: 600;
  color: var(--text-main);
  background: white;
  padding: 8px 16px;
  border-radius: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid #e2e8f0;
}

.content-area {
  margin-top: 70px;
  height: calc(100vh - 70px);
}
</style>