<script setup>
/**
 * ========== COMPONENT: HomeDetailView.vue ==========
 * Purpose: Hiển thị chi tiết vùng trồng với timeline nhật ký canh tác hiện đại
 * Related Files:
 *   - src/composables/useHome.js (Logic & state)
 *   - src/views/HomeView.vue (Main view)
 *   - src/assets/styles/tailwind.css (Global utilities)
 */

import { ref } from 'vue'; // Vue ref hook

// ========== PROPS & EMITS ==========
// Props nhận từ parent component
defineProps({
      vung: {
            type: Object, // Object chứa thông tin vùng trồng
            required: true
      }
});

// Emits gửi lên parent component
defineEmits(['back', 'openQR']); // 'back': quay lại danh sách, 'openQR': mở modal QR

// ========== STATE ==========
// State: Hoạt động được chọn hiện tại
const selectedActivity = ref('bon_phan');
// State: Form data cho nhập hoạt động
const formData = ref({
      activity: 'bon_phan',
      datetime: new Date().toISOString().slice(0, 16),
      material: '',
      quantity: '',
      images: []
});

// ========== ACTIVITY TYPES ==========
// Danh sách các loại hoạt động canh tác
const activities = [
      { id: 'gieo_hat', name: 'Gieo hạt', icon: 'grain', color: 'orange' },
      { id: 'bon_phan', name: 'Bón phân', icon: 'compost', color: 'green', selected: true },
      { id: 'phun_thuoc', name: 'Phun thuốc', icon: 'pest_control', color: 'blue' },
      { id: 'tuoi_nuoc', name: 'Tưới nước', icon: 'water_drop', color: 'cyan' },
      { id: 'lam_co', name: 'Làm cỏ', icon: 'grass', color: 'lime' },
      { id: 'thu_hoach', name: 'Thu hoạch', icon: 'agriculture', color: 'yellow' }
];

// ========== METHODS ==========
/**
 * Handler: Chọn loại hoạt động
 * @param {string} activityId - ID của hoạt động
 */
const selectActivity = (activityId) => {
      selectedActivity.value = activityId;
      formData.value.activity = activityId;
};

/**
 * Handler: Submit form nhập hoạt động
 */
const submitActivity = () => {
      // TODO: Gửi dữ liệu lên server/API
      console.log('Form data:', formData.value);
      // Reset form
      formData.value = {
            activity: selectedActivity.value,
            datetime: new Date().toISOString().slice(0, 16),
            material: '',
            quantity: '',
            images: []
      };
};
</script>

