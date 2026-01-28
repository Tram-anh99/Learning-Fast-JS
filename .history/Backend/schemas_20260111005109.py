"""
========== Pydantic Schemas ==========
Purpose: Define Request/Response models cho FastAPI
Architecture: Data validation và serialization với Pydantic

Module này định nghĩa:
- Request schemas: Validate input data từ client
- Response schemas: Format output data cho client
- Base schemas: Các model dùng chung
- DTO (Data Transfer Objects) giữa layers

Pydantic Benefits:
- Tự động validate type và format
- Parse JSON thành Python objects
- Serialize Python objects thành JSON
- Generate OpenAPI/Swagger documentation

Kết nối đến:
- routes/*.py: Import schemas để validate request/response
- models/*.py: Map SQLAlchemy models sang Pydantic schemas
- FastAPI: Auto-validate request body, query params, path params

Structure:
1. Health & Base Schemas (utility schemas)
2. Vùng Trồng Schemas (Farm/Vung models)
3. Loại Cây Schemas (Crop type models)
4. Chủ Vùng Schemas (Farm owner models)
5. Lịch Sử Canh Tác Schemas (Activity history models)
6. Thống Kê Schemas (Statistics models)
7. Chart Schemas (Chart data models)
8. Search & Filter Schemas (Query parameters)
"""

# Import Pydantic classes để tạo schemas
# BaseModel: Base class, Field: Field config, ConfigDict: Model config
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List  # Optional: Field có thể None, List: Array type
# date: Date only (YYYY-MM-DD), datetime: Date + time
from datetime import date, datetime


# ========================================================================
# ========== SECTION 1: HEALTH & BASE SCHEMAS ==========
# ========================================================================

class HealthResponse(BaseModel):
    """
    Schema cho health check endpoint response

    Usage: GET /api/health

    Response example:
    {
        "status": "healthy",
        "message": "Backend API is running",
        "version": "1.0.0",
        "database_connected": true,
        "total_tables": 18
    }

    Kết nối đến:
    - app.py: health_check() endpoint return HealthResponse
    - Frontend: api.js -> getHealthStatus() parse response này
    """
    status: str                  # "healthy" hoặc "unhealthy"
    message: str                 # Message mô tả trạng thái
    version: str                 # API version (1.0.0)
    database_connected: bool     # Database connection status (true/false)
    total_tables: int            # Số bảng trong schema (18 tables)


class ResponseBase(BaseModel):
    """
    Base schema cho generic API responses

    Usage: Return generic success/error messages

    Example:
    {
        "success": true,
        "message": "Operation completed",
        "data": {"key": "value"}
    }

    Kết nối đến:
    - routes/*.py: Return ResponseBase cho các operations đơn giản
    """
    success: bool                          # True/False để chỉ success status
    message: str                           # Message mô tả kết quả
    data: Optional[dict] = None           # Optional data payload


# ========================================================================
# ========== SECTION 2: VÙNG TRỒNG (FARMS) SCHEMAS ==========
# ========================================================================

class ToaDoBase(BaseModel):
    """
    Base schema cho tọa độ (coordinates) của vùng trồng

    Fields:
    - latitude: Vĩ độ (North/South) - VD: 10.7626
    - longitude: Kinh độ (East/West) - VD: 106.6821
    - thu_tu: Thứ tự điểm trong polygon (1, 2, 3, ...)

    Usage:
    - Tạo polygon trên bản đồ để đánh dấu ranh giới vùng trồng
    - Mỗi vùng trồng có nhiều tọa độ (List[ToaDo])

    Kết nối đến:
    - models/toa_do.py: ToaDo SQLAlchemy model
    - Frontend: MapComponent.vue -> draw polygon on map
    """
    latitude: float     # Vĩ độ (lat) - float để support decimal degrees
    longitude: float    # Kinh độ (lng) - float để support decimal degrees
    thu_tu: int         # Thứ tự điểm (1, 2, 3, ...) để vẽ polygon đúng order


class ToaDoResponse(ToaDoBase):
    """
    Response schema cho tọa độ (có thêm id từ database)

    Inherits: ToaDoBase (latitude, longitude, thu_tu)
    Adds: id (primary key từ database)

    Usage: GET /api/farms/{id} -> return farm với list coordinates

    Kết nối đến:
    - routes/farms.py: get_farm_by_id() return VungTrongDetail với toa_do: List[ToaDoResponse]
    """
    id: int  # Primary key từ bảng nongsan.toa_do

    # ConfigDict config cho Pydantic v2
    # from_attributes=True: Allow create từ SQLAlchemy model (model.id, model.latitude, ...)
    model_config = ConfigDict(from_attributes=True)


