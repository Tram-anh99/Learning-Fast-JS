"""
========== Pydantic Schemas ==========
Request/Response models
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime


# ========== Health & Base Schemas ==========

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str
    database_connected: bool
    total_tables: int


class ResponseBase(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


# ========== Vùng Trồng Schemas ==========

class ToaDoBase(BaseModel):
    latitude: float
    longitude: float
    thu_tu: int


class ToaDoResponse(ToaDoBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class VungTrongBase(BaseModel):
    ma_vung: str
    ten_vung: str
    dia_chi: Optional[str] = None
    dien_tich_ha: Optional[float] = None
    ngay_cap_ma: Optional[date] = None
    ngay_het_han: Optional[date] = None


class VungTrongCreate(VungTrongBase):
    chu_vung_id: Optional[int] = None
    trang_thai_id: Optional[int] = None
    toa_do: Optional[List[ToaDoBase]] = []


class VungTrongResponse(VungTrongBase):
    id: int
    chu_vung_id: Optional[int] = None
    trang_thai_id: Optional[int] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class VungTrongDetail(VungTrongResponse):
    """Chi tiết vùng trồng với relationships"""
    toa_do: List[ToaDoResponse] = []
    chu_vung: Optional[dict] = None
    trang_thai: Optional[dict] = None
    cay_trong: List[dict] = []


# ========== Loại Cây Schemas ==========

class LoaiCayBase(BaseModel):
    ma_cay: str
    ten_cay: str
    ten_khoa_hoc: Optional[str] = None
    mo_ta: Optional[str] = None


class LoaiCayCreate(LoaiCayBase):
    pass


class LoaiCayResponse(LoaiCayBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========== Chủ Vùng Schemas ==========

class ChuVungBase(BaseModel):
    ma_chu: Optional[str] = None
    ten_chu: str
    loai_chu: Optional[str] = "ca_nhan"
    cccd_mst: Optional[str] = None
    dia_chi: Optional[str] = None
    dien_thoai: Optional[str] = None
    email: Optional[str] = None


class ChuVungCreate(ChuVungBase):
    pass


class ChuVungResponse(ChuVungBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========== Lịch Sử Canh Tác Schemas ==========

class LichSuCanhTacBase(BaseModel):
    vung_trong_id: int
    loai_hoat_dong_id: Optional[int] = None
    ngay_thuc_hien: date
    mo_ta: Optional[str] = None
    phan_bon_id: Optional[int] = None
    thuoc_bvtv_id: Optional[int] = None
    luong_su_dung: Optional[float] = None
    don_vi: Optional[str] = None
    ket_qua: Optional[str] = None
    nguoi_thuc_hien: Optional[str] = None


class LichSuCanhTacCreate(LichSuCanhTacBase):
    pass


class LichSuCanhTacResponse(LichSuCanhTacBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ========== Thống Kê Schemas ==========

class ThongKeResponse(BaseModel):
    tong_vung_trong: int
    vung_con_han: int
    vung_sap_het_han: int
    vung_het_han: int
    tong_dien_tich: float
    tong_san_luong: float


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_farms: int
    active_farms: int
    total_area_ha: float
    total_production: float
    recent_activities: int
    chart_data: dict


# ========== Chart Schemas ==========

class ChartDataset(BaseModel):
    label: Optional[str] = None
    data: List[float]
    backgroundColor: Optional[str | List[str]] = None
    borderColor: Optional[str] = None
    tension: Optional[float] = None


class ChartData(BaseModel):
    labels: List[str]
    datasets: List[ChartDataset]


# ========== Search & Filter ==========

class SearchParams(BaseModel):
    query: Optional[str] = None
    trang_thai_id: Optional[int] = None
    chu_vung_id: Optional[int] = None
    skip: int = 0
    limit: int = 100


class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[dict]
