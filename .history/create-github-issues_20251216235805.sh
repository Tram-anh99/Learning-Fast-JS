#!/bin/bash

# Script to create GitHub issues for Learning-Fast-JS project
# Usage: ./create-github-issues.sh

REPO="Tram-anh99/Learning-Fast-JS"

echo "🚀 Creating GitHub Issues for $REPO..."
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
echo "Creating Issue #1: Camera QR Scan Integration..."
gh issue create \
  --repo "$REPO" \
  --title "📷 Camera QR Scan Integration" \
  --label "enhancement,feature,camera,qr-code,phase-2" \
  --body "## 📷 Camera QR Scan Integration

### Description
Implement real-time camera QR code scanning using html5-qrcode library to allow users to scan QR codes directly from their device camera instead of manual input.

### Current State
- ✅ QRScanner.vue modal exists with manual input
- ✅ Placeholder for camera scan ready
- ❌ html5-qrcode library not integrated

### Proposed Solution
1. Install html5-qrcode package
   \`\`\`bash
   npm install html5-qrcode
   \`\`\`

2. Update QRScanner.vue:
   - Add camera preview container
   - Initialize Html5Qrcode scanner
   - Handle successful scan callback
   - Handle scan errors
   - Add camera permissions request
   - Add camera stop on modal close

3. Add camera toggle button
4. Test on mobile devices (iOS/Android)

### Acceptance Criteria
- [ ] Camera preview shows in QRScanner modal
- [ ] Successfully scans QR codes from camera
- [ ] Auto-redirects to product details after scan
- [ ] Handles camera permissions gracefully
- [ ] Works on mobile browsers (iOS Safari, Chrome Android)
- [ ] Fallback to manual input if camera unavailable

### Technical Details
**Files to modify:**
- \`Frontend/src/components/QRScanner.vue\`
- \`Frontend/package.json\`

**Dependencies:**
- html5-qrcode: ^2.3.8

### Priority
🔴 High"

echo ""

# Issue #2: PWA Offline Mode
echo "Creating Issue #2: PWA Offline Mode..."
gh issue create \
  --repo "$REPO" \
  --title "📱 PWA Offline Mode Implementation" \
  --label "enhancement,pwa,offline,service-worker,phase-2" \
  --body "## 📱 PWA Offline Mode Implementation

### Description
Convert the application to a Progressive Web App (PWA) with offline capabilities, allowing users to access basic features without internet connection.

### Current State
- ❌ No service worker
- ❌ No PWA manifest
- ❌ No offline fallback

### Proposed Solution
1. Install Vite PWA plugin
   \`\`\`bash
   npm install vite-plugin-pwa -D
   \`\`\`

2. Create manifest.json
   - App name, icons, theme colors
   - Display mode: standalone
   - Start URL configuration

3. Implement Service Worker
   - Cache static assets (CSS, JS, images)
   - Cache API responses
   - Offline fallback page
   - Background sync for diary entries

4. Add install prompt for mobile
5. Add offline indicator in UI

### Acceptance Criteria
- [ ] App installable on mobile devices
- [ ] Static assets cached and accessible offline
- [ ] Offline indicator shows when no connection
- [ ] Diary entries saved locally and synced when online
- [ ] Map tiles cached for frequently visited areas
- [ ] Works offline after first visit

### Technical Details
**New files:**
- \`Frontend/public/manifest.json\`
- \`Frontend/src/registerServiceWorker.js\`

**Files to modify:**
- \`Frontend/vite.config.js\`
- \`Frontend/index.html\`

**Dependencies:**
- vite-plugin-pwa: ^0.17.0
- workbox-window: ^7.0.0

### Priority
🟡 Medium"

echo ""

# Issue #3: Push Notifications
echo "Creating Issue #3: Push Notifications..."
gh issue create \
  --repo "$REPO" \
  --title "🔔 Push Notifications for Alerts" \
  --label "enhancement,notifications,push,backend,phase-2" \
  --body "## 🔔 Push Notifications for Alerts

### Description
Implement push notifications to alert users about important events such as pest warnings, harvest reminders, and system alerts.

### Current State
- ❌ No notification system
- ❌ No backend notification service

### Proposed Solution
1. Frontend: Web Push API
   - Request notification permissions
   - Subscribe to push notifications
   - Handle notification display
   - Handle notification clicks

2. Backend: Push notification service
   - FCM (Firebase Cloud Messaging) integration
   - Notification triggers:
     - Pest/disease warnings
     - Harvest time reminders
     - Weather alerts
     - System notifications

3. Add notification preferences in settings
4. Add notification history/logs

### Acceptance Criteria
- [ ] Users can enable/disable notifications
- [ ] Notifications work on desktop browsers
- [ ] Notifications work on mobile (PWA)
- [ ] Users can customize notification types
- [ ] Notifications link to relevant pages
- [ ] Notification history accessible

### Technical Details
**Files to create:**
- \`Frontend/src/composables/useNotifications.js\`
- \`Backend/services/notificationService.js\`

**Files to modify:**
- \`Frontend/src/views/SettingsView.vue\` (new)
- Service worker for notification handling

**Dependencies:**
- firebase: ^10.7.0 (optional, for FCM)

### Priority
🟡 Medium"

echo ""

# Issue #4: Export PDF/Excel Reports
echo "Creating Issue #4: Export PDF/Excel Reports..."
gh issue create \
  --repo "$REPO" \
  --title "📄 Export Dashboard Reports (PDF/Excel)" \
  --label "enhancement,export,pdf,excel,reporting,phase-2" \
  --body "## 📄 Export Dashboard Reports (PDF/Excel)

### Description
Allow users to export dashboard data, statistics, and charts to PDF and Excel formats for reporting and record-keeping.

### Current State
- ❌ No export functionality
- ❌ Data only viewable in-app

### Proposed Solution
1. PDF Export:
   - Use jsPDF + html2canvas
   - Export dashboard layout with charts
   - Export crop details with timeline
   - Export diary history
   - Add company logo/header

2. Excel Export:
   - Use xlsx library
   - Export DataTable to Excel
   - Export statistics summary
   - Export diary entries
   - Multiple sheets per workbook

3. Add export buttons to relevant views
4. Add export options dialog (format, date range)

### Acceptance Criteria
- [ ] Dashboard exports to PDF with charts intact
- [ ] DataTable exports to Excel (.xlsx)
- [ ] Diary history exports to both formats
- [ ] Exported files include metadata (date, user)
- [ ] Charts render correctly in PDF
- [ ] Excel data properly formatted
- [ ] File download works on all browsers

### Technical Details
**Files to create:**
- \`Frontend/src/utils/exportToPDF.js\`
- \`Frontend/src/utils/exportToExcel.js\`

**Files to modify:**
- \`Frontend/src/views/QuanLyView.vue\`
- \`Frontend/src/views/DiaryPage.vue\`
- \`Frontend/src/components/DataTableComponent.vue\`

**Dependencies:**
- jspdf: ^2.5.1
- html2canvas: ^1.4.1
- xlsx: ^0.18.5

### Priority
🟡 Medium"

echo ""

# Issue #5: Multi-Language Support
echo "Creating Issue #5: Multi-Language Support..."
gh issue create \
  --repo "$REPO" \
  --title "🌐 Multi-Language Support (Vietnamese/English)" \
  --label "enhancement,i18n,localization,multi-language,phase-2" \
  --body "## 🌐 Multi-Language Support (Vietnamese/English)

### Description
Add internationalization (i18n) to support multiple languages, starting with Vietnamese (default) and English.

### Current State
- ❌ All text hardcoded in Vietnamese
- ❌ No i18n framework

### Proposed Solution
1. Install vue-i18n
   \`\`\`bash
   npm install vue-i18n@9
   \`\`\`

2. Create translation files:
   - \`locales/vi.json\` - Vietnamese (default)
   - \`locales/en.json\` - English

3. Extract all text strings to translation files:
   - UI labels, buttons, titles
   - Error messages
   - Validation messages
   - Placeholder text

4. Add language switcher in header/settings
5. Persist language preference in localStorage

### Acceptance Criteria
- [ ] All UI text translatable
- [ ] Language switcher in header
- [ ] Default language: Vietnamese
- [ ] English translations complete
- [ ] Language preference persisted
- [ ] No missing translation keys
- [ ] Date/time formatting follows locale
- [ ] Number formatting follows locale

### Technical Details
**Files to create:**
- \`Frontend/src/locales/vi.json\`
- \`Frontend/src/locales/en.json\`
- \`Frontend/src/plugins/i18n.js\`

**Files to modify:**
- \`Frontend/src/main.js\`
- All Vue components (replace text with \$t())
- All composables with text

**Dependencies:**
- vue-i18n: ^9.8.0

### Priority
🟡 Medium"

echo ""

# Issue #6: Real-Time Backend Sync
echo "Creating Issue #6: Real-Time Backend Sync..."
gh issue create \
  --repo "$REPO" \
  --title "🔄 Real-Time Backend Sync with WebSocket" \
  --label "backend,websocket,real-time,sync,phase-3" \
  --body "## 🔄 Real-Time Backend Sync with WebSocket

### Description
Implement real-time data synchronization between frontend and backend using WebSocket for live updates across all users.

### Current State
- ❌ Mock data only (no backend)
- ❌ No real-time updates
- ❌ No WebSocket connection

### Proposed Solution
1. Backend: Node.js + Socket.io
   - Setup Express server
   - Implement Socket.io server
   - Database integration (MongoDB/PostgreSQL)
   - REST API + WebSocket events

2. Frontend: Socket.io client
   - Connect to WebSocket server
   - Listen for real-time events:
     - New vùng trồng added
     - Status updates
     - Pest warnings
     - User actions
   - Update UI in real-time
   - Handle reconnection

3. Sync events:
   - Crop status changes
   - Diary entries
   - Map updates
   - Notifications

### Acceptance Criteria
- [ ] WebSocket connection established
- [ ] Real-time updates across all connected clients
- [ ] Dashboard updates without page refresh
- [ ] Map updates in real-time
- [ ] Handles connection loss gracefully
- [ ] Reconnects automatically
- [ ] Performance optimized (throttling/debouncing)

### Technical Details
**Backend:**
- Node.js + Express
- Socket.io
- Database (TBD)

**Frontend files to create:**
- \`Frontend/src/services/websocket.js\`
- \`Frontend/src/composables/useWebSocket.js\`

**Dependencies:**
- socket.io-client: ^4.6.0

### Priority
🔴 High"

echo ""

# Issue #7: User Authentication
echo "Creating Issue #7: User Authentication & Roles..."
gh issue create \
  --repo "$REPO" \
  --title "🔐 User Authentication and Role-Based Access Control" \
  --label "backend,auth,security,rbac,phase-3" \
  --body "## 🔐 User Authentication and Role-Based Access Control

### Description
Implement user authentication system with role-based access control (RBAC) for farmers, managers, and administrators.

### Current State
- ❌ No authentication
- ❌ All features public
- ❌ No user management

### Proposed Solution
1. Backend: Auth system
   - JWT authentication
   - Password hashing (bcrypt)
   - Refresh token mechanism
   - Role-based middleware

2. User roles:
   - **Farmer:** View own crops, update diary
   - **Manager:** View all crops, generate reports
   - **Admin:** Full access + user management

3. Frontend: Auth flow
   - Login/Register pages
   - Protected routes
   - Role-based component visibility
   - Token management
   - Auto logout on expiry

4. Features:
   - Login/Logout
   - Register new users
   - Password reset
   - Profile management
   - Permission checks

### Acceptance Criteria
- [ ] Users can register/login/logout
- [ ] JWT tokens securely stored
- [ ] Protected routes redirect to login
- [ ] Role-based feature access
- [ ] Admin can manage users
- [ ] Session persists across page refresh
- [ ] Auto logout on token expiry
- [ ] Password reset flow works

### Technical Details
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

### Priority
🔴 High"

echo ""

# Issue #8: Advanced Analytics
echo "Creating Issue #8: Advanced Analytics Dashboard..."
gh issue create \
  --repo "$REPO" \
  --title "📈 Advanced Analytics Dashboard" \
  --label "enhancement,analytics,charts,ai,phase-3" \
  --body "## 📈 Advanced Analytics Dashboard

### Description
Enhance dashboard with advanced analytics features including historical trends, predictive analytics, and AI-powered insights.

### Current State
- ✅ Basic charts (Pie, Bar, Line)
- ❌ No historical data visualization
- ❌ No trend analysis
- ❌ No predictions

### Proposed Solution
1. New chart types:
   - Radar chart: Multi-dimensional crop comparison
   - Scatter plot: Correlation analysis
   - Heat map: Geographic productivity
   - Sankey diagram: Export flow
   - Gauge charts: Performance indicators

2. Historical analysis:
   - Time series trends
   - Year-over-year comparison
   - Seasonal patterns
   - Growth rate calculations

3. Predictive features:
   - Harvest prediction
   - Yield forecasting
   - Price trend predictions
   - Weather impact analysis

4. Custom date range selector
5. Comparison mode (compare periods)
6. Export analytics reports

### Acceptance Criteria
- [ ] 5+ new chart types implemented
- [ ] Historical data visualized (6+ months)
- [ ] Date range selector functional
- [ ] Comparison mode works
- [ ] Predictive insights displayed
- [ ] Performance optimized for large datasets
- [ ] Mobile-responsive charts

### Technical Details
**Files to create:**
- \`Frontend/src/components/RadarChartComponent.vue\`
- \`Frontend/src/components/ScatterPlotComponent.vue\`
- \`Frontend/src/components/HeatMapComponent.vue\`
- \`Frontend/src/components/DateRangePicker.vue\`
- \`Frontend/src/composables/useAnalytics.js\`
- \`Frontend/src/utils/predictions.js\`

**Dependencies:**
- chart.js plugins
- date-fns: ^3.0.0

### Priority
🟡 Medium"

echo ""

# Issue #9: Optimize Map Performance
echo "Creating Issue #9: Optimize Map Performance..."
gh issue create \
  --repo "$REPO" \
  --title "⚡ Optimize Map Performance for Large Datasets" \
  --label "performance,map,optimization" \
  --body "## ⚡ Optimize Map Performance for Large Datasets

### Description
Improve map rendering performance when displaying 100+ polygons with smooth interactions.

### Current State
- ⚠️ Lag with 50+ polygons
- ⚠️ Slow zoom/pan with many markers

### Proposed Solution
1. Implement clustering for markers
2. Use canvas renderer instead of SVG
3. Lazy load polygons (viewport-based)
4. Simplify polygon coordinates
5. Add loading indicators
6. Virtualize large datasets

### Acceptance Criteria
- [ ] Smooth 60fps with 100+ polygons
- [ ] Zoom/pan responsive
- [ ] Marker clustering works
- [ ] No UI freezing

### Technical Details
**Files to modify:**
- \`Frontend/src/composables/useMapLogic.js\`
- \`Frontend/src/components/MapComponent.vue\`

**Dependencies:**
- leaflet.markercluster: ^1.5.3

### Priority
🟡 Medium"

echo ""

# Issue #10: Add Unit Tests
echo "Creating Issue #10: Add Unit Tests..."
gh issue create \
  --repo "$REPO" \
  --title "🧪 Add Unit Tests with Vitest" \
  --label "testing,vitest,unit-tests,quality" \
  --body "## 🧪 Add Unit Tests with Vitest

### Description
Implement comprehensive unit tests for composables, utilities, and critical components.

### Proposed Solution
1. Setup Vitest
   \`\`\`bash
   npm install -D vitest @vue/test-utils happy-dom
   \`\`\`

2. Test coverage targets:
   - Composables: 80%+
   - Utilities: 90%+
   - Components: 60%+

3. Test files:
   - \`useHome.test.js\`
   - \`useCharts.test.js\`
   - \`useDiary.test.js\`
   - \`statusHelpers.test.js\`
   - Component tests

### Acceptance Criteria
- [ ] Vitest configured
- [ ] All composables tested
- [ ] Critical components tested
- [ ] CI/CD integration
- [ ] Coverage reports generated

### Priority
🔴 High"

echo ""

# Issue #11: Add E2E Tests
echo "Creating Issue #11: Add E2E Tests..."
gh issue create \
  --repo "$REPO" \
  --title "🎭 Add E2E Tests with Playwright" \
  --label "testing,e2e,playwright,quality" \
  --body "## 🎭 Add E2E Tests with Playwright

### Description
Implement end-to-end tests for critical user journeys.

### Test Scenarios
1. User search & filter crops
2. View crop details & timeline
3. Add diary entry
4. Export reports
5. QR code scan

### Acceptance Criteria
- [ ] Playwright configured
- [ ] 5+ critical flows tested
- [ ] Tests run in CI/CD
- [ ] Screenshots on failure

### Priority
🟡 Medium"

echo ""
echo "✅ All issues created successfully!"
echo "🔗 View issues at: https://github.com/$REPO/issues"