class VungTrongBase(BaseModel):
    """
    Base schema cho Vùng Trồng (Farm) - các fields cơ bản

    Fields:
    - ma_vung: Mã vùng trồng (unique code) - VD: "MSVT001"
    - ten_vung: Tên vùng trồng - VD: "Vườn A"
    - dia_chi: Địa chỉ vùng trồng
    - dien_tich_ha: Diện tích (hecta)
    - ngay_cap_ma: Ngày cấp mã vùng trồng
    - ngay_het_han: Ngày hết hạn mã

    Usage: Base schema được kế thừa bởi Create/Response schemas

    Kết nối đến:
    - models/vung.py: Vung SQLAlchemy model
    - Bảng: nongsan.vung
    """
    ma_vung: str                          # Mã vùng (unique) - VD: "MSVT001"
    ten_vung: str                         # Tên vùng - VD: "Vườn A"
    dia_chi: Optional[str] = None        # Địa chỉ (optional)
    dien_tich_ha: Optional[float] = None  # Diện tích hecta (optional)
    ngay_cap_ma: Optional[date] = None   # Ngày cấp mã (optional)
    ngay_het_han: Optional[date] = None  # Ngày hết hạn (optional)


class VungTrongCreate(VungTrongBase):
    """
    Schema cho creating new Vùng Trồng (POST request)

    Inherits: VungTrongBase (ma_vung, ten_vung, dia_chi, ...)
    Adds:
    - chu_vung_id: FK đến bảng chu_vung (owner)
    - trang_thai_id: FK đến bảng trang_thai (status)
    - toa_do: List coordinates để vẽ polygon

    Usage: POST /api/farms/
    Request body: VungTrongCreate

    Example:
    {
        "ma_vung": "MSVT004",
        "ten_vung": "Vườn D",
        "dia_chi": "123 Street",
        "dien_tich_ha": 5.5,
        "chu_vung_id": 1,
        "trang_thai_id": 1,
        "toa_do": [
            {"latitude": 10.7626, "longitude": 106.6821, "thu_tu": 1},
            {"latitude": 10.7627, "longitude": 106.6822, "thu_tu": 2}
        ]
    }

    Kết nối đến:
    - routes/farms.py: create_farm(farm: VungTrongCreate)
    - Frontend: api.js -> createFarm(farmData)
    """
    chu_vung_id: Optional[int] = None           # FK to chu_vung.id (owner)
    trang_thai_id: Optional[int] = None         # FK to trang_thai.id (status)
    toa_do: Optional[List[ToaDoBase]] = []      # List tọa độ để vẽ polygon


class VungTrongResponse(VungTrongBase):
    """
    Schema cho Vùng Trồng response (GET request)

    Inherits: VungTrongBase
    Adds:
    - id: Primary key
    - chu_vung_id, trang_thai_id: Foreign keys
    - created_at: Timestamp tạo record

    Usage: GET /api/farms/ -> List[VungTrongResponse]

    Kết nối đến:
    - routes/farms.py: get_farms() return List[VungTrongResponse]
    - Frontend: HomeView.vue, QuanLyView.vue display farm list
    """
    id: int                              # Primary key từ vung.id
    chu_vung_id: Optional[int] = None    # FK to chu_vung.id
    trang_thai_id: Optional[int] = None  # FK to trang_thai.id
    created_at: datetime                 # Timestamp khi tạo record

    # Allow parse from SQLAlchemy model
    model_config = ConfigDict(from_attributes=True)