<template>
      <!-- Container chính: flex column, full height -->
      <div class="flex flex-col h-full">

            <!-- Cover image header: hiển thị ảnh nền của vùng trồng -->
            <div class="relative flex items-end h-56 bg-center bg-cover"
                  :style="{ backgroundImage: `url(${vung.anh})` }">
                  <!-- Gradient overlay: tối dần từ dưới lên trên (từ đen sang trong suốt) -->
                  <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>

                  <!-- Text content: tên và chứng nhận -->
                  <div class="relative z-10 w-full p-4 text-white">
                        <!-- Tên vùng trồng -->
                        <h2 class="text-2xl font-bold text-shadow">{{ vung.ten }}</h2>

                        <!-- Badge chứng nhận (VietGAP, GlobalGAP, etc) -->
                        <span
                              class="inline-block px-3 py-1 mt-2 text-xs font-bold text-gray-800 bg-yellow-400 rounded-md">
                              <!-- Icon sao -->
                              <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3 h-3 mr-1" viewBox="0 0 20 20"
                                    fill="currentColor">
                                    <path
                                          d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                              </svg>
                              <!-- Tên chứng nhận -->
                              {{ vung.chungNhan }}
                        </span>
                  </div>
            </div>

            <!-- Scrollable content area: nội dung chính có thể cuộn dọc -->
            <div class="flex-grow p-4 space-y-4 overflow-y-auto pb-32">

                  <!-- Info grid: 2 cột hiển thị mã số và diện tích -->
                  <div class="grid grid-cols-2 gap-2">
                        <!-- Cột 1: Mã số vùng trồng -->
                        <div class="p-3 border border-gray-200 rounded-lg bg-gray-50">
                              <label class="block mb-1 text-xs text-gray-600">Mã số</label>
                              <strong class="text-gray-800">{{ vung.ma }}</strong>
                        </div>

                        <!-- Cột 2: Diện tích vùng trồng -->
                        <div class="p-3 border border-gray-200 rounded-lg bg-gray-50">
                              <label class="block mb-1 text-xs text-gray-600">Diện tích</label>
                              <strong class="text-gray-800">{{ vung.dienTich }}</strong>
                        </div>
                  </div>

                  <!-- Nhóm thông tin chủ thể: Thông tin hộ canh tác / hợp tác xã -->
                  <div class="p-4 border-l-4 border-green-500 bg-green-50 rounded-lg">
                        <!-- Tiêu đề nhóm -->
                        <h4 class="mb-3 text-sm font-bold text-gray-800 flex items-center gap-2">
                              <!-- Icon nhà -->
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-green-600" fill="currentColor"
                                    viewBox="0 0 20 20">
                                    <path
                                          d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                              </svg>
                              Chủ thể canh tác
                        </h4>

                        <!-- Danh sách thông tin chủ thể -->
                        <div class="space-y-2 text-sm">
                              <!-- Tên hộ -->
                              <div class="flex justify-between">
                                    <span class="text-gray-600">Hộ/Công ty:</span>
                                    <strong class="text-gray-800">{{ vung.hoTen || 'Hộ nông dân' }}</strong>
                              </div>
                              <!-- Địa chỉ -->
                              <div class="flex justify-between">
                                    <span class="text-gray-600">Địa chỉ:</span>
                                    <strong class="text-gray-800">{{ vung.diaChi || 'Khu vực Đồng bằng Sông Cửu Long'
                                          }}</strong>
                              </div>
                              <!-- Hợp tác xã -->
                              <div class="flex justify-between">
                                    <span class="text-gray-600">HTX trực thuộc:</span>
                                    <strong class="text-gray-800">{{ vung.hopTacXa || 'HTX Nông sản an toàn' }}</strong>
                              </div>
                              <!-- Số điện thoại -->
                              <div class="flex justify-between">
                                    <span class="text-gray-600">Liên hệ:</span>
                                    <strong class="text-gray-800">{{ vung.dienThoai || '(028) 1234 5678' }}</strong>
                              </div>
                        </div>
                  </div>

                  <!-- ========== NHẬT KÝ CANH TÁC (MODERN TIMELINE) ========== -->

                  <!-- Phần 1: Chọn hoạt động -->
                  <section>
                        <!-- Tiêu đề -->
                        <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2 mb-4">
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-600" fill="currentColor"
                                   viewBox="0 0 20 20">
                                   <path d="M3 4a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V4z" />
                              </svg>
                              Hôm nay bác làm gì?
                        </h3>

                        <!-- Grid hoạt động -->
                        <div class="grid grid-cols-3 gap-3">
                              <button
                                   v-for="activity in activities"
                                   :key="activity.id"
                                   @click="selectActivity(activity.id)"
                                   :class="[
                                        'group relative flex flex-col items-center justify-center p-4 rounded-2xl transition-all duration-300',
                                        selectedActivity === activity.id
                                             ? `bg-green-600 text-white shadow-lg scale-105`
                                             : 'bg-white border border-gray-200 hover:border-green-300 hover:shadow-md'
                                   ]">
                                   <!-- Icon hoạt động -->
                                   <div :class="[
                                        'h-10 w-10 rounded-lg flex items-center justify-center mb-2 transition-transform group-hover:scale-110',
                                        selectedActivity === activity.id
                                             ? 'bg-white/20'
                                             : `bg-${activity.color}-100 text-${activity.color}-600`
                                   ]">
                                        <span class="material-symbols-outlined text-2xl">{{ activity.icon }}</span>
                                   </div>
                                   <!-- Tên hoạt động -->
                                   <span class="text-xs font-bold text-center leading-tight">{{ activity.name }}</span>
                              </button>
                        </div>
                  </section>

                  <!-- Phần 2: Form nhập hoạt động -->
                  <section class="bg-green-50 p-4 rounded-2xl border border-green-200">
                        <!-- Tiêu đề form -->
                        <div class="flex items-center justify-between mb-4">
                              <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-600"
                                         fill="currentColor" viewBox="0 0 20 20">
                                         <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM16.243 15.657a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM10 18a1 1 0 011-1h1a1 1 0 110 2h-1a1 1 0 01-1-1zM5.757 16.243a1 1 0 00-1.414 1.414l.707.707a1 1 0 001.414-1.414l-.707-.707zM4 10a1 1 0 01-1-1V8a1 1 0 112 0v1a1 1 0 01-1 1zM4.343 4.343a1 1 0 00-1.414 1.414l.707.707a1 1 0 001.414-1.414L4.343 4.343z" />
                                    </svg>
                                    Chi tiết hoạt động
                              </h3>
                        </div>

                        <!-- Form fields -->
                        <form @submit.prevent="submitActivity" class="space-y-4">
                              <!-- Thời gian -->
                              <div>
                                    <label class="block text-xs font-bold text-gray-700 mb-2">Thời gian thực hiện</label>
                                    <input
                                         v-model="formData.datetime"
                                         type="datetime-local"
                                         class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-green-600 focus:border-transparent" />
                              </div>

                              <!-- Vật tư sử dụng -->
                              <div class="bg-white p-3 rounded-lg space-y-3">
                                    <label class="block text-xs font-bold text-green-700 flex items-center gap-1">
                                         <span class="material-symbols-outlined text-sm">inventory_2</span>
                                         Vật tư sử dụng
                                    </label>
                                    <input
                                         v-model="formData.material"
                                         type="text"
                                         placeholder="Phân NPK 20-20-15, Phân Urê, v.v..."
                                         class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-green-600 focus:border-transparent" />

                                    <!-- Liều lượng -->
                                    <div class="flex gap-2">
                                         <input
                                              v-model="formData.quantity"
                                              type="number"
                                              placeholder="Số lượng"
                                              class="flex-1 px-3 py-2 border border-gray-300 rounded-l-lg text-sm focus:ring-2 focus:ring-green-600" />
                                         <select class="px-3 py-2 border border-l-0 border-gray-300 rounded-r-lg text-sm bg-white focus:ring-2 focus:ring-green-600">
                                              <option>kg</option>
                                              <option>lít</option>
                                              <option>chai</option>
                                              <option>túi</option>
                                         </select>
                                    </div>
                              </div>

                              <!-- Hình ảnh -->
                              <div>
                                    <label class="block text-xs font-bold text-gray-700 mb-2">Hình ảnh thực tế</label>
                                    <div class="grid grid-cols-3 gap-2">
                                         <button
                                              type="button"
                                              class="aspect-square flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-green-400 bg-green-50 text-green-600 hover:bg-green-100 transition-colors">
                                              <span class="material-symbols-outlined text-2xl">add_a_photo</span>
                                              <span class="text-[10px] font-bold mt-1">Thêm</span>
                                         </button>
                                    </div>
                              </div>

                              <!-- Buttons -->
                              <div class="flex gap-3 pt-2">
                                    <button
                                         type="reset"
                                         class="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-gray-700 font-bold hover:bg-gray-50 transition-colors">
                                         Hủy
                                    </button>
                                    <button
                                         type="submit"
                                         class="flex-1 py-2 px-4 rounded-lg bg-green-600 text-white font-bold shadow-lg hover:bg-green-700 transition-colors flex items-center justify-center gap-2">
                                         <span class="material-symbols-outlined text-sm">save</span>
                                         Lưu
                                    </button>
                              </div>
                        </form>

                        <!-- Mẹo -->
                        <div class="mt-4 bg-amber-100 text-amber-900 p-3 rounded-lg flex items-start gap-2 border border-amber-200">
                              <span class="material-symbols-outlined text-lg flex-shrink-0">lightbulb</span>
                              <div class="text-xs">
                                   <p class="font-bold mb-1">Mẹo cho bác:</p>
                                   <p>Bón phân vào sáng sớm hoặc chiều mát để cây hấp thụ tốt nhất.</p>
                              </div>
                        </div>
                  </section>

                  <!-- Phần 3: Hoạt động gần đây -->
                  <section>
                        <!-- Tiêu đề -->
                        <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2 mb-4">
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-green-600" fill="currentColor"
                                   viewBox="0 0 20 20">
                                   <path fill-rule="evenodd"
                                        d="M5 2a1 1 0 011 1v1h1a1 1 0 000-2H6V3a1 1 0 01-1 1V2zm0 4a2 2 0 012-2h6a2 2 0 012 2v6a2 2 0 01-2 2H7a2 2 0 01-2-2V6zm2-1h6v6H7V6z"
                                        clip-rule="evenodd" />
                              </svg>
                              Hoạt động gần đây
                        </h3>

                        <!-- Danh sách hoạt động -->
                        <div class="space-y-3">
                              <div v-for="(log, idx) in vung.nhatKy" :key="idx"
                                   class="bg-white p-4 rounded-lg border border-gray-200 hover:shadow-md transition-shadow">
                                   <!-- Icon + Tên hoạt động -->
                                   <div class="flex items-start gap-3">
                                        <!-- Icon -->
                                        <div class="h-12 w-12 rounded-full bg-green-100 flex items-center justify-center text-green-600 flex-shrink-0">
                                             <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="currentColor"
                                                  viewBox="0 0 20 20">
                                                  <path
                                                       d="M7 9a2 2 0 11-4 0 2 2 0 014 0zm6 2a1 1 0 100-2 1 1 0 000 2zM7 14a3 3 0 11-6 0 3 3 0 016 0zM15 3a1 1 0 100-2 1 1 0 000 2zm2 6a1 1 0 11-2 0 1 1 0 012 0zm-4-3a1 1 0 100-2 1 1 0 000 2z" />
                                             </svg>
                                        </div>

                                        <!-- Content -->
                                        <div class="flex-grow">
                                             <h4 class="font-bold text-gray-800">{{ log.hoatDong }}</h4>
                                             <p class="text-sm text-gray-600">{{ log.chiTiet }}</p>
                                        </div>

                                        <!-- Thời gian -->
                                        <div class="text-right text-xs">
                                             <span class="block font-bold text-gray-600">{{ log.ngay }}</span>
                                             <span class="block text-gray-400">{{ log.gio || '08:30' }}</span>
                                        </div>
                                   </div>
                              </div>
                        </div>
                  </section>

            </div>

            <!-- Action buttons: nút hành động ở cuối (sticky) -->
            <div class="sticky bottom-0 flex-shrink-0 p-4 space-y-2 border-t border-gray-200 bg-white bg-opacity-90">
                  <!-- Nút Mã QR Truy xuất: emit event 'openQR' với mã vùng -->
                  <button @click="$emit('openQR', vung.ma)"
                        class="flex items-center justify-center w-full gap-2 py-3 font-semibold text-white transition-colors bg-green-600 rounded-lg hover:bg-green-700">
                        <!-- Icon QR code -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path
                                    d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zm10-9a2 2 0 110 4 2 2 0 010-4zM2 15a1 1 0 101 2h1a1 1 0 100-2H3z" />
                        </svg>
                        Mã QR Truy xuất
                  </button>

                  <!-- Nút Quay lại: emit event 'back' để trở lại danh sách -->
                  <button @click="$emit('back')"
                        class="w-full py-2 font-semibold text-gray-800 transition-colors bg-gray-200 rounded-lg hover:bg-gray-300">
                        Quay lại
                  </button>
            </div>

      </div>
</template>
