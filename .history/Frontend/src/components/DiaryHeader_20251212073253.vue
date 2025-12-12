<script setup>
// Props nhận hàm lấy ngày hiện tại
defineProps({
  getCurrentDate: {
    type: Function,
    required: true
  }
});
</script>

<template>
  <!-- Header dính ở trên cùng -->
  <header class="sticky top-0 z-30 p-4 bg-white border-b border-gray-100 shadow-sm/50 backdrop-blur-md bg-white/90">
    <div class="flex items-center justify-between">
      <!-- Tiêu đề + Ngày tháng -->
      <div>
        <h1 class="text-xl font-extrabold tracking-tight text-green-700">
          Nhật Ký Đồng Ruộng
        </h1>
        <p class="text-sm text-gray-500 font-medium mt-0.5 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1 text-green-500" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
          </svg>
          Hôm nay, {{ getCurrentDate() }}
        </p>
      </div>

      <!-- Avatar người dùng -->
      <div class="flex items-center justify-center w-10 h-10 overflow-hidden bg-green-100 border-2 border-white rounded-full shadow-sm">
        <img src="https://i.pravatar.cc/150?img=3" alt="User" class="object-cover w-full h-full">
      </div>
    </div>
  </header>
</template>
