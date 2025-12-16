#!/bin/bash

# Script to create bilingual GitHub issues for Learning-Fast-JS project
# Usage: ./create-github-issues-bilingual.sh

REPO="Tram-anh99/Learning-Fast-JS"

echo "🚀 Creating Bilingual GitHub Issues for $REPO..."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed!"
    echo "📥 Install with: brew install gh"
    echo "Then authenticate with: gh auth login"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub!"
    echo "🔐 Run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is ready!"
echo ""

# Issue #1: Camera QR Scan Integration
echo "Creating Issue #1: Tích hợp Quét QR bằng Camera | Camera QR Scan Integration..."
gh issue create \
  --repo "$REPO" \
  --title "📷 Tích hợp Quét QR bằng Camera | Camera QR Scan Integration" \
  --label "enhancement,feature,camera,qr-code,phase-2" \
  --body "## 📷 Tích hợp Quét QR bằng Camera | Camera QR Scan Integration

### 📝 Mô tả | Description
**[VI]** Triển khai quét mã QR trực tiếp bằng camera thiết bị sử dụng thư viện html5-qrcode, cho phép người dùng quét mã QR thay vì nhập thủ công.

**[EN]** Implement real-time camera QR code scanning using html5-qrcode library to allow users to scan QR codes directly from their device camera instead of manual input.

---

