"""
========== API Routes: Vùng Trồng (Farm Zones Management) ==========
File: routes/farms.py
Purpose: RESTful API endpoints cho CRUD operations vùng trồng

Endpoints:
- GET    /api/farms/              : List all farms (phân trang, search, filter)
- GET    /api/farms/{id}          : Get farm details by ID (bao gồm tọa độ, cây trồng)
- POST   /api/farms/              : Create new farm
- PUT    /api/farms/{id}          : Update farm
- DELETE /api/farms/{id}          : Delete farm
- GET    /api/farms/by-code/{code}: Get farm by MSVT code

Models sử dụng:
- VungTrong, ToaDoVung (models/vung_trong.py)
- ToChucCaNhan (models/to_chuc_ca_nhan.py)
- TrangThaiVung (models/trang_thai_vung.py)

Frontend components:
- HomeView.vue: Hiển thị danh sách farms
- MapComponent.vue: Vẽ polygons từ tọa độ
- HomeDetailView.vue: Chi tiết farm

Kết nối:
- Database: nongsan.vung_trong, nongsan.toa_do_vung
- Schemas: schemas.py (VungTrongCreate, VungTrongResponse, VungTrongDetail)
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
    # skip: Số records bỏ qua (pagination offset)
    # ge=0: Greater or equal 0, không cho số âm
    # Example: skip=0 (trang 1), skip=10 (trang 2 với limit=10)
    
    limit: int = Query(100, le=1000),
    # limit: Số records tối đa trả về
    # le=1000: Less or equal 1000, giới hạn tối đa để tránh quá tải
    # Default: 100 records/page
    
    search: Optional[str] = None,
    # search: Từ khóa tìm kiếm (tìm trong ma_vung và ten_vung)
    # Optional: Có thể bỏ qua
    # Example: search="Lúa" → tìm vùng có chữ "Lúa" trong tên
    
    trang_thai_id: Optional[int] = None,
    # trang_thai_id: Filter theo trạng thái (1=Hoạt động, 2=Tạm ngưng, ...)
    # Optional: Nếu không truyền thì lấy tất cả trạng thái
    
    db: Session = Depends(get_db)
    # db: Database session từ dependency injection
    # Depends(get_db): FastAPI tự động inject session, auto close sau request
):
    """
    ========== Lấy danh sách vùng trồng (Get All Farms) ==========
    
    Endpoint: GET /api/farms/
    
    Chức năng:
    - Lấy danh sách tất cả vùng trồng với phân trang
    - Hỗ trợ tìm kiếm theo mã vùng hoặc tên vùng
    - Filter theo trạng thái
    - Eager loading chu_so_huu và trang_thai để tránh N+1 queries
    
    Query Parameters:
    - skip: Offset cho pagination (default: 0)
    - limit: Số records/page (default: 100, max: 1000)
    - search: Từ khóa tìm kiếm (optional)
    - trang_thai_id: Filter theo trạng thái (optional)
    
    Response Format:
    {
        "total": 50,           # Tổng số vùng trồng (sau filter)
        "skip": 0,             # Offset hiện tại
        "limit": 100,          # Limit hiện tại
        "data": [...]          # Array các farm objects
    }
    
    Usage Example:
    - GET /api/farms/?skip=0&limit=20
    - GET /api/farms/?search=Lúa
    - GET /api/farms/?trang_thai_id=1&limit=50
    
    Performance:
    - Sử dụng joinedload() để eager load relationships (1 query thay vì N+1)
    - Index trên ma_vung, ten_vung để tối ưu search
    """
    
    # ========== BUILD QUERY ==========
    query = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        # Eager load chủ sở hữu (LEFT OUTER JOIN)
        # Tránh N+1 problem: Thay vì query riêng cho mỗi farm.chu_so_huu
        # → 1 query duy nhất với JOIN
        
        joinedload(VungTrong.trang_thai)
        # Eager load trạng thái vùng
        # Lấy thông tin màu sắc, tên trạng thái trong cùng query
    )
    
    # ========== APPLY FILTERS ==========
    
    # Filter 1: Search by ma_vung hoặc ten_vung
    if search:
        query = query.filter(
            or_(
                # ilike: Case-insensitive LIKE (không phân biệt hoa thường)
                # %search%: Tìm kiếm substring (chứa search ở bất kỳ đâu)
                VungTrong.ma_vung.ilike(f"%{search}%"),
                VungTrong.ten_vung.ilike(f"%{search}%")
            )
            # or_(): Thỏa mãn 1 trong 2 điều kiện
            # Example: search="Lúa" → ma_vung LIKE '%Lúa%' OR ten_vung LIKE '%Lúa%'
        )
    
    # Filter 2: Filter theo trạng thái
    if trang_thai_id:
        query = query.filter(VungTrong.trang_thai_id == trang_thai_id)
        # Exact match với trang_thai_id
        # Example: trang_thai_id=1 → chỉ lấy vùng đang hoạt động
    
    # ========== COUNT & PAGINATE ==========
    
    # Đếm tổng số records (sau khi filter)
    total = query.count()
    # SQL: SELECT COUNT(*) FROM vung_trong WHERE ...
    # Cần để frontend tính số trang
    
    # Phân trang và execute query
    farms = query.offset(skip).limit(limit).all()
    # offset(skip): Bỏ qua {skip} records đầu tiên
    # limit(limit): Lấy tối đa {limit} records
    # .all(): Execute query, trả về list objects
    # SQL: SELECT * FROM vung_trong ... LIMIT {limit} OFFSET {skip}
    
    # ========== FORMAT RESPONSE ==========
    # Biến đổi ORM objects thành dict để trả về JSON
    # (FastAPI auto serialize dict → JSON)
    
    data = []
    for farm in farms:
        farm_dict = {
            "id": farm.id,
            # ID primary key (integer)
            
            "ma_vung": farm.ma_vung,
            # Mã vùng trồng VietGAP (string, unique)
            # Example: "MSVT001", "MSVT002"
            
            "ten_vung": farm.ten_vung,
            # Tên vùng trồng
            # Example: "Vùng Lúa An Lộc 1"
            
            "dia_chi": farm.dia_chi,
            # Địa chỉ cụ thể vùng trồng
            
            "dien_tich": farm.dien_tich,
            # Diện tích (hecta) - kiểu Numeric trong DB
            # Python tự convert sang float/Decimal
            
            "ngay_tao": farm.ngay_tao.isoformat() if farm.ngay_tao else None,
            # Ngày tạo record
            # .isoformat(): Convert datetime → string ISO 8601 format
            # Example: "2026-01-01T10:30:00"
            # if ... else None: Xử lý trường hợp NULL
            
            "chu_so_huu": {
                # Thông tin chủ sở hữu (tổ chức/cá nhân)
                # Nested object để frontend dễ sử dụng
                "id": farm.chu_so_huu.id,
                "ten_to_chuc": farm.chu_so_huu.ten_to_chuc
                # Tên tổ chức hoặc tên cá nhân
            } if farm.chu_so_huu else None,
            # Nếu không có chủ sở hữu → trả về None
            
            "trang_thai": {
                # Thông tin trạng thái vùng
                "id": farm.trang_thai.id,
                "ten_trang_thai": farm.trang_thai.ten_trang_thai,
                # Example: "Đang hoạt động", "Tạm ngưng"
                
                "mau_sac": farm.trang_thai.mau_sac
                # Màu sắc HEX để hiển thị badge
                # Example: "#4CAF50" (xanh lá), "#FF9800" (cam)
            } if farm.trang_thai else None
        }
        data.append(farm_dict)
    
    # ========== RETURN PAGINATED RESPONSE ==========
    return {
        "total": total,
        # Tổng số vùng trồng (sau filter)
        # Frontend dùng để tính: số trang = ceil(total / limit)
        
        "skip": skip,
        # Offset hiện tại - frontend biết đang ở trang nào
        
        "limit": limit,
        # Số items/page - frontend dùng cho pagination UI
        
        "data": data
        # Array các farm objects
    }


@router.get("/{farm_id}", response_model=VungTrongDetail)
async def get_farm_by_id(
    farm_id: int,
    # farm_id: ID vùng trồng (path parameter)
    # FastAPI tự động parse từ URL: /api/farms/123 → farm_id=123
    
    db: Session = Depends(get_db)
):
    """
    ========== Lấy chi tiết vùng trồng (Get Farm Detail by ID) ==========
    
    Endpoint: GET /api/farms/{farm_id}
    
    Chức năng:
    - Lấy thông tin chi tiết 1 vùng trồng
    - Bao gồm: thông tin cơ bản, chủ sở hữu, trạng thái, tọa độ polygon, cây trồng
    - Eager load tất cả relationships để tránh N+1 queries
    
    Path Parameters:
    - farm_id: ID của vùng trồng (integer)
    
    Response:
    - 200: Farm detail object với đầy đủ thông tin
    - 404: Không tìm thấy vùng trồng
    
    Usage:
    - Frontend: HomeDetailView.vue (hiển thị chi tiết farm)
    - Frontend: MapComponent.vue (vẽ polygon từ tọa độ)
    """
    
    # ========== QUERY WITH EAGER LOADING ==========
    farm = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        # Load chủ sở hữu (to_chuc_ca_nhan)
        
        joinedload(VungTrong.trang_thai),
        # Load trạng thái vùng
        
        joinedload(VungTrong.toa_do),
        # Load tất cả tọa độ (ToaDoVung) - nhiều records
        # Ví dụ: 1 polygon có 10 điểm → 10 ToaDoVung records
        
        joinedload(VungTrong.cay_trong)
        # Load thông tin cây trồng (VungCayTrong junction table)
    ).filter(VungTrong.id == farm_id).first()
    # .first(): Lấy record đầu tiên (hoặc None nếu không tìm thấy)
    # Vì ID là primary key nên chỉ có 0 hoặc 1 kết quả
    
    # ========== HANDLE NOT FOUND ==========
    if not farm:
        # Nếu không tìm thấy → HTTP 404 Not Found
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy vùng trồng ID {farm_id}"
            # detail: Message trả về cho frontend
        )
    
    # ========== FORMAT DETAIL RESPONSE ==========
    # Tạo dict chi tiết với đầy đủ thông tin
    farm_dict = {
        "id": farm.id,
        "ma_vung": farm.ma_vung,
        "ten_vung": farm.ten_vung,
        "dia_chi": farm.dia_chi,
        "dien_tich": farm.dien_tich,
        # Diện tích (Numeric)
        
        "chu_so_huu_id": farm.chu_so_huu_id,
        "trang_thai_id": farm.trang_thai_id,
        # Foreign key IDs
        
        "ngay_tao": farm.ngay_tao.isoformat() if farm.ngay_tao else None,
        "ngay_cap_nhat": farm.ngay_cap_nhat.isoformat() if farm.ngay_cap_nhat else None,
        # Timestamps
        
        "chu_so_huu": {
            # Thông tin chủ sở hữu đầy đủ
            "id": farm.chu_so_huu.id,
            "ten_to_chuc": farm.chu_so_huu.ten_to_chuc,
            "dien_thoai": farm.chu_so_huu.dien_thoai if hasattr(farm.chu_so_huu, 'dien_thoai') else None,
            "email": farm.chu_so_huu.email if hasattr(farm.chu_so_huu, 'email') else None
        } if farm.chu_so_huu else None,
        
        "trang_thai": {
            # Thông tin trạng thái
            "id": farm.trang_thai.id,
            "ten_trang_thai": farm.trang_thai.ten_trang_thai,
            "mau_sac": farm.trang_thai.mau_sac
        } if farm.trang_thai else None,
        
        "toa_do": [
            # List tọa độ polygon, sắp xếp theo thứ tự
            # Frontend dùng để vẽ polygon trên map
            {
                "id": td.id,
                "vi_do": float(td.vi_do) if td.vi_do else None,
                # Vĩ độ (latitude) - convert Numeric → float
                
                "kinh_do": float(td.kinh_do) if td.kinh_do else None,
                # Kinh độ (longitude)
                
                "thu_tu": td.thu_tu
                # Thứ tự điểm trong polygon (1, 2, 3, ...)
            }
            for td in sorted(farm.toa_do, key=lambda x: x.thu_tu)
            # sorted(): Sắp xếp theo thu_tu để vẽ polygon đúng
        ],
        
        "cay_trong": [
            # List cây trồng trong vùng (từ VungCayTrong)
            # TODO: Expand with crop details nếu cần
            {"id": ct.id, "loai_cay_id": ct.loai_cay_id}
            for ct in farm.cay_trong
        ] if farm.cay_trong else []
    }
    
    return farm_dict


@router.post("/", response_model=VungTrongResponse, status_code=201)
async def create_farm(
    farm_data: VungTrongCreate,
    # farm_data: Request body (Pydantic model)
    # FastAPI tự động validate theo schema VungTrongCreate
    # Nếu không hợp lệ → HTTP 422 Unprocessable Entity
    
    db: Session = Depends(get_db)
):
    """
    ========== Tạo vùng trồng mới (Create New Farm) ==========
    
    Endpoint: POST /api/farms/
    
    Chức năng:
    - Tạo vùng trồng mới trong database
    - Kiểm tra ma_vung unique constraint
    - Tự động thêm tọa độ polygon nếu có
    
    Request Body: VungTrongCreate schema
    - ma_vung: Mã vùng (unique, bắt buộc)
    - ten_vung: Tên vùng (bắt buộc)
    - dien_tich: Diện tích hecta
    - chu_so_huu_id: FK tới to_chuc_ca_nhan
    - trang_thai_id: FK tới trang_thai_vung
    - toa_do: List các điểm tọa độ (optional)
    
    Response:
    - 201 Created: Vùng trồng mới vừa tạo
    - 400 Bad Request: ma_vung bị trùng
    - 422: Dữ liệu không hợp lệ
    
    Note:
    - Schema hiện tại có fields cũ (ngay_cap_ma, ngay_het_han, chu_vung_id)
    - Cần update schema để match models mới
    """
    
    # ========== VALIDATE UNIQUE CONSTRAINT ==========
    # Kiểm tra ma_vung đã tồn tại chưa
    existing = db.query(VungTrong).filter(VungTrong.ma_vung == farm_data.ma_vung).first()
    if existing:
        # Nếu đã tồn tại → HTTP 400 Bad Request
        raise HTTPException(
            status_code=400,
            detail=f"Mã vùng {farm_data.ma_vung} đã tồn tại"
        )
    
    # ========== CREATE FARM OBJECT ==========
    # NOTE: Schema cũ có fields không match models mới
    # TODO: Update schema VungTrongCreate để bỏ ngay_cap_ma, ngay_het_han, chu_vung_id
    new_farm = VungTrong(
        ma_vung=farm_data.ma_vung,
        ten_vung=farm_data.ten_vung,
        dia_chi=farm_data.dia_chi,
        dien_tich=farm_data.dien_tich,
        # ngay_cap_ma=farm_data.ngay_cap_ma,  # TODO: Fields cũ, bỏ
        # ngay_het_han=farm_data.ngay_het_han,  # TODO: Fields cũ, bỏ
        chu_so_huu_id=getattr(farm_data, 'chu_so_huu_id', None),
        # getattr: Lấy giá trị nếu có, None nếu không
        trang_thai_id=getattr(farm_data, 'trang_thai_id', None)
    )
    
    # ========== ADD TO DB SESSION ==========
    db.add(new_farm)
    # Thêm object vào session (chưa lưu DB)
    
    db.flush()
    # Flush để lấy ID ngay (không chờ commit)
    # Sau flush: new_farm.id đã có giá trị
    # Cần ID để tạo ToaDoVung với FK vung_trong_id
    
    # ========== ADD COORDINATES ==========
    # Nếu request có gửi tọa độ polygon
    if hasattr(farm_data, 'toa_do') and farm_data.toa_do:
        for toa_do in farm_data.toa_do:
            # Tạo mỗi điểm tọa độ
            coord = ToaDoVung(
                vung_trong_id=new_farm.id,
                # FK tới vùng trồng vừa tạo
                
                vi_do=getattr(toa_do, 'vi_do', getattr(toa_do, 'latitude', None)),
                # Thử vi_do trước, nếu không có thì thử latitude (backward compatible)
                
                kinh_do=getattr(toa_do, 'kinh_do', getattr(toa_do, 'longitude', None)),
                # Tương tự cho kinh_do/longitude
                
                thu_tu=toa_do.thu_tu
                # Thứ tự điểm trong polygon
            )
            db.add(coord)
    
    # ========== COMMIT TRANSACTION ==========
    db.commit()
    # Lưu tất cả thay đổi vào database
    # Thực hiện transaction: INSERT vùng trồng + INSERT tọa độ
    
    db.refresh(new_farm)
    # Refresh để lấy lại data từ DB (bao gồm auto-generated fields)
    # Ví dụ: ngay_tao (server_default=func.now())
    
    return new_farm
    # FastAPI tự serialize object → JSON theo VungTrongResponse schema


@router.put("/{farm_id}", response_model=VungTrongResponse)
async def update_farm(
    farm_id: int,
    farm_data: VungTrongCreate,
    db: Session = Depends(get_db)
):
    """
    ========== Cập nhật thông tin vùng trồng (Update Farm) ==========
    
    Endpoint: PUT /api/farms/{farm_id}
    
    Chức năng:
    - Cập nhật thông tin vùng trồng hiện có
    - Không update ma_vung (unique identifier)
    - Tự động update ngay_cap_nhat timestamp
    
    Note: Schema cũ - cần update để match models mới
    """
    
    # ========== FIND FARM ==========
    farm = db.query(VungTrong).filter(VungTrong.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy vùng trồng ID {farm_id}"
        )
    
    # ========== UPDATE FIELDS ==========
    # Update các fields từ request data
    farm.ten_vung = farm_data.ten_vung
    farm.dia_chi = farm_data.dia_chi
    farm.dien_tich = farm_data.dien_tich
    
    # TODO: Remove old fields after schema update
    # farm.ngay_cap_ma = farm_data.ngay_cap_ma
    # farm.ngay_het_han = farm_data.ngay_het_han
    # farm.chu_vung_id = farm_data.chu_vung_id
    
    if hasattr(farm_data, 'chu_so_huu_id'):
        farm.chu_so_huu_id = farm_data.chu_so_huu_id
    if hasattr(farm_data, 'trang_thai_id'):
        farm.trang_thai_id = farm_data.trang_thai_id
    
    # ========== SAVE CHANGES ==========
    db.commit()
    # ngay_cap_nhat tự động update (onupdate=func.now())
    
    db.refresh(farm)
    # Lấy lại data mới nhất từ DB
    
    return farm


@router.delete("/{farm_id}")
async def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db)
):
    """
    ========== Xóa vùng trồng (Delete Farm) ==========
    
    Endpoint: DELETE /api/farms/{farm_id}
    
    Chức năng:
    - Xóa vùng trồng khỏi database
    - Cascade delete: Tự động xóa tọa độ, cây trồng, lịch sử
    
    Response:
    - 200: Xóa thành công
    - 404: Không tìm thấy vùng trồng
    
    Warning:
    - Hành động KHÔNG THỂ HOÀN TÁC!
    - Nên cân nhắc soft delete (update trang_thai) thay vì hard delete
    """
    
    # ========== FIND FARM ==========
    farm = db.query(VungTrong).filter(VungTrong.id == farm_id).first()
    if not farm:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy vùng trồng ID {farm_id}"
        )
    
    # ========== DELETE ==========
    db.delete(farm)
    # Đánh dấu xóa trong session
    # Cascade delete tự động xóa:
    # - toa_do_vung (ondelete="CASCADE")
    # - vung_cay_trong (ondelete="CASCADE")
    # - lich_su_canh_tac (ondelete="CASCADE")
    
    db.commit()
    # Thực hiện DELETE trong database
    
    return {
        "success": True,
        "message": f"Đã xóa vùng trồng {farm.ma_vung}"
    }


@router.get("/by-code/{ma_vung}")
async def get_farm_by_code(
    ma_vung: str,
    # ma_vung: Mã vùng trồng VietGAP (path parameter)
    # Example: /api/farms/by-code/MSVT001
    
    db: Session = Depends(get_db)
):
    """
    ========== Lấy vùng trồng theo mã MSVT (Get Farm by Code) ==========
    
    Endpoint: GET /api/farms/by-code/{ma_vung}
    
    Chức năng:
    - Lấy thông tin vùng trồng qua mã MSVT (thay vì ID)
    - Hữu ích cho QR code scanning
    - Trả về thông tin rút gọn (không đầy đủ như get by ID)
    
    Path Parameters:
    - ma_vung: Mã vùng (string, unique)
    
    Use Case:
    - Frontend scan QR code → lấy ma_vung → call endpoint này
    - Kiểm tra vùng trồng có tồn tại không
    - Hiển thị thông tin báo cáo
    
    Response:
    - 200: Thông tin vùng trồng rút gọn
    - 404: Không tìm thấy mã vùng
    """
    
    # ========== QUERY WITH EAGER LOADING ==========
    farm = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        # Load chủ sở hữu
        
        joinedload(VungTrong.trang_thai),
        # Load trạng thái
        
        joinedload(VungTrong.toa_do)
        # Load tọa độ (nếu cần vẽ map)
    ).filter(VungTrong.ma_vung == ma_vung).first()
    # Filter by ma_vung (unique column, indexed)
    
    # ========== HANDLE NOT FOUND ==========
    if not farm:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy mã vùng {ma_vung}"
        )
    
    # ========== RETURN COMPACT INFO ==========
    # Trả về thông tin rút gọn (không cần đầy đủ như detail endpoint)
    return {
        "id": farm.id,
        "ma_vung": farm.ma_vung,
        "ten_vung": farm.ten_vung,
        
        "chu_so_huu": farm.chu_so_huu.ten_to_chuc if farm.chu_so_huu else None,
        # Chỉ trả về tên (không cần nested object)
        
        "trang_thai": farm.trang_thai.ten_trang_thai if farm.trang_thai else None,
        # Chỉ trả về tên trạng thái
        
        "dien_tich": farm.dien_tich,
        "dia_chi": farm.dia_chi
    }
