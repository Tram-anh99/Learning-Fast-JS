<template>
  <div class="min-h-screen bg-gray-50 text-gray-800 font-sans pb-24">
    
    <div v-if="viewMode === 'list'">
      <header class="bg-green-600 text-white p-4 shadow-md sticky top-0 z-50">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-xl font-bold">Nhật Ký Ruộng</h1>
            <p class="text-green-100 text-xs mt-0.5">Hôm nay: {{ getCurrentDate() }}</p>
          </div>
          <div class="bg-white/20 p-2 rounded-lg cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
        </div>
      </header>

      <div class="px-4 py-3 bg-white shadow-sm mb-4">
        <div class="flex space-x-2 overflow-x-auto no-scrollbar py-1">
          <button class="px-4 py-1.5 bg-green-100 text-green-800 rounded-full text-sm font-semibold whitespace-nowrap border border-green-200">Tất cả</button>
          <button class="px-4 py-1.5 bg-gray-100 text-gray-600 rounded-full text-sm font-medium whitespace-nowrap border border-transparent">Thửa A</button>
          <button class="px-4 py-1.5 bg-gray-100 text-gray-600 rounded-full text-sm font-medium whitespace-nowrap border border-transparent">Thửa B</button>
        </div>
      </div>

      <div class="px-4 space-y-3">
        <div v-for="(item, index) in diaryList" :key="index" class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-start active:bg-gray-50 transition duration-150">
          <div :class="`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center text-2xl mr-4 ${getIconBgColor(item.type)}`">
            {{ getActivityIcon(item.type) }}
          </div>
          
          <div class="flex-grow">
            <div class="flex justify-between items-start">
              <h3 class="font-bold text-gray-800 text-lg leading-tight">{{ item.title }}</h3>
              <span class="text-xs text-gray-400 font-medium bg-gray-100 px-2 py-1 rounded">{{ item.date }}</span>
            </div>
            <p class="text-sm text-green-700 font-medium mt-1">{{ item.field }}</p>
            <p class="text-sm text-gray-500 mt-1 line-clamp-1">{{ item.details }}</p>
          </div>
        </div>

        <div class="h-12"></div>
      </div>

      <button 
        @click="switchToCreate"
        class="fixed bottom-6 right-6 w-16 h-16 bg-green-600 hover:bg-green-700 text-white rounded-full shadow-lg flex items-center justify-center transform hover:scale-105 transition duration-200 z-40 focus:outline-none focus:ring-4 focus:ring-green-300">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
    </div>


    <div v-if="viewMode === 'create'" class="animate-fade-in-up">
      <header class="bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center sticky top-0 z-50 shadow-sm">
        <button @click="viewMode = 'list'" class="text-gray-500 hover:text-gray-700 font-medium py-2 px-2 -ml-2">
          Hủy bỏ
        </button>
        <h1 class="text-lg font-bold text-gray-800">Ghi chép mới</h1>
        <button @click="saveEntry" class="bg-green-600 text-white px-5 py-2 rounded-lg font-bold shadow-sm hover:bg-green-700 active:bg-green-800 transition">
          Lưu
        </button>
      </header>

      <div class="p-4 space-y-6">
        
        <section class="bg-white p-4 rounded-xl shadow-sm border border-gray-100 space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Thời gian thực hiện</label>
            <input type="datetime-local" v-model="form.timestamp" class="w-full p-3 bg-gray-50 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none transition text-gray-700 font-medium">
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">Thửa ruộng</label>
            <div class="relative">
              <select v-model="form.field" class="w-full p-3 bg-gray-50 border border-gray-300 rounded-lg appearance-none focus:ring-2 focus:ring-green-500 focus:border-green-500 outline-none text-gray-700 font-medium">
                <option value="Thửa A (Gần nhà)">🏡 Thửa A (Gần nhà)</option>
                <option value="Thửa B (Bãi bồi)">🌊 Thửa B (Bãi bồi)</option>
                <option value="Thửa C (Sau đồi)">⛰️ Thửa C (Sau đồi)</option>
              </select>
              <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
              </div>
            </div>
          </div>
        </section>

        <section>
          <label class="block text-sm font-semibold text-gray-700 mb-3 ml-1">Loại công việc</label>
          <div class="grid grid-cols-3 gap-3">
            <button 
              v-for="act in activityTypes" 
              :key="act.id"
              @click="form.type = act.id"
              :class="[
                'flex flex-col items-center justify-center p-3 rounded-xl border-2 transition duration-200 h-24 shadow-sm',
                form.type === act.id 
                  ? 'border-green-500 bg-green-50 text-green-700 ring-1 ring-green-500' 
                  : 'border-transparent bg-white text-gray-600 hover:bg-gray-50'
              ]"
            >
              <span class="text-3xl mb-1 filter drop-shadow-sm">{{ act.icon }}</span>
              <span class="text-xs font-bold">{{ act.name }}</span>
            </button>
          </div>
        </section>

        <section v-if="form.type" class="bg-white p-4 rounded-xl shadow-sm border border-green-100 animate-fade-in ring-1 ring-green-500/20">
          <h3 class="text-green-700 font-bold mb-4 flex items-center border-b border-green-100 pb-2">
            <span class="mr-2 text-xl">{{ getActivityIcon(form.type) }}</span>
            Chi tiết {{ getActivityName(form.type) }}
          </h3>

          <div v-if="form.type === 'fertilizer'" class="space-y-4">
            <div>
              <label class="text-xs font-bold text-gray-500 uppercase">Tên phân bón</label>
              <input v-model="form.detailName" type="text" placeholder="VD: NPK, Đạm Phú Mỹ..." class="mt-1 w-full p-3 border rounded-lg focus:ring-green-500 focus:border-green-500">
            </div>
            <div>
              <label class="text-xs font-bold text-gray-500 uppercase">Khối lượng</label>
              <div class="flex items-center mt-1">
                <input v-model="form.detailAmount" type="number" placeholder="0" class="w-full p-3 border rounded-l-lg focus:ring-green-500 focus:border-green-500">
                <span class="bg-gray-100 border border-l-0 border-gray-200 p-3 rounded-r-lg font-bold text-gray-600">Kg</span>
              </div>
            </div>
          </div>

          <div v-else-if="form.type === 'spray'" class="space-y-4">
            <div>
              <label class="text-xs font-bold text-gray-500 uppercase">Tên thuốc</label>
              <input v-model="form.detailName" type="text" placeholder="VD: Chess 50WG..." class="mt-1 w-full p-3 border rounded-lg focus:ring-green-500 focus:border-green-500">
            </div>
            <div>
              <label class="text-xs font-bold text-gray-500 uppercase">Đối tượng phòng trừ</label>
              <input v-model="form.detailTarget" type="text" placeholder="VD: Rầy nâu, Đạo ôn..." class="mt-1 w-full p-3 border rounded-lg focus:ring-green-500 focus:border-green-500">
            </div>
          </div>

          <div v-else class="space-y-4">
            <div>
              <label class="text-xs font-bold text-gray-500 uppercase">Ghi chú công việc</label>
              <textarea v-model="form.note" rows="3" placeholder="Mô tả chi tiết..." class="mt-1 w-full p-3 border rounded-lg focus:ring-green-500 focus:border-green-500"></textarea>
            </div>
          </div>
        </section>

        <section class="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
          <label class="block text-sm font-semibold text-gray-700 mb-3">Hình ảnh thực tế</label>
          <label class="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 hover:border-green-400 transition">
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <svg class="w-10 h-10 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
              <p class="text-sm text-gray-500 font-medium">Bấm để chụp ảnh</p>
            </div>
            <input type="file" class="hidden" @change="handleImageUpload" />
          </label>
          <div v-if="form.imagePreview" class="mt-3 relative">
             <img :src="form.imagePreview" class="w-full h-48 object-cover rounded-lg shadow-md">
             <button @click="form.imagePreview = null" class="absolute top-2 right-2 bg-red-500 text-white rounded-full p-1 shadow">
               <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
             </button>
          </div>
        </section>

      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'DiaryPage',
  data() {
    return {
      viewMode: 'list', // 'list' | 'create'
      
      // Dữ liệu danh sách giả lập
      diaryList: [
        { type: 'fertilizer', title: 'Bón thúc đợt 1', field: 'Thửa A (Gần nhà)', details: 'NPK 20-20-15: 50kg', date: '07/12' },
        { type: 'spray', title: 'Phun trừ rầy', field: 'Thửa B (Bãi bồi)', details: 'Chess 50WG - Rầy nâu', date: '05/12' },
        { type: 'water', title: 'Tưới nước', field: 'Thửa A (Gần nhà)', details: 'Chạy máy 2h', date: '04/12' },
        { type: 'tillage', title: 'Làm đất gieo sạ', field: 'Thửa C (Sau đồi)', details: 'Cày ải phơi đất', date: '01/12' },
      ],

      // Cấu hình loại hoạt động
      activityTypes: [
        { id: 'tillage', name: 'Làm đất', icon: '🚜' },
        { id: 'sow', name: 'Gieo trồng', icon: '🌱' },
        { id: 'fertilizer', name: 'Bón phân', icon: '🌾' },
        { id: 'spray', name: 'Phun thuốc', icon: '💊' },
        { id: 'water', name: 'Tưới nước', icon: '💧' },
        { id: 'harvest', name: 'Thu hoạch', icon: '💰' },
      ],

      // Form data
      form: {
        timestamp: '',
        field: 'Thửa A (Gần nhà)',
        type: null,
        detailName: '',
        detailAmount: '',
        detailTarget: '',
        note: '',
        imagePreview: null
      }
    }
  },
  methods: {
    // Tiện ích ngày tháng
    getCurrentDate() {
      return new Date().toLocaleDateString('vi-VN', { weekday: 'long', day: 'numeric', month: 'numeric' });
    },
    
    // Logic hiển thị Icon/Màu sắc
    getActivityIcon(id) {
      const act = this.activityTypes.find(a => a.id === id);
      return act ? act.icon : '📝';
    },
    getActivityName(id) {
      const act = this.activityTypes.find(a => a.id === id);
      return act ? act.name : '';
    },
    getIconBgColor(type) {
      const colors = {
        fertilizer: 'bg-yellow-100 text-yellow-600',
        spray: 'bg-red-100 text-red-600',
        water: 'bg-blue-100 text-blue-600',
        harvest: 'bg-green-100 text-green-600',
        tillage: 'bg-orange-100 text-orange-600',
        sow: 'bg-emerald-100 text-emerald-600'
      };
      return colors[type] || 'bg-gray-100 text-gray-600';
    },

    // Chuyển đổi màn hình
    switchToCreate() {
      // Reset form
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      this.form.timestamp = now.toISOString().slice(0, 16);
      
      this.form.type = null;
      this.form.detailName = '';
      this.form.detailAmount = '';
      this.form.detailTarget = '';
      this.form.note = '';
      this.form.imagePreview = null;
      
      this.viewMode = 'create';
    },

    handleImageUpload(event) {
      // Giả lập preview ảnh
      const file = event.target.files[0];
      if (file) {
        this.form.imagePreview = URL.createObjectURL(file);
      }
    },

    saveEntry() {
      if (!this.form.type) {
        alert("Bác chưa chọn công việc nào cả!");
        return;
      }

      // Tạo object dữ liệu mới
      let detailsText = '';
      if (this.form.type === 'fertilizer') detailsText = `${this.form.detailName}: ${this.form.detailAmount}kg`;
      else if (this.form.type === 'spray') detailsText = `${this.form.detailName} - ${this.form.detailTarget}`;
      else detailsText = this.form.note || 'Không có ghi chú';

      const newEntry = {
        type: this.form.type,
        title: this.getActivityName(this.form.type),
        field: this.form.field,
        details: detailsText,
        date: new Date().toLocaleDateString('vi-VN', {day: '2-digit', month: '2-digit'})
      };

      // Đẩy vào đầu danh sách
      this.diaryList.unshift(newEntry);
      
      // Xong thì quay về
      alert("Đã lưu nhật ký thành công!");
      this.viewMode = 'list';
    }
  }
}
</script>

<style scoped>
/* Hiệu ứng trượt lên nhẹ nhàng khi mở form */
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Ẩn thanh cuộn ngang ở bộ lọc nhưng vẫn cho cuộn */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>