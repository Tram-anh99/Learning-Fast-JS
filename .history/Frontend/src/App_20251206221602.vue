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
  
  /* HIỆU ỨNG KÍNH XANH ĐẬM (Dark Green Glass) */
  background: rgba(5, 150, 105, 0.25); /* Màu xanh trong suốt 25% */
  backdrop-filter: blur(16px);          /* Làm mờ hậu cảnh */
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3); /* Viền sáng nhẹ */
  box-shadow: var(--shadow-glass);
  
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  position: fixed; top: 0; width: 100%; z-index: 2000;
  box-sizing: border-box;
}

.logo {
  font-size: 1.6rem;
  font-weight: 800;
  color: #064e3b; /* Chữ xanh đậm hẳn để dễ đọc trên nền kính */
  text-shadow: 0 1px 0 rgba(255,255,255,0.4); /* Bóng chữ nhẹ */
  letter-spacing: -0.5px;
}

.nav-link {
  color: #065f46; /* Xanh đậm */
  text-decoration: none;
  margin: 0 15px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.nav-link:hover, .nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.4); /* Nền trắng mờ khi hover */
  color: #047857;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.user-info {
  background: rgba(255, 255, 255, 0.5);
  padding: 8px 16px;
  border-radius: 20px;
  color: #064e3b;
  font-weight: 600;
  border: 1px solid rgba(255,255,255,0.6);
}

.content-area {
  margin-top: 70px;
  height: calc(100vh - 70px);
}
</style>