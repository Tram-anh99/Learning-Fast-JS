<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="app-layout">
    <header class="top-navbar">
      <div class="brand">
        <i class="fas fa-leaf logo-icon"></i>
        <div class="brand-text">
          <span class="brand-title">Hệ thống Quản lý Vùng trồng</span>
          <span class="brand-subtitle">Luận văn Thạc sĩ CNTT</span>
        </div>
      </div>

      <nav class="nav-links">
        <router-link to="/" class="nav-item">
          <i class="fas fa-globe-asia"></i> Bản đồ WebGIS
        </router-link>
        <router-link to="/nhat-ky-canh-tac" class="nav-item">
          <i class="fas fa-clipboard-list"></i> Nhật ký Canh tác
        </router-link>
        <router-link to="/quan-ly" class="nav-item">
          <i class="fas fa-chart-pie"></i> Quản lý Vùng trồng
        </router-link>

      </nav>

      <div class="user-profile">
        <span class="role-badge">Nhà nông</span>
        <span class="user-avatar">N</span>
      </div>
    </header>

    <main class="content-area">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* Import Font Awesome trong index.html để hiện icon nhé */
/* src/App.vue */

.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100%;
  /* Đổi 100vw thành 100% để tránh bị tràn ngang */
  overflow: hidden;
}

/* Header với màu mới */
.top-navbar {
  min-height: 60px;
  background: #24504b;
  color: #fbfced;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
  z-index: 2000;
  box-shadow: 0 2px 8px rgba(36, 80, 75, 0.2);
  gap: 20px;
  flex-wrap: wrap;
}

@media (max-width: 1024px) {
  .top-navbar {
    padding: 10px 16px;
    min-height: 50px;
  }
}

@media (max-width: 768px) {
  .top-navbar {
    padding: 8px 12px;
    gap: 8px;
    min-height: auto;
  }
}

/* QUAN TRỌNG: Khung chứa nội dung */
.content-area {
  flex-grow: 1;
  /* Chiếm hết phần còn lại */
  position: relative;
  /* Làm điểm tựa cho con bên trong */
  width: 100%;
  background-color: #fbfced;
  overflow-y: auto;
  /* Cho phép scroll dọc */
  overflow-x: hidden;
  /* Ngăn scroll ngang */
}

/* ... giữ nguyên các class khác ... */


.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.logo-icon {
  font-size: 1.8rem;
  color: #fbfced;
}

@media (max-width: 768px) {
  .logo-icon {
    font-size: 1.5rem;
  }
}

.brand-text {
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px) {
  .brand-text {
    display: none;
  }
}

.brand-title {
  font-weight: 700;
  font-size: 1.1rem;
  text-transform: uppercase;
}

.brand-subtitle {
  font-size: 0.75rem;
  opacity: 0.8;
}

.nav-links {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-direction: row;
}

@media (max-width: 1024px) {
  .nav-links {
    gap: 8px;
  }
}

@media (max-width: 768px) {
  .top-navbar {
    flex-wrap: wrap;
  }

  .brand {
    order: 1;
    flex: 1;
  }

  .user-profile {
    order: 2;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    gap: 6px;
    order: 3;
  }
}

.nav-item {
  color: #fbfced;
  text-decoration: none;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 10px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 2px solid transparent;
  background: rgba(251, 252, 237, 0.1);
  white-space: nowrap;
}

@media (max-width: 1024px) {
  .nav-item {
    padding: 8px 16px;
    font-size: 0.85rem;
  }
}

@media (max-width: 768px) {
  .nav-item {
    padding: 8px 12px;
    font-size: 0.85rem;
    gap: 8px;
    width: 100%;
    justify-content: flex-start;
  }
}

.nav-item i {
  flex-shrink: 0;
}

.nav-item:hover {
  background-color: rgba(251, 252, 237, 0.2);
  border-color: rgba(251, 252, 237, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.nav-item.active {
  background: #fbfced;
  color: #24504b;
  font-weight: 600;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  border-color: #fbfced;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .user-profile {
    gap: 6px;
  }
}

.role-badge {
  font-size: 0.8rem;
  background: rgba(251, 252, 237, 0.2);
  padding: 2px 8px;
  border-radius: 4px;
  color: #fbfced;
}

@media (max-width: 768px) {
  .role-badge {
    display: none;
  }
}

.user-avatar {
  width: 36px;
  height: 36px;
  background-color: #fbfced;
  color: #24504b;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  border: 2px solid rgba(251, 252, 237, 0.3);
}

@media (max-width: 768px) {
  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 0.9rem;
  }
}
</style>