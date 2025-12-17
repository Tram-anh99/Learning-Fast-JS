<script setup>
import { RouterView, useRoute } from 'vue-router';
import { ref, computed } from 'vue';

const route = useRoute();
const showTooltip = ref(null);

// Compute active route
const isActive = (path) => {
  return route.path === path || (path !== '/' && route.path.startsWith(path));
};

const toggleTooltip = (name) => {
  showTooltip.value = showTooltip.value === name ? null : name;
};
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

    <!-- Mobile Bottom Navigation -->
    <nav class="mobile-bottom-nav">
      <router-link to="/" class="mobile-nav-item" :class="{ active: isActive('/') }">
        <i class="fas fa-globe-asia"></i>
        <span class="nav-label">Bản đồ</span>
      </router-link>
      
      <router-link to="/nhat-ky-canh-tac" class="mobile-nav-item" :class="{ active: isActive('/nhat-ky-canh-tac') }">
        <i class="fas fa-clipboard-list"></i>
        <span class="nav-label">Nhật ký</span>
      </router-link>
      
      <router-link to="/quan-ly" class="mobile-nav-item" :class="{ active: isActive('/quan-ly') }">
        <i class="fas fa-chart-pie"></i>
        <span class="nav-label">Quản lý</span>
      </router-link>
    </nav>
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
    padding: 12px 16px;
  }
}

@media (max-width: 768px) {
  .top-navbar {
    padding: 8px 12px;
    gap: 8px;
  }
}

/* QUAN TRỌNG: Khung chứa nội dung */
.content-area {
  flex-grow: 1;
  /* Chiếm hết phần còn lại */
  position: relative;
  /* Làm điểm tựa cho con bên trong */
  width: 100%;
  height: 100%;
  background-color: #fbfced;
  overflow: hidden;
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
    gap: 8px;
  }

  .brand {
    order: 1;
    flex: 1;
  }

  .user-profile {
    order: 2;
  }

  .nav-links {
    order: 3;
    width: 100%;
    flex-direction: column;
    gap: 6px;
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
    padding: 10px 14px;
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

/* Mobile Bottom Navigation */
.mobile-bottom-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: #24504b;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
  z-index: 3000;
  justify-content: space-around;
  align-items: center;
  padding: 0 16px;
  border-radius: 20px 20px 0 0;
}

@media (max-width: 768px) {
  .mobile-bottom-nav {
    display: flex;
  }

  /* Hide desktop navigation on mobile */
  .nav-links {
    display: none;
  }

  /* Add bottom padding to content to prevent overlap */
  .content-area {
    padding-bottom: 56px;
  }
}

.mobile-nav-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fbfced;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 10px;
  transition: all 0.3s ease;
  min-width: 50px;
}

.mobile-nav-item i {
  font-size: 1.15rem;
}

.nav-label {
  font-size: 0.6rem;
  font-weight: 500;
  margin-top: 2px;
  opacity: 0.85;
}

.mobile-nav-item.active .nav-label {
  opacity: 1;
  font-weight: 600;
}

.mobile-nav-item:active,
.mobile-nav-item:hover {
  background: rgba(251, 252, 237, 0.1);
}

.mobile-nav-item.active {
  background: rgba(251, 252, 237, 0.2);
  color: #fbfced;
}

.mobile-nav-item.active i {
  color: #fbfced;
  filter: drop-shadow(0 0 6px rgba(251, 252, 237, 0.5));
}
</style>