### 📊 Trạng thái hiện tại | Current State
- ✅ QRScanner.vue modal đã có với nhập liệu thủ công | Modal exists with manual input
- ✅ Placeholder sẵn sàng cho quét camera | Placeholder ready for camera scan
- ❌ Chưa tích hợp thư viện html5-qrcode | html5-qrcode library not integrated

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Cài đặt package | Install package
\`\`\`bash
npm install html5-qrcode
\`\`\`

**Bước 2 | Step 2:** Cập nhật QRScanner.vue
- [VI] Thêm container hiển thị camera
- [EN] Add camera preview container
- [VI] Khởi tạo Html5Qrcode scanner
- [EN] Initialize Html5Qrcode scanner
- [VI] Xử lý callback khi quét thành công
- [EN] Handle successful scan callback
- [VI] Xử lý lỗi quét
- [EN] Handle scan errors
- [VI] Yêu cầu quyền truy cập camera
- [EN] Request camera permissions
- [VI] Dừng camera khi đóng modal
- [EN] Stop camera on modal close

**Bước 3 | Step 3:** Thêm nút chuyển đổi camera | Add camera toggle button

**Bước 4 | Step 4:** Kiểm thử trên thiết bị di động | Test on mobile devices (iOS/Android)

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Hiển thị camera preview trong modal QRScanner | [EN] Camera preview shows in modal
- [ ] [VI] Quét thành công mã QR từ camera | [EN] Successfully scans QR codes from camera
- [ ] [VI] Tự động chuyển đến trang chi tiết sau khi quét | [EN] Auto-redirects to product details
- [ ] [VI] Xử lý quyền camera hợp lý | [EN] Handles camera permissions gracefully
- [ ] [VI] Hoạt động trên trình duyệt mobile | [EN] Works on mobile browsers (iOS/Android)
- [ ] [VI] Có fallback về nhập thủ công | [EN] Fallback to manual input if unavailable

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Files:** \`Frontend/src/components/QRScanner.vue\`, \`package.json\`

**Dependencies:** html5-qrcode: ^2.3.8

**Độ ưu tiên | Priority:** 🔴 Cao | High"

echo ""

# Issue #2: PWA Offline Mode
echo "Creating Issue #2: Chế độ Offline PWA | PWA Offline Mode..."
gh issue create \
  --repo "$REPO" \
  --title "📱 Chế độ Offline PWA | PWA Offline Mode Implementation" \
  --label "enhancement,pwa,offline,service-worker,phase-2" \
  --body "## 📱 Triển khai Chế độ Offline PWA | PWA Offline Mode Implementation

### 📝 Mô tả | Description
**[VI]** Chuyển đổi ứng dụng thành Progressive Web App (PWA) với khả năng offline, cho phép người dùng truy cập các tính năng cơ bản mà không cần kết nối internet.

**[EN]** Convert the application to a Progressive Web App (PWA) with offline capabilities, allowing users to access basic features without internet connection.

---

### 📊 Trạng thái hiện tại | Current State
- ❌ Chưa có service worker | No service worker
- ❌ Chưa có PWA manifest | No PWA manifest
- ❌ Chưa có fallback offline | No offline fallback

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Cài đặt Vite PWA plugin
\`\`\`bash
npm install vite-plugin-pwa -D
\`\`\`

**Bước 2 | Step 2:** Tạo manifest.json
- [VI] Tên ứng dụng, icons, màu theme
- [EN] App name, icons, theme colors
- [VI] Chế độ hiển thị: standalone
- [EN] Display mode: standalone
- [VI] Cấu hình Start URL
- [EN] Start URL configuration

**Bước 3 | Step 3:** Triển khai Service Worker
- [VI] Cache tài nguyên tĩnh (CSS, JS, images)
- [EN] Cache static assets (CSS, JS, images)
- [VI] Cache API responses
- [EN] Cache API responses
- [VI] Trang fallback offline
- [EN] Offline fallback page
- [VI] Background sync cho diary entries
- [EN] Background sync for diary entries

**Bước 4 | Step 4:** Thêm prompt cài đặt cho mobile | Add install prompt for mobile

**Bước 5 | Step 5:** Thêm chỉ báo offline trong UI | Add offline indicator in UI

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Ứng dụng có thể cài đặt trên thiết bị di động | [EN] App installable on mobile devices
- [ ] [VI] Tài nguyên tĩnh được cache và truy cập offline | [EN] Static assets cached and accessible offline
- [ ] [VI] Chỉ báo offline hiển thị khi mất kết nối | [EN] Offline indicator shows when no connection
- [ ] [VI] Diary entries lưu local và sync khi online | [EN] Diary entries saved locally and synced when online
- [ ] [VI] Map tiles được cache cho khu vực thường xuyên | [EN] Map tiles cached for frequently visited areas
- [ ] [VI] Hoạt động offline sau lần truy cập đầu tiên | [EN] Works offline after first visit

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Files mới | New files:**
- \`Frontend/public/manifest.json\`
- \`Frontend/src/registerServiceWorker.js\`

**Files sửa | Files to modify:**
- \`Frontend/vite.config.js\`
- \`Frontend/index.html\`

**Dependencies:**
- vite-plugin-pwa: ^0.17.0
- workbox-window: ^7.0.0

**Độ ưu tiên | Priority:** 🟡 Trung bình | Medium"

echo ""

# Issue #3: Push Notifications
echo "Creating Issue #3: Thông báo Push | Push Notifications..."
gh issue create \
  --repo "$REPO" \
  --title "🔔 Thông báo Push cho Cảnh báo | Push Notifications for Alerts" \
  --label "enhancement,notifications,push,backend,phase-2" \
  --body "## 🔔 Thông báo Push cho Cảnh báo | Push Notifications for Alerts

### 📝 Mô tả | Description
**[VI]** Triển khai hệ thống thông báo push để cảnh báo người dùng về các sự kiện quan trọng như cảnh báo sâu bệnh, nhắc nhở thu hoạch, và cảnh báo hệ thống.

**[EN]** Implement push notifications to alert users about important events such as pest warnings, harvest reminders, and system alerts.

---

### 📊 Trạng thái hiện tại | Current State
- ❌ Chưa có hệ thống thông báo | No notification system
- ❌ Chưa có backend notification service | No backend notification service

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Frontend - Web Push API
- [VI] Yêu cầu quyền thông báo | [EN] Request notification permissions
- [VI] Subscribe push notifications | [EN] Subscribe to push notifications
- [VI] Xử lý hiển thị thông báo | [EN] Handle notification display
- [VI] Xử lý click thông báo | [EN] Handle notification clicks

**Bước 2 | Step 2:** Backend - Push notification service
- [VI] Tích hợp FCM (Firebase Cloud Messaging) | [EN] FCM integration
- [VI] Triggers thông báo: | [EN] Notification triggers:
  - Cảnh báo sâu bệnh | Pest/disease warnings
  - Nhắc nhở thu hoạch | Harvest reminders
  - Cảnh báo thời tiết | Weather alerts
  - Thông báo hệ thống | System notifications

**Bước 3 | Step 3:** Thêm tùy chọn thông báo trong settings | Add notification preferences

**Bước 4 | Step 4:** Thêm lịch sử thông báo | Add notification history/logs

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Người dùng có thể bật/tắt thông báo | [EN] Users can enable/disable notifications
- [ ] [VI] Thông báo hoạt động trên desktop browsers | [EN] Notifications work on desktop browsers
- [ ] [VI] Thông báo hoạt động trên mobile (PWA) | [EN] Notifications work on mobile (PWA)
- [ ] [VI] Người dùng tùy chỉnh loại thông báo | [EN] Users can customize notification types
- [ ] [VI] Thông báo link đến trang liên quan | [EN] Notifications link to relevant pages
- [ ] [VI] Lịch sử thông báo có thể truy cập | [EN] Notification history accessible

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Files mới | New files:**
- \`Frontend/src/composables/useNotifications.js\`
- \`Backend/services/notificationService.js\`

**Files sửa | Files to modify:**
- \`Frontend/src/views/SettingsView.vue\` (new)
- Service worker for notification handling

**Dependencies:** firebase: ^10.7.0 (optional, for FCM)

**Độ ưu tiên | Priority:** 🟡 Trung bình | Medium"

echo ""

# Issue #4: Export PDF/Excel
echo "Creating Issue #4: Xuất báo cáo PDF/Excel | Export PDF/Excel Reports..."
gh issue create \
  --repo "$REPO" \
  --title "📄 Xuất Báo cáo Dashboard (PDF/Excel) | Export Dashboard Reports" \
  --label "enhancement,export,pdf,excel,reporting,phase-2" \
  --body "## 📄 Xuất Báo cáo Dashboard (PDF/Excel) | Export Dashboard Reports

### 📝 Mô tả | Description
**[VI]** Cho phép người dùng xuất dữ liệu dashboard, thống kê và biểu đồ sang định dạng PDF và Excel để báo cáo và lưu trữ.

**[EN]** Allow users to export dashboard data, statistics, and charts to PDF and Excel formats for reporting and record-keeping.

---

### 📊 Trạng thái hiện tại | Current State
- ❌ Chưa có chức năng xuất | No export functionality
- ❌ Dữ liệu chỉ xem trong app | Data only viewable in-app

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Xuất PDF | PDF Export
- [VI] Sử dụng jsPDF + html2canvas | [EN] Use jsPDF + html2canvas
- [VI] Xuất layout dashboard với biểu đồ | [EN] Export dashboard layout with charts
- [VI] Xuất chi tiết cây trồng với timeline | [EN] Export crop details with timeline
- [VI] Xuất lịch sử nhật ký | [EN] Export diary history
- [VI] Thêm logo/header công ty | [EN] Add company logo/header

**Bước 2 | Step 2:** Xuất Excel | Excel Export
- [VI] Sử dụng thư viện xlsx | [EN] Use xlsx library
- [VI] Xuất DataTable sang Excel | [EN] Export DataTable to Excel
- [VI] Xuất tổng hợp thống kê | [EN] Export statistics summary
- [VI] Xuất diary entries | [EN] Export diary entries
- [VI] Nhiều sheets mỗi workbook | [EN] Multiple sheets per workbook

**Bước 3 | Step 3:** Thêm nút xuất ở các views liên quan | Add export buttons to relevant views

**Bước 4 | Step 4:** Thêm dialog tùy chọn xuất | Add export options dialog (format, date range)

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Dashboard xuất PDF với biểu đồ nguyên vẹn | [EN] Dashboard exports to PDF with charts intact
- [ ] [VI] DataTable xuất Excel (.xlsx) | [EN] DataTable exports to Excel (.xlsx)
- [ ] [VI] Lịch sử Diary xuất cả 2 định dạng | [EN] Diary history exports to both formats
- [ ] [VI] Files xuất có metadata (ngày, người dùng) | [EN] Exported files include metadata (date, user)
- [ ] [VI] Biểu đồ render đúng trong PDF | [EN] Charts render correctly in PDF
- [ ] [VI] Dữ liệu Excel format đúng | [EN] Excel data properly formatted
- [ ] [VI] Download hoạt động trên mọi browser | [EN] File download works on all browsers

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Files mới | New files:**
- \`Frontend/src/utils/exportToPDF.js\`
- \`Frontend/src/utils/exportToExcel.js\`

**Files sửa | Files to modify:**
- \`Frontend/src/views/QuanLyView.vue\`
- \`Frontend/src/views/DiaryPage.vue\`
- \`Frontend/src/components/DataTableComponent.vue\`

**Dependencies:**
- jspdf: ^2.5.1
- html2canvas: ^1.4.1
- xlsx: ^0.18.5

**Độ ưu tiên | Priority:** 🟡 Trung bình | Medium"

echo ""

# Issue #5: Multi-Language Support
echo "Creating Issue #5: Hỗ trợ Đa ngôn ngữ | Multi-Language Support..."
gh issue create \
  --repo "$REPO" \
  --title "🌐 Hỗ trợ Đa ngôn ngữ (Việt/Anh) | Multi-Language Support (VI/EN)" \
  --label "enhancement,i18n,localization,multi-language,phase-2" \
  --body "## 🌐 Hỗ trợ Đa ngôn ngữ (Việt/Anh) | Multi-Language Support (Vietnamese/English)

### 📝 Mô tả | Description
**[VI]** Thêm quốc tế hóa (i18n) để hỗ trợ nhiều ngôn ngữ, bắt đầu với Tiếng Việt (mặc định) và Tiếng Anh.

**[EN]** Add internationalization (i18n) to support multiple languages, starting with Vietnamese (default) and English.

---

### 📊 Trạng thái hiện tại | Current State
- ❌ Tất cả text hardcoded bằng Tiếng Việt | All text hardcoded in Vietnamese
- ❌ Chưa có i18n framework | No i18n framework

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Cài đặt vue-i18n
\`\`\`bash
npm install vue-i18n@9
\`\`\`

**Bước 2 | Step 2:** Tạo files dịch | Create translation files
- \`locales/vi.json\` - Tiếng Việt (mặc định | default)
- \`locales/en.json\` - English

**Bước 3 | Step 3:** Trích xuất text strings | Extract text strings
- [VI] Labels UI, nút, tiêu đề | [EN] UI labels, buttons, titles
- [VI] Thông báo lỗi | [EN] Error messages
- [VI] Thông báo validation | [EN] Validation messages
- [VI] Placeholder text | [EN] Placeholder text

**Bước 4 | Step 4:** Thêm bộ chuyển ngôn ngữ | Add language switcher in header/settings

**Bước 5 | Step 5:** Lưu tùy chọn ngôn ngữ | Persist language preference in localStorage

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Tất cả text UI có thể dịch | [EN] All UI text translatable
- [ ] [VI] Bộ chuyển ngôn ngữ trong header | [EN] Language switcher in header
- [ ] [VI] Ngôn ngữ mặc định: Tiếng Việt | [EN] Default language: Vietnamese
- [ ] [VI] Bản dịch Tiếng Anh hoàn chỉnh | [EN] English translations complete
- [ ] [VI] Tùy chọn ngôn ngữ được lưu | [EN] Language preference persisted
- [ ] [VI] Không có translation key bị thiếu | [EN] No missing translation keys
- [ ] [VI] Format ngày/giờ theo locale | [EN] Date/time formatting follows locale
- [ ] [VI] Format số theo locale | [EN] Number formatting follows locale

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Files mới | New files:**
- \`Frontend/src/locales/vi.json\`
- \`Frontend/src/locales/en.json\`
- \`Frontend/src/plugins/i18n.js\`

**Files sửa | Files to modify:**
- \`Frontend/src/main.js\`
- Tất cả Vue components (thay text bằng \$t()) | All Vue components (replace text with \$t())
- Tất cả composables có text | All composables with text

**Dependencies:** vue-i18n: ^9.8.0

**Độ ưu tiên | Priority:** 🟡 Trung bình | Medium"

echo ""

# Issue #6: Real-Time Backend Sync
echo "Creating Issue #6: Đồng bộ Backend Realtime | Real-Time Backend Sync..."
gh issue create \
  --repo "$REPO" \
  --title "🔄 Đồng bộ Backend Realtime với WebSocket | Real-Time Backend Sync" \
  --label "backend,websocket,real-time,sync,phase-3" \
  --body "## 🔄 Đồng bộ Backend Realtime với WebSocket | Real-Time Backend Sync with WebSocket

### 📝 Mô tả | Description
**[VI]** Triển khai đồng bộ dữ liệu realtime giữa frontend và backend sử dụng WebSocket để cập nhật trực tiếp trên tất cả người dùng.

**[EN]** Implement real-time data synchronization between frontend and backend using WebSocket for live updates across all users.

---

### 📊 Trạng thái hiện tại | Current State
- ❌ Chỉ có mock data (không có backend) | Mock data only (no backend)
- ❌ Không có cập nhật realtime | No real-time updates
- ❌ Không có kết nối WebSocket | No WebSocket connection

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Backend - Node.js + Socket.io
- [VI] Setup Express server | [EN] Setup Express server
- [VI] Triển khai Socket.io server | [EN] Implement Socket.io server
- [VI] Tích hợp Database (MongoDB/PostgreSQL) | [EN] Database integration
- [VI] REST API + WebSocket events | [EN] REST API + WebSocket events

**Bước 2 | Step 2:** Frontend - Socket.io client
- [VI] Kết nối WebSocket server | [EN] Connect to WebSocket server
- [VI] Lắng nghe events realtime: | [EN] Listen for real-time events:
  - Vùng trồng mới được thêm | New vùng trồng added
  - Cập nhật trạng thái | Status updates
  - Cảnh báo sâu bệnh | Pest warnings
  - Hành động người dùng | User actions
- [VI] Cập nhật UI realtime | [EN] Update UI in real-time
- [VI] Xử lý reconnection | [EN] Handle reconnection

**Bước 3 | Step 3:** Sync events
- [VI] Thay đổi trạng thái cây trồng | [EN] Crop status changes
- [VI] Diary entries | [EN] Diary entries
- [VI] Cập nhật bản đồ | [EN] Map updates
- [VI] Thông báo | [EN] Notifications

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Kết nối WebSocket thành công | [EN] WebSocket connection established
- [ ] [VI] Cập nhật realtime trên tất cả clients | [EN] Real-time updates across all connected clients
- [ ] [VI] Dashboard cập nhật không cần refresh | [EN] Dashboard updates without page refresh
- [ ] [VI] Bản đồ cập nhật realtime | [EN] Map updates in real-time
- [ ] [VI] Xử lý mất kết nối hợp lý | [EN] Handles connection loss gracefully
- [ ] [VI] Tự động reconnect | [EN] Reconnects automatically
- [ ] [VI] Performance tối ưu (throttling/debouncing) | [EN] Performance optimized

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Backend:**
- Node.js + Express
- Socket.io
- Database (TBD)

**Frontend files mới | New files:**
- \`Frontend/src/services/websocket.js\`
- \`Frontend/src/composables/useWebSocket.js\`

**Dependencies:** socket.io-client: ^4.6.0

**Độ ưu tiên | Priority:** 🔴 Cao | High"

echo ""

# Issue #7: User Authentication
echo "Creating Issue #7: Xác thực & Phân quyền | User Authentication & Roles..."
gh issue create \
  --repo "$REPO" \
  --title "🔐 Xác thực Người dùng và Phân quyền | User Authentication & RBAC" \
  --label "backend,auth,security,rbac,phase-3" \
  --body "## 🔐 Xác thực Người dùng và Phân quyền | User Authentication and Role-Based Access Control

### 📝 Mô tả | Description
**[VI]** Triển khai hệ thống xác thực người dùng với phân quyền dựa trên vai trò (RBAC) cho nông dân, quản lý và quản trị viên.

**[EN]** Implement user authentication system with role-based access control (RBAC) for farmers, managers, and administrators.

---

### 📊 Trạng thái hiện tại | Current State
- ❌ Không có xác thực | No authentication
- ❌ Tất cả tính năng công khai | All features public
- ❌ Không có quản lý người dùng | No user management

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Backend - Auth system
- [VI] Xác thực JWT | [EN] JWT authentication
- [VI] Hash mật khẩu (bcrypt) | [EN] Password hashing (bcrypt)
- [VI] Cơ chế refresh token | [EN] Refresh token mechanism
- [VI] Middleware phân quyền | [EN] Role-based middleware

**Bước 2 | Step 2:** Vai trò người dùng | User roles
- **[VI] Nông dân:** Xem cây trồng riêng, cập nhật nhật ký
- **[EN] Farmer:** View own crops, update diary
- **[VI] Quản lý:** Xem tất cả cây trồng, tạo báo cáo
- **[EN] Manager:** View all crops, generate reports
- **[VI] Admin:** Toàn quyền + quản lý người dùng
- **[EN] Admin:** Full access + user management

**Bước 3 | Step 3:** Frontend - Auth flow
- [VI] Trang Login/Register | [EN] Login/Register pages
- [VI] Protected routes | [EN] Protected routes
- [VI] Hiển thị component theo vai trò | [EN] Role-based component visibility
- [VI] Quản lý token | [EN] Token management
- [VI] Auto logout khi hết hạn | [EN] Auto logout on expiry

**Bước 4 | Step 4:** Tính năng | Features
- [VI] Đăng nhập/Đăng xuất | [EN] Login/Logout
- [VI] Đăng ký người dùng mới | [EN] Register new users
- [VI] Reset mật khẩu | [EN] Password reset
- [VI] Quản lý hồ sơ | [EN] Profile management
- [VI] Kiểm tra quyền | [EN] Permission checks

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Người dùng có thể đăng ký/đăng nhập/đăng xuất | [EN] Users can register/login/logout
- [ ] [VI] JWT tokens lưu trữ an toàn | [EN] JWT tokens securely stored
- [ ] [VI] Protected routes chuyển hướng đến login | [EN] Protected routes redirect to login
- [ ] [VI] Truy cập tính năng theo vai trò | [EN] Role-based feature access
- [ ] [VI] Admin có thể quản lý người dùng | [EN] Admin can manage users
- [ ] [VI] Session duy trì qua page refresh | [EN] Session persists across page refresh
- [ ] [VI] Auto logout khi token hết hạn | [EN] Auto logout on token expiry
- [ ] [VI] Luồng reset mật khẩu hoạt động | [EN] Password reset flow works

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Backend files:**
- \`Backend/controllers/authController.js\`
- \`Backend/middleware/auth.js\`
- \`Backend/models/User.js\`

**Frontend files:**
- \`Frontend/src/views/LoginView.vue\`
- \`Frontend/src/views/RegisterView.vue\`
- \`Frontend/src/composables/useAuth.js\`
- \`Frontend/src/router/index.js\` (add guards)

**Dependencies:**
- jsonwebtoken: ^9.0.2
- bcryptjs: ^2.4.3

**Độ ưu tiên | Priority:** 🔴 Cao | High"

echo ""

# Issue #8: Advanced Analytics
echo "Creating Issue #8: Dashboard Phân tích Nâng cao | Advanced Analytics Dashboard..."
gh issue create \
  --repo "$REPO" \
  --title "📈 Dashboard Phân tích Nâng cao | Advanced Analytics Dashboard" \
  --label "enhancement,analytics,charts,ai,phase-3" \
  --body "## 📈 Dashboard Phân tích Nâng cao | Advanced Analytics Dashboard

### 📝 Mô tả | Description
**[VI]** Nâng cao dashboard với tính năng phân tích nâng cao bao gồm xu hướng lịch sử, phân tích dự đoán và insights được hỗ trợ AI.

**[EN]** Enhance dashboard with advanced analytics features including historical trends, predictive analytics, and AI-powered insights.

---

### 📊 Trạng thái hiện tại | Current State
- ✅ Biểu đồ cơ bản (Pie, Bar, Line) | Basic charts
- ❌ Chưa có trực quan hóa dữ liệu lịch sử | No historical data visualization
- ❌ Chưa có phân tích xu hướng | No trend analysis
- ❌ Chưa có dự đoán | No predictions

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Loại biểu đồ mới | New chart types
- [VI] Radar chart: So sánh đa chiều cây trồng | [EN] Radar chart: Multi-dimensional crop comparison
- [VI] Scatter plot: Phân tích tương quan | [EN] Scatter plot: Correlation analysis
- [VI] Heat map: Năng suất theo địa lý | [EN] Heat map: Geographic productivity
- [VI] Sankey diagram: Luồng xuất khẩu | [EN] Sankey diagram: Export flow
- [VI] Gauge charts: Chỉ số hiệu suất | [EN] Gauge charts: Performance indicators

**Bước 2 | Step 2:** Phân tích lịch sử | Historical analysis
- [VI] Xu hướng chuỗi thời gian | [EN] Time series trends
- [VI] So sánh năm qua năm | [EN] Year-over-year comparison
- [VI] Mô hình theo mùa | [EN] Seasonal patterns
- [VI] Tính toán tốc độ tăng trưởng | [EN] Growth rate calculations

**Bước 3 | Step 3:** Tính năng dự đoán | Predictive features
- [VI] Dự đoán thu hoạch | [EN] Harvest prediction
- [VI] Dự báo năng suất | [EN] Yield forecasting
- [VI] Dự đoán xu hướng giá | [EN] Price trend predictions
- [VI] Phân tích tác động thời tiết | [EN] Weather impact analysis

**Bước 4 | Step 4:** Bộ chọn khoảng ngày tùy chỉnh | Custom date range selector

**Bước 5 | Step 5:** Chế độ so sánh (so sánh các khoảng thời gian) | Comparison mode

**Bước 6 | Step 6:** Xuất báo cáo phân tích | Export analytics reports

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] 5+ loại biểu đồ mới được triển khai | [EN] 5+ new chart types implemented
- [ ] [VI] Dữ liệu lịch sử trực quan (6+ tháng) | [EN] Historical data visualized (6+ months)
- [ ] [VI] Bộ chọn khoảng ngày hoạt động | [EN] Date range selector functional
- [ ] [VI] Chế độ so sánh hoạt động | [EN] Comparison mode works
- [ ] [VI] Insights dự đoán được hiển thị | [EN] Predictive insights displayed
- [ ] [VI] Performance tối ưu cho dataset lớn | [EN] Performance optimized for large datasets
- [ ] [VI] Biểu đồ responsive trên mobile | [EN] Mobile-responsive charts

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Files mới | New files:**
- \`Frontend/src/components/RadarChartComponent.vue\`
- \`Frontend/src/components/ScatterPlotComponent.vue\`
- \`Frontend/src/components/HeatMapComponent.vue\`
- \`Frontend/src/components/DateRangePicker.vue\`
- \`Frontend/src/composables/useAnalytics.js\`
- \`Frontend/src/utils/predictions.js\`

**Dependencies:**
- chart.js plugins
- date-fns: ^3.0.0

**Độ ưu tiên | Priority:** 🟡 Trung bình | Medium"

echo ""

# Issue #9: Optimize Map Performance
echo "Creating Issue #9: Tối ưu Hiệu suất Bản đồ | Optimize Map Performance..."
gh issue create \
  --repo "$REPO" \
  --title "⚡ Tối ưu Hiệu suất Bản đồ | Optimize Map Performance" \
  --label "performance,map,optimization" \
  --body "## ⚡ Tối ưu Hiệu suất Bản đồ cho Dataset Lớn | Optimize Map Performance for Large Datasets

### 📝 Mô tả | Description
**[VI]** Cải thiện hiệu suất render bản đồ khi hiển thị 100+ polygons với tương tác mượt mà.

**[EN]** Improve map rendering performance when displaying 100+ polygons with smooth interactions.

---

### 📊 Trạng thái hiện tại | Current State
- ⚠️ Lag với 50+ polygons | Lag with 50+ polygons
- ⚠️ Zoom/pan chậm với nhiều markers | Slow zoom/pan with many markers

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Triển khai clustering cho markers | Implement clustering for markers

**Bước 2 | Step 2:** Sử dụng canvas renderer thay vì SVG | Use canvas renderer instead of SVG

**Bước 3 | Step 3:** Lazy load polygons (dựa trên viewport) | Lazy load polygons (viewport-based)

**Bước 4 | Step 4:** Đơn giản hóa tọa độ polygon | Simplify polygon coordinates

**Bước 5 | Step 5:** Thêm loading indicators | Add loading indicators

**Bước 6 | Step 6:** Virtualize datasets lớn | Virtualize large datasets

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Mượt 60fps với 100+ polygons | [EN] Smooth 60fps with 100+ polygons
- [ ] [VI] Zoom/pan responsive | [EN] Zoom/pan responsive
- [ ] [VI] Marker clustering hoạt động | [EN] Marker clustering works
- [ ] [VI] Không đóng băng UI | [EN] No UI freezing

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Files sửa | Files to modify:**
- \`Frontend/src/composables/useMapLogic.js\`
- \`Frontend/src/components/MapComponent.vue\`

**Dependencies:** leaflet.markercluster: ^1.5.3

**Độ ưu tiên | Priority:** 🟡 Trung bình | Medium"

echo ""

# Issue #10: Unit Tests
echo "Creating Issue #10: Thêm Unit Tests | Add Unit Tests..."
gh issue create \
  --repo "$REPO" \
  --title "🧪 Thêm Unit Tests với Vitest | Add Unit Tests with Vitest" \
  --label "testing,vitest,unit-tests,quality" \
  --body "## 🧪 Thêm Unit Tests với Vitest | Add Unit Tests with Vitest

### 📝 Mô tả | Description
**[VI]** Triển khai unit tests toàn diện cho composables, utilities và components quan trọng.

**[EN]** Implement comprehensive unit tests for composables, utilities, and critical components.

---

### 💡 Giải pháp đề xuất | Proposed Solution

**Bước 1 | Step 1:** Setup Vitest
\`\`\`bash
npm install -D vitest @vue/test-utils happy-dom
\`\`\`

**Bước 2 | Step 2:** Mục tiêu test coverage | Test coverage targets
- [VI] Composables: 80%+ | [EN] Composables: 80%+
- [VI] Utilities: 90%+ | [EN] Utilities: 90%+
- [VI] Components: 60%+ | [EN] Components: 60%+

**Bước 3 | Step 3:** Test files
- \`useHome.test.js\`
- \`useCharts.test.js\`
- \`useDiary.test.js\`
- \`statusHelpers.test.js\`
- Component tests

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Vitest được cấu hình | [EN] Vitest configured
- [ ] [VI] Tất cả composables được test | [EN] All composables tested
- [ ] [VI] Components quan trọng được test | [EN] Critical components tested
- [ ] [VI] Tích hợp CI/CD | [EN] CI/CD integration
- [ ] [VI] Báo cáo coverage được tạo | [EN] Coverage reports generated

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Dependencies:**
- vitest: latest
- @vue/test-utils: latest
- happy-dom: latest

**Độ ưu tiên | Priority:** 🔴 Cao | High"

echo ""

# Issue #11: E2E Tests
echo "Creating Issue #11: Thêm E2E Tests | Add E2E Tests..."
gh issue create \
  --repo "$REPO" \
  --title "🎭 Thêm E2E Tests với Playwright | Add E2E Tests with Playwright" \
  --label "testing,e2e,playwright,quality" \
  --body "## 🎭 Thêm E2E Tests với Playwright | Add E2E Tests with Playwright

### 📝 Mô tả | Description
**[VI]** Triển khai end-to-end tests cho các user journeys quan trọng.

**[EN]** Implement end-to-end tests for critical user journeys.

---

### 💡 Kịch bản Test | Test Scenarios

1. [VI] Tìm kiếm & lọc cây trồng | [EN] User search & filter crops
2. [VI] Xem chi tiết cây trồng & timeline | [EN] View crop details & timeline
3. [VI] Thêm diary entry | [EN] Add diary entry
4. [VI] Xuất báo cáo | [EN] Export reports
5. [VI] Quét mã QR | [EN] QR code scan

---

### ✅ Tiêu chí chấp nhận | Acceptance Criteria
- [ ] [VI] Playwright được cấu hình | [EN] Playwright configured
- [ ] [VI] 5+ luồng quan trọng được test | [EN] 5+ critical flows tested
- [ ] [VI] Tests chạy trong CI/CD | [EN] Tests run in CI/CD
- [ ] [VI] Screenshots khi thất bại | [EN] Screenshots on failure

---

### 🛠️ Chi tiết kỹ thuật | Technical Details

**Dependencies:** @playwright/test: latest

**Độ ưu tiên | Priority:** 🟡 Trung bình | Medium"

echo ""
echo "✅ All bilingual issues created successfully!"
echo "🔗 View issues at: https://github.com/$REPO/issues"
