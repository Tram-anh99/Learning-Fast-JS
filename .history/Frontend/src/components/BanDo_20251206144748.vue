<script setup>
import { ref } from 'vue';
import BanDo from './components/BanDo.vue';

// DỮ LIỆU TẬP TRUNG TẠI ĐÂY (Single Source of Truth)
const danhSachVung = ref([
      {
            id: 1,
            maSo: 'VT-001',
            ten: 'Xoài Cát Chu',
            toaDo: [ // Thêm tọa độ vào đây
                  [10.762, 106.660],
                  [10.770, 106.670],
                  [10.760, 106.670]
            ]
      },
      {
            id: 2,
            maSo: 'VT-002',
            ten: 'Thanh Long',
            // Tạm thời để null hoặc tọa độ giả khác để test sau
            toaDo: []
      }
]);

const chonVung = (vung) => {
      console.log("Chọn vùng:", vung);
};
</script>

<template>
      <div class="webgis-layout">
            <aside class="sidebar">
                  <div class="list-container">
                        <ul>
                              <li v-for="vung in danhSachVung" :key="vung.id" @click="chonVung(vung)" class="list-item">
                                    <strong>{{ vung.maSo }}</strong> - {{ vung.ten }}
                              </li>
                        </ul>
                  </div>
            </aside>

            <main class="map-wrapper">
                  <BanDo :duLieuDauVao="danhSachVung" />
            </main>
      </div>
</template>