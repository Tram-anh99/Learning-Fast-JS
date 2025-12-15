<script setup>
/**
 * ========== VIEW: DiaryPage.vue ==========
 * Mục đích: Trang nhật ký canh tác - Người dùng ghi lại các hoạt động nông sản hàng ngày
 * 
 * Kiến trúc:
 *   - Thành phần con:
 *     • DiaryActivitySelector.vue - Grid chọn loại hoạt động (Gieo, Bón, Phun, Tưới, Làm cỏ, Thu hoạch)
 *     • DiaryActivityForm.vue - Form nhập chi tiết hoạt động (loại, thời gian, vật tư, liều lượng, ảnh)
 *     • DiaryActivityHistory.vue - Lịch sử hoạt động gần đây
 *   - Styling: src/assets/styles/tailwind.css (Tailwind utilities toàn cục)
 * 
 * Tính năng:
 *   - Chọn hoạt động từ 6 loại khác nhau
 *   - Chọn thửa đất để ghi nhật ký (mã số VT-001, VT-002, VT-003 đồng bộ với WebGIS)
 *   - Form động thay đổi tùy theo hoạt động chọn (loại, vật tư, thị trường xuất khẩu)
 *   - Upload hình ảnh thực tế
 *   - Xem lịch sử hoạt động đã thực hiện
 *   - Lưu nhật ký và xem chi tiết
 */

// ========== IMPORTS ==========
// ref: Vue 3 Composition API hook để tạo reactive state
import { ref } from 'vue';

// Thành phần: Lưới chọn hoạt động (6 nút bấm với icon)
import DiaryActivitySelector from '../components/DiaryActivitySelector.vue';

// Thành phần: Form nhập liệu hoạt động với input động
import DiaryActivityForm from '../components/DiaryActivityForm.vue';

// Thành phần: Danh sách hoạt động gần đây dạng timeline
import DiaryActivityHistory from '../components/DiaryActivityHistory.vue';

// ========== STATE ==========
/**
 * selectedActivity: Hoạt động canh tác hiện tại được chọn
 * Type: Ref<String>
 * Values: 'gieo' | 'compost' | 'pest' | 'water' | 'weeding' | 'harvest'
 * Default: 'compost' (Bón phân)
 * Usage: Xác định loại form được hiển thị và các tùy chọn input
 */
const selectedActivity = ref('compost');

/**
 * showForm: Điều khiển hiển thị/ẩn form nhập liệu
 * Type: Ref<Boolean>
 * Default: true (form luôn hiển thị)
 * Usage: Có thể ẩn form khi xem chi tiết hoặc trên mobile
 */
const showForm = ref(true);

/**
 * selectedField: Thửa đất được chọn để ghi nhật ký
 * Type: Ref<String>
 * Default: 'field-001' (thửa đất đầu tiên)
 * Usage: Xác định thửa đất nào sẽ được ghi nhân hoạt động
 */
const selectedField = ref('field-001');

// ========== DATA ==========
/**
 * activities: Danh sách các loại hoạt động canh tác có sẵn
 * Structure: Array<{id: string, name: string, icon: string, color: string}>
 * 
 * Thông tin chi tiết:
 *   - id: Định danh duy nhất (dùng làm selectedActivity value)
 *   - name: Tên tiếng Việt hiển thị
 *   - icon: Material Symbols icon name (e.g., 'grain', 'compost', 'water_drop')
 *   - color: Tailwind color class cho icon background
 * 
 * Ứng dụng:
 *   - Render nút chọn hoạt động trong DiaryActivitySelector
 *   - Cung cấp icon & tên cho form header
 *   - Xác định loại dữ liệu cho vật tư và liều lượng
 */
const activities = ref([
  // Gieo hạt: Gieo trực tiếp hoặc gieo ươm
  { id: 'gieo', name: 'Gieo hạt', icon: 'grain', color: 'orange' },
  // Bón phân: Bón phân qua 3 giai đoạn
  { id: 'compost', name: 'Bón phân', icon: 'compost', color: 'green' },
  // Phun thuốc: Diệt sâu, bệnh, cỏ dại
  { id: 'pest', name: 'Phun thuốc', icon: 'pest_control', color: 'blue' },
  // Tưới nước: Tưới nhỏ giọt, gàu, máy bơm
  { id: 'water', name: 'Tưới nước', icon: 'water_drop', color: 'cyan' },
  // Làm cỏ: Làm cỏ tay, máy, hoặc thuốc
  { id: 'weeding', name: 'Làm cỏ', icon: 'grass', color: 'lime' },
  // Thu hoạch: Thu hoạch tay hoặc máy + chọn thị trường
  { id: 'harvest', name: 'Thu hoạch', icon: 'agriculture', color: 'yellow' },
]);

