<script setup>
/**
 * ========== COMPONENT: DiaryActivityForm.vue ==========
 * Purpose: Form nhập liệu chi tiết hoạt động canh tác (Seeding, Fertilizing, Spraying, Watering, Weeding, Harvesting)
 * 
 * Architecture:
 *   - Parent: DiaryPage passes selectedActivity, activities, formData
 *   - Child: None
 *   - Communication: v-model-like pattern via update:formData emit
 * 
 * Features:
 *   - Dynamic form inputs based on selected activity type
 *   - Activity type selector with predefined options per activity
 *   - Material/resource selector with auto-populated options
 *   - Quantity input with unit display
 *   - Market selection for harvest activity (conditional)
 *   - Image upload & management (add/remove)
 *   - Auto-reset form when activity changes
 *   - User tips section with activity-specific guidance
 * 
 * Props:
 *   - selectedActivity (String): Activity ID (gieo, compost, pest, water, weeding, harvest)
 *   - activities (Array): List of all activities with name, icon properties
 *   - formData (Object): Current form state {activityType, datetime, material, quantity, unit, market, images}
 *   - selectedField (Object): Selected field metadata {id, ma, name, crop, area, status}
 * 
 * Emits:
 *   - update:formData (Object): Emit when form data changes (for v-model pattern)
 *   - save (): Save the activity entry
 *   - cancel (): Discard changes and close form
 *   - removeImage (Number): Delete image at specified index
 */

// ========== IMPORTS ==========
// ref, watch, computed: Vue 3 Composition API for reactivity management
import { ref, watch, computed } from 'vue';

// ========== PROPS ==========
// Define props with types and descriptions
const props = defineProps({
  // selectedActivity: Current selected activity ID (acts as form context key)
  selectedActivity: String,
  
  // activities: Array of available activities [{id, name, icon, color}] used in header
  activities: Array,
  
  // formData: Current form state object with activity details
  formData: Object,
  
  // selectedField: Metadata about selected thửa đất (field/plot)
  selectedField: Object
});

// ========== EMITS ==========
// Define custom events emitted to parent component
const emit = defineEmits([
  // update:formData: Emit new formData object when any input changes (synchronization pattern)
  'update:formData',
  // save: Emit when save button clicked to persist the activity
  'save',
  // cancel: Emit when cancel button clicked to discard changes
  'cancel',
  // removeImage: Emit with index when delete image button clicked
  'removeImage'
]);

// ========== DATA ==========
/**
 * activityDetails: Mapping of activity IDs to their specific form options
 * Structure:
 *   - key: activity ID (gieo, compost, pest, water, weeding, harvest)
 *   - value: {name: display name, types: [activity subtypes], materials: [available inputs], markets?: [export markets]}
 * 
 * Purpose: Dynamically populate select options based on selected activity
 * Example: When selectedActivity='harvest', form shows market selection + harvest-specific materials
 */
const activityDetails = {
  // Gieo (Seeding): Sowing seeds - direct or nursery methods
  gieo: {
    name: 'Gieo hạt',
    // types: Different seeding methods
    types: ['Gieo trực tiếp', 'Gieo ươm'],
    // materials: Available seed types
    materials: ['Hạt lúa F1', 'Hạt lúa thường', 'Hạt giống rau cải', 'Hạt giống dưa leo']
  },
  
  // Compost (Bón phân): Fertilizer application - multiple stages
  compost: {
    name: 'Bón phân',
    // types: Fertilizer application stages (basal, tillering, flowering)
    types: ['Bón phân - Đợt 1 (Bón lót)', 'Bón phân - Đợt 2 (Thúc chồi)', 'Bón phân - Đợt 3 (Thúc trái)'],
    // materials: Available fertilizer brands/types
    materials: ['Phân NPK 20-20-15 - Bình Điền', 'Phân Urê (Đạm Phú Mỹ)', 'Phân Kali', 'Phân vi lượng']
  },
  
  // Pest (Phun thuốc): Pest & disease control - insecticide, fungicide, herbicide
  pest: {
    name: 'Phun thuốc',
    // types: Pest control categories
    types: ['Phun thuốc sâu', 'Phun thuốc bệnh', 'Phun thuốc cỏ'],
    // materials: Available chemical products
    materials: ['Thuốc sâu Imidacloprid', 'Thuốc bệnh Mancozeb', 'Thuốc cỏ Paraquat', 'Thuốc sinh học']
  },
  
  // Water (Tưới nước): Irrigation methods
  water: {
    name: 'Tưới nước',
    // types: Irrigation techniques
    types: ['Tưới nhỏ giọt', 'Tưới gàu', 'Tưới máy bơm'],
    // materials: Water source types
    materials: ['Nước giếu', 'Nước kênh', 'Nước mưa', 'Nước giếu khoan']
  },
  
  // Weeding (Làm cỏ): Weed management methods
  weeding: {
    name: 'Làm cỏ',
    // types: Weeding techniques
    types: ['Làm cỏ bằng tay', 'Làm cỏ bằng máy', 'Phun thuốc diệt cỏ'],
    // materials: Tools and herbicides
    materials: ['Công cụ làm cỏ', 'Máy cắt cỏ', 'Thuốc diệt cỏ']
  },
  
  // Harvest (Thu hoạch): Harvesting + market selection
  harvest: {
    name: 'Thu hoạch',
    // types: Harvesting methods (manual vs mechanical)
    types: ['Thu hoạch bằng tay', 'Thu hoạch bằng máy'],
    // materials: Harvesting equipment
    materials: ['Liềm gặt', 'Máy gặt đập', 'Bao dứa', 'Rổ đựng'],
    // markets: Export markets (unique to harvest - added in conditional rendering)
    markets: ['Thị trường nội địa', 'Xuất khẩu EU', 'Xuất khẩu Nhật Bản', 'Xuất khẩu Trung Quốc', 'Xuất khẩu Mỹ', 'Xuất khẩu ASEAN']
  }
};