class VungTrongDetail(VungTrongResponse):
    """
    Schema chi tiết Vùng Trồng với relationships (join tables)

    Inherits: VungTrongResponse
    Adds:
    - toa_do: List tọa độ (JOIN với bảng toa_do)
    - chu_vung: Thông tin chủ vùng (JOIN với bảng chu_vung)
    - trang_thai: Thông tin trạng thái (JOIN với bảng trang_thai)
    - cay_trong: List cây trồng trong vùng (JOIN với bảng cay_trong)

    Usage: GET /api/farms/{id} -> VungTrongDetail (1 record với full info)

    Example response:
    {
        "id": 1,
        "ma_vung": "MSVT001",
        "ten_vung": "Vườn A",
        "toa_do": [
            {"id": 1, "latitude": 10.7626, "longitude": 106.6821, "thu_tu": 1}
        ],
        "chu_vung": {
            "id": 1,
            "ten_chu": "Nguyễn Văn A"
        },
        "trang_thai": {
            "id": 1,
            "ten_trang_thai": "Còn hạn"
        },
        "cay_trong": [
            {"id": 1, "ten_cay": "Lúa"}
        ]
    }

    Kết nối đến:
    - routes/farms.py: get_farm_by_id(id) return VungTrongDetail
    - Frontend: MapComponent.vue -> display farm details on map
    """
    toa_do: List[ToaDoResponse] = []    # List tọa độ (coordinates)
    chu_vung: Optional[dict] = None      # Chủ vùng info (owner)
    trang_thai: Optional[dict] = None    # Trạng thái info (status)
    cay_trong: List[dict] = []           # List cây trồng (crops)


# ========================================================================
# ========== SECTION 3: LOẠI CÂY (CROP TYPES) SCHEMAS ==========
# ========================================================================

class LoaiCayBase(BaseModel):
    """
    Base schema cho Loại Cây (Crop Type)

    Fields:
    - ma_cay: Mã loại cây (unique code) - VD: "LUA01"
    - ten_cay: Tên loại cây - VD: "Lúa"
    - ten_khoa_hoc: Tên khoa học - VD: "Oryza sativa"
    - mo_ta: Mô tả loại cây

    Usage: Base schema cho Create/Response

    Kết nối đến:
    - models/loai_cay.py: LoaiCay SQLAlchemy model
    - Bảng: nongsan.loai_cay
    """
    ma_cay: str                           # Mã loại cây (unique)
    ten_cay: str                          # Tên loại cây
    ten_khoa_hoc: Optional[str] = None   # Tên khoa học (optional)
    mo_ta: Optional[str] = None          # Mô tả (optional)


class LoaiCayCreate(LoaiCayBase):
    """
    Schema cho creating new Loại Cây

    Usage: POST /api/crops/

    Kết nối đến:
    - routes/crops.py: create_crop(crop: LoaiCayCreate)
    """
    pass  # Không có thêm fields, chỉ inherit LoaiCayBase


class LoaiCayResponse(LoaiCayBase):
    """
    Schema cho Loại Cây response

    Adds:
    - id: Primary key
    - created_at: Timestamp

    Usage: GET /api/crops/ -> List[LoaiCayResponse]

    Kết nối đến:
    - routes/crops.py: get_crops() return List[LoaiCayResponse]
    """
    id: int              # Primary key từ loai_cay.id
    created_at: datetime  # Timestamp tạo record

    model_config = ConfigDict(from_attributes=True)


# ========================================================================
# ========== SECTION 4: CHỦ VÙNG (FARM OWNERS) SCHEMAS ==========
# ========================================================================

class ChuVungBase(BaseModel):
    """
    Base schema cho Chủ Vùng (Farm Owner)

    Fields:
    - ma_chu: Mã chủ vùng (unique code)
    - ten_chu: Tên chủ vùng
    - loai_chu: Loại chủ ("ca_nhan", "doanh_nghiep", "hop_tac_xa")
    - cccd_mst: CCCD (cá nhân) hoặc MST (doanh nghiệp)
    - dia_chi: Địa chỉ
    - dien_thoai: Số điện thoại
    - email: Email

    Usage: Base schema cho Create/Response

    Kết nối đến:
    - models/chu_vung.py: ChuVung SQLAlchemy model
    - Bảng: nongsan.chu_vung
    """
    ma_chu: Optional[str] = None         # Mã chủ (optional, có thể auto-generate)
    ten_chu: str                         # Tên chủ vùng (required)
    loai_chu: Optional[str] = "ca_nhan"  # Loại chủ (default: "ca_nhan")
    cccd_mst: Optional[str] = None       # CCCD/MST (optional)
    dia_chi: Optional[str] = None        # Địa chỉ (optional)
    dien_thoai: Optional[str] = None     # Điện thoại (optional)
    email: Optional[str] = None          # Email (optional)


class ChuVungCreate(ChuVungBase):
    """
    Schema cho creating new Chủ Vùng

    Usage: POST /api/owners/

    Kết nối đến:
    - routes/owners.py: create_owner(owner: ChuVungCreate)
    """
    pass  # No additional fields


