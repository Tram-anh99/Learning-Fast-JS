<template>
  <div class="min-h-screen font-sans text-gray-800 bg-slate-50 pb-28">

    <header class="sticky top-0 z-30 p-4 bg-white border-b border-gray-100 shadow-sm/50 backdrop-blur-md bg-white/90">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-extrabold tracking-tight text-green-700">Nhật Ký Đồng Ruộng</h1>
          <p class="text-sm text-gray-500 font-medium mt-0.5 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1 text-green-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" /></svg>
            Hôm nay, {{ getCurrentDate() }}
          </p>
        </div>
        <div class="flex items-center justify-center w-10 h-10 overflow-hidden bg-green-100 border-2 border-white rounded-full shadow-sm">
          <img src="https://i.pravatar.cc/150?img=3" alt="User" class="object-cover w-full h-full">
        </div>
      </div>
    </header>

    <main class="p-4 space-y-5">

      <section class="grid grid-cols-2 gap-3">
        <div class="relative flex flex-col justify-between h-24 p-4 overflow-hidden text-white bg-green-600 shadow-sm rounded-2xl">
          <span class="relative z-10 text-sm font-medium opacity-80">Công việc tuần này</span>
          <span class="relative z-10 text-3xl font-bold">12</span>
          <svg class="absolute w-20 h-20 text-green-500 opacity-50 -right-2 -bottom-4" fill="currentColor" viewBox="0 0 20 20"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" /><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" /></svg>
        </div>
         <div class="flex flex-col justify-between h-24 p-4 bg-white border border-gray-100 shadow-sm rounded-2xl">
          <span class="text-sm font-medium text-gray-500">Thửa đang canh tác</span>
          <span class="text-3xl font-bold text-gray-800">03 <span class="text-lg font-normal text-gray-400">/ 05</span></span>
        </div>
      </section>

      <section>
        <h2 class="flex items-center justify-between mb-3 text-lg font-bold text-gray-800">
          Hoạt động gần đây
          <button class="text-sm font-medium text-green-600">Xem tất cả</button>
        </h2>

        <div class="space-y-3">
          <div v-for="(item, index) in diaryList" :key="index" class="group bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex items-start transition-all duration-200 hover:shadow-md active:scale-[0.98] cursor-pointer">
            
            <div class="flex flex-col items-center justify-center flex-shrink-0 p-2 mr-4 border bg-slate-50 rounded-xl w-14 border-slate-100">
               <span class="text-xs font-bold text-red-500 uppercase">{{ item.dateMonth }}</span>
               <span class="text-2xl font-extrabold text-gray-700 leading-none mt-0.5">{{ item.dateDay }}</span>
            </div>

            <div class="flex-grow pt-1">
              <div class="flex items-start justify-between">
                <h3 class="font-bold text-gray-800 text-[17px] leading-tight group-hover:text-green-700 transition-colors">{{ item.title }}</h3>
                 <span class="ml-2 text-lg opacity-70">{{ getActivityIcon(item.type) }}</span>
              </div>
              
              <div class="flex items-center mt-2 text-sm font-medium text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" class="flex-shrink-0 w-4 h-4 mr-1 text-green-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd" /></svg>
                <span class="truncate">{{ item.field }}</span>
              </div>
              <div class="mt-1 text-sm text-gray-600 pl-5 relative before:absolute before:left-2 before:top-2 before:w-1.5 before:h-1.5 before:bg-gray-300 before:rounded-full line-clamp-2">
                 {{ item.details }}
              </div>
            </div>

          </div>
        </div>
      </section>

    </main>

    <button 
      @click="alert('Chức năng thêm mới sẽ sớm ra mắt!')"
      class="fixed z-40 flex items-center justify-center text-3xl text-white transition-transform bg-green-600 rounded-full shadow-lg bottom-20 right-4 w-14 h-14 shadow-green-600/30 active:scale-90">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" /></svg>
    </button>

    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] px-2 py-2 z-30 flex justify-around items-center pb-safe">
      <a href="#" class="flex flex-col items-center p-2 text-green-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" viewBox="0 0 20 20" fill="currentColor"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" /></svg>
        <span class="text-[11px] font-bold">Trang chủ</span>
      </a>
      <a href="#" class="flex flex-col items-center p-2 text-gray-400 transition-colors hover:text-green-600">
         <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 7m0 13V7m0 0L9 7" /></svg>
        <span class="text-[11px] font-medium">Bản đồ</span>
      </a>
       <div class="w-12"></div>

      <a href="#" class="flex flex-col items-center p-2 text-gray-400 transition-colors hover:text-green-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
        <span class="text-[11px] font-medium">Báo cáo</span>
      </a>
      <a href="#" class="flex flex-col items-center p-2 text-gray-400 transition-colors hover:text-green-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
        <span class="text-[11px] font-medium">Tài khoản</span>
      </a>
    </nav>

  </div>
</template>

<script>
export default {
  name: 'DiaryPageModern',
  data() {
    return {
      // Dữ liệu mẫu đã được tách ngày/tháng để hiển thị đẹp hơn
      diaryList: [
        { type: 'fertilizer', title: 'Bón thúc đợt 1', field: 'Thửa A (Gần nhà)', details: 'Sử dụng NPK 20-20-15. Liều lượng 50kg/công. Thời tiết mát mẻ.', dateDay: '08', dateMonth: 'T12' },
        { type: 'spray', title: 'Phun thuốc trừ rầy', field: 'Thửa B (Bãi bồi)', details: 'Phát hiện rầy nâu mật độ cao. Phun kèm thuốc bám dính.', dateDay: '05', dateMonth: 'T12' },
        { type: 'water', title: 'Tưới nước', field: 'Thửa A (Gần nhà)', details: 'Chạy máy bơm 2 giờ để giữ ẩm chân ruộng.', dateDay: '04', dateMonth: 'T12' },
        { type: 'tillage', title: 'Làm đất gieo sạ', field: 'Thửa C (Sau đồi)', details: 'Cày ải phơi đất chuẩn bị cho vụ Đông Xuân.', dateDay: '01', dateMonth: 'T12' },
        { type: 'sow', title: 'Xuống giống lúa', field: 'Thửa D (Mới thuê)', details: 'Gieo sạ giống ST25. Mật độ 120kg/ha.', dateDay: '28', dateMonth: 'T11' },
      ],
      activityTypes: [
        { id: 'tillage', icon: '🚜' },
        { id: 'sow', icon: '🌱' },
        { id: 'fertilizer', icon: '🌾' },
        { id: 'spray', icon: '💊' },
        { id: 'water', icon: '💧' },
        { id: 'harvest', icon: '💰' },
      ],
    }
  },
  methods: {
    getCurrentDate() {
        // Hàm lấy ngày tháng năm hiện tại
      return new Date().toLocaleDateString('vi-VN', { day: 'numeric', month: 'long', year: 'numeric' });
    },
    getActivityIcon(id) {
      const act = this.activityTypes.find(a => a.id === id);
      return act ? act.icon : '📝';
    },
     alert(msg) {
        // Hàm alert tạm thời
        window.alert(msg);
    }
  }
}
</script>

<style scoped>
/* Hỗ trợ padding cho các thiết bị có tai thỏ (iPhone X trở lên) ở dưới đáy */
.pb-safe {
    padding-bottom: env(safe-area-inset-bottom, 8px);
}
</style>