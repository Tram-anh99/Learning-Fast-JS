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
  height: 60px; /* Gọn gàng hơn */
  
  /* NỀN XANH ĐẬM ĐẶC - KHÔNG KÍNH MỜ */
  background-color: var(--primary-dark);
  border-bottom: 1px solid #0f291e;
  
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  position: fixed; top: 0; width: 100%; z-index: 2000;
  box-sizing: border-box;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 1.3rem;
  font-weight: 700;
  color: #ffffff; /* Trắng tinh */
  text-transform: uppercase; /* Chữ in hoa cho mạnh mẽ */
  letter-spacing: 1px;
  display: flex; align-items: center; gap: 10px;
}

.nav-link {
  color: #d8f3dc; /* Màu xanh phấn nhạt */
  text-decoration: none;
  margin: 0 10px;
  font-weight: 500;
  font-size: 0.9rem;
  padding: 8px 16px;
  border-radius: 4px; /* Bo góc vuông vức 4px thôi */
  transition: all 0.2s;
}

.nav-link:hover {
  background-color: rgba(255,255,255,0.1);
  color: white;
}

.nav-link.router-link-active {
  background-color: var(--primary-main); /* Nền xanh sáng hơn chút */
  color: white;
  border-left: 3px solid #74c69d; /* Điểm nhấn bên trái */
}

.user-info {
  font-size: 0.9rem;
  color: #ecfdf5;
}

.content-area {
  margin-top: 60px;
  height: calc(100vh - 60px);
}
</style>