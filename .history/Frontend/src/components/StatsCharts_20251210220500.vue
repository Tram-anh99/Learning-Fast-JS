<template>
  <div class="grid grid-cols-1 gap-6 mb-8 md:grid-cols-2">
    
    <div class="p-5 bg-white border border-gray-100 shadow-sm rounded-2xl">
      <h3 class="mb-4 font-bold text-gray-800">Thống kê sử dụng thuốc BVTV (Quý 3/2023)</h3>
      <div class="relative h-64">
        <Bar :data="barData" :options="barOptions" />
      </div>
    </div>

    <div class="p-5 bg-white border border-gray-100 shadow-sm rounded-2xl">
      <h3 class="mb-4 font-bold text-gray-800">Tổng quan sử dụng phân bón</h3>
      <div class="relative flex justify-center h-64">
        <Doughnut :data="pieData" :options="pieOptions" />
      </div>
    </div>

  </div>
</template>

<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
} from 'chart.js'
import { Bar, Doughnut } from 'vue-chartjs'

// 1. Đăng ký các thành phần biểu đồ cần dùng
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement)

// ============ CẤU HÌNH BIỂU ĐỒ CỘT (BAR) ============
const barData = {
  labels: ['Tháng 1', 'Tháng 2', 'Tháng 3'],
  datasets: [
    {
      label: 'Hóa học',
      backgroundColor: '#2563eb', // Màu xanh dương đậm
      data: [2200, 1800, 2300],
      borderRadius: 4
    },
    {
      label: 'Sinh học',
      backgroundColor: '#0d9488', // Màu xanh cổ vịt
      data: [900, 1400, 1200],
      borderRadius: 4
    },
    {
      label: 'Thảo mộc',
      backgroundColor: '#84cc16', // Màu xanh lá mạ
      data: [300, 600, 800],
      borderRadius: 4
    }
  ]
}

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' }
  },
  scales: {
    y: { beginAtZero: true }
  }
}

// ============ CẤU HÌNH BIỂU ĐỒ TRÒN (DOUGHNUT) ============
const pieData = {
  labels: ['Phân hữu cơ', 'Phân vô cơ', 'Phân vi sinh'],
  datasets: [
    {
      backgroundColor: ['#2563eb', '#0d9488', '#84cc16'], // Màu giống cột bên kia
      data: [45, 30, 25],
      hoverOffset: 4
    }
  ]
}

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'right' } // Chú thích nằm bên phải
  }
}
</script>