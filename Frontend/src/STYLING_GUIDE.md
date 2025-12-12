/\*\*

-    🎨 MODERN & TRENDY STYLING GUIDE
-    ================================
-
-    Phong cách thiết kế hiện đại, trẻ trung cho WebGIS
-    Sử dụng: Gradient, Glassmorphism, Smooth Animations
     \*/

// ============================================================================
// ✨ DESIGN PRINCIPLES
// ============================================================================

1. GRADIENT & COLOR
   ✓ Sử dụng gradient cho buttons, cards, icons
   ✓ Màu chuyển từ sáng → tối (135deg diagonal)
   ✓ Tránh màu "deadflat" - luôn có độ sâu

2. GLASSMORPHISM
   ✓ backdrop-blur-xl/md/sm - mờ nền phía sau
   ✓ border-white/50-80 - viền trắng bán trong suốt
   ✓ bg-white/80-90 - nền trắng bán trong suốt
   ✓ from-white via-slate-50 to-blue-50 - gradient tinh tế

3. SMOOTH ANIMATIONS
   ✓ cubic-bezier(0.4, 0, 0.2, 1) - ease-out modern
   ✓ cubic-bezier(0.175, 0.885, 0.32, 1.275) - bounce/spring
   ✓ duration-200/300/400 - thời gian phù hợp
   ✓ transition-all - mượt tất cả properties

4. SHADOWS & DEPTH
   ✓ shadow-md - bóng trung bình (thường)
   ✓ shadow-lg → shadow-xl - hover effect
   ✓ Tăng bóng khi hover để tạo cảm giác lifting
   ✓ Blur radius 3xl-5xl cho decorative elements

5. ROUNDED CORNERS
   ✓ rounded-xl, rounded-2xl, rounded-3xl (không rounded-lg)
   ✓ Tránh góc vuông - trẻ hơn
   ✓ Kết hợp border-radius lớn với gradient

6. HOVER & INTERACTION
   ✓ hover:shadow-lg/xl - tăng bóng
   ✓ hover:scale-105/110 - phóng to nhẹ
   ✓ hover:-translate-y-0.5 - nâng nhẹ lên
   ✓ active:scale-95 - ấn xuống
   ✓ group-hover: - hover cho icon/element con

// ============================================================================
// 🎭 COMPONENT STYLING PATTERNS
// ============================================================================

MODAL (QRModal)
├─ Backdrop: bg-black/40 + backdrop-blur-md (mờ mềm)
├─ Card: bg-gradient-to-br from-white via-slate-50 to-blue-50
├─ Border: border-white/80 (viền trắng tinh tế)
├─ Decorative: Gradient circles (position: absolute) phía sau text
├─ Glow effect: Inset box-shadow để tạo halo quanh QR
├─ Buttons:
│ ├─ Primary: linear-gradient(135deg, from-green-500 to-emerald-600)
│ ├─ Secondary: hover:bg-gray-100/80 (light hover)
│ └─ Active: active:scale-95 (animation ấn xuống)
└─ Animations: animate-fade-in + animate-scale-up

STAT CARDS
├─ Background: from-white to-slate-50 (gradient tinh tế)
├─ Border: border-white/50
├─ Hover: border-white/80 + shadow-lg (scale-1 không đổi)
├─ Icon box: linear-gradient + shadow-lg
├─ Icon hover: scale-110 + shadow-xl (nâng lên)
└─ Backdrop: backdrop-blur-sm (optional)

