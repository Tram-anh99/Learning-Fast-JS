/**
 * ========== COMPOSABLE: useLineChartData.js ==========
 * Purpose: Cung cấp dữ liệu cho biểu đồ đường
 * Hiển thị mối quan hệ giữa thị trường xuất khẩu và loại cây
 */

/**
 * Dữ liệu biểu đồ đường: Mối quan hệ thị trường - Loại cây
 *
 * Thông tin:
 *   - labels: Các loại cây trồng
 *   - datasets: Mỗi dataset là một thị trường xuất khẩu với dữ liệu sản lượng/giá trị
 */
const lineChartData = {
     labels: ["Lúa", "Xoài", "Thanh long", "Cà phê", "Tiêu", "Dâu tây"],
     datasets: [
          {
               label: "Nhật Bản",
               data: [4500, 8200, 6800, 3200, 2100, 9500],
               borderColor: "#FF6B6B",
               backgroundColor: "rgba(255, 107, 107, 0.05)",
               borderWidth: 2,
               tension: 0.4,
               fill: true,
               pointRadius: 3,
               pointBackgroundColor: "#FF6B6B",
               pointBorderColor: "#fff",
               pointBorderWidth: 1,
          },
          {
               label: "Mỹ",
               data: [3800, 6500, 7200, 4800, 3500, 8200],
               borderColor: "#4ECDC4",
               backgroundColor: "rgba(78, 205, 196, 0.05)",
               borderWidth: 2,
               tension: 0.4,
               fill: true,
               pointRadius: 3,
               pointBackgroundColor: "#4ECDC4",
               pointBorderColor: "#fff",
               pointBorderWidth: 1,
          },
          {
               label: "EU",
               data: [5200, 7100, 5500, 6200, 4800, 7800],
               borderColor: "#FFE66D",
               backgroundColor: "rgba(255, 230, 109, 0.05)",
               borderWidth: 2,
               tension: 0.4,
               fill: true,
               pointRadius: 3,
               pointBackgroundColor: "#FFE66D",
               pointBorderColor: "#fff",
               pointBorderWidth: 1,
          },
          {
               label: "Trung Quốc",
               data: [6200, 4500, 8100, 7500, 5600, 3200],
               borderColor: "#95E1D3",
               backgroundColor: "rgba(149, 225, 211, 0.05)",
               borderWidth: 2,
               tension: 0.4,
               fill: true,
               pointRadius: 3,
               pointBackgroundColor: "#95E1D3",
               pointBorderColor: "#fff",
               pointBorderWidth: 1,
          },
     ],
};

/**
 * Chart.js options cho biểu đồ đường
 */
const lineChartOptions = {
     responsive: true,
     maintainAspectRatio: true,
     plugins: {
          legend: {
               position: "bottom",
               labels: {
                    font: { size: 10, weight: 400 },
                    color: "#374151",
                    padding: 8,
                    usePointStyle: true,
                    pointStyle: "circle",
                    boxWidth: 8,
                    boxHeight: 8,
               },
          },
          tooltip: {
               backgroundColor: "rgba(0, 0, 0, 0.85)",
               padding: 8,
               titleFont: { size: 11, weight: 600 },
               bodyFont: { size: 10 },
               borderColor: "rgba(255, 255, 255, 0.2)",
               borderWidth: 1,
               displayColors: true,
               callbacks: {
                    label: (context) => {
                         return `${
                              context.dataset.label
                         }: ${context.parsed.y.toLocaleString("vi-VN")} tấn`;
                    },
               },
          },
     },
     scales: {
          y: {
               beginAtZero: true,
               max: 10000,
               ticks: {
                    font: { size: 9 },
                    color: "#9CA3AF",
                    padding: 5,
                    callback: (value) => {
                         return value.toLocaleString("vi-VN");
                    },
               },
               grid: {
                    color: "rgba(0, 0, 0, 0.05)",
                    drawBorder: false,
               },
          },
          x: {
               ticks: {
                    font: { size: 10, weight: 400 },
                    color: "#374151",
                    padding: 8,
                    maxRotation: 0,
                    minRotation: 0,
               },
               grid: {
                    display: false,
                    drawBorder: false,
               },
          },
     },
};

export { lineChartData, lineChartOptions };
