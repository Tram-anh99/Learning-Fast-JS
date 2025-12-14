<script setup>
/**
 * ========== COMPONENT: DiaryActivityHistory.vue ==========
 * Purpose: Display recent farming activity history (last 24 hours, past week, etc)
 * Helps farmer review activities they just performed
 * 
 * Architecture:
 *   - Parent: DiaryPage or dashboard
 *   - Child: None
 *   - Communication: Props in, display only
 * 
 * Features:
 *   - Chronological list of recent activities
 *   - Activity icons with color-coded backgrounds
 *   - Activity title and description
 *   - Time indicators (Today, Yesterday, etc) + time detail (HH:MM)
 *   - Hover effects on activity cards
 *   - "View All" link to see full history
 * 
 * Props:
 *   - activities (Array): Recent activity records
 *     Structure: Array<{id, title, description, icon, bgColor, iconColor, time, timeDetail}>
 *     Example: { id: 1, title: "Bón phân - Đợt 1", description: "Phân NPK 50kg", icon: "grain", bgColor: "bg-green-100", iconColor: "text-green-600", time: "Hôm nay", timeDetail: "14:30" }
 */

// ========== IMPORTS ==========
// (No imports needed - display only component using slots and arrays)

// ========== PROPS ==========
// Define props for activities data
defineProps({
  // activities: Array of activity records to display in chronological order
  // Type: Array<Object>
  // Required fields in each activity object:
  //   - id: unique identifier for list rendering
  //   - title: activity name (e.g., "Bón phân - Đợt 1")
  //   - description: details (e.g., "Phân NPK 50kg")
  //   - icon: Material Symbol icon name (e.g., "grain", "water_drop")
  //   - bgColor: background color class (e.g., "bg-green-100", "bg-blue-100")
  //   - iconColor: text color class (e.g., "text-green-600", "text-blue-600")
  //   - time: relative time (e.g., "Hôm nay", "Hôm qua", "2 ngày trước")
  //   - timeDetail: exact time (e.g., "14:30", "09:15")
  activities: Array
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