BUTTONS
├─ Primary: linear-gradient(135deg, #1b4332, #0f2818)
├─ Hover: from-green-600 to-emerald-700 + shadow-xl
├─ Padding: px-4 py-2.5 (thoải mái, không quá chật)
├─ Radius: rounded-xl (không lg)
├─ Active: active:scale-95 (ấn xuống)
└─ Font: font-semibold (đủ đậm)

BADGES
├─ Style: gradient + shadow-sm + px-3 py-1.5
├─ Success: linear-gradient(135deg, #d1fae5, #a7f3d0)
├─ Warning: linear-gradient(135deg, #fef3c7, #fde68a)
├─ Danger: linear-gradient(135deg, #fee2e2, #fecaca)
└─ Font: font-bold (nổi bật)

TABLE ROWS
├─ Header: gradient-to-r from-slate-100 to-slate-50
├─ Hover: bg-blue-50/50 + scale-[1.01] (nhẹ nhàng)
├─ Border: border-slate-200 (tinh tế)
└─ Transition: transition-all duration-200 (mượt)

PANELS
├─ Background: from-white to-slate-50 (gradient)
├─ Border: border-white/50
├─ Shadow: shadow-md
├─ Backdrop: backdrop-blur-sm
└─ Radius: rounded-2xl (không xl)

MAP CONTROLS
├─ Default: linear-gradient(135deg, #f8fafc, #f1f5f9)
├─ Hover: from-[#e2e8f0] to-[#cbd5e1] + shadow-md
├─ Active: linear-gradient(135deg, #1b4332, #0f2818) + shadow-lg
├─ Border: border-2 (nổi bật hơn border-1)
└─ Radius: rounded-xl

// ============================================================================
// 🎬 ANIMATION LIBRARY
// ============================================================================

.animate-fade-in
├─ Duration: 0.3s
├─ Easing: cubic-bezier(0.4, 0, 0.2, 1)
└─ Effect: opacity 0 → 1

.animate-scale-up
├─ Duration: 0.4s
├─ Easing: cubic-bezier(0.175, 0.885, 0.32, 1.275)
└─ Effect: scale 0.85 + opacity 0 → 1

.animate-slide-up
├─ Duration: 0.4s
├─ Effect: translateY(20px) + opacity → final

.animate-bounce-in
├─ Duration: 0.5s
├─ Effect: scale 0.3 → 1.05 → 1 (elastic)

.animate-fade-in-up
├─ Duration: 0.5s
├─ Effect: translateY(30px) + fade

.animate-pulse-gentle
├─ Duration: 2s (infinite)
├─ Effect: opacity 1 → 0.7 (subtle)

.animate-glow
├─ Duration: 2s (infinite)
├─ Effect: box-shadow từ nhỏ → lớn

.animate-shimmer
├─ Duration: 2s (infinite)
├─ Effect: background-position animation (loading effect)

// ============================================================================
// 🎨 COLOR PALETTE (Modern)
// ============================================================================

Primary (Xanh đậm - Tin tưởng):
├─ #1b4332 (Đậm)
├─ #0f2818 (Rất đậm - gradient end)
└─ Linear: 135deg, #1b4332 → #0f2818

Success (Xanh lá - Tích cực):
├─ #10b981 (Light)
├─ #059669 (Medium)
└─ Gradient: 135deg, #10b981 → #059669

Warning (Vàng cam - Cảnh báo):
├─ #f59e0b (Light)
├─ #d97706 (Dark)
└─ Gradient: 135deg, #f59e0b → #d97706

Neutral (Xám - Cân bằng):
├─ white (Nền chính)
├─ #f8fafc (Slate-50)
├─ #e2e8f0 (Slate-200)
└─ #1f2937 (Gray-800 - Text chính)

Accent (Xanh dương - Highlight):
├─ #3b82f6 (Blue-500)
├─ #0284c7 (Cyan-600)
└─ Dùng cho hyperlinks, focus states

// ============================================================================
// 📐 SPACING & SIZING SYSTEM
// ============================================================================

Cards/Panels: px-6 py-5 → px-8 py-6 (spacious)
Buttons: px-4 py-2.5 (không px-3 py-1.5)
Icons: w-14 h-14 → w-16 h-16 (lớn hơn)
Rounded: xl/2xl/3xl (không lg/md)
Shadows: md/lg/xl (không sm)
Gaps: gap-4 → gap-6 (thoải mái)
Borders: border-2 (nổi bật hơn)

// ============================================================================
// 🧩 COMBINATION EXAMPLES
// ============================================================================

✨ MODERN BUTTON
class="px-4 py-2.5 bg-gradient-to-r from-green-500 to-emerald-600
hover:from-green-600 hover:to-emerald-700
text-white font-semibold rounded-xl
shadow-lg hover:shadow-xl
transition-all duration-200
active:scale-95"

✨ STAT CARD
class="flex-1 bg-gradient-to-br from-white to-slate-50
px-6 py-5 rounded-2xl shadow-md
border border-white/50
hover:shadow-lg hover:border-white/80
transition-all duration-300
backdrop-blur-sm"

✨ MODAL
class="relative w-full max-w-sm
bg-gradient-to-br from-white via-slate-50 to-blue-50
rounded-3xl shadow-2xl p-8
border border-white/80
backdrop-blur-xl
animate-scale-up"

✨ ICON BOX
class="w-14 h-14 rounded-xl flex justify-center items-center
text-2xl text-white font-bold
bg-gradient-to-br from-green-500 to-emerald-600
shadow-lg
hover:scale-110 transition-all duration-300"

✨ TABLE ROW
class="transition-all duration-200"
with .hover-effect-on-parent to child

// ============================================================================
// 💡 BEST PRACTICES
// ============================================================================

1. NEVER use solid colors - always gradient or glassmorphism
2. ALWAYS add hover effects - shadow, scale, or color change
3. Use cubic-bezier for smooth, organic animations
4. Add z-10 to decorative elements to avoid overlap
5. Keep text readable - use text shadows if necessary
6. Test on mobile - touch/tap should feel responsive
7. Use group-hover for related elements animation
8. Border-radius should be modern (xl/2xl minimum)
9. Shadows should increase on hover (depth illusion)
10. Animations should feel snappy (200-400ms)

// ============================================================================
// 🎯 FILES TO CHECK
// ============================================================================

✓ src/components/QRModal.vue - UPDATED (Modern design)
✓ src/assets/styles/tailwind.css - UPDATED (All gradients & animations)
✓ tailwind.config.js - Custom colors defined
✓ StatsBarComponent.vue - Uses updated .stat-card + .icon-box
✓ DataTableComponent.vue - Uses updated table styles
✓ All buttons - Use .btn-primary or gradient inline

// ============================================================================
// 📝 NOTES
// ============================================================================

-    Phong cách: Glassmorphism + Gradient + Smooth animations
-    Trẻ trung: Modern colors, generous spacing, rounded corners
-    Hiện đại: Subtle shadows, blur effects, elastic interactions
-    Vue 3: group-hover, @click handlers work perfectly
-    Tailwind: No scoped CSS - all utilities used from global CSS
-    Performance: Animations use GPU (transform, opacity)
-    Accessibility: Keep hover effects subtle, support reduced-motion

\*/
