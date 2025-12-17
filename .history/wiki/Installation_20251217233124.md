# 🛠️ Cài Đặt / Installation

## Yêu cầu hệ thống / System Requirements

| Yêu cầu | Phiên bản                     |
| ------- | ----------------------------- |
| Node.js | 18.x trở lên                  |
| npm     | 9.x hoặc yarn 1.22.x          |
| Git     | Latest                        |
| Browser | Chrome, Firefox, Safari, Edge |

---

## Bước 1: Clone Repository

```bash
git clone https://github.com/Tram-anh99/Learning-Fast-JS.git
cd Learning-Fast-JS
```

---

## Bước 2: Cài đặt Frontend

```bash
cd Frontend
npm install
```

### Dependencies chính / Main Dependencies

| Package     | Version | Mô tả                    |
| ----------- | ------- | ------------------------ |
| vue         | 3.5.13  | Framework chính          |
| vite        | 6.0.1   | Build tool               |
| tailwindcss | 3.4.19  | CSS framework            |
| leaflet     | 1.9.4   | WebGIS maps              |
| chart.js    | 4.5.1   | Charts library           |
| vue-chartjs | 5.3.2   | Vue wrapper for Chart.js |
| qrcode.vue3 | 3.1.8   | QR code generation       |
| vue-router  | 4.5.0   | Routing                  |

---

## Bước 3: Cấu hình môi trường (Tùy chọn)

Tạo file `.env` trong folder `Frontend/`:

```env
VITE_API_URL=http://localhost:3000/api
VITE_MAP_TILE_URL=https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
```

---

## Bước 4: Chạy Development Server

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: `http://localhost:5173`

---

## Bước 5: Build Production

```bash
npm run build
```

Output sẽ nằm trong folder `dist/`

---

## 📱 Test trên Mobile

Để test trên điện thoại cùng mạng LAN:

```bash
npm run dev -- --host
```

Sau đó truy cập bằng IP máy tính: `http://192.168.x.x:5173`

---

## ❓ Troubleshooting

### Lỗi npm install

```bash
# Clear cache và cài lại
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Lỗi port đã được sử dụng

```bash
# Chạy với port khác
npm run dev -- --port 3000
```

### Lỗi Leaflet không hiển thị

Kiểm tra file `main.css` đã import Leaflet CSS:

```css
@import "leaflet/dist/leaflet.css";
```
