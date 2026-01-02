# 🔐 TODO: AUTHENTICATION SYSTEM

## 📋 TỔNG QUAN

Hệ thống đang thiếu chức năng **Authentication & Authorization (RBAC)**. Đây là yêu cầu quan trọng để phân quyền người dùng theo 3 vai trò: Admin, Nha nông, Khách.

---

## 🎯 MỤC TIÊU

### 1. User Authentication
- Login/Logout functionality
- JWT token management
- Password hashing (bcrypt)
- Session management
- Remember me feature

### 2. Role-Based Access Control (RBAC)
- **Admin:** Full access (CRUD tất cả)
- **Nha nông:** CRUD nhật ký của vùng mình quản lý
- **Khách:** Read-only truy xuất nguồn gốc (public)

### 3. User Management
- CRUD users (Admin only)
- Assign roles (Admin only)
- Change password
- Profile management

---

## 📦 BACKEND TASKS

### Phase 1: Database Models (2-3 giờ)

#### 1.1 Tạo User Model
**File:** `Backend/models/user.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    NHA_NONG = "NHA_NONG"
    KHACH = "KHACH"

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'nongsan'}
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    phone = Column(String(20))
    
    role = Column(Enum(UserRole), default=UserRole.KHACH, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationship: Nha nông có thể quản lý nhiều vùng
    managed_farms = relationship("VungTrong", back_populates="user", foreign_keys="[VungTrong.user_id]")
    
    # Relationship: User tạo nhật ký
    diary_entries = relationship("LichSuCanhTac", back_populates="user", foreign_keys="[LichSuCanhTac.user_id]")
```

#### 1.2 Update VungTrong Model
**File:** `Backend/models/vung_trong.py`

Thêm field:
```python
user_id = Column(Integer, ForeignKey('nongsan.users.id'), nullable=True, comment='ID người quản lý')
user = relationship("User", back_populates="managed_farms", foreign_keys=[user_id])
```

#### 1.3 Update LichSuCanhTac Model
**File:** `Backend/models/lich_su.py`

Thêm field:
```python
user_id = Column(Integer, ForeignKey('nongsan.users.id'), nullable=True, comment='ID người tạo nhật ký')
user = relationship("User", back_populates="diary_entries", foreign_keys=[user_id])
```

#### 1.4 Database Migration
```sql
-- Create users table
CREATE TABLE nongsan.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(20),
    role VARCHAR(20) DEFAULT 'KHACH' NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Add user_id to vung_trong
ALTER TABLE nongsan.vung_trong ADD COLUMN user_id INTEGER REFERENCES nongsan.users(id);

-- Add user_id to lich_su_canh_tac
ALTER TABLE nongsan.lich_su_canh_tac ADD COLUMN user_id INTEGER REFERENCES nongsan.users(id);

-- Create indexes
CREATE INDEX idx_users_email ON nongsan.users(email);
CREATE INDEX idx_users_username ON nongsan.users(username);
CREATE INDEX idx_vung_trong_user ON nongsan.vung_trong(user_id);
CREATE INDEX idx_lich_su_user ON nongsan.lich_su_canh_tac(user_id);

-- Insert default admin user (password: admin123)
INSERT INTO nongsan.users (email, username, hashed_password, full_name, role, is_active, is_verified)
VALUES ('admin@example.com', 'admin', '$2b$12$...', 'Administrator', 'ADMIN', TRUE, TRUE);
```

---

### Phase 2: Authentication Logic (3-4 giờ)

