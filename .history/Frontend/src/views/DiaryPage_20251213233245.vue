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
// Chứa thông tin: id, ma (mã số vùng trồng - đồng bộ với WebGIS), tên, diện tích, loại cây, tình trạng
// Ma số phải thống nhất với `danhSachGoc` trong HomeView để tích hợp bản đồ
const fields = ref([
  { id: 'field-001', ma: 'VT-003', name: 'Thửa 1 - Lúa ST25', area: 10, crop: 'Lúa ST25', status: 'Thu hoạch' },
  { id: 'field-002', ma: 'VT-001', name: 'Thửa 2 - Xoài Cát Hòa Lộc', area: 5, crop: 'Xoài', status: 'Đang canh tác' },
  { id: 'field-003', ma: 'VT-002', name: 'Thửa 3 - Thanh Long Ruột Đỏ', area: 3.2, crop: 'Thanh long', status: 'Đang canh tác' }
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

// Lịch sử hoạt động gần đây
// Hiển thị các hoạt động vừa thực hiện để người dùng có thể tra cứu
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

// ============================================
// METHODS - Các hàm xử lý sự kiện
// ============================================

/**
 * Chọn loại hoạt động canh tác
 * @param {string} activityId - ID của hoạt động được chọn
 */
const selectActivity = (activityId) => {
  selectedActivity.value = activityId;
};

/**
 * Chọn thửa đất để ghi nhật ký
 * @param {string} fieldId - ID của thửa đất được chọn
 */
const selectField = (fieldId) => {
  selectedField.value = fieldId;
};

/**
 * Hủy nhập liệu và reset form về trạng thái ban đầu
 */
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

/**
 * Lưu hoạt động canh tác
 * Ghi nhật ký với mã số vùng trồng để liên kết với bản đồ WebGIS
 * TODO: Kết nối API để lưu vào database
 */
const handleSave = () => {
  // Lấy thông tin thửa đất được chọn (bao gồm mã số vùng trồng)
  const selectedFieldData = fields.value.find(f => f.id === selectedField.value);
  
  console.log('Lưu hoạt động:', {
    fieldId: selectedField.value,
    fieldCode: selectedFieldData?.ma, // Mã số vùng trồng (VT-001, VT-002, v.v.)
    fieldName: selectedFieldData?.name,
    activity: selectedActivity.value,
    data: formData.value,
    timestamp: new Date().toISOString()
  });
  alert('Hoạt động đã được lưu!');
};

/**
 * Xóa hình ảnh khỏi form
 * @param {number} index - Vị trí ảnh cần xóa
 */
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
              'long', day: 'numeric'
          }) }}</span>
        </div>
      </div>

      <!-- Chọn Thửa Đất Section -->
      <section class="mb-8 bg-white rounded-2xl shadow-sm border border-[#D7CCC8]/20 p-6">
        <h3 class="flex items-center gap-2 mb-4 text-lg font-bold text-gray-800">
          <span class="material-symbols-outlined text-[#2E7D32]">agriculture</span>
          Chọn thửa đất canh tác
        </h3>
        <!-- Danh sách thửa đất -->
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          <!-- Loop qua từng thửa đất -->
          <button v-for="field in fields" :key="field.id" @click="selectField(field.id)" :class="[
            'p-4 rounded-xl border-2 text-left transition-all duration-300',
            selectedField === field.id
              ? 'border-[#2E7D32] bg-[#E8F5E9] shadow-md'
              : 'border-[#D7CCC8]/30 bg-white hover:border-[#D7CCC8] hover:shadow-sm'
          ]">
            <!-- Mã số vùng trồng (đồng bộ với bản đồ WebGIS) -->
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-bold text-gray-800">{{ field.name }}</h4>
              <span class="px-2 py-1 text-xs font-bold rounded-lg bg-[#FFF3E0] text-[#E65100]">
                {{ field.ma }}
              </span>
            </div>
            <!-- Thông tin thửa đất -->
            <div class="space-y-1 text-sm">
              <p class="text-gray-600">
                <span class="font-semibold">Loại cây:</span>
                {{ field.crop }}
              </p>
              <p class="text-gray-600">
                <span class="font-semibold">Diện tích:</span>
                {{ field.area }} ha
              </p>
              <p :class="['text-xs font-bold', selectedField === field.id ? 'text-[#2E7D32]' : 'text-gray-500']">
                {{ field.status }}
              </p>
            </div>
          </button>
        </div>
      </section>

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
          <DiaryActivityForm 
            :selectedActivity="selectedActivity" 
            :activities="activities" 
            :formData="formData"
            :selectedField="fields.find(f => f.id === selectedField)"
            @update:formData="(newData) => formData = newData" 
            @save="handleSave" 
            @cancel="handleCancel"
            @removeImage="removeImage" 
          />
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
