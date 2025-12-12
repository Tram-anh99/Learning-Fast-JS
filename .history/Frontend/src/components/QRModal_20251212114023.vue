<script setup>
/**
 * ========== COMPONENT: QRModal.vue ==========
 * Purpose: Modal QR code dùng chung cho tra cứu & truy xuất nguồn gốc
 * Dùng bởi:
 *   - src/views/HomeView.vue (Tra cứu nông sản)
 *   - src/views/TraceabilityPage.vue (Truy xuất nguồn gốc)
 * Related Composables:
 *   - src/composables/useHome.js
 *   - src/composables/useTraceability.js
 * Styling:
 *   - src/assets/styles/tailwind.css (animate-fade-in, animate-scale-up)
 */

import QrcodeVue from 'qrcode.vue';

defineProps({
      show: {
            type: Boolean,
            required: true
      },
      qrValue: {
            type: String,
            required: true
      }
});

defineEmits(['close']);
</script>

<template>
      <!-- Backdrop với glassmorphism -->
      <div v-if="show" @click.self="$emit('close')"
            class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-md animate-fade-in">
            <!-- Modal Card - Compact size -->
            <div
                  class="relative w-full max-w-xs bg-gradient-to-br from-white via-slate-50 to-blue-50 rounded-2xl shadow-2xl p-6 text-center animate-scale-up border border-white/80">

                  <!-- Decorative gradient circles (smaller) -->
                  <div
                        class="absolute -top-16 -right-16 w-32 h-32 bg-gradient-to-br from-green-400/20 to-blue-400/20 rounded-full blur-2xl">
                  </div>
                  <div
                        class="absolute -bottom-16 -left-16 w-32 h-32 bg-gradient-to-br from-blue-400/20 to-purple-400/20 rounded-full blur-2xl">
                  </div>

                  <!-- Close button -->
                  <button @click="$emit('close')"
                        class="absolute top-3 right-3 p-1.5 hover:bg-gray-100 text-gray-500 hover:text-gray-700 transition-all duration-200 rounded-full"
                        title="Đóng">
                        <svg class="w-4 h-4 hover:rotate-90 transition-transform duration-300" fill="none"
                              viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                        </svg>
                  </button>

                  <!-- Header Section - Compact -->
                  <div class="relative z-10 mb-5">
                        <div class="flex justify-center mb-2">
                              <div
                                    class="px-3 py-1 bg-gradient-to-r from-green-400 to-blue-400 rounded-full text-[11px] font-bold text-white shadow-md">
                                    ✨ Chia sẻ
                              </div>
                        </div>

                        <h3
                              class="text-xl font-bold bg-gradient-to-r from-gray-900 via-green-700 to-blue-700 bg-clip-text text-transparent mb-1">
                              Mã QR
                        </h3>
                        <p class="text-xs text-gray-600">
                              Quét bằng Camera hoặc Zalo
                        </p>
                  </div>

                  <!-- QR Code Container - Compact -->
                  <div class="relative z-10 flex justify-center mb-4">
                        <div class="relative">
                              <!-- Glow effect (subtle) -->
                              <div
                                    class="absolute inset-0 bg-gradient-to-r from-green-400 to-blue-400 rounded-xl blur-lg opacity-20 hover:opacity-40 transition-opacity duration-300">
                              </div>

                              <!-- QR Card - Smaller -->
                              <div
                                    class="relative bg-white p-4 rounded-xl shadow-lg border-2 border-slate-200 hover:shadow-xl transition-all duration-300">
                                    <QrcodeVue :value="qrValue" :size="180" level="H" render-as="svg"
                                          foreground="#0d7a4a" />
                              </div>
                        </div>
                  </div>

                  <!-- URL Display Section - Compact -->
                  <div
                        class="relative z-10 mb-4 p-3 bg-gradient-to-r from-slate-100 to-blue-50 rounded-lg border border-slate-200/50 hover:border-slate-300 transition-all duration-200">
                        <p class="text-[11px] text-gray-600 font-semibold uppercase tracking-wider mb-1.5 opacity-70">
                              🔗 Link truy cập
                        </p>
                        <p class="text-xs text-gray-700 font-mono break-all">
                              {{ qrValue }}
                        </p>
                  </div>

                  <!-- Action Buttons - Compact -->
                  <div class="relative z-10">
                        <button @click="$emit('close')"
                              class="w-full py-2 px-3 text-gray-600 font-semibold rounded-lg hover:bg-gray-100 transition-all duration-200 text-sm border border-gray-200">
                              Đóng
                        </button>
                  </div>

            </div>
      </div>
</template>
