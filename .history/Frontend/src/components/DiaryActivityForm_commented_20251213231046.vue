<script setup>
// ============================================
// COMPONENT: DiaryActivityForm
// ============================================
// Mục đích: Form nhập liệu chi tiết hoạt động canh tác
// Cho phép nhập loại hoạt động, thời gian, vật tư, liều lượng, hình ảnh
//
// Cách dùng:
// <DiaryActivityForm
//   :selectedActivity="selectedActivity"
//   :activities="activities"
//   :formData="formData"
//   @update:formData="(newData) => formData = newData"
//   @save="handleSave"
//   @cancel="handleCancel"
//   @removeImage="removeImage"
// />
// ============================================

// Props nhận dữ liệu từ component cha
defineProps({
  selectedActivity: String, // ID hoạt động được chọn
  activities: Array,        // Danh sách hoạt động để lấy tên, icon
  formData: Object          // Dữ liệu form (loại, thời gian, vật tư, liều lượng, ảnh)
});

// Emits sự kiện từ component con
defineEmits([
  'update:formData', // Cập nhật dữ liệu form
  'save',            // Lưu hoạt động
  'cancel',          // Hủy nhập liệu
  'removeImage'      // Xóa hình ảnh
]);
</script>

<template>
  <!-- Form nhập liệu hoạt động -->
  <div class="sticky top-24">
    <!-- Card form chính -->
    <div class="bg-white rounded-3xl shadow-xl border border-[#2E7D32]/10 overflow-hidden relative">
      <!-- Thanh màu xanh ở đầu form -->
      <div class="h-3 bg-[#2E7D32] w-full"></div>
      
      <!-- Nội dung form -->
      <div class="p-6 sm:p-8">
        <!-- Header form: hiển thị tên hoạt động và icon -->
        <div class="flex items-center justify-between mb-6">
          <div>
            <!-- Label "Hoạt động mới" -->
            <span class="text-xs font-bold text-[#8D6E63] uppercase tracking-wider mb-1 block">Hoạt động mới</span>
            <!-- Tên hoạt động được chọn từ danh sách activities -->
            <h3 class="text-2xl font-black text-[#2E7D32] flex items-center gap-2">
              {{ activities.find(a => a.id === selectedActivity)?.name || 'Bón phân' }}
            </h3>
          </div>
          <!-- Icon hoạt động lớn ở bên phải -->
          <div class="bg-[#E8F5E9] p-2 rounded-full">
            <span class="material-symbols-outlined text-[#2E7D32] text-3xl">{{ activities.find(a => a.id === selectedActivity)?.icon || 'compost' }}</span>
          </div>
        </div>

        <!-- Form inputs -->
        <form class="space-y-6" @submit.prevent>
          <!-- Phần 1: Loại hoạt động và thời gian -->
          <div class="space-y-4">
            <!-- Select loại hoạt động (Đợt 1, 2, 3) -->
            <div>
              <label class="block text-sm font-bold text-[#5D4037] mb-2">Loại hoạt động</label>
              <select :value="formData.activityType" @input="$emit('update:formData', { ...formData, activityType: $event.target.value })" class="block w-full rounded-xl border border-[#D7CCC8] bg-[#FAFAF5]/50 py-3 pl-4 pr-10 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm transition-colors cursor-pointer font-medium">
                <option>Bón phân - Đợt 1 (Bón lót)</option>
                <option>Bón phân - Đợt 2 (Thúc chồi)</option>
                <option>Bón phân - Đợt 3 (Thúc trái)</option>
              </select>
            </div>
            
            <!-- Input thời gian thực hiện hoạt động -->
            <div>
              <label class="block text-sm font-bold text-[#5D4037] mb-2">Thời gian thực hiện</label>
              <input :value="formData.datetime" @input="$emit('update:formData', { ...formData, datetime: $event.target.value })" class="block w-full rounded-xl border border-[#D7CCC8] bg-[#FAFAF5]/50 py-3 px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm font-medium" type="datetime-local" />
            </div>
          </div>

          <!-- Phần 2: Vật tư và liều lượng (nền xanh nhạt) -->
          <div class="bg-[#E8F5E9]/30 p-4 rounded-2xl space-y-4 border border-[#2E7D32]/10">
            <!-- Select vật tư sử dụng -->
            <div>
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">inventory_2</span>
                Vật tư sử dụng
              </label>
              <select :value="formData.material" @input="$emit('update:formData', { ...formData, material: $event.target.value })" class="block w-full rounded-xl border border-[#D7CCC8] bg-white py-3 pl-4 pr-10 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm">
                <option>Phân NPK 20-20-15 - Bình Điền</option>
                <option>Phân Urê (Đạm Phú Mỹ)</option>
                <option>Phân Kali</option>
              </select>
            </div>
            
            <!-- Input liều lượng / số lượng với đơn vị -->
            <div>
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">scale</span>
                Liều lượng / Số lượng
              </label>
              <div class="flex rounded-xl shadow-sm">
                <!-- Input số liệu -->
                <input :value="formData.quantity" @input="$emit('update:formData', { ...formData, quantity: $event.target.value })" class="block w-full rounded-l-xl border border-[#D7CCC8] border-r-0 bg-white py-3 px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm" type="number" />
                <!-- Đơn vị (kg, tấn, lít, etc) -->
                <span class="inline-flex items-center rounded-r-xl border border-l-0 border-[#D7CCC8] bg-white px-4 text-gray-500 font-bold sm:text-sm">
                  {{ formData.unit }}
                </span>
              </div>
            </div>
          </div>

          <!-- Phần 3: Hình ảnh thực tế -->
          <div>
            <label class="block text-sm font-bold text-[#5D4037] mb-2">Hình ảnh thực tế</label>
            <div class="grid grid-cols-4 gap-2">
              <!-- Nút thêm ảnh -->
              <button class="aspect-square flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-[#2E7D32]/40 bg-[#E8F5E9]/20 text-[#2E7D32] hover:bg-[#E8F5E9]/50 transition-colors" type="button">
                <span class="material-symbols-outlined text-2xl mb-1">add_a_photo</span>
                <span class="text-[10px] font-bold">Thêm</span>
              </button>
              
              <!-- Hiển thị ảnh đã thêm -->
              <div
                v-for="(image, index) in formData.images"
                :key="index"
                class="aspect-square relative group"
              >
                <img :alt="`Preview ${index}`" class="w-full h-full object-cover rounded-xl shadow-sm" :src="image" />
                <!-- Nút xóa ảnh (hiện khi hover) -->
                <button @click="$emit('removeImage', index)" class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 shadow-md opacity-0 group-hover:opacity-100 transition-opacity" type="button">
                  <span class="material-symbols-outlined text-[14px] block">close</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Phần 4: Nút hành động (Hủy / Lưu) -->
          <div class="pt-2 flex items-center gap-3">
            <!-- Nút Hủy -->
            <button @click="$emit('cancel')" class="flex-1 py-3.5 px-6 rounded-xl border border-[#D7CCC8] text-[#8D6E63] font-bold hover:bg-[#FAFAF5] transition-colors" type="button">
              Hủy
            </button>
            <!-- Nút Lưu hoạt động -->
            <button @click="$emit('save')" class="flex-[2] py-3.5 px-6 rounded-xl bg-[#2E7D32] text-white font-bold shadow-lg shadow-[#2E7D32]/30 hover:bg-green-800 hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2" type="button">
              <span class="material-symbols-outlined">save</span>
              Lưu hoạt động
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Mẹo cho người dùng (nền nâu) -->
    <div class="mt-6 bg-[#8D6E63] text-white p-4 rounded-2xl flex items-start gap-3 shadow-lg">
      <!-- Icon lightbulb -->
      <span class="material-symbols-outlined text-yellow-300">lightbulb</span>
      <div class="text-sm">
        <!-- Tiêu đề mẹo -->
        <p class="font-bold mb-1">Mẹo cho Bác Ba:</p>
        <!-- Nội dung mẹo liên quan đến hoạt động -->
        <p class="opacity-90">Nên bón phân vào sáng sớm hoặc chiều mát để cây hấp thụ tốt nhất.</p>
      </div>
    </div>
  </div>
</template>
