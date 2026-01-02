"""
========== ROUTES: DIARY API (Nhật ký Canh tác) ==========

Mục đích:
API endpoints cho quản lý lịch sử/nhật ký canh tác

Endpoints:
1. GET /api/diary/                  - List nhật ký với filter, pagination
2. GET /api/diary/{entry_id}        - Chi tiết một nhật ký
3. POST /api/diary/                 - Tạo nhật ký mới
4. PUT /api/diary/{entry_id}        - Cập nhật nhật ký
5. DELETE /api/diary/{entry_id}     - Xóa nhật ký
6. GET /api/diary/activity-types/   - Danh sách loại hoạt động

Models sử dụng:
- LichSuCanhTac: Lịch sử hoạt động canh tác
- LoaiHoatDong: Phân loại hoạt động

Schemas:
- LichSuCanhTacCreate: Request schema tạo/update
- LichSuCanhTacResponse: Response schema
- PaginatedResponse: Pagination wrapper

Database tables:
- nongsan.lich_su_canh_tac (15 columns)
- nongsan.loai_hoat_dong (6 columns)

Frontend components:
- Frontend/src/views/DiaryPage.vue
- Frontend/src/components/DiaryActivityForm.vue
- Frontend/src/components/DiaryActivityHistory.vue

Note:
- Schemas có fields cũ, cần update match models mới
"""

# ========== IMPORTS ==========
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from typing import List, Optional
from datetime import date
from database import get_db
from models.lich_su import LichSuCanhTac, LoaiHoatDong
from schemas import (
    LichSuCanhTacCreate, LichSuCanhTacResponse,
    PaginatedResponse
)

router = APIRouter(prefix="/diary", tags=["Diary"])


@router.get("/", response_model=PaginatedResponse)
async def get_diary_entries(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    vung_trong_id: Optional[int] = None,
    loai_hoat_dong_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """
    ========== Danh sách Nhật ký (List Diary) ==========
    
    Chức năng:
    - List lịch sử canh tác với filters
    - Pagination + eager load loại hoạt động
    - Sắp xếp mới nhất trước
    
    Filters:
    - vung_trong_id: Theo vùng
    - loai_hoat_dong_id: Theo loại hoạt động
    - from_date/to_date: Khoảng thời gian
    
    Note: Response dùng fields cũ (mo_ta, luong_su_dung, created_at)
    """
    
    # ========== BUILD QUERY + EAGER LOAD ==========
    query = db.query(LichSuCanhTac).options(
        joinedload(LichSuCanhTac.loai_hoat_dong)
    )
    
    # ========== APPLY FILTERS ==========
    if vung_trong_id:
        query = query.filter(LichSuCanhTac.vung_trong_id == vung_trong_id)
    
    if loai_hoat_dong_id:
        query = query.filter(LichSuCanhTac.loai_hoat_dong_id == loai_hoat_dong_id)
    
    if from_date:
        query = query.filter(LichSuCanhTac.ngay_thuc_hien >= from_date)
    
    if to_date:
        query = query.filter(LichSuCanhTac.ngay_thuc_hien <= to_date)
    
    # ========== COUNT + ORDER + PAGINATE ==========
    total = query.count()
    query = query.order_by(desc(LichSuCanhTac.ngay_thuc_hien))
    entries = query.offset(skip).limit(limit).all()
    
    # ========== FORMAT RESPONSE ==========
    # TODO: Fields cũ (mo_ta, luong_su_dung, don_vi, ket_qua, created_at, nhom)
    # Models mới dùng: tieu_de, noi_dung, lieu_luong_*, ngay_tao
    data = []
    for entry in entries:
        entry_dict = {
            "id": entry.id,
            "vung_trong_id": entry.vung_trong_id,
            "loai_hoat_dong_id": entry.loai_hoat_dong_id,
            "ngay_thuc_hien": entry.ngay_thuc_hien,
            "mo_ta": getattr(entry, 'noi_dung', None),
            "phan_bon_id": entry.phan_bon_id,
            "thuoc_bvtv_id": entry.thuoc_bvtv_id,
            "luong_su_dung": getattr(entry, 'lieu_luong_phan_bon', None) or getattr(entry, 'lieu_luong_thuoc', None),
            "don_vi": None,
            "ket_qua": None,
            "nguoi_thuc_hien": entry.nguoi_thuc_hien,
            "created_at": getattr(entry, 'ngay_tao', None),
            "loai_hoat_dong": {
                "id": entry.loai_hoat_dong.id,
                "ten_loai": entry.loai_hoat_dong.ten_loai,
                "nhom": None,
                "icon": entry.loai_hoat_dong.icon
            } if entry.loai_hoat_dong else None
        }
        data.append(entry_dict)
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": data
    }


@router.get("/{entry_id}", response_model=LichSuCanhTacResponse)
async def get_diary_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Lấy chi tiết một nhật ký
    """
    entry = db.query(LichSuCanhTac).filter(
        LichSuCanhTac.id == entry_id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy nhật ký ID {entry_id}")
    
    return entry


@router.post("/", response_model=LichSuCanhTacResponse, status_code=201)
async def create_diary_entry(
    entry_data: LichSuCanhTacCreate,
    db: Session = Depends(get_db)
):
    """
    Tạo nhật ký canh tác mới
    """
    new_entry = LichSuCanhTac(**entry_data.model_dump())
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return new_entry


@router.put("/{entry_id}", response_model=LichSuCanhTacResponse)
async def update_diary_entry(
    entry_id: int,
    entry_data: LichSuCanhTacCreate,
    db: Session = Depends(get_db)
):
    """
    Cập nhật nhật ký
    """
    entry = db.query(LichSuCanhTac).filter(
        LichSuCanhTac.id == entry_id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy nhật ký ID {entry_id}")
    
    # Update fields
    for key, value in entry_data.model_dump().items():
        setattr(entry, key, value)
    
    db.commit()
    db.refresh(entry)
    
    return entry


@router.delete("/{entry_id}")
async def delete_diary_entry(entry_id: int, db: Session = Depends(get_db)):
    """
    Xóa nhật ký
    """
    entry = db.query(LichSuCanhTac).filter(
        LichSuCanhTac.id == entry_id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy nhật ký ID {entry_id}")
    
    db.delete(entry)
    db.commit()
    
    return {"success": True, "message": f"Đã xóa nhật ký ID {entry_id}"}


@router.get("/activity-types/", response_model=List[dict])
async def get_activity_types(db: Session = Depends(get_db)):
    """
    Lấy danh sách loại hoạt động canh tác
    """
    types = db.query(LoaiHoatDong).all()
    
    return [
        {
            "id": t.id,
            "ma_loai": t.ma_loai,
            "ten_loai": t.ten_loai,
            "nhom": t.nhom,
            "icon": t.icon
        }
        for t in types
    ]
