<script setup>
import { useDiary } from '../composables/useDiary';
import DiaryHeader from '../components/DiaryHeader.vue';
import DiaryActivityCard from '../components/DiaryActivityCard.vue';
import DiaryNavigation from '../components/DiaryNavigation.vue';

// Sử dụng composable nhật ký
const { diaryList, getCurrentDate, getActivityIcon } = useDiary();

// Hàm xử lý nút thêm mới
const handleAddNew = () => {
  window.alert('Chức năng thêm mới sẽ sớm ra mắt!');
};
</script>

<template>
  <div class="min-h-screen font-sans text-gray-800 bg-slate-50 pb-28">
    
    <!-- Header -->
    <DiaryHeader :getCurrentDate="getCurrentDate" />

    <!-- Main content -->
    <main class="p-4 space-y-5">

      <!-- Phần thống kê -->
      <section class="grid grid-cols-2 gap-3">
        <!-- Card công việc tuần này -->
        <div class="relative flex flex-col justify-between h-24 p-4 overflow-hidden text-white bg-green-600 shadow-sm rounded-2xl">
          <span class="relative z-10 text-sm font-medium opacity-80">Công việc tuần này</span>
          <span class="relative z-10 text-3xl font-bold">12</span>
          <svg class="absolute w-20 h-20 text-green-500 opacity-50 -right-2 -bottom-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
          </svg>
        </div>

        <!-- Card thửa đang canh tác -->
        <div class="flex flex-col justify-between h-24 p-4 bg-white border border-gray-100 shadow-sm rounded-2xl">
          <span class="text-sm font-medium text-gray-500">Thửa đang canh tác</span>
          <span class="text-3xl font-bold text-gray-800">03 <span class="text-lg font-normal text-gray-400">/ 05</span></span>
        </div>
      </section>

      <!-- Phần hoạt động gần đây -->
      <section>
        <h2 class="flex items-center justify-between mb-3 text-lg font-bold text-gray-800">
          Hoạt động gần đây
          <button class="text-sm font-medium text-green-600 transition-colors hover:text-green-700">
            Xem tất cả
          </button>
        </h2>

        <!-- Danh sách thẻ hoạt động -->
        <div class="space-y-3">
          <DiaryActivityCard 
            v-for="item in diaryList" 
            :key="item.id"
            :item="item"
            :getActivityIcon="getActivityIcon"
          />
        </div>
      </section>

    </main>

    <!-- Nút thêm mới (FAB) -->
    <button 
      @click="handleAddNew"
      class="fixed z-40 flex items-center justify-center text-3xl text-white transition-transform bg-green-600 rounded-full shadow-lg bottom-20 right-4 w-14 h-14 shadow-green-600/30 active:scale-90 hover:bg-green-700"
      title="Thêm hoạt động mới"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
      </svg>
    </button>

    <!-- Navigation bar -->
    <DiaryNavigation />

  </div>
</template>
