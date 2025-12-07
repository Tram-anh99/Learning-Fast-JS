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
/* CSS TOÀN CỤC */
body { margin: 0; padding: 0; font-family: 'Segoe UI', sans-serif; }

.navbar {
  height: 60px;
  background-color: #42b883; /* Màu xanh chủ đạo */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  color: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  position: fixed; /* Ghim lên đầu */
  top: 0; width: 100%; z-index: 2000;
  box-sizing: border-box;
}

.logo { font-size: 1.2rem; font-weight: bold; }

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  margin: 0 15px;
  font-weight: 500;
  transition: 0.2s;
}

.nav-link:hover, .nav-link.router-link-active {
  color: white;
  border-bottom: 2px solid white;
  padding-bottom: 5px;
}

.content-area {
  margin-top: 60px; /* Đẩy nội dung xuống để không bị Navbar che mất */
  height: calc(100vh - 60px); /* Chiều cao còn lại */
}
</style>