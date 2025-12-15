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
  <!-- ========== ACTIVITY HISTORY SECTION ========== -->
  <!-- Section: Main container for recent activity list -->
  <section>

    <!-- ========== SECTION HEADER ========== -->
    <!-- Header: Flex between title (left) and "View All" link (right) -->
    <!-- mb-4 = 16px bottom margin before activity list -->
    <!-- mt-8 = 32px top margin (distance from previous section) -->
    <div class="flex items-center justify-between mb-4 mt-8">
      <!-- Title: "Hoạt động gần đây" = Recent Activities -->
      <!-- h3 = heading level 3, text-lg = 18px font, font-bold = 700 weight -->
      <!-- flex items-center gap-2 = icon + text horizontally with 8px gap -->
      <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
        <!-- Icon: history = Material Symbol for past/time-based data -->
        <!-- text-[#2E7D32] = green color matching app theme -->
        <span class="material-symbols-outlined text-[#2E7D32]">history</span>
        <!-- Label text -->
        Hoạt động gần đây
      </h3>

      <!-- "View All" link: Navigate to full history page -->
      <!-- text-sm = 14px small font, font-bold = 700 weight -->
      <!-- text-[#2E7D32] = green color matching app theme -->
      <!-- hover:underline = underline appears on hover for interactive feedback -->
      <a class="text-sm font-bold text-[#2E7D32] hover:underline" href="#">
        Xem tất cả
      </a>
    </div>

    <!-- ========== ACTIVITY LIST ========== -->
    <!-- Activity list wrapper: space-y-3 = 12px vertical gap between items -->
    <div class="space-y-3">

      <!-- ========== ACTIVITY ITEM LOOP ========== -->
      <!-- v-for: Loop through activities array, render card for each -->
      <!-- :key: Unique identifier (activity.id) for Vue's list rendering -->
      <div v-for="activity in activities" :key="activity.id"
        class="bg-white p-4 rounded-2xl flex items-center shadow-sm hover:shadow-md transition-shadow">

        <!-- ========== ACTIVITY ICON ========== -->
        <!-- Icon container: h-12 w-12 = 48px x 48px square -->
        <!-- rounded-full = circle shape (border-radius 9999px) -->
        <!-- flex items-center justify-center = center icon inside circle -->
        <!-- mr-4 = 16px right margin before activity info -->
        <!-- flex-shrink-0 = don't shrink below content size (preserves icon size) -->
        <!-- :class: Dynamic background & text color classes from activity object -->
        <div
          :class="['h-12 w-12 rounded-full flex items-center justify-center mr-4 flex-shrink-0', activity.bgColor, activity.iconColor]">
          <!-- Material Symbol icon: Dynamic icon from activity.icon property -->
          <!-- Icon name examples: "grain" (seeding), "water_drop" (watering), "spray" (spraying) -->
          <span class="material-symbols-outlined">{{ activity.icon }}</span>
        </div>

        <!-- ========== ACTIVITY INFO ========== -->
        <!-- Info wrapper: flex-grow = expand to fill available space -->
        <div class="flex-grow">
          <!-- Activity title: e.g., "Bón phân - Đợt 1", "Tưới nước" -->
          <!-- h4 = heading level 4, font-bold = 700, text-gray-800 = dark gray -->
          <h4 class="font-bold text-gray-800">{{ activity.title }}</h4>

          <!-- Activity description: More details (e.g., "Phân NPK 50kg", "Nước từ giếu") -->
          <!-- text-sm = 14px small font, text-[#5D4037] = dark brown color -->
          <p class="text-sm text-[#5D4037]">{{ activity.description }}</p>
        </div>

        <!-- ========== ACTIVITY TIME ========== -->
        <!-- Time wrapper: text-right = right-align time information -->
        <div class="text-right">
          <!-- Relative time: "Hôm nay" (Today), "Hôm qua" (Yesterday), etc -->
          <!-- block = full width block element -->
          <!-- text-sm = 14px font, font-bold = 700, text-gray-600 = medium gray -->
          <span class="block text-sm font-bold text-gray-600">{{ activity.time }}</span>

          <!-- Exact time: HH:MM format (e.g., "14:30", "09:15") -->
          <!-- block = full width block element -->
          <!-- text-xs = 12px very small font, text-gray-400 = light gray color -->
          <span class="block text-xs text-gray-400">{{ activity.timeDetail }}</span>
        </div>
      </div>
    </div>
  </section>
</template>
