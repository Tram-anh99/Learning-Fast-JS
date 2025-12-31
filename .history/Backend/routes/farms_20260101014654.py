"""
========== API Routes: Vùng Trồng ==========
Endpoints cho quản lý vùng trồng (Farm Zones)
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from typing import List, Optional
from database import get_db
from models.vung_trong import VungTrong, ToaDoVung
from models.to_chuc_ca_nhan import ToChucCaNhan
from models.trang_thai_vung import TrangThaiVung
from schemas import (
    VungTrongCreate, VungTrongResponse, VungTrongDetail,
    PaginatedResponse, SearchParams
)

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.get("/", response_model=PaginatedResponse)
async def get_all_farms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = None,
    trang_thai_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Lấy danh sách vùng trồng với phân trang và filter
    """
    query = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        joinedload(VungTrong.trang_thai)
    )
    
    # Search filter
    if search:
        query = query.filter(
            or_(
                VungTrong.ma_vung.ilike(f"%{search}%"),
                VungTrong.ten_vung.ilike(f"%{search}%")
            )
        )
    
    # Status filter
    if trang_thai_id:
        query = query.filter(VungTrong.trang_thai_id == trang_thai_id)
    
    # Count total
    total = query.count()
    
    # Paginate
    farms = query.offset(skip).limit(limit).all()
    
    # Format response
    data = []
    for farm in farms:
        farm_dict = {
            "id": farm.id,
            "ma_vung": farm.ma_vung,
            "ten_vung": farm.ten_vung,
            "dia_chi": farm.dia_chi,
            "dien_tich": farm.dien_tich,
            "ngay_tao": farm.ngay_tao.isoformat() if farm.ngay_tao else None,
            "chu_so_huu": {
                "id": farm.chu_so_huu.id,
                "ten_to_chuc": farm.chu_so_huu.ten_to_chuc
            } if farm.chu_so_huu else None,
            "trang_thai": {
                "id": farm.trang_thai.id,
                "ten_trang_thai": farm.trang_thai.ten_trang_thai,
                "mau_sac": farm.trang_thai.mau_sac
            } if farm.trang_thai else None
        }
        data.append(farm_dict)
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": data
    }


@router.get("/{farm_id}", response_model=VungTrongDetail)
async def get_farm_by_id(farm_id: int, db: Session = Depends(get_db)):
    """
    Lấy chi tiết vùng trồng theo ID
    """
    farm = db.query(VungTrong).options(
        joinedload(VungTrong.chu_vung),
        joinedload(VungTrong.trang_thai),
        joinedload(VungTrong.toa_do),
        joinedload(VungTrong.cay_trong)
    ).filter(VungTrong.id == farm_id).first()
    
    if not farm:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy vùng trồng ID {farm_id}")
    
    # Format response
    farm_dict = {
        "id": farm.id,
        "ma_vung": farm.ma_vung,
        "ten_vung": farm.ten_vung,
        "dia_chi": farm.dia_chi,
        "dien_tich": farm.dien_tich,
        "ngay_cap_ma": farm.ngay_cap_ma,
        "ngay_het_han": farm.ngay_het_han,
        "chu_vung_id": farm.chu_vung_id,
        "trang_thai_id": farm.trang_thai_id,
        "created_at": farm.created_at,
        "chu_vung": {
            "id": farm.chu_vung.id,
            "ten_chu": farm.chu_vung.ten_chu,
            "dien_thoai": farm.chu_vung.dien_thoai
        } if farm.chu_vung else None,
        "trang_thai": {
            "id": farm.trang_thai.id,
            "ten_trang_thai": farm.trang_thai.ten_trang_thai,
            "mau_sac": farm.trang_thai.mau_sac
        } if farm.trang_thai else None,
        "toa_do": [
            {
                "id": td.id,
                "latitude": td.latitude,
                "longitude": td.longitude,
                "thu_tu": td.thu_tu
            }
            for td in sorted(farm.toa_do, key=lambda x: x.thu_tu)
        ],
        "cay_trong": []  # TODO: Add crop details
    }
    
    return farm_dict


@router.post("/", response_model=VungTrongResponse, status_code=201)
async def create_farm(farm_data: VungTrongCreate, db: Session = Depends(get_db)):
    """
    Tạo vùng trồng mới
    """
    # Check ma_vung uniqueness
    existing = db.query(VungTrong).filter(VungTrong.ma_vung == farm_data.ma_vung).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Mã vùng {farm_data.ma_vung} đã tồn tại")
    
    # Create farm
    new_farm = VungTrong(
        ma_vung=farm_data.ma_vung,
        ten_vung=farm_data.ten_vung,
        dia_chi=farm_data.dia_chi,
        dien_tich=farm_data.dien_tich,
        ngay_cap_ma=farm_data.ngay_cap_ma,
        ngay_het_han=farm_data.ngay_het_han,
        chu_vung_id=farm_data.chu_vung_id,
        trang_thai_id=farm_data.trang_thai_id
    )
    
    db.add(new_farm)
    db.flush()  # Get ID before commit
    
    # Add coordinates
    if farm_data.toa_do:
        for toa_do in farm_data.toa_do:
            coord = ToaDoVung(
                vung_trong_id=new_farm.id,
                latitude=toa_do.latitude,
                longitude=toa_do.longitude,
                thu_tu=toa_do.thu_tu
            )
            db.add(coord)
    
    db.commit()
    db.refresh(new_farm)
    
    return new_farm


@router.put("/{farm_id}", response_model=VungTrongResponse)
async def update_farm(farm_id: int, farm_data: VungTrongCreate, db: Session = Depends(get_db)):
    """
    Cập nhật thông tin vùng trồng
    """
    farm = db.query(VungTrong).filter(VungTrong.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy vùng trồng ID {farm_id}")
    
    # Update fields
    farm.ten_vung = farm_data.ten_vung
    farm.dia_chi = farm_data.dia_chi
    farm.dien_tich = farm_data.dien_tich
    farm.ngay_cap_ma = farm_data.ngay_cap_ma
    farm.ngay_het_han = farm_data.ngay_het_han
    farm.chu_vung_id = farm_data.chu_vung_id
    farm.trang_thai_id = farm_data.trang_thai_id
    
    db.commit()
    db.refresh(farm)
    
    return farm


@router.delete("/{farm_id}")
async def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    """
    Xóa vùng trồng
    """
    farm = db.query(VungTrong).filter(VungTrong.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy vùng trồng ID {farm_id}")
    
    db.delete(farm)
    db.commit()
    
    return {"success": True, "message": f"Đã xóa vùng trồng {farm.ma_vung}"}


@router.get("/by-code/{ma_vung}")
async def get_farm_by_code(ma_vung: str, db: Session = Depends(get_db)):
    """
    Lấy thông tin vùng trồng theo mã MSVT
    """
    farm = db.query(VungTrong).options(
        joinedload(VungTrong.chu_vung),
        joinedload(VungTrong.trang_thai),
        joinedload(VungTrong.toa_do)
    ).filter(VungTrong.ma_vung == ma_vung).first()
    
    if not farm:
        raise HTTPException(status_code=404, detail=f"Không tìm thấy mã vùng {ma_vung}")
    
    return {
        "id": farm.id,
        "ma_vung": farm.ma_vung,
        "ten_vung": farm.ten_vung,
        "chu_vung": farm.chu_vung.ten_chu if farm.chu_vung else None,
        "trang_thai": farm.trang_thai.ten_trang_thai if farm.trang_thai else None
    }
