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
      <div class="flex flex-col h-full bg-white">

            <!-- Cover image header - Minimalist -->
            <div class="relative h-48 bg-center bg-cover flex-shrink-0"
                  :style="{ backgroundImage: `url(${vung.anh})` }">
                  <div class="absolute inset-0 bg-gradient-to-b from-black/30 to-black/60"></div>
            </div>

            <!-- Scrollable content - Minimalist cards -->
            <div class="flex-grow overflow-y-auto pb-4">
                  
                  <!-- Header info - Overlay on image -->
                  <div class="px-5 pt-4 pb-6 -mt-16 relative z-10">
                        <div class="bg-white rounded-2xl shadow-lg p-4">
                              <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ vung.ten }}</h2>
                              <div class="flex items-center gap-2 flex-wrap">
                                    <span class="inline-flex items-center gap-1 px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-semibold">
                                          ⭐ {{ vung.chungNhan }}
                                    </span>
                                    <span class="text-sm text-gray-600">{{ vung.dienTich }}</span>
                              </div>
                        </div>
                  </div>

                  <!-- Info cards in grid -->
                  <div class="px-5 space-y-3">
                        
                        <!-- Mã số card -->
                        <div class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-4 border border-gray-200">
                              <div class="text-xs text-gray-600 font-semibold uppercase tracking-wide mb-1">Mã số vùng</div>
                              <div class="text-lg font-bold text-gray-900">{{ vung.ma }}</div>
                        </div>

                        <!-- Chủ thể card - Highlight -->
                        <div class="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-4 border border-blue-200">
                              <div class="text-xs text-blue-700 font-semibold uppercase tracking-wide mb-2">Chủ thể canh tác</div>
                              <div class="text-sm font-bold text-gray-900 mb-1">{{ vung.hoKinhDoanh }}</div>
                              <div class="text-xs text-gray-700">📍 {{ vung.diaChi }}</div>
                        </div>

                        <!-- Timeline section -->
                        <div class="mt-5">
                              <h4 class="text-sm font-bold text-gray-900 mb-3 uppercase tracking-wide text-xs">Nhật ký hoạt động</h4>
                              
                              <div class="space-y-2">
                                    <div v-for="(log, idx) in vung.nhatKy" :key="idx" 
                                          class="bg-gray-50 rounded-lg p-3 border border-gray-200 hover:border-gray-300 transition-colors">
                                          <div class="flex justify-between items-start gap-2 mb-1">
                                                <div class="font-semibold text-gray-900 text-sm">{{ log.hoatDong }}</div>
                                                <span class="text-xs text-gray-500 whitespace-nowrap">{{ log.ngay }}</span>
                                          </div>
                                          <p class="text-xs text-gray-600 leading-relaxed">{{ log.chiTiet }}</p>
                                    </div>
                              </div>
                        </div>

                  </div>

            </div>

            <!-- Action buttons - Sticky bottom -->
            <div class="flex-shrink-0 px-5 py-4 border-t border-gray-200 bg-white space-y-2">
                  <button @click="$emit('openQR', vung.ma)"
                        class="w-full py-3 px-4 bg-green-600 hover:bg-green-700 text-white font-semibold rounded-xl transition-colors active:scale-95">
                        🔗 Mã QR
                  </button>
                  <button @click="$emit('back')"
                        class="w-full py-3 px-4 bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold rounded-xl transition-colors border border-gray-300 active:scale-95">
                        ← Quay lại
                  </button>
            </div>

      </div>
</template>
