<script setup>
import { onMounted } from 'vue';
import { useMapLogic } from '../composables/useMapLogic';

const props = defineProps({
      danhSachVung: { type: Array, required: true },
      diemNongSauBenh: { type: Array, required: true }
});

const { mapContainer, cheDoXem, batCheDoSauBenh, batCheDoHanhChinh, initMap, vẽMarkerVùng } = useMapLogic();

onMounted(() => {
      initMap();
      vẽMarkerVùng(props.danhSachVung);
});

const handleBatCheDoSauBenh = () => batCheDoSauBenh(props.diemNongSauBenh);
</script>

<template>
      <div class="flex-[2] relative rounded-xl overflow-hidden shadow-md border border-white">
            <div ref="mapContainer" class="z-0 w-full h-full"></div>

            <div class="absolute top-5 right-5 z-50 bg-white p-2.5 rounded-lg shadow-lg flex flex-col gap-2 w-44">
                  <h4 class="m-0 text-xs font-semibold uppercase text-slate-600">
                        <i class="fas fa-layer-group"></i> Lớp dữ liệu
                  </h4>

                  <button :class="{ 'map-control-btn-active': cheDoXem === 'hanh_chinh' }" @click="batCheDoHanhChinh"
                        class="map-control-btn">
                        <i class="fas fa-map"></i> Hành chính
                  </button>

                  <button :class="{ 'map-control-btn-active': cheDoXem === 'sau_benh' }" @click="handleBatCheDoSauBenh"
                        class="map-control-btn">
                        <i class="fas fa-biohazard"></i> Mật độ Sâu bệnh
                  </button>

                  <button :class="{ 'map-control-btn-active': cheDoXem === 'phan_bon' }" class="map-control-btn">
                        <i class="fas fa-flask"></i> Dư lượng Thuốc
                  </button>
            </div>
      </div>
</template>
