"""
========== ROUTES: THUỐC BVTV API (Pesticides) ==========

Mục đích:
API endpoints cho quản lý danh mục thuốc bảo vệ thực vật

Endpoints:
1. GET /api/pesticides/groups/       - Danh sách nhóm thuốc
2. POST /api/pesticides/groups/      - Tạo nhóm thuốc mới
3. GET /api/pesticides/              - Danh sách thuốc (filter, pagination)
4. GET /api/pesticides/{id}          - Chi tiết thuốc
5. POST /api/pesticides/             - Tạo thuốc mới
6. PUT /api/pesticides/{id}          - Cập nhật thuốc
7. DELETE /api/pesticides/{id}       - Xóa thuốc

Models:
- NhomThuocBVTV: Nhóm thuốc (Trừ sâu, Trừ nấm, Diệt cỏ)
- ThuocBVTV: Chi tiết thuốc BVTV

Schemas:
- NhomThuocBVTVCreate/Response
- ThuocBVTVCreate/Response

Database tables:
- nongsan.nhom_thuoc_bvtv
- nongsan.thuoc_bvtv
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional
from database import get_db
from models.thuoc_bvtv import ThuocBVTV, NhomThuocBVTV
from schemas import (
    ThuocBVTVCreate, ThuocBVTVResponse,
    NhomThuocBVTVCreate, NhomThuocBVTVResponse,
    PaginatedResponse
)

router = APIRouter(prefix="/pesticides", tags=["Pesticides"])


@router.get("/groups/", response_model=list[NhomThuocBVTVResponse])
async def get_pesticide_groups(db: Session = Depends(get_db)):
    """
    ========== Danh sách Nhóm Thuốc BVTV ==========
    
    Endpoint: GET /api/pesticides/groups/
    
    Chức năng:
    - Lấy tất cả nhóm thuốc
    - Dùng cho dropdown/selector
    
    Response: List[NhomThuocBVTVResponse]
    - Danh sách nhóm (Trừ sâu, Trừ nấm, Diệt cỏ, etc.)
    """
    groups = db.query(NhomThuocBVTV).all()
    return groups


@router.post("/groups/", response_model=NhomThuocBVTVResponse, status_code=201)
async def create_pesticide_group(
    group_data: NhomThuocBVTVCreate,
    db: Session = Depends(get_db)
):
    """Tạo nhóm thuốc mới"""
    # Check unique
    existing = db.query(NhomThuocBVTV).filter(
        NhomThuocBVTV.ma_nhom == group_data.ma_nhom
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Mã nhóm {group_data.ma_nhom} đã tồn tại"
        )
    
    new_group = NhomThuocBVTV(**group_data.model_dump())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.get("/", response_model=PaginatedResponse)
async def get_pesticides(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    nhom_thuoc_id: Optional[int] = None,
    trang_thai_su_dung: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    ========== Danh sách Thuốc BVTV ==========
    
    Endpoint: GET /api/pesticides/
    
    Chức năng:
    - List thuốc với filter và pagination
    - Eager load nhóm thuốc
    
    Query Parameters:
    - skip, limit: Pagination
    - nhom_thuoc_id: Filter theo nhóm
    - trang_thai_su_dung: Filter theo trạng thái (Được phép, Hạn chế, Cấm)
    - search: Tìm kiếm theo tên/mã/hoạt chất
    """
    query = db.query(ThuocBVTV).options(
        joinedload(ThuocBVTV.nhom_thuoc)
    )
    
    # Filters
    if nhom_thuoc_id:
        query = query.filter(ThuocBVTV.nhom_thuoc_id == nhom_thuoc_id)
    
    if trang_thai_su_dung:
        query = query.filter(ThuocBVTV.trang_thai_su_dung == trang_thai_su_dung)
    
    if search:
        query = query.filter(
            (ThuocBVTV.ten_thuoc.ilike(f"%{search}%")) |
            (ThuocBVTV.ma_thuoc.ilike(f"%{search}%")) |
            (ThuocBVTV.ten_hoat_chat.ilike(f"%{search}%"))
        )
    
    total = query.count()
    pesticides = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [ThuocBVTVResponse.model_validate(p).model_dump() for p in pesticides]
    }


@router.get("/{pesticide_id}", response_model=ThuocBVTVResponse)
async def get_pesticide(pesticide_id: int, db: Session = Depends(get_db)):
    """Chi tiết thuốc BVTV"""
    pesticide = db.query(ThuocBVTV).options(
        joinedload(ThuocBVTV.nhom_thuoc)
    ).filter(ThuocBVTV.id == pesticide_id).first()
    
    if not pesticide:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy thuốc BVTV ID {pesticide_id}"
        )
    
    return pesticide


@router.post("/", response_model=ThuocBVTVResponse, status_code=201)
async def create_pesticide(
    pesticide_data: ThuocBVTVCreate,
    db: Session = Depends(get_db)
):
    """Tạo thuốc BVTV mới"""
    # Check unique
    existing = db.query(ThuocBVTV).filter(
        ThuocBVTV.ma_thuoc == pesticide_data.ma_thuoc
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Mã thuốc {pesticide_data.ma_thuoc} đã tồn tại"
        )
    
    new_pesticide = ThuocBVTV(**pesticide_data.model_dump())
    db.add(new_pesticide)
    db.commit()
    db.refresh(new_pesticide)
    return new_pesticide


@router.put("/{pesticide_id}", response_model=ThuocBVTVResponse)
async def update_pesticide(
    pesticide_id: int,
    pesticide_data: ThuocBVTVCreate,
    db: Session = Depends(get_db)
):
    """Cập nhật thuốc BVTV"""
    pesticide = db.query(ThuocBVTV).filter(ThuocBVTV.id == pesticide_id).first()
    if not pesticide:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy thuốc BVTV ID {pesticide_id}"
        )
    
    for key, value in pesticide_data.model_dump().items():
        setattr(pesticide, key, value)
    
    db.commit()
    db.refresh(pesticide)
    return pesticide


@router.delete("/{pesticide_id}")
async def delete_pesticide(pesticide_id: int, db: Session = Depends(get_db)):
    """Xóa thuốc BVTV"""
    pesticide = db.query(ThuocBVTV).filter(ThuocBVTV.id == pesticide_id).first()
    if not pesticide:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy thuốc BVTV ID {pesticide_id}"
        )
    
    db.delete(pesticide)
    db.commit()
    return {"success": True, "message": f"Đã xóa thuốc BVTV {pesticide.ma_thuoc}"}