// ========== COMPUTED ==========
/**
 * currentActivityData: Computed property that returns form options for current activity
 * Dependencies: props.selectedActivity
 * Logic:
 *   1. Look up selectedActivity ID in activityDetails object
 *   2. Return corresponding types, materials, and optional markets array
 *   3. Default to 'compost' if activity not found (fallback)
 * Usage: Populates select options dynamically when activity changes
 */
const currentActivityData = computed(() => {
  // Return activity details or fallback to compost activity
  return activityDetails[props.selectedActivity] || activityDetails.compost;
});

// ========== LIFECYCLE HOOKS ==========
/**
 * watch: selectedActivity
 * Purpose: Auto-reset form when user switches to different activity
 * Behavior:
 *   1. Listen for selectedActivity prop changes
 *   2. Get new activity's default type and material
 *   3. Emit update:formData with new defaults
 *   4. Ensures form fields match selected activity context
 */
watch(() => props.selectedActivity, (newActivity) => {
  // Get details for new activity
  const details = activityDetails[newActivity];
  // Emit updated formData with new activity's defaults
  // Keeps quantity, unit, datetime but resets activityType and material
  emit('update:formData', {
    ...props.formData,
    // Set default activity type (first option from types array)
    activityType: details.types[0],
    // Set default material (first option from materials array)
    material: details.materials[0]
  });
});
</script>

