<script setup>
// Import cái bản đồ vừa tạo vào để dùng
import BanDo from './components/BanDo.vue';
</script>

<template>
  <div class="main-layout">
    <header>
      <h1>Quản lý Mã số Vùng trồng (WebGIS)</h1>
    </header>

    <main>
      <BanDo />
    </main>
  </div>
</template>

<style>
/* CSS cho bố cục trang */
.main-layout {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

header {
  text-align: center;
  margin-bottom: 20px;
  color: #2c3e50;
}
</style>