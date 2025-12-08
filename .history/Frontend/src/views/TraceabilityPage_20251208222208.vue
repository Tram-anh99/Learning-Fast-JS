<template>
  <div class="min-h-screen pb-10 font-sans bg-gray-50">
    
    <div class="relative bg-white pb-6 rounded-b-[30px] shadow-sm overflow-hidden">
      <div class="absolute inset-0 h-32 bg-green-600"></div>
      
      <div class="relative flex flex-col items-center px-4 pt-12">
        <div class="z-10 w-32 h-32 overflow-hidden bg-white border-4 border-white rounded-full shadow-lg">
          <img src="https://images.unsplash.com/photo-1591586520286-df059a495743?q=80&w=200" alt="Sản phẩm" class="object-cover w-full h-full">
        </div>

        <h1 class="mt-3 text-2xl font-extrabold text-center text-gray-800">Xoài Cát Hòa Lộc</h1>
        <div class="flex gap-2 mt-2">
          <span class="px-3 py-1 text-xs font-bold text-green-700 bg-green-100 border border-green-200 rounded-full">VietGAP</span>
          <span class="px-3 py-1 text-xs font-bold text-blue-700 bg-blue-100 border border-blue-200 rounded-full">OCOP 4 Sao</span>
        </div>

        <p class="mt-2 text-xs text-gray-400">Mã lô: 2023-XL-005</p>
      </div>
    </div>

    <div class="px-4 mt-6">
      <h2 class="flex items-center mb-3 text-lg font-bold text-gray-800">
        <span class="w-1 h-6 mr-2 bg-green-600 rounded-full"></span>
        Thông tin nhà vườn
      </h2>
      <div class="flex items-start p-4 bg-white border border-gray-100 shadow-sm rounded-xl">
        <img src="https://i.pravatar.cc/150?img=11" class="w-12 h-12 mr-3 border border-gray-200 rounded-full">
        <div>
          <p class="font-bold text-gray-800">Hộ canh tác: Nguyễn Văn A</p>
          <p class="mt-1 text-sm text-gray-500">Hợp tác xã Nông nghiệp Mỹ Xương</p>
          <p class="flex items-center mt-1 text-sm text-gray-500">
            <svg class="w-4 h-4 mr-1 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z"/></svg>
            Cao Lãnh, Đồng Tháp
          </p>
        </div>
      </div>
    </div>

    <div class="px-4 mt-6">
      <h2 class="flex items-center mb-3 text-lg font-bold text-gray-800">
        <span class="w-1 h-6 mr-2 bg-green-600 rounded-full"></span>
        Vị trí vùng trồng
      </h2>
      <div class="p-2 bg-white border border-gray-100 shadow-sm rounded-xl">
        <div class="relative w-full h-48 overflow-hidden rounded-lg cursor-pointer bg-slate-200 group">
          <iframe 
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3925.337142490799!2d105.787682!3d10.314876!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMTDCsDE4JzUzLjYiTiAxMDXCsDQ3JzE1LjciRQ!5e0!3m2!1svi!2s!4v1639038290000!5m2!1svi!2s" 
            width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy">
          </iframe>
          
          <div class="absolute px-2 py-1 text-xs font-bold text-green-700 rounded shadow bottom-2 right-2 bg-white/90 backdrop-blur">
            📍 Xem trên bản đồ lớn
          </div>
        </div>
        <p class="mt-2 text-xs italic text-center text-gray-500">Dữ liệu GIS được xác thực bởi Sở NN&PTNT</p>
      </div>
    </div>

    <div class="px-4 mt-6">
      <h2 class="flex items-center mb-3 text-lg font-bold text-gray-800">
        <span class="w-1 h-6 mr-2 bg-green-600 rounded-full"></span>
        Hành trình sinh trưởng
      </h2>
      
      <div class="p-5 bg-white border border-gray-100 shadow-sm rounded-xl">
        <div class="relative pb-6 pl-6 border-l-2 border-green-200 last:pb-0 last:border-0">
          <div class="absolute -left-[9px] top-0 w-4 h-4 bg-green-500 rounded-full border-2 border-white shadow"></div>
          <div class="flex items-start justify-between">
            <h3 class="text-sm font-bold text-gray-800">Thu hoạch & Đóng gói</h3>
            <span class="text-xs font-semibold bg-green-100 text-green-800 px-2 py-0.5 rounded">08/12</span>
          </div>
          <p class="mt-1 text-sm text-gray-500">Thu hoạch lứa 1, trọng lượng trung bình 350g/trái.</p>
        </div>

        <div class="relative pb-6 pl-6 border-l-2 border-green-200">
          <div class="absolute -left-[9px] top-0 w-4 h-4 bg-gray-300 rounded-full border-2 border-white"></div>
          <div class="flex items-start justify-between">
            <h3 class="text-sm font-bold text-gray-600">Kiểm định dư lượng</h3>
            <span class="text-xs text-gray-400">01/12</span>
          </div>
          <p class="mt-1 text-sm text-gray-500">Đạt chuẩn an toàn thực phẩm. Không phát hiện thuốc BVTV.</p>
          <div class="inline-flex items-center px-2 py-1 mt-2 text-xs text-blue-600 rounded cursor-pointer bg-blue-50">
            📄 Xem phiếu kết quả
          </div>
        </div>

        <div class="relative pb-0 pl-6 border-l-2 border-transparent">
           <div class="absolute -left-[9px] top-0 w-4 h-4 bg-gray-300 rounded-full border-2 border-white"></div>
           <div class="flex items-start justify-between">
            <h3 class="text-sm font-bold text-gray-600">Xuống giống</h3>
            <span class="text-xs text-gray-400">15/08</span>
          </div>
          <p class="mt-1 text-sm text-gray-500">Gieo trồng tại thửa số 5.</p>
        </div>
      </div>
    </div>

    <div class="px-4 mt-8 mb-4">
        <button class="flex items-center justify-center w-full py-3 font-bold text-white transition transform bg-green-600 shadow-lg hover:bg-green-700 rounded-xl shadow-green-600/30 active:scale-95">
            <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
            Liên hệ mua hàng
        </button>
        <p class="mt-4 text-xs text-center text-gray-400">Powered by WebGIS Master Thesis © 2025</p>
    </div>

  </div>
</template>

<script>
export default {
  name: 'TraceabilityPage',
  // Sau này bạn sẽ dùng ID từ URL để gọi API lấy dữ liệu thật
  // mounted() {
  //   const productId = this.$route.params.id; 
  //   // Call API(productId) ...
  // }
}
</script>