class ChuVungResponse(ChuVungBase):
    """
    Schema cho Chủ Vùng response

    Adds:
    - id: Primary key
    - created_at: Timestamp

    Usage: GET /api/owners/ -> List[ChuVungResponse]

    Kết nối đến:
    - routes/owners.py: get_owners() return List[ChuVungResponse]
    """
    id: int              # Primary key từ chu_vung.id
    created_at: datetime  # Timestamp tạo record

    model_config = ConfigDict(from_attributes=True)


# ========================================================================
# ========== SECTION 5: LỊCH SỬ CANH TÁC (ACTIVITY HISTORY) SCHEMAS ==========
# ========================================================================

class LichSuCanhTacBase(BaseModel):
    """
    Base schema cho Lịch Sử Canh Tác (Activity History)

    Fields matching database columns:
    - vung_trong_id: FK to vung_trong.id (required)
    - loai_hoat_dong_id: FK to loai_hoat_dong.id  
    - ngay_thuc_hien: Ngày thực hiện hoạt động
    - tieu_de: Tiêu đề hoạt động
    - noi_dung: Nội dung chi tiết
    - nguoi_thuc_hien: Người thực hiện
    - thua_ruong: Thửa ruộng
    - phan_bon_id: FK to phan_bon.id
    - lieu_luong_phan_bon: Liều lượng phân bón
    - thuoc_bvtv_id: FK to thuoc_bvtv.id
    - lieu_luong_thuoc: Liều lượng thuốc
    - ghi_chu: Ghi chú

    Usage: Base schema cho Create/Response
    """
    vung_trong_id: int                           # FK (required)
    loai_hoat_dong_id: Optional[int] = None      # FK loại hoạt động
    ngay_thuc_hien: date                         # Ngày thực hiện (required)
    tieu_de: Optional[str] = None                # Tiêu đề
    noi_dung: Optional[str] = None               # Nội dung chi tiết
    nguoi_thuc_hien: Optional[str] = None        # Người thực hiện
    thua_ruong: Optional[str] = None             # Thửa ruộng
    phan_bon_id: Optional[int] = None            # FK phân bón
    lieu_luong_phan_bon: Optional[str] = None    # Liều lượng phân bón
    thuoc_bvtv_id: Optional[int] = None          # FK thuốc BVTV
    lieu_luong_thuoc: Optional[str] = None       # Liều lượng thuốc
    ghi_chu: Optional[str] = None                # Ghi chú


class LichSuCanhTacCreate(LichSuCanhTacBase):
    """
    Schema cho creating new Lịch Sử Canh Tác

    Usage: POST /api/diary/

    Kết nối đến:
    - routes/diary.py: create_diary(diary: LichSuCanhTacCreate)
    - Frontend: DiaryActivityForm.vue submit form
    """
    pass


class LichSuCanhTacResponse(LichSuCanhTacBase):
    """
    Schema cho Lịch Sử Canh Tác response

    Adds:
    - id: Primary key
    - ngay_tao: Timestamp tạo record (from model)
    - ngay_cap_nhat: Timestamp cập nhật (from model)

    Usage: GET /api/diary/ -> List[LichSuCanhTacResponse]
    """
    id: int                            # Primary key
    ngay_tao: Optional[datetime] = None      # Timestamp tạo
    ngay_cap_nhat: Optional[datetime] = None  # Timestamp cập nhật

    model_config = ConfigDict(from_attributes=True)


# ========================================================================
# ========== SECTION 6: THỐNG KÊ (STATISTICS) SCHEMAS ==========
# ========================================================================

class ThongKeResponse(BaseModel):
    """
    Schema cho thống kê tổng quan

    Fields:
    - tong_vung_trong: Tổng số vùng trồng
    - vung_con_han: Số vùng còn hạn
    - vung_sap_het_han: Số vùng sắp hết hạn (< 30 ngày)
    - vung_het_han: Số vùng hết hạn
    - tong_dien_tich: Tổng diện tích (hecta)
    - tong_san_luong: Tổng sản lượng (tấn)

    Usage: GET /api/stats/overview -> ThongKeResponse

    Kết nối đến:
    - routes/charts.py: get_stats() return ThongKeResponse
    - Frontend: StatsBarComponent.vue display stats
    """
    tong_vung_trong: int      # Tổng số vùng
    vung_con_han: int         # Vùng còn hạn
    vung_sap_het_han: int     # Vùng sắp hết hạn
    vung_het_han: int         # Vùng hết hạn
    tong_dien_tich: float     # Tổng diện tích (ha)
    tong_san_luong: float     # Tổng sản lượng (tấn)


