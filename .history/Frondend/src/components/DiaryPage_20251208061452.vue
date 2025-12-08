<template>
      <div class="diary-container bg-gray-100 min-h-screen pb-20">
            <div v-if="mode === 'list'">
                  <header class="bg-green-600 text-white p-4 flex justify-between items-center sticky top-0 z-10">
                        <h1 class="text-xl font-bold">Nhật ký đồng ruộng</h1>
                  </header>

                  <div class="p-4">
                        <div v-for="(item, index) in diaryEntries" :key="index"
                              class="bg-white p-4 rounded-lg shadow mb-3 flex items-center">
                              <div
                                    class="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-2xl mr-4">
                                    {{ getActivityIcon(item.type) }}
                              </div>
                              <div class="flex-grow">
                                    <h3 class="font-bold text-gray-800">{{ item.title }}</h3>
                                    <p class="text-sm text-gray-500">{{ item.field }} - {{ item.details }}</p>
                              </div>
                              <div class="text-sm text-gray-400 ml-2">
                                    {{ item.date }}
                              </div>
                        </div>
                  </div>

                  <button @click="mode = 'add'"
                        class="fixed bottom-6 right-6 bg-green-600 text-white rounded-full w-16 h-16 flex items-center justify-center text-4xl shadow-lg hover:bg-green-700 focus:outline-none">
                        +
                  </button>
            </div>


            <div v-if="mode === 'add'" class="bg-gray-50 min-h-screen">
                  <header class="bg-white p-4 flex justify-between items-center border-b sticky top-0 z-10">
                        <button @click="mode = 'list'" class="text-gray-500 text-lg">Hủy</button>
                        <h1 class="text-lg font-bold">Ghi chép mới</h1>
                        <button @click="saveEntry"
                              class="bg-green-600 text-white px-6 py-2 rounded font-bold">Lưu</button>
                  </header>

                  <div class="p-4 space-y-4">
                        <div class="bg-white p-4 rounded-lg shadow">
                              <div class="mb-4">
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Thời gian</label>
                                    <input type="datetime-local" v-model="form.date"
                                          class="w-full p-3 border rounded bg-gray-50 text-lg">
                              </div>
                              <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Chọn thửa ruộng</label>
                                    <select v-model="form.field" class="w-full p-3 border rounded bg-gray-50 text-lg">
                                          <option value="Thửa A (Gần nhà)">Thửa A (Gần nhà)</option>
                                          <option value="Thửa B (Bãi bồi)">Thửa B (Bãi bồi)</option>
                                    </select>
                              </div>
                        </div>

                        <div class="bg-white p-4 rounded-lg shadow">
                              <label class="block text-sm font-medium text-gray-700 mb-3">Bạn vừa làm công việc
                                    gì?</label>
                              <div class="grid grid-cols-3 gap-3">
                                    <button v-for="(act, idx) in activityTypes" :key="idx" @click="form.type = act.id"
                                          :class="['p-3 rounded-lg flex flex-col items-center border-2', form.type === act.id ? 'border-green-500 bg-green-50' : 'border-gray-200 bg-white']">
                                          <span class="text-3xl mb-1">{{ act.icon }}</span>
                                          <span class="text-sm font-medium">{{ act.name }}</span>
                                    </button>
                              </div>
                        </div>

                        <div v-if="form.type" class="bg-white p-4 rounded-lg shadow animate-fade-in">
                              <h3 class="font-bold mb-3 text-green-700">Chi tiết {{ getActivityName(form.type) }}</h3>

                              <div v-if="form.type === 'fertilizer'" class="space-y-3">
                                    <input type="text" placeholder="Tên loại phân (VD: NPK 20-20-15)"
                                          class="w-full p-3 border rounded">
                                    <div class="flex items-center">
                                          <input type="number" placeholder="Số lượng"
                                                class="flex-grow p-3 border rounded mr-2">
                                          <span class="font-bold p-3 bg-gray-100 rounded">Kg</span>
                                    </div>
                              </div>

                              <div v-if="form.type === 'spray'" class="space-y-3">
                                    <input type="text" placeholder="Tên thuốc BVTV" class="w-full p-3 border rounded">
                                    <input type="text" placeholder="Phòng trừ đối tượng nào? (VD: Rầy nâu)"
                                          class="w-full p-3 border rounded">
                              </div>

                              <div v-if="!['fertilizer', 'spray'].includes(form.type)">
                                    <textarea placeholder="Ghi chú thêm về công việc..." rows="3"
                                          class="w-full p-3 border rounded"></textarea>
                              </div>
                        </div>

                        <div class="bg-white p-4 rounded-lg shadow">
                              <label class="block text-sm font-medium text-gray-700 mb-3">Hình ảnh (nếu có)</label>
                              <div
                                    class="border-2 border-dashed border-gray-300 rounded-lg p-6 flex flex-col items-center justify-center text-gray-400 bg-gray-50">
                                    <span class="text-4xl">📷</span>
                                    <span class="mt-2">Bấm để chụp hoặc chọn ảnh</span>
                                    <input type="file" class="hidden">
                              </div>
                        </div>

                  </div>
            </div>
      </div>
