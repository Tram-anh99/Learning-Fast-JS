<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="app-layout">
  <header class="top-navbar">
    <div class="brand">
      <i class="fas fa-seedling logo-icon"></i>
      <div class="brand-text">
        <span class="brand-title">Hệ thống Quản lý Vùng trồng</span>
        <span class="brand-subtitle">Luận văn Thạc sĩ CNTT</span>
      </div>
    </div>

    <nav class="nav-links">
      <router-link to="/" class="nav-item active">
        <i class="fas fa-globe-asia"></i> Bản đồ WebGIS
      </router-link>
      <router-link to="/quan-ly" class="nav-item">
        <i class="fas fa-clipboard-list"></i> Nhật ký Canh tác
      </router-link>
      <a href="#" class="nav-item">
        <i class="fas fa-chart-pie"></i> Thống kê
      </a>
    </nav>

    <div class="user-profile">
      <span class="role-badge">Nhà nông</span>
      <span class="user-avatar">N</span>
    </div>
  </header>

  <main class="content-area">
    <RouterView />
  </main>
</template>

<style scoped>
/* Import Font Awesome trong index.html để hiện icon nhé */

.top-navbar {
  height: 60px;
  /* Màu xanh nông nghiệp đậm đà, nghiêm túc */
  background: linear-gradient(to right, #1b4332, #2d6a4f);
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1100;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 1.8rem;
  color: #74c69d;
}

/* Màu mầm cây sáng */

.brand-text {
  display: flex;
  flex-direction: column;
}

.brand-title {
  font-weight: 700;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.brand-subtitle {
  font-size: 0.75rem;
  color: #a8dba8;
  font-weight: 300;
}

.nav-links {
  display: flex;
  gap: 5px;
}

.nav-item {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 6px;
  transition: all 0.2s;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item:hover,
.nav-item.active {
  background-color: rgba(255, 255, 255, 0.15);
  color: #fff;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.role-badge {
  font-size: 0.8rem;
  background: rgba(0, 0, 0, 0.2);
  padding: 2px 8px;
  border-radius: 4px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background-color: #d8f3dc;
  color: #1b4332;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.content-area {
  flex-grow: 1;
  position: relative;
  overflow: hidden;
}
</style>a