class DashboardStats(BaseModel):
    """
    Schema cho dashboard statistics (tổng hợp nhiều loại stats)

    Fields:
    - total_farms: Tổng số vùng trồng
    - active_farms: Số vùng đang hoạt động
    - total_area_ha: Tổng diện tích (hecta)
    - total_production: Tổng sản lượng
    - recent_activities: Số hoạt động gần đây
    - chart_data: Dữ liệu cho các biểu đồ

    Usage: GET /api/dashboard/stats -> DashboardStats

    Kết nối đến:
    - routes/charts.py: get_dashboard_stats() return DashboardStats
    - Frontend: QuanLyView.vue display dashboard
    """
    total_farms: int           # Tổng số vùng
    active_farms: int          # Vùng đang hoạt động
    total_area_ha: float       # Tổng diện tích
    total_production: float    # Tổng sản lượng
    recent_activities: int     # Số hoạt động gần đây
    chart_data: dict           # Data cho charts (flexible dict)


# ========================================================================
# ========== SECTION 7: CHART SCHEMAS ==========
# ========================================================================

class ChartDataset(BaseModel):
    """
    Schema cho 1 dataset trong Chart (Chart.js format)

    Fields:
    - label: Label của dataset (VD: "Sản lượng 2024")
    - data: Array số liệu (VD: [10, 20, 30, 40])
    - backgroundColor: Màu nền (1 màu hoặc array màu)
    - borderColor: Màu viền
    - tension: Độ cong của line chart (0.0 - 1.0)

    Usage: Part of ChartData

    Example:
    {
        "label": "Sản lượng 2024",
        "data": [10, 20, 30],
        "backgroundColor": "#4CAF50",
        "borderColor": "#2E7D32",
        "tension": 0.4
    }

    Kết nối đến:
    - Frontend: Chart components (BarChartComponent.vue, LineChartComponent.vue)
    - Chart.js library
    """
    label: Optional[str] = None                      # Label của dataset
    data: List[float]                                # Array data points
    # Màu nền (single hoặc array)
    backgroundColor: Optional[str | List[str]] = None
    borderColor: Optional[str] = None                # Màu viền
    tension: Optional[float] = None                  # Line tension (0.0 - 1.0)


class ChartData(BaseModel):
    """
    Schema cho Chart data (Chart.js format)

    Fields:
    - labels: Array labels cho trục X (VD: ["Jan", "Feb", "Mar"])
    - datasets: Array of ChartDataset

    Usage: Return chart data cho Frontend

    Example:
    {
        "labels": ["Jan", "Feb", "Mar"],
        "datasets": [
            {
                "label": "Sản lượng",
                "data": [10, 20, 30],
                "backgroundColor": "#4CAF50"
            }
        ]
    }

    Kết nối đến:
    - routes/charts.py: All chart endpoints return ChartData
    - Frontend: BarChartComponent.vue, LineChartComponent.vue, PieChartComponent.vue
    """
    labels: List[str]           # Labels cho trục X
    datasets: List[ChartDataset]  # Array datasets


# ========================================================================
# ========== SECTION 8: SEARCH & FILTER SCHEMAS ==========
# ========================================================================

class SearchParams(BaseModel):
    """
    Schema cho search/filter parameters

    Fields:
    - query: Search query string (tìm theo tên, mã, ...)
    - trang_thai_id: Filter theo trạng thái
    - chu_vung_id: Filter theo chủ vùng
    - skip: Số records bỏ qua (pagination)
    - limit: Số records tối đa trả về (pagination)

    Usage: GET /api/farms/?query=Vườn&trang_thai_id=1&skip=0&limit=10

    Example:
    {
        "query": "Vườn",
        "trang_thai_id": 1,
        "chu_vung_id": null,
        "skip": 0,
        "limit": 10
    }

    Kết nối đến:
    - routes/farms.py: search_farms(params: SearchParams)
    - Frontend: Search/filter components
    """
    query: Optional[str] = None          # Search query
    trang_thai_id: Optional[int] = None  # Filter by status
    chu_vung_id: Optional[int] = None    # Filter by owner
    skip: int = 0                         # Pagination: skip records
    limit: int = 100                      # Pagination: max records