</template>

<script>
export default {
      name: 'DiaryPage',
      data() {
            return {
                  mode: 'list', // 'list' hoặc 'add' để chuyển màn hình
                  // Dữ liệu mẫu cho danh sách
                  diaryEntries: [
                        { type: 'fertilizer', title: 'Bón thúc đợt 1', field: 'Thửa A', details: 'NPK - 50kg', date: '07/12' },
                        { type: 'spray', title: 'Phun trừ rầy', field: 'Thửa B', details: 'Chess - 2 bình', date: '05/12' },
                        { type: 'water', title: 'Tưới nước', field: 'Thửa A', details: 'Chạy máy 2h', date: '04/12' },
                  ],
                  // Định nghĩa các loại hoạt động để tạo nút
                  activityTypes: [
                        { id: 'tillage', name: 'Làm đất', icon: '🚜' },
                        { id: 'sow', name: 'Gieo trồng', icon: '🌱' },
                        { id: 'fertilizer', name: 'Bón phân', icon: '🌾' },
                        { id: 'spray', name: 'Phun thuốc', icon: '💊' },
                        { id: 'water', name: 'Tưới nước', icon: '💧' },
                        { id: 'harvest', name: 'Thu hoạch', icon: '💰' },
                  ],
                  // Dữ liệu cho form thêm mới
                  form: {
                        date: new Date().toISOString().slice(0, 16), // Lấy ngày giờ hiện tại cho input datetime-local
                        field: 'Thửa A (Gần nhà)',
                        type: null, // Loại hoạt động đang chọn
                        details: {}
                  }
            }
      },
      methods: {
            // Hàm tiện ích lấy icon từ ID
            getActivityIcon(typeId) {
                  const act = this.activityTypes.find(a => a.id === typeId);
                  return act ? act.icon : '📋';
            },
            // Hàm tiện ích lấy tên từ ID
            getActivityName(typeId) {
                  const act = this.activityTypes.find(a => a.id === typeId);
                  return act ? act.name : 'Hoạt động';
            },
            saveEntry() {
                  // 1. Validate dữ liệu (VD: chưa chọn loại hoạt động thì báo lỗi)
                  if (!this.form.type) {
                        alert("Vui lòng chọn loại công việc bạn đã làm!");
                        return;
                  }

                  // 2. Gọi API để lưu dữ liệu (Ở đây chỉ mô phỏng)
                  console.log("Đang lưu nhật ký:", this.form);
                  alert("Đã lưu thành công!");

                  // 3. Reset form và quay về trang danh sách
                  this.mode = 'list';
                  this.form.type = null;
                  // (Thực tế bạn nên load lại danh sách diaryEntries từ API)
            }
      }
}
</script>

<style scoped>
/* Hiệu ứng hiện dần cho mượt */
.animate-fade-in {
      animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
      from {
            opacity: 0;
            transform: translateY(10px);
      }

      to {
            opacity: 1;
            transform: translateY(0);
      }
}

/* Tăng kích thước font chữ mặc định cho dễ đọc trên mobile */
.diary-container {
      font-size: 16px;
}

input,
select,
textarea,
button {
      font-size: 1rem;
      /* 16px */
}

/* Nếu bạn không dùng Tailwind, bạn sẽ cần viết CSS khá nhiều để nó đẹp như mô tả
   Ví dụ class cho nút bấm hoạt động:
.activity-btn {
   display: flex; flex-direction: column; align-items: center;
   padding: 12px; border: 2px solid #eee; border-radius: 8px; background: white;
}
.activity-btn.active {
   border-color: #22c55e; background-color: #f0fdf4;
}
*/
</style>