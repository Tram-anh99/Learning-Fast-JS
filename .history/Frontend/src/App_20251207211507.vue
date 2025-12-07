<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="app-layout">
    
    <div class="header">
      <h2>🌱 Hệ thống Quản lý Vùng trồng</h2>
    </div>

    <div class="main-content">
      <RouterView />
    </div>

  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Cao 100% màn hình */
  width: 100vw;
}

.header {
  height: 60px;
  background-color: #1b4332;
  color: white;
  display: flex;
  align-items: center;
  padding-left: 20px;
  flex-shrink: 0; /* Không được co lại */
}

.main-content {
  flex-grow: 1; /* Chiếm hết phần còn lại */
  position: relative;
  background-color: #f0f0f0; /* Màu xám để biết khung có hiện ko */
  width: 100%;
}
</style>