class PaginatedResponse(BaseModel):
    """
    Schema cho paginated response

    Fields:
    - total: Tổng số records (để tính total pages)
    - skip: Số records đã bỏ qua
    - limit: Số records tối đa mỗi page
    - data: Array data cho page hiện tại

    Usage: GET /api/farms/ -> PaginatedResponse

    Example:
    {
        "total": 100,
        "skip": 0,
        "limit": 10,
        "data": [
            {"id": 1, "ma_vung": "MSVT001", ...},
            {"id": 2, "ma_vung": "MSVT002", ...}
        ]
    }

    Frontend calculation:
    - current_page = skip / limit + 1
    - total_pages = ceil(total / limit)
    - has_next = skip + limit < total

    Kết nối đến:
    - routes/farms.py: get_farms() return PaginatedResponse
    - Frontend: DataTableComponent.vue display paginated data
    """
    total: int         # Tổng số records
    skip: int          # Records đã bỏ qua
    limit: int         # Max records per page
    data: List[dict]   # Data array cho page hiện tại


# ========================================================================
# ========== SECTION 8: PHÂN BÓN & THUỐC BVTV SCHEMAS ==========
# ========================================================================

# --- Loại Phân Bón Schemas ---
class LoaiPhanBonBase(BaseModel):
    ma_loai: str = Field(..., description='Mã loại phân bón (unique)')
    ten_loại: str = Field(..., description='Tên loại')
    mo_ta: Optional[str] = Field(None, description='Mô tả')


class LoaiPhanBonCreate(LoaiPhanBonBase):
    pass


class LoaiPhanBonResponse(LoaiPhanBonBase):
    id: int
    ngay_tao: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Phân Bón Schemas ---


class PhanBonBase(BaseModel):
    ma_phan_bon: str = Field(..., description='Mã phân bón (unique)')
    ten_phan_bon: str = Field(..., description='Tên phân bón')
    loai_phan_bon_id: Optional[int] = Field(
        None, description='ID loại phân bón')
    thanh_phan: Optional[str] = Field(None, description='Thành phần hóa học')
    don_vi: Optional[str] = Field(None, description='Đơn vị (kg, tấn, bao)')
    mo_ta: Optional[str] = Field(None, description='Mô tả, hướng dẫn')


class PhanBonCreate(PhanBonBase):
    pass


class PhanBonResponse(PhanBonBase):
    id: int
    ngay_tao: datetime
    loai_phan_bon: Optional[LoaiPhanBonResponse] = None
    model_config = ConfigDict(from_attributes=True)

# --- Nhóm Thuốc BVTV Schemas ---


class NhomThuocBVTVBase(BaseModel):
    ma_nhom: str = Field(..., description='Mã nhóm (unique)')
    ten_nhom: str = Field(..., description='Tên nhóm')
    mo_ta: Optional[str] = Field(None, description='Mô tả')


class NhomThuocBVTVCreate(NhomThuocBVTVBase):
    pass


class NhomThuocBVTVResponse(NhomThuocBVTVBase):
    id: int
    ngay_tao: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Thuốc BVTV Schemas ---


class ThuocBVTVBase(BaseModel):
    ma_thuoc: str = Field(..., description='Mã thuốc (unique)')
    ten_thuoc: str = Field(..., description='Tên thương mại')
    ten_hoat_chat: Optional[str] = Field(None, description='Tên hoạt chất')
    ham_luong: Optional[str] = Field(None, description='Hàm lượng (%)')
    nhom_thuoc_id: Optional[int] = Field(None, description='ID nhóm thuốc')
    dang_bao_che: Optional[str] = Field(
        None, description='Dạng bào chế (EC, WP, SC)')
    trang_thai_su_dung: Optional[str] = Field(
        None, description='Trạng thái (Được phép, Hạn chế, Cấm)')
    mo_ta: Optional[str] = Field(None, description='Mô tả, hướng dẫn')


class ThuocBVTVCreate(ThuocBVTVBase):
    pass


class ThuocBVTVResponse(ThuocBVTVBase):
    id: int
    ngay_tao: datetime
    nhom_thuoc: Optional[NhomThuocBVTVResponse] = None
    model_config = ConfigDict(from_attributes=True)
