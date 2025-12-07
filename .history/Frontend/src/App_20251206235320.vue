<script setup>
import { RouterView } from 'vue-router';
// Nếu bạn có file logo, hãy bỏ comment dòng dưới và đặt file logo.svg vào src/assets/
// import logo from '@/assets/logo.svg';
</script>

<template>
  <header class="top-navbar">
    <div class="brand">
      <i class="fas fa-leaf logo-icon"></i>
      <span class="brand-name">VN-AgriTrace</span>
    </div>
    <nav class="nav-links">
      <router-link to="/" class="nav-item active">WebGIS</router-link>
      <a href="#" class="nav-item">Maprs</a>
      <a href="#" class="nav-item">Panjests</a>
      <a href="#" class="nav-item">Logoin</a>
    </nav>
    <div class="user-profile">
      <span class="user-avatar">RM</span>
    </div>
  </header>

  <main class="content-area">
    <RouterView />
  </main>
</template>

<style scoped>
.top-navbar {
  height: 56px;
  /* Chiều cao chuẩn Material Design */
  background-color: var(--primary-color);
  color: var(--light-text-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: var(--shadow-sm);
  z-index: 1100;
  /* Đảm bảo nằm trên cùng */
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 1.5rem;
  color: var(--secondary-color);
}

.logo-img {
  height: 32px;
}

.brand-name {
  font-weight: 700;
  font-size: 1.25rem;
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  gap: 8px;
}

.nav-item {
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.nav-item:hover,
.nav-item.active {
  color: var(--light-text-color);
  background-color: rgba(255, 255, 255, 0.15);
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background-color: var(--secondary-color);
  color: var(--light-text-color);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 700;
  font-size: 0.9rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.content-area {
  flex-grow: 1;
  position: relative;
  /* Quan trọng để định vị các thành phần con tuyệt đối */
  overflow: hidden;
}
</style>