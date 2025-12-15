<script setup>
/**
 * ========== COMPONENT: HomeDetailView.vue ==========
 * Purpose: Hiển thị chi tiết vùng trồng (cover ảnh, timeline, info)
 * Related Files:
 *   - src/composables/useHome.js (Logic & state)
 *   - src/views/HomeView.vue (Main view)
 *   - src/assets/styles/tailwind.css (Global utilities)
 */

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
                        <div class="p-3 rounded-lg" style="background-color: #fbfced;">
                              <label class="block mb-1 text-xs" style="color: #6b7280;">Mã số</label>
                              <strong style="color: #24504b;">{{ vung.ma }}</strong>
                        </div>

                        <!-- Cột 2: Diện tích vùng trồng -->
                        <div class="p-3 rounded-lg" style="background-color: #fbfced;">
                              <label class="block mb-1 text-xs" style="color: #6b7280;">Diện tích</label>
                              <strong style="color: #24504b;">{{ vung.dienTich }}</strong>
                        </div>
                  </div>

                  <!-- Nhóm thông tin chủ thể: Thông tin hộ canh tác / hợp tác xã -->
                  <div class="p-4 rounded-lg" style="background-color: #e8f5e9; border-left: 4px solid #24504b;">
                        <!-- Tiêu đề nhóm -->
                        <h4 class="mb-3 text-sm font-bold flex items-center gap-2" style="color: #24504b;">
                              <!-- Icon nhà -->
                              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="currentColor"
                                    viewBox="0 0 20 20" style="color: #24504b;">
                                    <path
                                          d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                              </svg>
                              Chủ thể canh tác
                        </h4>

                        <!-- Danh sách thông tin chủ thể -->
                        <div class="space-y-2 text-sm">
                              <!-- Tên hộ -->
                              <div class="flex justify-between">
                                    <span style="color: #6b7280;">Hộ/Công ty:</span>
                                    <strong style="color: #24504b;">{{ vung.hoTen || 'Hộ nông dân' }}</strong>
                              </div>
                              <!-- Địa chỉ -->
                              <div class="flex justify-between">
                                    <span style="color: #6b7280;">Địa chỉ:</span>
                                    <strong style="color: #24504b;">{{ vung.diaChi || 'Khu vực Đồng bằng Sông Cửu Long'
                                          }}</strong>
                              </div>
                              <!-- Hợp tác xã -->
                              <div class="flex justify-between">
                                    <span style="color: #6b7280;">HTX trực thuộc:</span>
                                    <strong style="color: #24504b;">{{ vung.hopTacXa || 'HTX Nông sản an toàn'
                                          }}</strong>
                              </div>
                              <!-- Số điện thoại -->
                              <div class="flex justify-between">
                                    <span style="color: #6b7280;">Liên hệ:</span>
                                    <strong style="color: #24504b;">{{ vung.dienThoai || '(028) 1234 5678' }}</strong>
                              </div>
                        </div>
                  </div>

                  <!-- Timeline: hiển thị nhật ký hoạt động canh tác -->
                  <div>
                        <!-- Tiêu đề timeline với icon lịch -->
                        <h4 class="pb-2 mb-3 text-sm font-bold"
                              style="color: #24504b; border-bottom: 2px solid #e5e7eb;">
                              <!-- Icon lịch -->
                              <svg xmlns="http://www.w3.org/2000/svg" class="inline w-4 h-4 mr-2" viewBox="0 0 20 20"
                                    fill="currentColor">
                                    <path fill-rule="evenodd"
                                          d="M5 2a1 1 0 011 1v1h1a1 1 0 000-2H6V3a1 1 0 01-1 1V2zM3 5a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm0 2h14v8H3V7z"
                                          clip-rule="evenodd" />
                              </svg>
                              Nhật ký Canh tác
                        </h4>

                        <!-- Timeline list: lặp qua mảng nhật ký -->
                        <div class="pl-4 ml-2 space-y-3" style="border-left: 2px solid #e5e7eb;">
                              <!-- Mỗi mục nhật ký -->
                              <div v-for="(log, idx) in vung.nhatKy" :key="idx" class="relative">
                                    <!-- Dot indicator: điểm tròn xanh bên trái -->
                                    <div class="absolute w-3 h-3 rounded-full -left-5 top-1.5"
                                          style="background-color: #24504b;">
                                    </div>

                                    <!-- Nội dung nhật ký -->
                                    <!-- Ngày hoạt động -->
                                    <div class="mb-1 text-xs" style="color: #6b7280;">{{ log.ngay }}</div>
                                    <!-- Tên hoạt động (vd: "Bón phân", "Tỉa cành") -->
                                    <div class="text-sm font-semibold" style="color: #24504b;">{{ log.hoatDong }}</div>
                                    <!-- Chi tiết hoạt động -->
                                    <div class="mt-1 text-xs" style="color: #6b7280;">{{ log.chiTiet }}</div>
                              </div>
                        </div>
                  </div>

            </div>

            <!-- Action buttons: nút hành động ở cuối (sticky) -->
            <div class="sticky bottom-0 flex-shrink-0 p-4 space-y-2"
                  style="background-color: #fbfced; border-top: 1px solid #e5e7eb;">
                  <!-- Nút Mã QR Truy xuất: emit event 'openQR' với mã vùng -->
                  <button @click="$emit('openQR', vung.ma)"
                        class="flex items-center justify-center w-full gap-2 py-3 font-semibold text-white transition-colors rounded-lg"
                        style="background-color: #24504b;" @mouseover="$event.target.style.backgroundColor = '#1a3a36'"
                        @mouseout="$event.target.style.backgroundColor = '#24504b'">
                        <!-- Icon QR code -->
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                              <path
                                    d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 6a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zm10-9a2 2 0 110 4 2 2 0 010-4zM2 15a1 1 0 101 2h1a1 1 0 100-2H3z" />
                        </svg>
                        Mã QR Truy xuất
                  </button>

                  <!-- Nút Quay lại: emit event 'back' để trở lại danh sách -->
                  <button @click="$emit('back')" class="w-full py-2 font-semibold transition-colors rounded-lg"
                        style="background-color: #e5e7eb; color: #24504b;"
                        @mouseover="$event.target.style.backgroundColor = '#d1d5db'"
                        @mouseout="$event.target.style.backgroundColor = '#e5e7eb'">
                        Quay lại
                  </button>
            </div>

      </div>
</template>
