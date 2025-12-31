"""
========== API Routes: Diary (Lịch sử canh tác) ==========
Endpoints cho nhật ký canh tác
"""

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
    Lấy danh sách nhật ký canh tác với filter
    """
    query = db.query(LichSuCanhTac).options(
        joinedload(LichSuCanhTac.loai_hoat_dong)
    )
    
    # Filters
    if vung_trong_id:
        query = query.filter(LichSuCanhTac.vung_trong_id == vung_trong_id)
    
    if loai_hoat_dong_id:
        query = query.filter(LichSuCanhTac.loai_hoat_dong_id == loai_hoat_dong_id)
    
    if from_date:
        query = query.filter(LichSuCanhTac.ngay_thuc_hien >= from_date)
    
    if to_date:
        query = query.filter(LichSuCanhTac.ngay_thuc_hien <= to_date)
    
    # Count total
    total = query.count()
    
    # Order by date desc
    query = query.order_by(desc(LichSuCanhTac.ngay_thuc_hien))
    
    # Paginate
    entries = query.offset(skip).limit(limit).all()
    
    # Format response
    data = []
    for entry in entries:
        entry_dict = {
            "id": entry.id,
            "vung_trong_id": entry.vung_trong_id,
            "loai_hoat_dong_id": entry.loai_hoat_dong_id,
            "ngay_thuc_hien": entry.ngay_thuc_hien,
            "mo_ta": entry.mo_ta,
            "phan_bon_id": entry.phan_bon_id,
            "thuoc_bvtv_id": entry.thuoc_bvtv_id,
            "luong_su_dung": entry.luong_su_dung,
            "don_vi": entry.don_vi,
            "ket_qua": entry.ket_qua,
            "nguoi_thuc_hien": entry.nguoi_thuc_hien,
            "created_at": entry.created_at,
            "loai_hoat_dong": {
                "id": entry.loai_hoat_dong.id,
                "ten_loai": entry.loai_hoat_dong.ten_loai,
                "nhom": entry.loai_hoat_dong.nhom,
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