/**
 * fields: Danh sách thửa đất của nông dân
 * Structure: Array<{id, ma, name, area, crop, status}>
 * 
 * Thông tin chi tiết:
 *   - id: Định danh duy nhất cho state (e.g., 'field-001')
 *   - ma: Mã số vùng trồng WebGIS (VT-001, VT-002, VT-003) - PHẢI đồng bộ với HomeView!
 *   - name: Tên thửa đất tiếng Việt
 *   - area: Diện tích (hectare)
 *   - crop: Loại cây trồng
 *   - status: Tình trạng canh tác ('Đang canh tác', 'Thu hoạch', 'Nghỉ đất', v.v.)
 * 
 * Ứng dụng:
 *   - Render dropdown/selector thửa đất
 *   - Xác định vùng trồng nào nhật ký được ghi vào
 *   - Đồng bộ với bản đồ WebGIS qua mã số (ma)
 */
const fields = ref([
  // Thửa 1: Lúa ST25, 10 hectare, trạng thái Thu hoạch
  { id: 'field-001', ma: 'VT-003', name: 'Thửa 1 - Lúa ST25', area: 10, crop: 'Lúa ST25', status: 'Thu hoạch' },
  // Thửa 2: Xoài Cát Hòa Lộc, 5 hectare, đang canh tác
  { id: 'field-002', ma: 'VT-001', name: 'Thửa 2 - Xoài Cát Hòa Lộc', area: 5, crop: 'Xoài', status: 'Đang canh tác' },
  // Thửa 3: Thanh Long Ruột Đỏ, 3.2 hectare, đang canh tác
  { id: 'field-003', ma: 'VT-002', name: 'Thửa 3 - Thanh Long Ruột Đỏ', area: 3.2, crop: 'Thanh long', status: 'Đang canh tác' }
]);

/**
 * formData: Dữ liệu form nhập liệu hoạt động
 * Structure: {activityType, datetime, material, quantity, unit, market, images}
 * 
 * Thông tin chi tiết:
 *   - activityType: Loại hoạt động cụ thể (e.g., "Bón phân - Đợt 1 (Bón lót)")
 *   - datetime: Thời gian thực hiện (ISO 8601: YYYY-MM-DDTHH:mm)
 *   - material: Vật tư sử dụng (e.g., "Phân NPK 20-20-15 - Bình Điền")
 *   - quantity: Số lượng vật tư
 *   - unit: Đơn vị (kg, tấn, lít, giờ, v.v.)
 *   - market: Thị trường xuất khẩu (chỉ dùng cho hoạt động 'harvest')
 *   - images: Mảng URL hình ảnh thực tế của hoạt động
 * 
 * Ứng dụng:
 *   - Đánh dấu hoạt động (v-model trong form)
 *   - Gửi tới server khi lưu nhật ký
 *   - Hiển thị trong lịch sử hoạt động
 */
const formData = ref({
  activityType: 'Bón phân - Đợt 1 (Bón lót)',
  datetime: new Date().toISOString().slice(0, 16),
  material: 'Phân NPK 20-20-15 - Bình Điền',
  quantity: 50,
  unit: 'kg',
  market: 'Thị trường nội địa', // Thị trường xuất khẩu (chỉ dùng cho hoạt động harvest)
  images: [
    'https://lh3.googleusercontent.com/aida-public/AB6AXuC8rlpuo0MV03QhAUUkn0q05WeV_z3xb3jhAQGqasHHlbVTAAr5rYcCh2YMZD4XCTT9YGrxadEHCgpiUHs8rU_2YqK45gUWRRA8tXPCyKV322kUY4vj1f0FPzhLnlx7pr_iPd8obOnBBvzNBtwrX_x0WZy7dnP5zw14TgSU4YvWF-mApgni22x0otIfw1siEU_R0OdOHdumodtkwLidwzbuSJBXzTAvXcwwsJfF4-2U9yoMurgTkiERVM20aCFxLy2o6KfH2eD8BRk',
    'https://lh3.googleusercontent.com/aida-public/AB6AXuCW4Q3jc1mqn9VDwA5LF1tbPNG5Qed02KUvgA4IgvFx1a-1sqXhNlCmXq7RmO9pcb2cq6KB-pvkSR6oEwtoYC9cDgep8gzLmcpWUXt7ZK2UKZ0vZwtsUQY23fGvMoJG8Aa6rbkAa9YgwGbh5DWREPMIPsQi-WTazi7f1lb0g4EcKHt5n96sdtfoxnZ_10p1eGKiyUGcELNtLBAKObN-888bcFMpBbrHutQXQ36gsG4gjNErzhP-JMEvL-9r9NxrjXqI45pfTpOa9SQ'
  ]
});

/**
 * recentActivities: Lịch sử hoạt động gần đây
 * Structure: Array<{id, icon, title, description, time, timeDetail, bgColor, iconColor}>
 * 
 * Thông tin chi tiết:
 *   - id: Định danh duy nhất
 *   - icon: Material Symbols icon name
 *   - title: Tên hoạt động
 *   - description: Chi tiết (vật tư, liều lượng, v.v.)
 *   - time: Thời gian tương đối ("Hôm nay", "Hôm qua", v.v.)
 *   - timeDetail: Thời gian chính xác (HH:MM)
 *   - bgColor: Tailwind background color class
 *   - iconColor: Tailwind text color class
 * 
 * Ứng dụng:
 *   - Render danh sách hoạt động trong DiaryActivityHistory
 *   - Giúp người dùng tra cứu các hoạt động vừa thực hiện
 */
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