#### 2.1 Install Dependencies
```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

#### 2.2 Create Auth Utils
**File:** `Backend/utils/auth.py`

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

#### 2.3 Create Auth Dependencies
**File:** `Backend/dependencies/auth.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserRole
from utils.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def require_admin(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

async def require_nha_nong(
    current_user: User = Depends(get_current_active_user)
) -> User:
    if current_user.role not in [UserRole.ADMIN, UserRole.NHA_NONG]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

---

### Phase 3: API Routes (4-5 giờ)

#### 3.1 Auth Routes
**File:** `Backend/routes/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models.user import User
from utils.auth import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies.auth import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(
    email: str,
    username: str,
    password: str,
    full_name: str,
    db: Session = Depends(get_db)
):
    """Đăng ký tài khoản mới (role mặc định: KHACH)"""
    # Check existing user
    existing = db.query(User).filter(
        (User.email == email) | (User.username == username)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    
    # Create user
    user = User(
        email=email,
        username=username,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        role="KHACH"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "User created successfully", "user_id": user.id}

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Đăng nhập và nhận JWT token"""
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role
        }
    }

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Lấy thông tin user hiện tại"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active
    }

@router.post("/change-password")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Đổi mật khẩu"""
    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}
```

#### 3.2 User Management Routes
**File:** `Backend/routes/users.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserRole
from dependencies.auth import require_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def list_users(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Lấy danh sách users (Admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    total = db.query(User).count()
    
    return {
        "items": users,
        "total": total,
        "page": skip // limit + 1,
        "size": limit
    }

@router.put("/{user_id}/role")
async def change_user_role(
    user_id: int,
    new_role: UserRole,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Đổi role của user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.role = new_role
    db.commit()
    
    return {"message": f"User role updated to {new_role}"}

@router.put("/{user_id}/status")
async def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    """Kích hoạt/vô hiệu hóa user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = not user.is_active
    db.commit()
    
    return {"message": f"User {'activated' if user.is_active else 'deactivated'}"}
```

#### 3.3 Update Existing Routes với Auth

**Farms Routes:** Thêm auth vào POST/PUT/DELETE
```python
# Backend/routes/farms.py
from dependencies.auth import require_admin

@router.post("/")
async def create_farm(
    farm_data: VungTrongCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)  # ⭐ ADD THIS
):
    # ... existing code
```

**Diary Routes:** Thêm filter by user
```python
# Backend/routes/diary.py
from dependencies.auth import require_nha_nong, get_current_active_user

@router.get("/")
async def list_diary(
    ma_vung: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)  # ⭐ ADD THIS
):
    query = db.query(LichSuCanhTac)
    
    # Nha nông chỉ xem nhật ký vùng mình quản lý
    if current_user.role == UserRole.NHA_NONG:
        farm_ids = [f.id for f in current_user.managed_farms]
        query = query.filter(LichSuCanhTac.vung_trong_id.in_(farm_ids))
    
    # ... rest of code
```

---

## 🎨 FRONTEND TASKS

### Phase 4: Frontend Auth (5-6 giờ)

#### 4.1 Auth Store/Composable
**File:** `Frontend/src/composables/useAuth.js`

```javascript
import { ref, computed } from 'vue';

const user = ref(null);
const token = ref(localStorage.getItem('token') || null);

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value);
  const isAdmin = computed(() => user.value?.role === 'ADMIN');
  const isNhaNong = computed(() => user.value?.role === 'NHA_NONG');
  
  async function login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    const response = await fetch('http://localhost:8000/api/auth/login', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Login failed');
    }
    
    const data = await response.json();
    token.value = data.access_token;
    user.value = data.user;
    localStorage.setItem('token', data.access_token);
  }
  
  async function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
  }
  
  async function fetchCurrentUser() {
    if (!token.value) return;
    
    const response = await fetch('http://localhost:8000/api/auth/me', {
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    });
    
    if (response.ok) {
      user.value = await response.json();
    }
  }
  
  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    isNhaNong,
    login,
    logout,
    fetchCurrentUser
  };
}
```

#### 4.2 Login Component
**File:** `Frontend/src/views/LoginView.vue`

```vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-blue-50">
    <div class="bg-white p-8 rounded-lg shadow-xl w-full max-w-md">
      <h2 class="text-2xl font-bold text-center mb-6">Đăng Nhập</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-sm font-medium mb-2">Tên đăng nhập</label>
          <input 
            v-model="username" 
            type="text" 
            class="w-full px-4 py-2 border rounded-lg"
            required
          />
        </div>
        
        <div class="mb-6">
          <label class="block text-sm font-medium mb-2">Mật khẩu</label>
          <input 
            v-model="password" 
            type="password" 
            class="w-full px-4 py-2 border rounded-lg"
            required
          />
        </div>
        
        <button 
          type="submit" 
          class="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700"
          :disabled="loading"
        >
          {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
        </button>
        
        <div v-if="error" class="mt-4 text-red-600 text-center">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '@/composables/useAuth';

const router = useRouter();
const { login } = useAuth();

const username = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

async function handleLogin() {
  try {
    loading.value = true;
    error.value = '';
    await login(username.value, password.value);
    router.push('/');
  } catch (err) {
    error.value = 'Sai tên đăng nhập hoặc mật khẩu';
  } finally {
    loading.value = false;
  }
}
</script>
```

#### 4.3 Route Guards
**File:** `Frontend/src/router/index.js`

```javascript
import { useAuth } from '@/composables/useAuth';

router.beforeEach((to, from, next) => {
  const { isAuthenticated, isAdmin } = useAuth();
  
  // Routes yêu cầu login
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/login');
    return;
  }
  
  // Routes chỉ dành cho Admin
  if (to.meta.requiresAdmin && !isAdmin.value) {
    next('/');
    return;
  }
  
  next();
});

// Update routes
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/quan-ly',
    name: 'QuanLy',
    component: () => import('@/views/QuanLyView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/diary',
    name: 'Diary',
    component: () => import('@/views/DiaryPage.vue'),
    meta: { requiresAuth: true }
  }
];
```

#### 4.4 Update API Calls với Bearer Token
**File:** `Frontend/src/services/api.js`

```javascript
import { useAuth } from '@/composables/useAuth';

export async function apiFetch(url, options = {}) {
  const { token } = useAuth();
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers
  };
  
  if (token.value) {
    headers['Authorization'] = `Bearer ${token.value}`;
  }
  
  const response = await fetch(url, {
    ...options,
    headers
  });
  
  if (response.status === 401) {
    // Token expired, redirect to login
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }
  
  return response;
}
```

---

## 📊 EFFORT ESTIMATE

| Task | Thời gian | Độ khó |
|------|-----------|--------|
| Database Models | 2-3 giờ | Medium |
| Auth Utils & Dependencies | 3-4 giờ | Medium |
| Backend API Routes | 4-5 giờ | Medium-High |
| Frontend Auth Store | 2-3 giờ | Medium |
| Frontend UI Components | 3-4 giờ | Easy-Medium |
| Testing & Debugging | 3-4 giờ | Medium |
| **TỔNG** | **17-23 giờ** | **2-3 ngày** |

---

## ✅ TESTING CHECKLIST

### Backend Testing
- [ ] Register new user (role: KHACH)
- [ ] Login with credentials
- [ ] Get current user info (GET /api/auth/me)
- [ ] Change password
- [ ] Admin can list all users
- [ ] Admin can change user roles
- [ ] Admin can activate/deactivate users
- [ ] Nha nông can only access their farms
- [ ] Public endpoints work without auth (QR trace)

### Frontend Testing
- [ ] Login form validation
- [ ] Successful login redirects to home
- [ ] Failed login shows error
- [ ] Protected routes require auth
- [ ] Admin-only routes check role
- [ ] Token stored in localStorage
- [ ] Logout clears token
- [ ] Auto-redirect on 401

---

## 🚀 DEPLOYMENT NOTES

### Environment Variables
```bash
# Backend .env
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend .env
VITE_API_URL=https://api.yoursite.com
```

### Security Best Practices
- ✅ Use strong SECRET_KEY (random 32+ chars)
- ✅ Enable HTTPS in production
- ✅ Set short token expiration (30 min)
- ✅ Implement refresh tokens for better UX
- ✅ Add rate limiting to login endpoint
- ✅ Log failed login attempts
- ✅ Implement 2FA for Admin accounts

---

## 📚 REFERENCES

- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- JWT: https://jwt.io/
- Passlib: https://passlib.readthedocs.io/
- Vue Router Guards: https://router.vuejs.org/guide/advanced/navigation-guards.html

---

**Created:** 01/01/2026  
**Priority:** HIGH  
**Complexity:** MEDIUM-HIGH  
**Status:** TODO (Not Started)
