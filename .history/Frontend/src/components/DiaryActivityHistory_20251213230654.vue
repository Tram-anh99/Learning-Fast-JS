<script setup>
// Props nhận dữ liệu từ component cha
defineProps({
      activities: Array // Danh sách hoạt động gần đây
});
</script>

<template>
      <!-- Section lịch sử hoạt động -->
      <section>
            <!-- Tiêu đề phần -->
            <div class="flex items-center justify-between mb-4 mt-8">
                  <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                        <span class="material-symbols-outlined text-[#2E7D32]">history</span>
                        Hoạt động gần đây
                  </h3>
                  <a class="text-sm font-bold text-[#2E7D32] hover:underline" href="#">Xem tất cả</a>
            </div>

            <!-- Danh sách hoạt động -->
            <div class="space-y-3">
                  <!-- Loop qua từng hoạt động gần đây -->
                  <div v-for="activity in activities" :key="activity.id"
                        class="bg-white p-4 rounded-2xl border border-[#D7CCC8]/20 flex items-center shadow-sm hover:shadow-md transition-shadow">
                        <!-- Icon hoạt động -->
                        <div
                              :class="['h-12 w-12 rounded-full flex items-center justify-center mr-4 flex-shrink-0', activity.bgColor, activity.iconColor]">
                              <span class="material-symbols-outlined">{{ activity.icon }}</span>
                        </div>

                        <!-- Thông tin hoạt động -->
                        <div class="flex-grow">
                              <!-- Tên hoạt động -->
                              <h4 class="font-bold text-gray-800">{{ activity.title }}</h4>
                              <!-- Chi tiết hoạt động -->
                              <p class="text-sm text-[#5D4037]">{{ activity.description }}</p>
                        </div>

                        <!-- Thời gian hoạt động -->
                        <div class="text-right">
                              <!-- Ngày hoạt động -->
                              <span class="block text-sm font-bold text-gray-600">{{ activity.time }}</span>
                              <!-- Giờ hoạt động -->
                              <span class="block text-xs text-gray-400">{{ activity.timeDetail }}</span>
                        </div>
                  </div>
            </div>
      </section>
</template>
