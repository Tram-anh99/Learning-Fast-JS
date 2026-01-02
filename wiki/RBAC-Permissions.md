# 🔐 Phân Quyền Người Dùng (RBAC - Role-Based Access Control)

## 👥 Các Vai Trò (Roles)

Hệ thống có 3 vai trò chính:

### 1. **Admin** (Quản trị viên)

-    **Quyền:**
     -    ✅ Full CRUD tất cả modules
     -    ✅ Quản lý user (thêm, xóa, đổi role)
     -    ✅ Quản lý danh mục (loại cây, phân bón, thuốc BVTV)
     -    ✅ Quản lý vùng trồng (MSVT)
     -    ✅ Xem tất cả nhật ký canh tác
     -    ✅ Dashboard & reports
     -    ✅ Chuyển trạng thái vùng trồng
-    **Không thể:**
     -    ❌ Không có giới hạn

### 2. **Nha Nông** (Farmer)

-    **Quyền:**
     -    ✅ Xem vùng trồng mình quản lý
     -    ✅ CRUD nhật ký canh tác (chỉ vùng của mình)
     -    ✅ Chọn phân bón, thuốc BVTV từ danh mục
     -    ✅ Xem dashboard của vùng mình
     -    ✅ Tạo QR code cho vùng của mình
-    **Không thể:**
     -    ❌ Không được tạo/xóa/sửa vùng trồng
     -    ❌ Không được xem vùng của người khác
     -    ❌ Không được thêm/xóa phân bón, thuốc vào danh mục
     -    ❌ Không được quản lý user

### 3. **Khách** (Guest/Public)

-    **Quyền:**
     -    ✅ Quét QR code
     -    ✅ Xem trang truy xuất nguồn gốc (public)
     -    ✅ Xem thông tin vùng trồng (read-only)
     -    ✅ Xem lịch sử canh tác (public fields only)
-    **Không thể:**
     -    ❌ Không được login
     -    ❌ Không được xem thông tin nhạy cảm
     -    ❌ Không được CRUD bất kỳ dữ liệu nào

---

## 📋 Ma Trận Quyền Chi Tiết

| Chức năng                  | Admin       | Nha Nông           | Khách                |
| -------------------------- | ----------- | ------------------ | -------------------- |
| **AUTHENTICATION**         |
| Login/Logout               | ✅          | ✅                 | ❌                   |
| Đổi mật khẩu               | ✅          | ✅                 | ❌                   |
| **USER MANAGEMENT**        |
| Xem danh sách users        | ✅          | ❌                 | ❌                   |
| Tạo user mới               | ✅          | ❌                 | ❌                   |
| Đổi role user              | ✅          | ❌                 | ❌                   |
| Xóa user                   | ✅          | ❌                 | ❌                   |
| **VÙNG TRỒNG (MSVT)**      |
| Xem danh sách vùng         | ✅          | ✅ (của mình)      | ✅ (public)          |
| Xem chi tiết vùng          | ✅          | ✅ (của mình)      | ✅ (public)          |
| Tạo vùng mới               | ✅          | ❌                 | ❌                   |
| Sửa vùng                   | ✅          | ❌                 | ❌                   |
| Xóa vùng                   | ✅          | ❌                 | ❌                   |
| Chuyển trạng thái vùng     | ✅          | ❌                 | ❌                   |
| **NHẬT KÝ CANH TÁC**       |
| Xem nhật ký                | ✅ (tất cả) | ✅ (của mình)      | ✅ (public)          |
| Thêm nhật ký               | ✅          | ✅ (vùng của mình) | ❌                   |
| Sửa nhật ký                | ✅          | ✅ (do mình tạo)   | ❌                   |
| Xóa nhật ký                | ✅          | ✅ (do mình tạo)   | ❌                   |
| **DANH MỤC**               |
| Xem loại cây               | ✅          | ✅                 | ✅                   |
| Thêm/Sửa/Xóa loại cây      | ✅          | ❌                 | ❌                   |
| Xem phân bón               | ✅          | ✅                 | ✅                   |
| Thêm/Sửa/Xóa phân bón      | ✅          | ❌                 | ❌                   |
| Xem thuốc BVTV             | ✅          | ✅                 | ✅                   |
| Thêm/Sửa/Xóa thuốc         | ✅          | ❌                 | ❌                   |
| **QR CODE & TRACEABILITY** |
| Tạo QR code                | ✅          | ✅ (vùng của mình) | ❌                   |
| Xem traceability           | ✅          | ✅                 | ✅ (public endpoint) |
| **DASHBOARD & REPORTS**    |
| Xem dashboard stats        | ✅          | ✅ (filtered)      | ❌                   |
| Xem charts                 | ✅          | ✅ (filtered)      | ❌                   |
| Export reports             | ✅          | ❌                 | ❌                   |

