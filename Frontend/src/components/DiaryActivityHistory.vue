<script setup>
// ============================================
// COMPONENT: DiaryActivityHistory
// ============================================
// Mục đích: Hiển thị lịch sử hoạt động gần đây
// Giúp người dùng tra cứu các hoạt động vừa thực hiện
//
// Cách dùng:
// <DiaryActivityHistory :activities="recentActivities" />
// ============================================

// Props nhận dữ liệu từ component cha
defineProps({
  activities: Array // Danh sách hoạt động gần đây (hôm nay, hôm qua, etc)
});
</script>

<template>
  <!-- Section lịch sử hoạt động -->
  <section>
    <!-- Tiêu đề phần với icon history -->
    <div class="flex items-center justify-between mb-4 mt-8">
      <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
        <span class="material-symbols-outlined text-[#2E7D32]">history</span>
        Hoạt động gần đây
      </h3>
      <!-- Link xem tất cả hoạt động -->
      <a class="text-sm font-bold text-[#2E7D32] hover:underline" href="#">Xem tất cả</a>
    </div>
    
    <!-- Danh sách hoạt động -->
    <div class="space-y-3">
      <!-- Loop qua từng hoạt động gần đây -->
      <div
        v-for="activity in activities"
        :key="activity.id"
        class="bg-white p-4 rounded-2xl border border-[#D7CCC8]/20 flex items-center shadow-sm hover:shadow-md transition-shadow"
      >
        <!-- Icon hoạt động với nền màu tương ứng -->
        <div :class="['h-12 w-12 rounded-full flex items-center justify-center mr-4 flex-shrink-0', activity.bgColor, activity.iconColor]">
          <span class="material-symbols-outlined">{{ activity.icon }}</span>
        </div>
        
        <!-- Thông tin hoạt động -->
        <div class="flex-grow">
          <!-- Tên hoạt động -->
          <h4 class="font-bold text-gray-800">{{ activity.title }}</h4>
          <!-- Chi tiết hoạt động (vật tư, số lượng, etc) -->
          <p class="text-sm text-[#5D4037]">{{ activity.description }}</p>
        </div>
        
        <!-- Thời gian hoạt động -->
        <div class="text-right">
          <!-- Ngày hoạt động (Hôm nay, Hôm qua, etc) -->
          <span class="block text-sm font-bold text-gray-600">{{ activity.time }}</span>
          <!-- Giờ thực hiện hoạt động -->
          <span class="block text-xs text-gray-400">{{ activity.timeDetail }}</span>
        </div>
      </div>
    </div>
  </section>
</template>
