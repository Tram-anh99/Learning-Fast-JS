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

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  /* Chữ màu Gradient */
  letter-spacing: -0.5px;
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