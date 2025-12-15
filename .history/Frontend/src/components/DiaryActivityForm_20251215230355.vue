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
  <!-- ========== MAIN CONTAINER ========== -->
  <!-- Form wrapper: sticky positioning at top so always visible while scrolling -->
  <div class="sticky top-24">

    <!-- ========== FORM CARD ========== -->
    <!-- Card container: white bg with rounded corners, shadow, subtle border -->
    <!-- Position: sticky top-24 = below header (top-0-20 for header + navigation) -->
    <div class="bg-white rounded-lg shadow-xl overflow-hidden relative" style="background-color: #fbfced;">

      <!-- Color bar: green accent line at top (h-3 = height 12px) -->
      <!-- Purpose: Visual indicator of form validity/activity type (always green #2E7D32) -->
      <div class="h-3 bg-[#2E7D32] w-full"></div>

      <!-- ========== FORM CONTENT ========== -->
      <!-- Main content wrapper: p-6 (24px) on mobile, p-8 (32px) on tablet+ (sm:) -->
      <div class="p-6 sm:p-8">

        <!-- ========== FORM HEADER ========== -->
        <!-- Header section: activity name + icon, flex between name (left) and icon (right) -->
        <!-- mb-6 = margin-bottom 24px to space from form inputs -->
        <div class="flex items-center justify-between mb-6">
          <!-- Left: Activity name info -->
          <div>
            <!-- Label: "Hoạt động mới" - small gray text above main title -->
            <!-- text-xs = very small font size, font-bold, uppercase, tracking-wider = letter spacing -->
            <!-- text-[#8D6E63] = brown color, mb-1 block = block element, 4px bottom margin -->
            <span class="text-xs font-bold text-[#8D6E63] uppercase tracking-wider mb-1 block">
              Hoạt động mới
            </span>
            <!-- Activity name: h3 = heading level 3, large size (2xl = 24px), bold black (font-black) -->
            <!-- text-[#2E7D32] = green color, flex items-center gap-2 = horizontally arranged items -->
            <!-- Find activity by selectedActivity ID, display name from activities array -->
            <h3 class="text-2xl font-black text-[#2E7D32] flex items-center gap-2">
              <!-- Dynamic: Loop through activities array, find selected one, get .name property -->
              {{activities.find(a => a.id === selectedActivity)?.name || 'Bón phân'}}
            </h3>
          </div>

          <!-- Right: Large activity icon -->
          <!-- Icon container: bg-[#E8F5E9] = light green background, p-2 = padding 8px -->
          <!-- rounded-full = circular shape (border-radius 9999px) -->
          <div class="bg-[#E8F5E9] p-2 rounded-full">
            <!-- Material Symbol icon: text-[#2E7D32] = green color, text-3xl = 30px -->
            <!-- Dynamic: Display corresponding Material Symbol icon for selected activity -->
            <span class="material-symbols-outlined text-[#2E7D32] text-3xl">
              {{activities.find(a => a.id === selectedActivity)?.icon || 'compost'}}
            </span>
          </div>
        </div>

        <!-- ========== FORM INPUTS ========== -->
        <!-- Form element: @submit.prevent = prevent page reload on submit -->
        <!-- space-y-6 = 24px margin-bottom between form sections -->
        <form class="space-y-6" @submit.prevent>

          <!-- ========== SECTION 1: Activity Type & DateTime ========== -->
          <!-- Section wrapper: space-y-4 = 16px gap between inputs -->
          <div class="space-y-4">

            <!-- ========== INPUT: Activity Type Select ========== -->
            <!-- Label: "Loại hoạt động" - activity subtype selector (e.g., "Gieo trực tiếp" vs "Gieo ươm") -->
            <div>
              <!-- Label text: text-sm = 14px, font-bold = 700, text-[#5D4037] = dark brown -->
              <!-- mb-2 = 8px bottom margin to separate from select input -->
              <label class="block text-sm font-bold text-[#5D4037] mb-2">
                Loại hoạt động
              </label>

              <!-- Select input: Activity type selector -->
              <!-- :value = bind to formData.activityType (one-way binding) -->
              <!-- @input = emit event when user selects option (two-way sync pattern) -->
              <!-- Dynamic options: Loop through currentActivityData.types array (changes per activity) -->
              <select :value="formData.activityType"
                @input="$emit('update:formData', { ...formData, activityType: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-[#FAFAF5]/50 px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm transition-colors cursor-pointer font-medium">
                <!-- Options loop: v-for over currentActivityData.types (activity-specific) -->
                <!-- :key = unique identifier (type string itself) -->
                <!-- :value = what gets stored in formData.activityType -->
                <option v-for="type in currentActivityData.types" :key="type" :value="type">
                  {{ type }}
                </option>
              </select>
            </div>

            <!-- ========== INPUT: DateTime ========== -->
            <!-- DateTime input: When was this activity done? -->
            <div>
              <!-- Label: "Thời gian thực hiện" -->
              <label class="block text-sm font-bold text-[#5D4037] mb-2">
                Thời gian thực hiện
              </label>

              <!-- DateTime input: User picks date + time -->
              <!-- :value = bind to formData.datetime -->
              <!-- @input = emit update when value changes -->
              <!-- type="datetime-local" = HTML5 date+time picker -->
              <input :value="formData.datetime"
                @input="$emit('update:formData', { ...formData, datetime: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-[#FAFAF5]/50 px-4 py-2 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm transition-colors cursor-pointer font-medium"
                type="datetime-local" />
            </div>
          </div>

          <!-- ========== SECTION 2: Material & Quantity (Light Green Background) ========== -->
          <!-- Material section: bg-[#E8F5E9]/30 = light green tint, p-4 = 16px padding all sides -->
          <!-- space-y-4 = 16px gap between inputs, border-[#2E7D32]/10 = thin green border -->
          <div class="bg-[#E8F5E9]/30 p-4 rounded-lg space-y-4 border border-[#2E7D32]/10">

            <!-- ========== INPUT: Material/Resource ========== -->
            <!-- Material selector: What product/material was used? (e.g., "Phân NPK 20-20-15") -->
            <div>
              <!-- Label with icon: flex items-center gap-1 = icon + text horizontally -->
              <!-- inventory_2 = Material Symbol icon for inventory/supplies -->
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">inventory_2</span>
                Vật tư sử dụng
              </label>

              <!-- Material select: Dynamic options per activity -->
              <!-- :value = bind to formData.material -->
              <!-- @input = emit update on change -->
              <select :value="formData.material"
                @input="$emit('update:formData', { ...formData, material: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-white px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm">
                <!-- Loop through currentActivityData.materials (changes per activity selected) -->
                <option v-for="material in currentActivityData.materials" :key="material" :value="material">
                  {{ material }}
                </option>
              </select>
            </div>

            <!-- ========== INPUT: Quantity/Amount ========== -->
            <!-- Quantity section: How much material was used? (e.g., "50 kg") -->
            <div>
              <!-- Label with icon: scale = Material Symbol for measurements -->
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">scale</span>
                Liều lượng / Số lượng
              </label>

              <!-- Quantity + Unit input: Two-part input (number + unit display) -->
              <!-- Flex: flex rounded-lg shadow-sm = horizontal layout with rounded border + shadow -->
              <div class="flex rounded-lg shadow-sm">

                <!-- Quantity input: Number field for amount -->
                <!-- :value = bind to formData.quantity -->
                <!-- @input = emit update on change -->
                <!-- type="number" = numeric input only, allows decimals -->
                <!-- rounded-l-lg = rounded corners only on left side -->
                <!-- border-r-0 = no right border (connects to unit display on right) -->
                <input :value="formData.quantity"
                  @input="$emit('update:formData', { ...formData, quantity: $event.target.value })"
                  class="block w-full h-12 rounded-l-lg border border-[#D7CCC8] border-r-0 bg-white px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm"
                  type="number" />

                <!-- Unit display: Read-only unit suffix (kg, lít, etc) -->
                <!-- inline-flex = inline horizontal layout with flex properties -->
                <!-- rounded-r-lg = rounded corners only on right side -->
                <!-- border-l-0 = no left border (connects to number input on left) -->
                <!-- Display formData.unit (e.g., "kg", "tấn", "lít") -->
                <span
                  class="inline-flex items-center h-12 rounded-r-lg border border-l-0 border-[#D7CCC8] bg-white px-4 text-gray-500 font-bold sm:text-sm">
                  {{ formData.unit }}
                </span>
              </div>
            </div>

            <!-- ========== CONDITIONAL: Market Selection for Harvest ========== -->
            <!-- Market selector: Only show when activity is "harvest" (export/sales related) -->
            <!-- v-if = conditionally render this section only if selectedActivity === 'harvest' -->
            <div v-if="selectedActivity === 'harvest'">
              <!-- Label with icon: global = Material Symbol for international/export -->
              <label class="block text-sm font-bold text-[#2E7D32] mb-2 flex items-center gap-1">
                <span class="material-symbols-outlined text-sm">public</span>
                Thị trường xuất khẩu
              </label>

              <!-- Market select: Where will harvested product be sold? -->
              <!-- :value = bind to formData.market (default: 'Thị trường nội địa') -->
              <!-- @input = emit update on selection change -->
              <select :value="formData.market || 'Thị trường nội địa'"
                @input="$emit('update:formData', { ...formData, market: $event.target.value })"
                class="block w-full h-12 rounded-lg border border-[#D7CCC8] bg-white px-4 text-gray-900 focus:border-[#2E7D32] focus:ring-2 focus:ring-[#2E7D32] sm:text-sm shadow-sm cursor-pointer font-medium">
                <!-- Loop through currentActivityData.markets (only harvest has this array) -->
                <option v-for="market in currentActivityData.markets" :key="market" :value="market">
                  {{ market }}
                </option>
              </select>
            </div>
          </div>

          <!-- ========== SECTION 3: Image Upload ========== -->
          <!-- Image gallery section: grid-cols-4 = 4 images per row -->
          <div>
            <!-- Label: "Hình ảnh thực tế" - Actual field photos -->
            <label class="block text-sm font-bold text-[#5D4037] mb-2">
              Hình ảnh thực tế
            </label>

            <!-- Image grid: grid grid-cols-4 gap-2 = 4 columns with 8px gap -->
            <div class="grid grid-cols-4 gap-2">

              <!-- ========== ADD IMAGE BUTTON ========== -->
              <!-- Add button: aspect-square = equal width/height (square shape) -->
              <!-- border-2 border-dashed = dashed border with 2px width -->
              <!-- Type: button = don't submit form when clicked -->
              <button
                class="aspect-square flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-[#2E7D32]/40 bg-[#E8F5E9]/20 text-[#2E7D32] hover:bg-[#E8F5E9]/50 transition-colors"
                type="button">
                <!-- Icon: add_a_photo = Material Symbol for adding photos -->
                <span class="material-symbols-outlined text-2xl mb-1">add_a_photo</span>
                <!-- Label: "Thêm" = Add -->
                <span class="text-[10px] font-bold">Thêm</span>
              </button>

              <!-- ========== IMAGE PREVIEW LOOP ========== -->
              <!-- Loop through formData.images array (uploaded/selected images) -->
              <!-- :key = unique index for each image -->
              <div v-for="(image, index) in formData.images" :key="index" class="aspect-square relative group">

                <!-- Image: Display preview of uploaded image -->
                <!-- object-cover = crop image to fill square while maintaining aspect ratio -->
                <!-- :src = dynamic image URL (data URL from file or server URL) -->
                <img :alt="`Preview ${index}`" class="w-full h-full object-cover rounded-lg shadow-sm" :src="image" />

                <!-- ========== DELETE BUTTON ========== -->
                <!-- Delete button: positioned absolute in top-right corner -->
                <!-- -top-1 -right-1 = positioned slightly outside corner for better UX -->
                <!-- opacity-0 group-hover:opacity-100 = only visible on hover over image -->
                <!-- @click = emit removeImage event with index to parent component -->
                <button @click="$emit('removeImage', index)"
                  class="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 shadow-md opacity-0 group-hover:opacity-100 transition-opacity"
                  type="button">
                  <!-- Icon: close = Material Symbol for delete/close action -->
                  <span class="material-symbols-outlined text-[14px] block">close</span>
                </button>
              </div>
            </div>
          </div>

          <!-- ========== SECTION 4: Action Buttons ========== -->
          <!-- Button container: pt-2 = 8px top padding, flex gap-3 = horizontal layout with 12px gap -->
          <div class="pt-2 flex items-center gap-3">

            <!-- ========== CANCEL BUTTON ========== -->
            <!-- Cancel: flex-1 = take 1 part of flex space -->
            <!-- border-[#D7CCC8] = sandy border, text-[#8D6E63] = brown text -->
            <!-- @click = emit cancel event to parent (close form without saving) -->
            <button @click="$emit('cancel')"
              class="flex-1 py-3.5 px-6 rounded-lg border border-[#D7CCC8] text-[#8D6E63] font-bold hover:bg-[#FAFAF5] transition-colors"
              type="button">
              Hủy
            </button>

            <!-- ========== SAVE BUTTON ========== -->
            <!-- Save: flex-[2] = take 2 parts of flex space (2x wider than cancel button) -->
            <!-- bg-[#2E7D32] = green background, text-white, shadow-lg shadow-[#2E7D32]/30 = green shadow -->
            <!-- hover: darker green + translated up + brighter shadow for interactive feedback -->
            <!-- flex items-center justify-center gap-2 = icon + text horizontally centered -->
            <!-- @click = emit save event to persist activity entry -->
            <button @click="$emit('save')"
              class="flex-[2] py-3.5 px-6 rounded-lg bg-[#2E7D32] text-white font-bold shadow-lg shadow-[#2E7D32]/30 hover:bg-green-800 hover:shadow-xl hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2"
              type="button">
              <!-- Icon: save = Material Symbol for save action -->
              <span class="material-symbols-outlined">save</span>
              <!-- Button text: "Lưu hoạt động" = Save Activity -->
              Lưu hoạt động
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ========== USER TIPS SECTION ========== -->
    <!-- Tips box: mt-6 = 24px top margin, brown background (#8D6E63) -->
    <!-- bg-[#8D6E63] text-white = brown container with white text -->
    <!-- p-4 rounded-lg = 16px padding, rounded corners -->
    <!-- flex items-start gap-3 = horizontal layout, aligned to top -->
    <div class="mt-6 bg-[#8D6E63] text-white p-4 rounded-lg flex items-start gap-3 shadow-lg">

      <!-- Icon: lightbulb = Material Symbol for tips/ideas -->
      <!-- text-yellow-300 = yellow color for attention -->
      <span class="material-symbols-outlined text-yellow-300">lightbulb</span>

      <!-- Tips content: text-sm = small font size -->
      <div class="text-sm">
        <!-- Tips title: "Mẹo cho Bác Ba:" = Tips for Uncle Ba (farmer) -->
        <!-- font-bold mb-1 = bold, 4px bottom margin before description -->
        <p class="font-bold mb-1">Mẹo cho Bác Ba:</p>

        <!-- Tips description: opacity-90 = slightly transparent white -->
        <!-- Content changes based on activity (hardcoded for now but could be dynamic) -->
        <p class="opacity-90">
          Nên bón phân vào sáng sớm hoặc chiều mát để cây hấp thụ tốt nhất.
        </p>
      </div>
    </div>
  </div>
</template>
