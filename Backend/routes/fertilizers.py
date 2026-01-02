"""
========== ROUTES: PHÂN BÓN API (Fertilizers) ==========

Mục đích:
API endpoints cho quản lý danh mục phân bón

Endpoints:
1. GET /api/fertilizers/categories/     - Danh sách loại phân bón
2. POST /api/fertilizers/categories/    - Tạo loại phân bón mới
3. GET /api/fertilizers/                - Danh sách phân bón (có filter, pagination)
4. GET /api/fertilizers/{id}            - Chi tiết phân bón
5. POST /api/fertilizers/               - Tạo phân bón mới
6. PUT /api/fertilizers/{id}            - Cập nhật phân bón
7. DELETE /api/fertilizers/{id}         - Xóa phân bón

Models:
- LoaiPhanBon: Loại phân bón (Đạm, Lân, Kali, Hữu cơ)
- PhanBon: Chi tiết phân bón

Schemas:
- LoaiPhanBonCreate/Response
- PhanBonCreate/Response

Database tables:
- nongsan.loai_phan_bon
- nongsan.phan_bon

Frontend components:
- Admin panel: Quản lý danh mục
- DiaryActivityForm: Dropdown chọn phân bón
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from database import get_db
from models.phan_bon import PhanBon, LoaiPhanBon
from schemas import (
    PhanBonCreate, PhanBonResponse,
    LoaiPhanBonCreate, LoaiPhanBonResponse,
    PaginatedResponse
)

router = APIRouter(prefix="/fertilizers", tags=["Fertilizers"])


@router.get("/categories/", response_model=list[LoaiPhanBonResponse])
async def get_fertilizer_categories(db: Session = Depends(get_db)):
    """
    ========== Danh sách Loại Phân Bón ==========
    
    Endpoint: GET /api/fertilizers/categories/
    
    Chức năng:
    - Lấy tất cả loại phân bón
    - Dùng cho dropdown/selector
    
    Response: List[LoaiPhanBonResponse]
    - Danh sách loại phân bón (Đạm, Lân, Kali, etc.)
    """
    categories = db.query(LoaiPhanBon).all()
    return categories


@router.post("/categories/", response_model=LoaiPhanBonResponse, status_code=201)
async def create_fertilizer_category(
    category_data: LoaiPhanBonCreate,
    db: Session = Depends(get_db)
):
    """
    ========== Tạo Loại Phân Bón ==========
    
    Endpoint: POST /api/fertilizers/categories/
    
    Chức năng:
    - Tạo loại phân bón mới
    - Admin only
    
    Request Body: LoaiPhanBonCreate
    - ma_loai: Mã loại (unique)
    - ten_loai: Tên loại
    - mo_ta: Mô tả (optional)
    """
    # Check unique
    existing = db.query(LoaiPhanBon).filter(
        LoaiPhanBon.ma_loai == category_data.ma_loai
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Mã loại {category_data.ma_loai} đã tồn tại"
        )
    
    new_category = LoaiPhanBon(**category_data.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/", response_model=PaginatedResponse)
async def get_fertilizers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    loai_phan_bon_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    ========== Danh sách Phân Bón ==========
    
    Endpoint: GET /api/fertilizers/
    
    Chức năng:
    - List phân bón với filter và pagination
    - Eager load loại phân bón
    
    Query Parameters:
    - skip, limit: Pagination
    - loai_phan_bon_id: Filter theo loại
    - search: Tìm kiếm theo tên/mã
    """
    query = db.query(PhanBon).options(
        joinedload(PhanBon.loai_phan_bon)
    )
    
    # Filters
    if loai_phan_bon_id:
        query = query.filter(PhanBon.loai_phan_bon_id == loai_phan_bon_id)
    
    if search:
        query = query.filter(
            (PhanBon.ten_phan_bon.ilike(f"%{search}%")) |
            (PhanBon.ma_phan_bon.ilike(f"%{search}%"))
        )
    
    total = query.count()
    fertilizers = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [PhanBonResponse.model_validate(f).model_dump() for f in fertilizers]
    }


@router.get("/{fertilizer_id}", response_model=PhanBonResponse)
async def get_fertilizer(fertilizer_id: int, db: Session = Depends(get_db)):
    """Chi tiết phân bón"""
    fertilizer = db.query(PhanBon).options(
        joinedload(PhanBon.loai_phan_bon)
    ).filter(PhanBon.id == fertilizer_id).first()
    
    if not fertilizer:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy phân bón ID {fertilizer_id}"
        )
    
    return fertilizer


@router.post("/", response_model=PhanBonResponse, status_code=201)
async def create_fertilizer(
    fertilizer_data: PhanBonCreate,
    db: Session = Depends(get_db)
):
    """Tạo phân bón mới"""
    # Check unique
    existing = db.query(PhanBon).filter(
        PhanBon.ma_phan_bon == fertilizer_data.ma_phan_bon
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Mã phân bón {fertilizer_data.ma_phan_bon} đã tồn tại"
        )
    
    new_fertilizer = PhanBon(**fertilizer_data.model_dump())
    db.add(new_fertilizer)
    db.commit()
    db.refresh(new_fertilizer)
    return new_fertilizer


@router.put("/{fertilizer_id}", response_model=PhanBonResponse)
async def update_fertilizer(
    fertilizer_id: int,
    fertilizer_data: PhanBonCreate,
    db: Session = Depends(get_db)
):
    """Cập nhật phân bón"""
    fertilizer = db.query(PhanBon).filter(PhanBon.id == fertilizer_id).first()
    if not fertilizer:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy phân bón ID {fertilizer_id}"
        )
    
    for key, value in fertilizer_data.model_dump().items():
        setattr(fertilizer, key, value)
    
    db.commit()
    db.refresh(fertilizer)
    return fertilizer


@router.delete("/{fertilizer_id}")
async def delete_fertilizer(fertilizer_id: int, db: Session = Depends(get_db)):
    """Xóa phân bón"""
    fertilizer = db.query(PhanBon).filter(PhanBon.id == fertilizer_id).first()
    if not fertilizer:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy phân bón ID {fertilizer_id}"
        )
    
    db.delete(fertilizer)
    db.commit()
    return {"success": True, "message": f"Đã xóa phân bón {fertilizer.ma_phan_bon}"}