---

## 🔧 Implementation Guide

### Backend: API Endpoint Protection

#### 1. Public Endpoints (Không cần auth)

```python
# Backend/routes/qr.py
@router.get("/trace/{ma_vung}")  # ✅ Public
async def get_public_traceability(ma_vung: str, db: Session = Depends(get_db)):
    """Khách có thể access"""
    return farm_data
```

#### 2. Authenticated Endpoints (Cần login)

```python
# Backend/routes/diary.py
from dependencies.auth import get_current_active_user

@router.get("/")
async def get_diary(
    current_user: User = Depends(get_current_active_user),  # ✅ Requires login
    db: Session = Depends(get_db)
):
    # Filter by user's farms nếu là Nha nông
    if current_user.role == UserRole.NHA_NONG:
        farm_ids = [f.id for f in current_user.managed_farms]
        query = query.filter(LichSuCanhTac.vung_trong_id.in_(farm_ids))

    return diary_entries
```

#### 3. Admin-Only Endpoints

```python
# Backend/routes/farms.py
from dependencies.auth import require_admin

@router.post("/")
async def create_farm(
    farm_data: VungTrongCreate,
    admin: User = Depends(require_admin),  # ✅ Admin only
    db: Session = Depends(get_db)
):
    """Chỉ Admin mới tạo được vùng trồng"""
    return new_farm
```

#### 4. Owner Check (Nha nông chỉ sửa của mình)

```python
# Backend/routes/diary.py
@router.put("/{entry_id}")
async def update_diary(
    entry_id: int,
    entry_data: LichSuCanhTacCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get entry
    entry = db.query(LichSuCanhTac).filter(LichSuCanhTac.id == entry_id).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Not found")

    # Check ownership (nếu không phải Admin)
    if current_user.role != UserRole.ADMIN:
        # Check nếu entry thuộc vùng mà user quản lý
        if entry.vung_trong_id not in [f.id for f in current_user.managed_farms]:
            raise HTTPException(status_code=403, detail="Not authorized")

        # Check nếu entry do user tạo
        if entry.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")

    # Update
    entry.tieu_de = entry_data.tieu_de
    db.commit()
    return entry
```

---

### Frontend: UI Permission Checks

#### 1. Route Guards

```javascript
// Frontend/src/router/index.js
import { useAuth } from "@/composables/useAuth";

router.beforeEach((to, from, next) => {
     const { isAuthenticated, isAdmin, isNhaNong } = useAuth();

     // Public routes
     if (to.meta.public) {
          next();
          return;
     }

     // Authenticated routes
     if (to.meta.requiresAuth && !isAuthenticated.value) {
          next("/login");
          return;
     }

     // Admin-only routes
     if (to.meta.requiresAdmin && !isAdmin.value) {
          next("/"); // Redirect to home
          return;
     }

     next();
});

const routes = [
     {
          path: "/",
          component: HomeView,
          meta: { public: true }, // ✅ Mọi người xem được
     },
     {
          path: "/quan-ly",
          component: QuanLyView,
          meta: { requiresAuth: true, requiresAdmin: true }, // ✅ Chỉ Admin
     },
     {
          path: "/diary",
          component: DiaryPage,
          meta: { requiresAuth: true }, // ✅ Admin + Nha nông
     },
     {
          path: "/trace/:ma_vung",
          component: TraceabilityPage,
          meta: { public: true }, // ✅ Public
     },
];
```

#### 2. Conditional Rendering

```vue
<!-- Frontend/src/views/DiaryPage.vue -->
<template>
     <div>
          <h1>Nhật Ký Canh Tác</h1>

          <!-- Chỉ hiện button "Thêm" cho authenticated users -->
          <button
               v-if="isAuthenticated"
               @click="openCreateForm"
               class="btn-primary"
          >
               + Thêm nhật ký
          </button>

          <!-- List nhật ký -->
          <div v-for="entry in diaryEntries" :key="entry.id">
               <h3>{{ entry.tieu_de }}</h3>

               <!-- Chỉ hiện nút Sửa/Xóa nếu user sở hữu entry -->
               <div v-if="canEdit(entry)">
                    <button @click="editEntry(entry)">Sửa</button>
                    <button @click="deleteEntry(entry)">Xóa</button>
               </div>
          </div>
     </div>
</template>

<script setup>
import { useAuth } from "@/composables/useAuth";

const { isAuthenticated, isAdmin, user } = useAuth();

function canEdit(entry) {
     // Admin có thể edit tất cả
     if (isAdmin.value) return true;

     // Nha nông chỉ edit của mình
     if (entry.user_id === user.value?.id) return true;

     return false;
}
</script>
```

