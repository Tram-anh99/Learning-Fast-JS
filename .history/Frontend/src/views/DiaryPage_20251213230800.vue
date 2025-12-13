<script setup>
import { ref } from 'vue';
import DiaryActivitySelector from '../components/DiaryActivitySelector.vue';
import DiaryActivityForm from '../components/DiaryActivityForm.vue';
import DiaryActivityHistory from '../components/DiaryActivityHistory.vue';

// ============================================
// STATE MANAGEMENT - Quản lý trạng thái chung
// ============================================

// Hoạt động hiện tại được chọn (mặc định: Bón phân)
const selectedActivity = ref('compost');
const showForm = ref(true);

// Thửa đất được chọn để ghi nhật ký (ID thửa đất mặc định)
const selectedField = ref('field-001');

// ============================================
// DATA - Dữ liệu tĩnh và động
// ============================================

// Danh sách các loại hoạt động canh tác
// Mỗi hoạt động có: id, tên, icon (Material Symbols), màu sắc
const activities = ref([
  { id: 'gieo', name: 'Gieo hạt', icon: 'grain', color: 'orange' },
  { id: 'compost', name: 'Bón phân', icon: 'compost', color: 'green' },
  { id: 'pest', name: 'Phun thuốc', icon: 'pest_control', color: 'blue' },
  { id: 'water', name: 'Tưới nước', icon: 'water_drop', color: 'cyan' },
  { id: 'weeding', name: 'Làm cỏ', icon: 'grass', color: 'lime' },
  { id: 'harvest', name: 'Thu hoạch', icon: 'agriculture', color: 'yellow' },
]);

// Danh sách thửa đất của nông dân
// Chứa thông tin: id, tên, diện tích, loại cây, tình trạng
const fields = ref([
  { id: 'field-001', name: 'Thửa 1 - Lúa', area: 2.5, crop: 'Lúa tưới', status: 'Đang canh tác' },
  { id: 'field-002', name: 'Thửa 2 - Rau', area: 1.8, crop: 'Rau cải', status: 'Đang canh tác' },
  { id: 'field-003', name: 'Thửa 3 - Dưa', area: 3.2, crop: 'Dưa leo', status: 'Đang canh tác' }
]);

// Dữ liệu form nhập liệu hoạt động
// Chứa thông tin: loại hoạt động, thời gian, vật tư, liều lượng, hình ảnh
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
    bgColor: 'bg-[#E8F5E9]',
    iconColor: 'text-[#2E7D32]'
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
    <main class="flex-1 w-full px-4 py-6 pb-16 mx-auto overflow-y-auto sm:px-6 lg:px-8 max-w-7xl">
      <!-- Header Section -->
      <div class="flex flex-col justify-between gap-4 mb-8 md:flex-row md:items-center">
        <div>
          <h2 class="text-3xl font-black text-[#2E7D32] mb-1">Hôm nay bác làm gì?</h2>
          <p class="text-[#5D4037] text-lg">Ghi lại hoạt động canh tác nhanh chóng và dễ dàng.</p>
        </div>
        <div class="flex items-center gap-2 bg-white px-4 py-2 rounded-2xl shadow-sm border border-[#D7CCC8]/30">
          <span class="material-symbols-outlined text-[#8D6E63]">calendar_today</span>
          <span class="font-medium text-gray-700">{{ new Date().toLocaleDateString('vi-VN', {
            year: 'numeric', month:
              'long', day: 'numeric' }) }}</span>
        </div>
      </div>

      <!-- Main Grid -->
      <div class="grid items-start grid-cols-1 gap-8 lg:grid-cols-12">
        <!-- Left Column: Activity Selection & History -->
        <div class="space-y-8 lg:col-span-7">
          <!-- Component chọn hoạt động -->
          <DiaryActivitySelector :activities="activities" :selectedActivity="selectedActivity"
            @select="selectActivity" />

          <!-- Component lịch sử hoạt động -->
          <DiaryActivityHistory :activities="recentActivities" />
        </div>

        <!-- Right Column: Form -->
        <div class="lg:col-span-5">
          <!-- Component form nhập liệu -->
          <DiaryActivityForm :selectedActivity="selectedActivity" :activities="activities" :formData="formData"
            @update:formData="(newData) => formData = newData" @save="handleSave" @cancel="handleCancel"
            @removeImage="removeImage" />
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
