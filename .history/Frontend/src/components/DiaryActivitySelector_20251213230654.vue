<script setup>
// Props nhận dữ liệu từ component cha
defineProps({
      activities: Array,      // Danh sách hoạt động
      selectedActivity: String // Hoạt động được chọn
});

// Emits sự kiện khi chọn hoạt động
defineEmits(['select']);
</script>

<template>
      <!-- Section chọn hoạt động -->
      <section>
            <!-- Tiêu đề phần -->
            <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                        <span class="material-symbols-outlined text-[#2E7D32]">grid_view</span>
                        Chọn hoạt động
                  </h3>
            </div>

            <!-- Grid các nút hoạt động -->
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
                  <!-- Loop qua từng hoạt động -->
                  <button v-for="activity in activities" :key="activity.id" @click="$emit('select', activity.id)"
                        :class="[
                              'group relative flex flex-col items-center justify-center p-6 rounded-3xl shadow-sm border transition-all duration-300 hover:-translate-y-1',
                              selectedActivity === activity.id
                                    ? 'bg-[#2E7D32] text-white shadow-[0_0_15px_rgba(76,175,80,0.3)] transform scale-[1.02] ring-4 ring-[#E8F5E9]'
                                    : 'bg-white border-transparent hover:border-[#2E7D32]/30 hover:shadow-[0_4px_20px_-2px_rgba(46,125,50,0.1)]'
                        ]">
                        <!-- Check icon nếu được chọn -->
                        <div v-if="selectedActivity === activity.id" class="absolute top-3 right-3">
                              <span class="material-symbols-outlined text-white/80 text-xl">check_circle</span>
                        </div>

                        <!-- Icon hoạt động -->
                        <div :class="[
                              'h-14 w-14 rounded-2xl flex items-center justify-center mb-3 transition-transform',
                              selectedActivity === activity.id
                                    ? 'bg-white/20'
                                    : `bg-${activity.color}-100 text-${activity.color}-600`,
                              selectedActivity !== activity.id && 'group-hover:scale-110'
                        ]">
                              <span class="material-symbols-outlined text-4xl">{{ activity.icon }}</span>
                        </div>

                        <!-- Tên hoạt động -->
                        <span
                              :class="['text-base font-bold', selectedActivity === activity.id ? 'text-white' : 'text-gray-700 group-hover:text-[#2E7D32]']">
                              {{ activity.name }}
                        </span>

                        <!-- Badge "Đang nhập" nếu được chọn -->
                        <span v-if="selectedActivity === activity.id"
                              class="text-xs bg-white/20 px-2 py-0.5 rounded-full mt-1">Đang nhập...</span>
                  </button>
            </div>
      </section>
</template>
