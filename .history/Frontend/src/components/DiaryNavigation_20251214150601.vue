<script setup>
// Navigation items
const navItems = [
      { id: 'home', icon: 'home', label: 'Trang chủ', active: true },
      { id: 'map', icon: 'map', label: 'Bản đồ', active: false },
      { id: 'report', icon: 'report', label: 'Báo cáo', active: false },
      { id: 'account', icon: 'account', label: 'Tài khoản', active: false },
];
</script>

<template>
      <!-- Navigation bar dính ở dưới cùng -->
      <nav
            class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] px-2 py-2 z-30 flex justify-around items-center pb-safe">
            <!-- Trang chủ (active) -->
            <a href="#" class="flex flex-col items-center p-2 text-green-600 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" viewBox="0 0 20 20"
                        fill="currentColor">
                        <path
                              d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                  </svg>
                  <span class="text-[11px] font-bold">Trang chủ</span>
            </a>

            <!-- Bản đồ -->
            <a href="#" class="flex flex-col items-center p-2 text-gray-400 transition-colors hover:text-green-600">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round"
                              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 7m0 13V7m0 0L9 7" />
                  </svg>
                  <span class="text-[11px] font-medium">Bản đồ</span>
            </a>

            <!-- FAB button placeholder -->
            <div class="w-12"></div>

            <!-- Báo cáo -->
            <a href="#" class="flex flex-col items-center p-2 text-gray-400 transition-colors hover:text-green-600">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round"
                              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <span class="text-[11px] font-medium">Báo cáo</span>
            </a>

            <!-- Tài khoản -->
            <a href="#" class="flex flex-col items-center p-2 text-gray-400 transition-colors hover:text-green-600">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round"
                              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span class="text-[11px] font-medium">Tài khoản</span>
            </a>
      </nav>
</template>

<style scoped>
/* Safe area: Hỗ trợ padding cho thiết bị có tai thỏ (iPhone X+) */
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 8px);
}
</style>
