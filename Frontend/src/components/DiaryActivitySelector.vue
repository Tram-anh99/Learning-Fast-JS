<script setup>
// ============================================
// COMPONENT: DiaryActivitySelector
// ============================================
// Mục đích: Hiển thị lưới các nút chọn hoạt động canh tác
// 
// Cách dùng:
// <DiaryActivitySelector 
//   :activities="activities"
//   :selectedActivity="selectedActivity"
//   @select="selectActivity"
// />
// ============================================

// Props nhận dữ liệu từ component cha
defineProps({
  activities: Array,       // Danh sách hoạt động (gieo, bón, phun, tưới, làm cỏ, thu hoạch)
  selectedActivity: String // ID hoạt động được chọn hiện tại
});

// Emits sự kiện khi chọn hoạt động
// Tham số truyền: activityId (string) - ID của hoạt động được chọn
defineEmits(['select']);
</script>

<template>
  <!-- Section chọn hoạt động -->
  <section>
    <!-- Tiêu đề phần với icon grid -->
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
        <span class="material-symbols-outlined text-[#2E7D32]">grid_view</span>
        Chọn hoạt động
      </h3>
    </div>
    
    <!-- Grid các nút hoạt động (2 cột trên mobile, 3 cột trên desktop) -->
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
      <!-- Loop qua từng hoạt động -->
      <button
        v-for="activity in activities"
        :key="activity.id"
        @click="$emit('select', activity.id)"
        :class="[
          'group relative flex flex-col items-center justify-center p-6 rounded-3xl shadow-sm border transition-all duration-300 hover:-translate-y-1',
          // Styling khi hoạt động được chọn
          selectedActivity === activity.id
            ? 'bg-[#2E7D32] text-white shadow-[0_0_15px_rgba(76,175,80,0.3)] transform scale-[1.02] ring-4 ring-[#E8F5E9]'
            // Styling khi chưa chọn
            : 'bg-white border-transparent hover:border-[#2E7D32]/30 hover:shadow-[0_4px_20px_-2px_rgba(46,125,50,0.1)]'
        ]"
      >
        <!-- Check icon ở góc phải khi được chọn -->
        <div v-if="selectedActivity === activity.id" class="absolute top-3 right-3">
          <span class="material-symbols-outlined text-white/80 text-xl">check_circle</span>
        </div>
        
        <!-- Icon hoạt động - đổi màu theo loại hoạt động -->
        <div
          :class="[
            'h-14 w-14 rounded-2xl flex items-center justify-center mb-3 transition-transform',
            selectedActivity === activity.id
              ? 'bg-white/20'  // Nền mờ khi chọn
              : `bg-${activity.color}-100 text-${activity.color}-600`,  // Nền sáng màu tương ứng
            selectedActivity !== activity.id && 'group-hover:scale-110'  // Scale up icon khi hover
          ]"
        >
          <span class="material-symbols-outlined text-4xl">{{ activity.icon }}</span>
        </div>
        
        <!-- Tên hoạt động -->
        <span :class="['text-base font-bold', selectedActivity === activity.id ? 'text-white' : 'text-gray-700 group-hover:text-[#2E7D32]']">
          {{ activity.name }}
        </span>
        
        <!-- Badge "Đang nhập..." hiển thị khi được chọn -->
        <span v-if="selectedActivity === activity.id" class="text-xs bg-white/20 px-2 py-0.5 rounded-full mt-1">Đang nhập...</span>
      </button>
    </div>
  </section>
</template>
