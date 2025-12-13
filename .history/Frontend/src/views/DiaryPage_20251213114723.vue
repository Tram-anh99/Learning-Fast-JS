<script setup>
import { ref } from 'vue';

// State quản lý hoạt động
const selectedActivity = ref('compost'); // Hoạt động đang chọn
const showForm = ref(true);

// Dữ liệu hoạt động
const activities = ref([
  { id: 'gieo', name: 'Gieo hạt', icon: 'grain', color: 'orange' },
  { id: 'compost', name: 'Bón phân', icon: 'compost', color: 'green' },
  { id: 'pest', name: 'Phun thuốc', icon: 'pest_control', color: 'blue' },
  { id: 'water', name: 'Tưới nước', icon: 'water_drop', color: 'cyan' },
  { id: 'weeding', name: 'Làm cỏ', icon: 'grass', color: 'lime' },
  { id: 'harvest', name: 'Thu hoạch', icon: 'agriculture', color: 'yellow' },
]);

// Form data
const formData = ref({
  activityType: 'Bón phân - Đợt 1 (Bón lót)',
  datetime: new Date().toISOString().slice(0, 16),
  material: 'Phân NPK 20-20-15 - Bình Điền',
  quantity: 50,
  unit: 'kg',
  images: [
    'https://lh3.googleusercontent.com/aida-public/AB6AXuC8rlpuo0MV03QhAUUkn0q05WeV_z3xb3jhAQGqasHHlbVTAAr5rYcCh2YMZD4XCTT9YGrxadEHCgpiUHs8rU_2YqK45gUWRRA8tXPCyKV322kUY4vj1f0FPzhLnlx7pr_iPd8obOnBBvzNBtwrX_x0WZy7dnP5zw14TgSU4YvWF-mApgni22x0otIfw1siEU_R0OdOHdumodtkwLidwzbuSJBXzTAvXcwwsJfF4-2U9yoMurgTkiERVM20aCFxLy2o6KfH2eD8BRk',
    'https://lh3.googleusercontent.com/aida-public/AB6AXuCW4Q3jc1mqn9VDwA5LF1tbPNG5Qed02KUvgA4IgvFx1a-1sqXhNlCmXq7RmO9pcb2cq6KB-pvkSR6oEwtoYC9cDgep8gzLmcpWUXt7ZK2UKZ0vZwtsUQY23fGvMoJG8Aa6rbkAa9YgwGbh5DWREPMIPsQi-WTazi7f1lb0g4EcKHt5n96sdtfoxnZ_10p1eGKiyUGcELNtLBAKObN-888bcFMpBbrHutQXQ36gsG4gjNErzhP-JMEvL-9r9NxrjXqI45pfTpOa9SQ'
  ]
});

// Hoạt động gần đây
const recentActivities = ref([
  {
    id: 1,
    icon: 'compost',
    title: 'Bón phân - Đợt 1',
    description: 'Phân NPK 20-20-15 • 50 kg',
    time: 'Hôm nay',
    timeDetail: '08:30 SA',
    bgColor: 'bg-agri-lightgreen',
    iconColor: 'text-agri-green'
  },
  {
    id: 2,
    icon: 'water_drop',
    title: 'Tưới nước',
    description: 'Tưới nhỏ giọt • 30 phút',
    time: 'Hôm qua',
    timeDetail: '16:15 CH',
    bgColor: 'bg-cyan-50',
    iconColor: 'text-cyan-600'
  }
]);

// Hàm chọn hoạt động
const selectActivity = (activityId) => {
  selectedActivity.value = activityId;
};

// Hàm xử lý form
const handleCancel = () => {
  formData.value = {
    activityType: 'Bón phân - Đợt 1 (Bón lót)',
    datetime: new Date().toISOString().slice(0, 16),
    material: 'Phân NPK 20-20-15 - Bình Điền',
    quantity: 50,
    unit: 'kg',
    images: []
  };
};

const handleSave = () => {
  console.log('Lưu hoạt động:', formData.value);
  alert('Hoạt động đã được lưu!');
};

const removeImage = (index) => {
  formData.value.images.splice(index, 1);
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-weight: 400;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
}

/* Custom scrollbar cho toàn trang */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #D7CCC8;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #8D6E63;
}
</style>

