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
     labels: [
          "Lúa",
          "Xoài",
          "Thanh long",
          "Cà phê",
          "Tiêu",
          "Dừa",
          "Sầu riêng",
          "Rau củ",
     ],
     datasets: [
          {
               label: "Trung Quốc",
               data: [6500, 7200, 8500, 4200, 5800, 3500, 9200, 2800],
               borderColor: "#FF6B6B",
               backgroundColor: "rgba(255, 107, 107, 0.07)",
               borderWidth: 2.1,
               tension: 0.4,
               fill: true,
               pointRadius: 3.5,
               pointBackgroundColor: "#FF6B6B",
               pointBorderColor: "#fff",
               pointBorderWidth: 1.2,
          },
          {
               label: "Hoa Kỳ",
               data: [4200, 6800, 7500, 5500, 4200, 2800, 5500, 1500],
               borderColor: "#4ECDC4",
               backgroundColor: "rgba(78, 205, 196, 0.07)",
               borderWidth: 2.1,
               tension: 0.4,
               fill: true,
               pointRadius: 3.5,
               pointBackgroundColor: "#4ECDC4",
               pointBorderColor: "#fff",
               pointBorderWidth: 1.2,
          },
          {
               label: "Châu Âu",
               data: [3500, 5200, 6800, 7200, 6500, 2200, 3800, 2500],
               borderColor: "#FFE66D",
               backgroundColor: "rgba(255, 230, 109, 0.07)",
               borderWidth: 2.1,
               tension: 0.4,
               fill: true,
               pointRadius: 3.5,
               pointBackgroundColor: "#FFE66D",
               pointBorderColor: "#fff",
               pointBorderWidth: 1.2,
          },
          {
               label: "Nhật Bản",
               data: [2800, 4500, 5200, 6800, 3500, 1800, 4200, 1200],
               borderColor: "#95E1D3",
               backgroundColor: "rgba(149, 225, 211, 0.07)",
               borderWidth: 2.1,
               tension: 0.4,
               fill: true,
               pointRadius: 3.5,
               pointBackgroundColor: "#95E1D3",
               pointBorderColor: "#fff",
               pointBorderWidth: 1.2,
          },
          {
               label: "ASEAN",
               data: [5500, 3200, 4800, 2500, 1800, 4200, 2500, 5800],
               borderColor: "#A8DADC",
               backgroundColor: "rgba(168, 218, 220, 0.07)",
               borderWidth: 2.1,
               tension: 0.4,
               fill: true,
               pointRadius: 3.5,
               pointBackgroundColor: "#A8DADC",
               pointBorderColor: "#fff",
               pointBorderWidth: 1.2,
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
                    font: { size: 10.5, weight: 400 },
                    color: "#374151",
                    padding: 15,
                    usePointStyle: true,
                    pointStyle: "circle",
                    boxWidth: 8.5,
                    boxHeight: 8.5,
               },
          },
          tooltip: {
               backgroundColor: "rgba(0, 0, 0, 0.85)",
               padding: 9,
               titleFont: { size: 11.5, weight: 600 },
               bodyFont: { size: 10.5 },
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
               title: {
                    display: true,
                    text: "Sản lượng xuất khẩu (tấn)",
                    font: { size: 11, weight: 600 },
                    color: "#374151",
                    padding: 8,
               },
               ticks: {
                    font: { size: 9.5 },
                    color: "#9CA3AF",
                    padding: 6,
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
               title: {
                    display: true,
                    text: "Loại cây trồng",
                    font: { size: 11, weight: 600 },
                    color: "#374151",
                    padding: 8,
               },
               ticks: {
                    font: { size: 9.5, weight: 400 },
                    color: "#374151",
                    padding: 9,
                    maxRotation: 25,
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