<template>
  <!-- Form nhập liệu hoạt động -->
  <div class="sticky top-24">
    <!-- Card form chính -->
    <div class="bg-white rounded-lg shadow-xl border border-[#2E7D32]/10 overflow-hidden relative">
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
              {{activities.find(a => a.id === selectedActivity)?.name || 'Bón phân'}}
            </h3>
          </div>
          <!-- Icon hoạt động lớn ở bên phải -->
          <div class="bg-[#E8F5E9] p-2 rounded-full">
            <span class="material-symbols-outlined text-[#2E7D32] text-3xl">{{activities.find(a => a.id ===
              selectedActivity)?.icon || 'compost'}}</span>
          </div>
        </div>

        <!-- Form inputs -->
        <form class="space-y-6" @submit.prevent>
          <!-- Phần 1: Loại hoạt động và thời gian -->
          <div class="space-y-4">
            <!-- Select loại hoạt động (phù hợp với hoạt động được chọn) -->
            <div>
              <label class="block text-sm font-bold text-[#5D4037] mb-2">Loại hoạt động</label>
              <select :value="formData.activityType"
                @input="$emit('update:formData', { ...formData, activityType: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-[#FAFAF5]/50 px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm transition-colors cursor-pointer font-medium">
                <!-- Động: Loop qua các loại hoạt động của activity được chọn -->
                <option v-for="type in currentActivityData.types" :key="type" :value="type">
                  {{ type }}
                </option>
              </select>
            </div>

            <!-- Input thời gian thực hiện hoạt động -->
            <div>
              <label class="block text-sm font-bold text-[#5D4037] mb-2">Thời gian thực hiện</label>
              <input :value="formData.datetime"
                @input="$emit('update:formData', { ...formData, datetime: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-[#FAFAF5]/50 px-4 py-2 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm transition-colors cursor-pointer font-medium"
                type="datetime-local" />
            </div>
          </div>

          <!-- Phần 2: Vật tư và liều lượng (nền xanh nhạt) -->
          <div class="bg-[#E8F5E9]/30 p-4 rounded-lg space-y-4 border border-[#2E7D32]/10">
            <!-- Select vật tư sử dụng (phù hợp với hoạt động được chọn) -->
            <div>
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">inventory_2</span>
                Vật tư sử dụng
              </label>
              <select :value="formData.material"
                @input="$emit('update:formData', { ...formData, material: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-white px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm">
                <!-- Động: Loop qua các vật tư của activity được chọn -->
                <option v-for="material in currentActivityData.materials" :key="material" :value="material">
                  {{ material }}
                </option>
              </select>
            </div>

            <!-- Input liều lượng / số lượng với đơn vị -->
            <div>
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">scale</span>
                Liều lượng / Số lượng
              </label>
              <div class="flex rounded-lg shadow-sm">
                <!-- Input số liệu -->
                <input :value="formData.quantity"
                  @input="$emit('update:formData', { ...formData, quantity: $event.target.value })"
                  class="block w-full h-12 rounded-l-lg border border-[#D7CCC8] border-r-0 bg-white px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm"
                  type="number" />
                <!-- Đơn vị (kg, tấn, lít, etc) -->
                <span
                  class="inline-flex items-center h-12 rounded-r-lg border border-l-0 border-[#D7CCC8] bg-white px-4 text-gray-500 font-bold sm:text-sm">
                  {{ formData.unit }}
                </span>
              </div>
            </div>

            <!-- Mục chọn thị trường xuất khẩu (chỉ hiển thị khi hoạt động là "harvest") -->
            <div v-if="selectedActivity === 'harvest'">
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">public</span>
                Thị trường xuất khẩu
              </label>
              <select :value="formData.market || 'Thị trường nội địa'"
                @input="$emit('update:formData', { ...formData, market: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-white px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm cursor-pointer font-medium">
                <option v-for="market in currentActivityData.markets" :key="market" :value="market">
                  {{ market }}
                </option>
              </select>
            </div>
          </div>

          <!-- Phần 3: Hình ảnh thực tế -->
          <div>
            <label class="block text-sm font-bold text-[#5D4037] mb-2">Hình ảnh thực tế</label>
            <div class="grid grid-cols-4 gap-2">
              <!-- Nút thêm ảnh -->
              <button
                class="aspect-square flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-[#2E7D32]/40 bg-[#E8F5E9]/20 text-[#2E7D32] hover:bg-[#E8F5E9]/50 transition-colors"
                type="button">
                <span class="material-symbols-outlined text-2xl mb-1">add_a_photo</span>
                <span class="text-[10px] font-bold">Thêm</span>
              </button>

              <!-- Hiển thị ảnh đã thêm -->
              <div v-for="(image, index) in formData.images" :key="index" class="aspect-square relative group">
                <img :alt="`Preview ${index}`" class="w-full h-full object-cover rounded-lg shadow-sm" :src="image" />
                <!-- Nút xóa ảnh (hiện khi hover) -->
                <button @click="$emit('removeImage', index)"
                  class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 shadow-md opacity-0 group-hover:opacity-100 transition-opacity"
                  type="button">
                  <span class="material-symbols-outlined text-[14px] block">close</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Phần 4: Nút hành động (Hủy / Lưu) -->
          <div class="pt-2 flex items-center gap-3">
            <!-- Nút Hủy -->
            <button @click="$emit('cancel')"
              class="flex-1 py-3.5 px-6 rounded-lg border border-[#D7CCC8] text-[#8D6E63] font-bold hover:bg-[#FAFAF5] transition-colors"
              type="button">
              Hủy
            </button>
            <!-- Nút Lưu hoạt động -->
            <button @click="$emit('save')"
              class="flex-[2] py-3.5 px-6 rounded-lg bg-[#2E7D32] text-white font-bold shadow-lg shadow-[#2E7D32]/30 hover:bg-green-800 hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2"
              type="button">
              <span class="material-symbols-outlined">save</span>
              Lưu hoạt động
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Mẹo cho người dùng (nền nâu) -->
    <div class="mt-6 bg-[#8D6E63] text-white p-4 rounded-lg flex items-start gap-3 shadow-lg">
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
