<script setup>
/**
 * ========== COMPONENT: HomeDetailView.vue ==========
 * Purpose: Hiển thị chi tiết vùng trồng (cover ảnh, timeline, info)
 * Related Files:
 *   - src/composables/useHome.js (Logic & state)
 *   - src/views/HomeView.vue (Main view)
 *   - src/assets/styles/tailwind.css (Global utilities)
 */

defineProps({
      vung: {
            type: Object,
            required: true
      }
});

defineEmits(['back', 'openQR']);
</script>

<template>
      <div class="flex flex-col h-full">

            <!-- Cover image header -->
            <div class="h-44 bg-cover bg-center relative flex items-end"
                  :style="{ backgroundImage: `url(${vung.anh})` }">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                  <div class="relative z-10 w-full p-4 text-white">
                        <h2 class="text-2xl font-bold text-shadow">{{ vung.ten }}</h2>
                        <span
                              class="inline-block mt-2 px-3 py-1 bg-yellow-400 text-gray-800 rounded-md text-xs font-bold">
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 inline mr-1" viewBox="0 0 20 20"
                                    fill="currentColor">
                                    <path
                                          d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                              </svg>
                              {{ vung.chungNhan }}
                        </span>
                  </div>
            </div>

            <!-- Scrollable content -->
            <div class="flex-grow overflow-y-auto p-4 space-y-4">

                  <!-- Info grid -->
                  <div class="grid grid-cols-2 gap-2">
                        <div class="bg-gray-50 rounded-lg p-3 border border-gray-200">
                              <label class="text-xs text-gray-600 block mb-1">Mã số</label>
                              <strong class="text-gray-800">{{ vung.ma }}</strong>
                        </div>
                        <div class="bg-gray-50 rounded-lg p-3 border border-gray-200">
                              <label class="text-xs text-gray-600 block mb-1">Diện tích</label>
                              <strong class="text-gray-800">{{ vung.dienTich }}</strong>
                        </div>
                  </div>

                  <!-- Timeline -->
                  <div>
                        <h4 class="font-bold text-gray-800 text-sm mb-3 pb-2 border-b-2 border-gray-200">
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 inline mr-2" viewBox="0 0 20 20"
                                    fill="currentColor">
                                    <path fill-rule="evenodd"
                                          d="M5 2a1 1 0 011 1v1h1a1 1 0 000-2H6V3a1 1 0 01-1 1V2zM3 5a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm0 2h14v8H3V7z"
                                          clip-rule="evenodd" />
                              </svg>
                              Nhật ký Canh tác
                        </h4>

                        <div class="space-y-3 border-l-2 border-gray-300 pl-4 ml-2">
                              <div v-for="(log, idx) in vung.nhatKy" :key="idx" class="relative">
                                    <!-- Dot -->
                                    <div
                                          class="absolute w-3 h-3 bg-green-500 rounded-full -left-5 top-1.5 border-2 border-white">
                                    </div>

                                    <!-- Content -->
                                    <div class="text-xs text-gray-500 mb-1">{{ log.ngay }}</div>
                                    <div class="font-semibold text-gray-800 text-sm">{{ log.hoatDong }}</div>
                                    <div class="text-gray-600 text-xs mt-1">{{ log.chiTiet }}</div>
                              </div>
                        </div>
                  </div>

            </div>

            <!-- Action buttons -->
            <div class="border-t border-gray-200 p-4 space-y-2 flex-shrink-0">
                  <button @click="$emit('openQR', vung.ma)"
                        class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition-colors flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path
                                    d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zm10-9a2 2 0 110 4 2 2 0 010-4zM2 15a1 1 0 101 2h1a1 1 0 100-2H3z" />
                        </svg>
                        Mã QR Truy xuất
                  </button>
                  <button @click="$emit('back')"
                        class="w-full bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-2 rounded-lg transition-colors">
                        Quay lại
                  </button>
            </div>

      </div>
</template>
