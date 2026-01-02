"""
========== ROUTES: QR CODE API (Traceability QR Generation) ==========

Mục đích:
API endpoints cho tạo mã QR truy xuất nguồn gốc

Endpoints:
1. GET /api/qr/generate/{ma_vung}  - Tạo QR code cho MSVT
2. GET /api/qr/trace/{ma_vung}     - Public traceability info (không cần auth)

Models:
- VungTrong: Thông tin vùng trồng

Chức năng QR:
- Generate QR code dạng base64 image
- QR data: URL trỏ đến trang công khai
- Public page hiển thị: MSVT, tên vùng, địa chỉ, bản đồ, lịch sử canh tác

Usage:
- Admin/Nha nông tạo QR để in nhãn sản phẩm
- Khách hàng quét QR → xem thông tin truy xuất nguồn gốc
"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models.vung_trong import VungTrong
from models.lich_su import LichSuCanhTac
import qrcode
from io import BytesIO
import base64

router = APIRouter(prefix="/qr", tags=["QR Code"])


@router.get("/generate/{ma_vung}")
async def generate_qr_code(
    ma_vung: str,
    # ma_vung: Mã số vùng trồng VietGAP
    # Example: MSVT001
    
    size: int = 300,
    # size: Kích thước QR code (pixels)
    # Default: 300x300px
    
    db: Session = Depends(get_db)
):
    """
    ========== Tạo mã QR cho MSVT (Generate QR Code) ==========
    
    Endpoint: GET /api/qr/generate/{ma_vung}
    
    Chức năng:
    - Kiểm tra MSVT có tồn tại không
    - Tạo QR code chứa URL công khai
    - Return QR image dạng base64
    
    Query Parameters:
    - size: Kích thước QR (default 300)
    
    Response:
    {
        "ma_vung": "MSVT001",
        "ten_vung": "Vùng Lúa An Lộc 1",
        "qr_code": "data:image/png;base64,iVBORw0KG..."
    }
    
    Use case:
    - Admin tạo QR → in nhãn sản phẩm
    - Frontend hiển thị QR trong modal
    """
    
    # ========== VALIDATE MSVT ==========
    farm = db.query(VungTrong).filter(
        VungTrong.ma_vung == ma_vung
    ).first()
    
    if not farm:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy mã vùng {ma_vung}"
        )
    
    # ========== GENERATE QR URL ==========
    # URL công khai cho khách hàng truy cập
    # TODO: Thay localhost bằng domain thực tế
    qr_url = f"http://localhost:5173/trace/{ma_vung}"
    # Example: http://nongsan.vn/trace/MSVT001
    
    # ========== CREATE QR CODE ==========
    qr = qrcode.QRCode(
        version=1,  # QR version (1-40), 1 = nhỏ nhất
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Kích thước mỗi ô
        border=4,  # Border size
    )
    qr.add_data(qr_url)  # Add URL data
    qr.make(fit=True)  # Optimize size
    
    # ========== GENERATE IMAGE ==========
    img = qr.make_image(fill_color="black", back_color="white")
    # Tạo PIL Image object
    
    # Resize to requested size
    img = img.resize((size, size))
    
    # ========== CONVERT TO BASE64 ==========
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    # ========== RETURN RESPONSE ==========
    return {
        "ma_vung": ma_vung,
        "ten_vung": farm.ten_vung,
        "qr_url": qr_url,
        "qr_code": f"data:image/png;base64,{img_base64}"
        # Data URL có thể dùng trực tiếp trong <img src="...">
    }


@router.get("/trace/{ma_vung}")
async def get_public_traceability(
    ma_vung: str,
    db: Session = Depends(get_db)
):
    """
    ========== Thông tin truy xuất công khai (Public Traceability) ==========
    
    Endpoint: GET /api/qr/trace/{ma_vung}
    
    Chức năng:
    - Endpoint công khai (không cần authentication)
    - Lấy thông tin vùng trồng + lịch sử canh tác
    - Tối ưu cho mobile (load nhanh)
    
    Response:
    {
        "farm": {...},         # Thông tin vùng trồng
        "owner": {...},        # Chủ sở hữu
        "status": {...},       # Trạng thái
        "coordinates": [...],  # Tọa độ polygon
        "history": [...]       # Lịch sử 10 hoạt động gần nhất
    }
    
    Use case:
    - Khách hàng quét QR → xem trang này
    - TraceabilityPage.vue fetch data từ endpoint này
    """
    
    # ========== LOAD FARM DATA ==========
    farm = db.query(VungTrong).options(
        joinedload(VungTrong.chu_so_huu),
        joinedload(VungTrong.trang_thai),
        joinedload(VungTrong.toa_do)
    ).filter(VungTrong.ma_vung == ma_vung).first()
    
    if not farm:
        raise HTTPException(
            status_code=404,
            detail=f"Không tìm thấy mã vùng {ma_vung}"
        )
    
    # ========== LOAD RECENT HISTORY ==========
    # Lấy 10 hoạt động gần nhất
    history = db.query(LichSuCanhTac).options(
        joinedload(LichSuCanhTac.loai_hoat_dong)
    ).filter(
        LichSuCanhTac.vung_trong_id == farm.id
    ).order_by(
        LichSuCanhTac.ngay_thuc_hien.desc()
    ).limit(10).all()
    
    # ========== FORMAT RESPONSE ==========
    return {
        "farm": {
            "ma_vung": farm.ma_vung,
            "ten_vung": farm.ten_vung,
            "dia_chi": farm.dia_chi,
            "dien_tich": float(farm.dien_tich) if farm.dien_tich else 0
        },
        "owner": {
            "ten_to_chuc": farm.chu_so_huu.ten_to_chuc if farm.chu_so_huu else None,
            "dia_chi": farm.chu_so_huu.dia_chi if farm.chu_so_huu else None,
            "dien_thoai": farm.chu_so_huu.dien_thoai if farm.chu_so_huu else None
        } if farm.chu_so_huu else None,
        "status": {
            "ten_trang_thai": farm.trang_thai.ten_trang_thai if farm.trang_thai else None,
            "mau_sac": farm.trang_thai.mau_sac if farm.trang_thai else None
        } if farm.trang_thai else None,
        "coordinates": [
            {
                "vi_do": float(coord.vi_do) if coord.vi_do else 0,
                "kinh_do": float(coord.kinh_do) if coord.kinh_do else 0,
                "thu_tu": coord.thu_tu
            }
            for coord in sorted(farm.toa_do, key=lambda x: x.thu_tu)
        ] if farm.toa_do else [],
        "history": [
            {
                "ngay_thuc_hien": h.ngay_thuc_hien.isoformat() if h.ngay_thuc_hien else None,
                "tieu_de": getattr(h, 'tieu_de', None),
                "noi_dung": getattr(h, 'noi_dung', None),
                "loai_hoat_dong": h.loai_hoat_dong.ten_loai if h.loai_hoat_dong else None,
                "nguoi_thuc_hien": h.nguoi_thuc_hien
            }
            for h in history
        ]
    }