#### 3. Disable Inputs

```vue
<!-- Frontend/src/components/FarmForm.vue -->
<template>
     <form>
          <input
               v-model="farm.ma_vung"
               :disabled="!isAdmin"
               placeholder="Mã vùng trồng"
          />

          <!-- Admin có thể chọn chủ sở hữu, Nha nông không -->
          <select v-model="farm.chu_so_huu_id" :disabled="!isAdmin">
               <option v-for="owner in owners" :value="owner.id">
                    {{ owner.ten_to_chuc }}
               </option>
          </select>
     </form>
</template>
```

---

## 📝 Dữ Liệu Mẫu Users

### Admin User

```sql
INSERT INTO nongsan.users (email, username, hashed_password, full_name, role, is_active, is_verified)
VALUES (
    'admin@example.com',
    'admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIzZj7L5n6',  -- Password: admin123
    'Administrator',
    'ADMIN',
    TRUE,
    TRUE
);
```

### Nha Nông User

```sql
INSERT INTO nongsan.users (email, username, hashed_password, full_name, role, is_active, is_verified)
VALUES (
    'nhanong1@example.com',
    'nhanong1',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIzZj7L5n6',  -- Password: farmer123
    'Nguyễn Văn A',
    'NHA_NONG',
    TRUE,
    TRUE
);

-- Gán vùng trồng cho Nha nông
UPDATE nongsan.vung_trong SET user_id = (SELECT id FROM nongsan.users WHERE username = 'nhanong1')
WHERE ma_vung IN ('MSVT001', 'MSVT002');
```

---

## 🧪 Testing Permissions

### 1. Test Admin Access

```bash
# Login as Admin
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=admin&password=admin123"
# Response: {"access_token": "eyJ..."}

# Use token
curl http://localhost:8000/api/farms/ \
  -H "Authorization: Bearer eyJ..."
# ✅ Should return all farms
```

### 2. Test Nha Nông Access

```bash
# Login as Nha nông
curl -X POST http://localhost:8000/api/auth/login \
  -d "username=nhanong1&password=farmer123"

# Try to access all farms
curl http://localhost:8000/api/farms/ \
  -H "Authorization: Bearer TOKEN"
# ✅ Should return only farms assigned to this user

# Try to create farm (should fail)
curl -X POST http://localhost:8000/api/farms/ \
  -H "Authorization: Bearer TOKEN" \
  -d '{"ma_vung":"TEST"}'
# ❌ Should return 403 Forbidden
```

### 3. Test Public Access

```bash
# No token needed
curl http://localhost:8000/api/qr/trace/MSVT001
# ✅ Should return public traceability info
```

---

## 📊 Permission Decision Tree

```
┌─────────────────────────────────────┐
│   User requests access to resource  │
└──────────────┬──────────────────────┘
               │
               ▼
         Is authenticated?
           ┌───┴───┐
          No      Yes
           │       │
           ▼       ▼
    Is public    Check role
    endpoint?      │
     ┌──┴──┐      ├─────────┬─────────┐
    No    Yes    Admin   Nha Nông  Khách
     │     │      │        │         │
     ▼     ▼      ▼        ▼         ▼
   401   Allow  Full    Filtered  Public
 Unauthorized   Access   Access   Access
```

---

## 🔒 Security Best Practices

1. **JWT Token:**

     - Short expiration (30 min)
     - Secure secret key
     - HTTPS only in production

2. **Password:**

     - Bcrypt hashing
     - Minimum 8 characters
     - No plain text storage

3. **API Security:**

     - Rate limiting
     - Input validation
     - SQL injection prevention (use ORM)
     - XSS prevention (sanitize inputs)

4. **Access Control:**
     - Always check ownership
     - Validate foreign keys
     - Log all sensitive operations

---

**Last Updated:** 02/01/2026  
**Status:** ⏳ TO BE IMPLEMENTED