<template>
  <div class="font-sans antialiased h-screen flex flex-col bg-[#FAFAF5]">
    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto py-6 px-4 sm:px-6 lg:px-8 w-full max-w-7xl mx-auto">
      <div class="mb-8 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 class="text-3xl font-black text-[#2E7D32] mb-1">Hôm nay bác làm gì?</h2>
          <p class="text-[#5D4037] text-lg">Ghi lại hoạt động canh tác nhanh chóng và dễ dàng.</p>
        </div>
        <div class="flex items-center gap-2 bg-white px-4 py-2 rounded-2xl shadow-sm border border-[#D7CCC8]/30">
          <span class="material-symbols-outlined text-[#8D6E63]">calendar_today</span>
          <span class="font-medium text-gray-700">{{ new Date().toLocaleDateString('vi-VN', { year: 'numeric', month: 'long', day: 'numeric' }) }}</span>
        </div>
      </div>

      <!-- Main Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Left Column: Activity Selection & History -->
        <div class="lg:col-span-7 space-y-8">
          <!-- Activity Selection -->
          <section>
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                <span class="material-symbols-outlined text-[#2E7D32]">grid_view</span>
                Chọn hoạt động
              </h3>
            </div>
            <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <button 
                v-for="activity in activities" 
                :key="activity.id"
                @click="selectActivity(activity.id)"
                :class="[
                  'group relative flex flex-col items-center justify-center p-6 rounded-3xl shadow-sm border transition-all duration-300 hover:-translate-y-1',
                  selectedActivity === activity.id
                    ? 'bg-[#2E7D32] text-white shadow-[0_0_15px_rgba(76,175,80,0.3)] transform scale-[1.02] ring-4 ring-[#E8F5E9]'
                    : 'bg-white border-transparent hover:border-[#2E7D32]/30 hover:shadow-[0_4px_20px_-2px_rgba(46,125,50,0.1)]'
                ]"
              >
                <div 
                  v-if="selectedActivity === activity.id"
                  class="absolute top-3 right-3"
                >
                  <span class="material-symbols-outlined text-white/80 text-xl">check_circle</span>
                </div>
                <div 
                  :class="[
                    'h-14 w-14 rounded-2xl flex items-center justify-center mb-3 transition-transform',
                    selectedActivity === activity.id
                      ? 'bg-white/20'
                      : `bg-${activity.color}-100 text-${activity.color}-600`,
                    !selectedActivity !== activity.id && 'group-hover:scale-110'
                  ]"
                >
                  <span class="material-symbols-outlined text-4xl">{{ activity.icon }}</span>
                </div>
                <span :class="['text-base font-bold', selectedActivity === activity.id ? 'text-white' : 'text-gray-700 group-hover:text-[#2E7D32]']">
                  {{ activity.name }}
                </span>
                <span v-if="selectedActivity === activity.id" class="text-xs bg-white/20 px-2 py-0.5 rounded-full mt-1">Đang nhập...</span>
              </button>
            </div>
          </section>

          <!-- Recent Activities -->
          <section>
            <div class="flex items-center justify-between mb-4 mt-8">
              <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                <span class="material-symbols-outlined text-[#2E7D32]">history</span>
                Hoạt động gần đây
              </h3>
              <a class="text-sm font-bold text-[#2E7D32] hover:underline" href="#">Xem tất cả</a>
            </div>
            <div class="space-y-3">
              <div 
                v-for="activity in recentActivities" 
                :key="activity.id"
                class="bg-white p-4 rounded-2xl border border-[#D7CCC8]/20 flex items-center shadow-sm hover:shadow-md transition-shadow"
              >
                <div :class="['h-12 w-12 rounded-full flex items-center justify-center mr-4 flex-shrink-0', activity.bgColor, activity.iconColor]">
                  <span class="material-symbols-outlined">{{ activity.icon }}</span>
                </div>
                <div class="flex-grow">
                  <h4 class="font-bold text-gray-800">{{ activity.title }}</h4>
                  <p class="text-sm text-[#5D4037]">{{ activity.description }}</p>
                </div>
                <div class="text-right">
                  <span class="block text-sm font-bold text-gray-600">{{ activity.time }}</span>
                  <span class="block text-xs text-gray-400">{{ activity.timeDetail }}</span>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Right Column: Form -->
        <div class="lg:col-span-5">
          <div>
            <div class="bg-white rounded-3xl shadow-xl border border-[#2E7D32]/10 overflow-hidden relative">
              <div class="h-3 bg-[#2E7D32] w-full"></div>
              <div class="p-6 sm:p-8">
                <!-- Form Header -->
                <div class="flex items-center justify-between mb-6">
                  <div>
                    <span class="text-xs font-bold text-[#8D6E63] uppercase tracking-wider mb-1 block">Hoạt động mới</span>
                    <h3 class="text-2xl font-black text-[#2E7D32] flex items-center gap-2">
                      {{ activities.find(a => a.id === selectedActivity)?.name || 'Bón phân' }}
                    </h3>
                  </div>
                  <div class="bg-[#E8F5E9] p-2 rounded-full">
                    <span class="material-symbols-outlined text-[#2E7D32] text-3xl">{{ activities.find(a => a.id === selectedActivity)?.icon || 'compost' }}</span>
                  </div>
                </div>

                <!-- Form -->
                <form class="space-y-6" @submit.prevent>
                  <!-- Activity Type -->
                  <div class="space-y-4">
                    <div>
                      <label class="block text-sm font-bold text-[#5D4037] mb-2">Loại hoạt động</label>
                      <div class="relative">
                        <select v-model="formData.activityType" class="block w-full rounded-xl border border-[#D7CCC8] bg-[#FAFAF5]/50 py-3 pl-4 pr-10 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm transition-colors cursor-pointer font-medium">
                          <option>Bón phân - Đợt 1 (Bón lót)</option>
                          <option>Bón phân - Đợt 2 (Thúc chồi)</option>
                          <option>Bón phân - Đợt 3 (Thúc trái)</option>
                        </select>
                      </div>
                    </div>
                    <div>
                      <label class="block text-sm font-bold text-[#5D4037] mb-2">Thời gian thực hiện</label>
                      <input v-model="formData.datetime" class="block w-full rounded-xl border border-[#D7CCC8] bg-[#FAFAF5]/50 py-3 px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm font-medium" type="datetime-local" />
                    </div>
                  </div>

                  <!-- Material & Quantity -->
                  <div class="bg-[#E8F5E9]/30 p-4 rounded-2xl space-y-4 border border-[#2E7D32]/10">
                    <div>
                      <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                        <span class="material-symbols-outlined text-sm">inventory_2</span>
                        Vật tư sử dụng
                      </label>
                      <select v-model="formData.material" class="block w-full rounded-xl border border-[#D7CCC8] bg-white py-3 pl-4 pr-10 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm">
                        <option>Phân NPK 20-20-15 - Bình Điền</option>
                        <option>Phân Urê (Đạm Phú Mỹ)</option>
                        <option>Phân Kali</option>
                      </select>
                    </div>
                    <div>
                      <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                        <span class="material-symbols-outlined text-sm">scale</span>
                        Liều lượng / Số lượng
                      </label>
                      <div class="flex rounded-xl shadow-sm">
                        <input v-model.number="formData.quantity" class="block w-full rounded-l-xl border border-[#D7CCC8] border-r-0 bg-white py-3 px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm" type="number" />
                        <span class="inline-flex items-center rounded-r-xl border border-l-0 border-[#D7CCC8] bg-white px-4 text-gray-500 font-bold sm:text-sm">
                          {{ formData.unit }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Images -->
                  <div>
                    <label class="block text-sm font-bold text-[#5D4037] mb-2">Hình ảnh thực tế</label>
                    <div class="grid grid-cols-4 gap-2">
                      <button class="aspect-square flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-[#2E7D32]/40 bg-[#E8F5E9]/20 text-[#2E7D32] hover:bg-[#E8F5E9]/50 transition-colors" type="button">
                        <span class="material-symbols-outlined text-2xl mb-1">add_a_photo</span>
                        <span class="text-[10px] font-bold">Thêm</span>
                      </button>
                      <div 
                        v-for="(image, index) in formData.images" 
                        :key="index"
                        class="aspect-square relative group"
                      >
                        <img :alt="`Preview ${index}`" class="w-full h-full object-cover rounded-xl shadow-sm" :src="image" />
                        <button @click="removeImage(index)" class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 shadow-md opacity-0 group-hover:opacity-100 transition-opacity" type="button">
                          <span class="material-symbols-outlined text-[14px] block">close</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Action Buttons -->
                  <div class="pt-2 flex items-center gap-3">
                    <button @click="handleCancel" class="flex-1 py-3.5 px-6 rounded-xl border border-[#D7CCC8] text-[#8D6E63] font-bold hover:bg-[#FAFAF5] transition-colors" type="button">
                      Hủy
                    </button>
                    <button @click="handleSave" class="flex-[2] py-3.5 px-6 rounded-xl bg-[#2E7D32] text-white font-bold shadow-lg shadow-[#2E7D32]/30 hover:bg-green-800 hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2" type="button">
                      <span class="material-symbols-outlined">save</span>
                      Lưu hoạt động
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <!-- Tips Section -->
            <div class="mt-6 bg-[#8D6E63] text-white p-4 rounded-2xl flex items-start gap-3 shadow-lg">
              <span class="material-symbols-outlined text-yellow-300">lightbulb</span>
              <div class="text-sm">
                <p class="font-bold mb-1">Mẹo cho Bác Ba:</p>
                <p class="opacity-90">Nên bón phân vào sáng sớm hoặc chiều mát để cây hấp thụ tốt nhất.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="py-6 bg-white border-t border-[#D7CCC8]/30 mt-8">
        <div class="text-center">
          <p class="text-sm text-[#5D4037] font-medium">© 2024 VN-AgriTrace. Hệ thống Quản lý & Truy xuất Nguồn gốc.</p>
        </div>
      </footer>
    </main>
  </div>
</template>