// ========== METHODS ==========
/**
 * selectActivity: Xử lý khi người dùng chọn hoạt động
 * Parameters:
 *   @param {string} activityId - ID của hoạt động được chọn
 * Behavior:
 *   1. Cập nhật selectedActivity ref
 *   2. Form tự động thay đổi loại/vật tư phù hợp (xử lý trong DiaryActivityForm)
 */
const selectActivity = (activityId) => {
  selectedActivity.value = activityId;
};

/**
 * selectField: Xử lý khi người dùng chọn thửa đất
 * Parameters:
 *   @param {string} fieldId - ID của thửa đất được chọn
 * Behavior:
 *   1. Cập nhật selectedField ref
 *   2. Hoạt động nhập sẽ được ghi vào thửa đất này
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
    market: 'Thị trường nội địa',
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
  background: #24504b;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(36, 80, 75, 0.8);
}
</style>

<template>
  <div class="font-sans antialiased h-screen flex flex-col" style="background-color: #fbfced;">
    <!-- Main Content -->
    <main class="flex-1 w-full px-4 py-6 pb-[80px] mx-auto sm:px-6 lg:px-8 max-w-7xl overflow-y-auto scrollbar-custom">
      <!-- Header Section -->
      <div class="flex flex-col justify-between gap-4 mb-8 md:flex-row md:items-center">
        <div>
          <h2 class="text-3xl font-black mb-1" style="color: #24504b;">Hôm nay bác làm gì?</h2>
          <p class="text-lg" style="color: rgba(36, 80, 75, 0.7);">Ghi lại hoạt động canh tác nhanh chóng và dễ dàng.
          </p>
        </div>
        <div class="flex items-center gap-2 bg-white px-4 py-2 rounded-2xl shadow-sm">
          <span class="material-symbols-outlined" style="color: #24504b;">calendar_today</span>
          <span class="font-medium" style="color: #24504b;">{{ new Date().toLocaleDateString('vi-VN', {
            year: 'numeric', month:
              'long', day: 'numeric'
          }) }}</span>
        </div>
      </div>

      <!-- Chọn Thửa Đất Section -->
      <section class="mb-8 bg-white rounded-2xl shadow-sm p-6">
        <h3 class="flex items-center gap-2 mb-4 text-lg font-bold" style="color: #24504b;">
          <span class="material-symbols-outlined" style="color: #24504b;">agriculture</span>
          Chọn thửa đất canh tác
        </h3>
        <!-- Danh sách thửa đất -->
        <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          <!-- Loop qua từng thửa đất -->
          <button v-for="field in fields" :key="field.id" @click="selectField(field.id)" :class="[
            'p-4 rounded-lg border-2 text-left transition-all duration-300',
            selectedField === field.id
              ? 'shadow-md'
              : 'bg-white hover:shadow-sm'
          ]" :style="{
            borderColor: selectedField === field.id ? '#24504b' : 'rgba(36, 80, 75, 0.2)',
            backgroundColor: selectedField === field.id ? 'rgba(36, 80, 75, 0.1)' : 'white'
          }">
            <!-- Mã số vùng trồng (đồng bộ với bản đồ WebGIS) -->
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-bold" style="color: #24504b;">{{ field.name }}</h4>
              <span class="px-2 py-1 text-xs font-bold rounded-lg"
                style="background-color: rgba(36, 80, 75, 0.2); color: #24504b;">
                {{ field.ma }}
              </span>
            </div>
            <!-- Thông tin thửa đất -->
            <div class="space-y-1 text-sm">
              <p style="color: rgba(36, 80, 75, 0.7);">
                <span class="font-semibold">Loại cây:</span>
                {{ field.crop }}
              </p>
              <p style="color: rgba(36, 80, 75, 0.7);">
                <span class="font-semibold">Diện tích:</span>
                {{ field.area }} ha
              </p>
              <p class="text-xs font-bold"
                :style="{ color: selectedField === field.id ? '#24504b' : 'rgba(36, 80, 75, 0.5)' }">
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
          <DiaryActivityForm :selectedActivity="selectedActivity" :activities="activities" :formData="formData"
            :selectedField="fields.find(f => f.id === selectedField)" @update:formData="(newData) => formData = newData"
            @save="handleSave" @cancel="handleCancel" @removeImage="removeImage" />
        </div>
      </div>

      <!-- Footer -->
      <footer class="mt-8 pt-6 pb-4 border-t border-gray-200 text-center text-gray-600 text-sm">
        <p>&copy; 2024 Hệ thống Quản lý Nông nghiệp. Phát triển bởi <span class="font-semibold text-gray-800">Dev
            Team</span></p>
        <p class="mt-2 text-xs text-gray-500">Cập nhật lần cuối: <span class="font-medium">{{ new
          Date().toLocaleDateString('vi-VN') }}</span></p>
      </footer>
    </main>
  </div>
</template>
