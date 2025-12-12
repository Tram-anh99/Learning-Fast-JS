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

            <!-- Cover image header - Compact -->
            <div class="relative flex items-end h-36 bg-center bg-cover flex-shrink-0"
                  :style="{ backgroundImage: `url(${vung.anh})` }">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
                  <div class="relative z-10 w-full p-3 text-white">
                        <h2 class="text-lg font-bold text-shadow">{{ vung.ten }}</h2>
                        <span
                              class="inline-block px-2 py-0.5 mt-1 text-xs font-bold text-gray-800 bg-yellow-400 rounded-md">
                              <svg xmlns="http://www.w3.org/2000/svg" class="inline w-2.5 h-2.5 mr-0.5" viewBox="0 0 20 20"
                                    fill="currentColor">
                                    <path
                                          d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                              </svg>
                              {{ vung.chungNhan }}
                        </span>
                  </div>
            </div>

            <!-- Scrollable content - Two column layout -->
            <div class="flex-grow p-3 overflow-y-auto">
                  <div class="grid grid-cols-1 lg:grid-cols-3 gap-3">
                        
                        <!-- Left column: Info & Timeline -->
                        <div class="lg:col-span-2 space-y-3">
                              <!-- Info grid -->
                              <div class="grid grid-cols-2 gap-2">
                                    <div class="p-2.5 border border-gray-200 rounded-lg bg-gray-50">
                                          <label class="block mb-1 text-xs text-gray-600">Mã số</label>
                                          <strong class="text-sm text-gray-800">{{ vung.ma }}</strong>
                                    </div>
                                    <div class="p-2.5 border border-gray-200 rounded-lg bg-gray-50">
                                          <label class="block mb-1 text-xs text-gray-600">Diện tích</label>
                                          <strong class="text-sm text-gray-800">{{ vung.dienTich }}</strong>
                                    </div>
                              </div>

                              <!-- Timeline with scroll -->
                              <div class="flex flex-col h-40 border border-gray-200 rounded-lg bg-gray-50 overflow-hidden">
                                    <h4 class="px-3 py-2 text-xs font-bold text-gray-800 border-b border-gray-200 flex-shrink-0">
                                          <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3.5 h-3.5 mr-1.5" viewBox="0 0 20 20"
                                                fill="currentColor">
                                                <path fill-rule="evenodd"
                                                      d="M5 2a1 1 0 011 1v1h1a1 1 0 000-2H6V3a1 1 0 01-1 1V2zM3 5a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm0 2h14v8H3V7z"
                                                      clip-rule="evenodd" />
                                          </svg>
                                          Nhật ký
                                    </h4>

                                    <div class="flex-grow overflow-y-auto">
                                          <div class="px-3 py-2 space-y-2">
                                                <div v-for="(log, idx) in vung.nhatKy" :key="idx" class="text-xs">
                                                      <div class="flex items-start gap-2">
                                                            <div class="w-2 h-2 bg-green-500 rounded-full mt-1.5 flex-shrink-0"></div>
                                                            <div class="flex-grow min-w-0">
                                                                  <div class="font-semibold text-gray-800 text-xs">{{ log.hoatDong }}</div>
                                                                  <div class="text-xs text-gray-500 mt-0.5">{{ log.ngay }}</div>
                                                                  <div class="text-xs text-gray-600 mt-0.5">{{ log.chiTiet }}</div>
                                                            </div>
                                                      </div>
                                                </div>
                                          </div>
                                    </div>
                              </div>
                        </div>

                        <!-- Right column: Analytics & Stats -->
                        <div class="space-y-3">
                              <!-- Yield Chart -->
                              <div class="p-3 border border-gray-200 rounded-lg bg-white">
                                    <h4 class="mb-2 text-xs font-bold text-gray-800 flex items-center">
                                          <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3.5 h-3.5 mr-1.5" viewBox="0 0 20 20"
                                                fill="currentColor">
                                                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
                                          </svg>
                                          Năng suất
                                    </h4>
                                    <canvas id="yieldChart" class="w-full" height="100"></canvas>
                              </div>

                              <!-- Weather Widget -->
                              <div class="p-3 border border-gray-200 rounded-lg bg-gradient-to-br from-blue-50 to-blue-100">
                                    <h4 class="mb-2 text-xs font-bold text-gray-800 flex items-center">
                                          <svg xmlns="http://www.w3.org/2000/svg" class="inline w-3.5 h-3.5 mr-1.5" viewBox="0 0 20 20"
                                                fill="currentColor">
                                                <path d="M5.5 13a3.5 3.5 0 01-.369-6.98 4 4 0 117.753-1.3A4.5 4.5 0 1113.5 13H11V9.413l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13H5.5z" />
                                          </svg>
                                          Thời tiết
                                    </h4>
                                    <div class="grid grid-cols-2 gap-2 text-center text-xs">
                                          <div>
                                                <div class="text-2xl">⛅</div>
                                                <div class="font-semibold text-gray-800 mt-1">{{ vung.thoiTiet.hienTai }}</div>
                                                <div class="text-xs text-gray-600">{{ vung.thoiTiet.nhietDo }}°C</div>
                                          </div>
                                          <div>
                                                <div class="text-2xl">🌧️</div>
                                                <div class="font-semibold text-gray-800 mt-1">Mưa</div>
                                                <div class="text-xs text-gray-600">{{ vung.thoiTiet.doAm }}%</div>
                                          </div>
                                    </div>
                              </div>

                              <!-- Stats Grid -->
                              <div class="grid grid-cols-2 gap-2">
                                    <div class="p-2.5 border border-gray-200 rounded-lg bg-yellow-50">
                                          <label class="block mb-1 text-xs text-gray-600">Năng suất</label>
                                          <strong class="text-sm text-gray-800">{{ vung.nangSuat }}</strong>
                                    </div>
                                    <div class="p-2.5 border border-gray-200 rounded-lg bg-green-50">
                                          <label class="block mb-1 text-xs text-gray-600">Sức khỏe</label>
                                          <strong class="text-sm text-gray-800">{{ vung.suc_khoe }}</strong>
                                    </div>
                              </div>

                              <!-- Action Buttons -->
                              <div class="flex gap-2">
                                    <button class="flex-1 px-3 py-1.5 bg-blue-600 text-white text-xs font-semibold rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-1">
                                          <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                                                <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                          </svg>
                                          Chỉnh sửa
                                    </button>
                                    <button class="flex-1 px-3 py-1.5 bg-gray-200 text-gray-800 text-xs font-semibold rounded-lg hover:bg-gray-300 transition-colors flex items-center justify-center gap-1">
                                          <svg xmlns="http://www.w3.org/2000/svg" class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                                                <path d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3.293 1.293a1 1 0 011.414 0L10 9.586l3.293-3.293a1 1 0 111.414 1.414L11.414 11l3.293 3.293a1 1 0 11-1.414 1.414L10 12.414l-3.293 3.293a1 1 0 01-1.414-1.414L8.586 11 5.293 7.707a1 1 0 010-1.414z" />
                                          </svg>
                                          Xóa
                                    </button>
                              </div>
                        </div>

                  </div>
            </div>

            <!-- Action buttons -->
            <div class="flex-shrink-0 p-5 space-y-3 border-t border-gray-200 bg-white">
                  <button @click="$emit('openQR', vung.ma)"
                        class="flex items-center justify-center w-full gap-2 py-3 font-semibold text-white transition-colors bg-green-600 rounded-lg hover:bg-green-700 active:scale-95">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path
                                    d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zm10-9a2 2 0 110 4 2 2 0 010-4zM2 15a1 1 0 101 2h1a1 1 0 100-2H3z" />
                        </svg>
                        Mã QR Truy xuất
                  </button>
                  <button @click="$emit('back')"
                        class="w-full py-3 font-semibold text-gray-700 transition-colors bg-gray-100 border border-gray-300 rounded-lg hover:bg-gray-200 active:scale-95">
                        ← Quay lại
                  </button>
            </div>

      </div>
</template>
