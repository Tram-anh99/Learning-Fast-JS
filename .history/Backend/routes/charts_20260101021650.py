"""
========== ROUTES: CHARTS & STATISTICS API ==========

Mục đích:
API endpoints cho biểu đồ thống kê và dashboard

Endpoints:
1. GET /api/charts/dashboard-stats     - Thống kê tổng quan dashboard
2. GET /api/charts/export-markets      - Biểu đồ thị trường xuất khẩu (Pie)
3. GET /api/charts/crop-production     - Biểu đồ sản lượng theo cây (Bar)
4. GET /api/charts/productivity-trend  - Xu hướng năng suất (Line)
5. GET /api/charts/farm-status         - Trạng thái vùng trồng (Pie)
6. GET /api/charts/activity-timeline   - Timeline hoạt động (Line)

Models sử dụng:
- VungTrong: Vùng trồng (farms data)
- VungCayTrong: Junction table vùng-cây
- LoaiCay: Loại cây trồng
- ThiTruong: Thị trường xuất khẩu
- CayThiTruong: Junction cây-thị trường
- LichSuCanhTac: Lịch sử hoạt động canh tác

Schemas:
- ChartData: Format data cho Chart.js
- DashboardStats: Thống kê dashboard
- ThongKeResponse: Response thống kê

Database tables:
- nongsan.vung_trong
- nongsan.vung_cay_trong
- nongsan.loai_cay
- nongsan.thi_truong
- nongsan.cay_thi_truong
- nongsan.lich_su_canh_tac

Frontend components:
- Frontend/src/views/QuanLyView.vue (dashboard)
- Frontend/src/components/PieChartComponent.vue
- Frontend/src/components/BarChartComponent.vue
- Frontend/src/components/LineChartComponent.vue

Note:
- Một số endpoints dùng fields cũ (ngay_het_han, dien_tich_ha)
- Cần update sau khi models hoàn thiện
- Return sample data nếu DB trống
"""

# ========== IMPORTS ==========
from fastapi import APIRouter, Depends, Query
# FastAPI: Router, dependency injection, query params

from sqlalchemy.orm import Session
# Session: Database session management

from sqlalchemy import func, case
# func: SQL functions (count, sum, avg, etc.)
# case: SQL CASE WHEN statements

from datetime import date, timedelta
# date: Working with dates
# timedelta: Date arithmetic

from database import get_db
# get_db: Dependency function for DB session

from models.vung_trong import VungTrong
from models.loai_cay import LoaiCay, VungCayTrong
from models.thi_truong import ThiTruong, CayThiTruong
from models.lich_su import LichSuCanhTac
# Import các models cần thiết

from schemas import ChartData, DashboardStats, ThongKeResponse
# Response schemas for chart data

# ========== ROUTER SETUP ==========
router = APIRouter(prefix="/charts", tags=["Charts"])
# Prefix: Tất cả endpoints bắt đầu với /api/charts
# Tags: Group trong Swagger docs


@router.get("/dashboard-stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db)
):
    """
    ========== Thống kê tổng quan Dashboard ==========
    
    Endpoint: GET /api/charts/dashboard-stats
    
    Chức năng:
    - Lấy các chỉ số KPI cho dashboard
    - Tổng số vùng trồng, diện tích, sản lượng
    - Đếm hoạt động gần đây (30 ngày)
    
    Response: DashboardStats schema
    - total_farms: Tổng số vùng trồng
    - active_farms: Vùng còn hạn
    - total_area_ha: Tổng diện tích (hecta)
    - total_production: Tổng sản lượng dự kiến (tấn)
    - recent_activities: Hoạt động 30 ngày gần đây
    
    Note: Dùng fields cũ, cần update sau
    """
    
    # ========== DATE RANGE ==========
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    
    # ========== COUNT TOTAL FARMS ==========
    total_farms = db.query(func.count(VungTrong.id)).scalar()
    # SQL: SELECT COUNT(id) FROM vung_trong
    
    # ========== COUNT ACTIVE FARMS ==========
    # TODO: Field ngay_het_han không có trong DB mới
    active_farms = db.query(func.count(VungTrong.id)).filter(
        VungTrong.ngay_het_han >= today
    ).scalar()
    # Cần update logic dựa vào trang_thai_id
    
    # ========== SUM AREA ==========
    # TODO: dien_tich_ha → dien_tich
    total_area = db.query(func.sum(VungTrong.dien_tich_ha)).scalar() or 0
    
    # ========== SUM PRODUCTION ==========
    total_production = db.query(func.sum(VungCayTrong.san_luong_du_kien)).scalar() or 0
    # Tổng sản lượng từ vung_cay_trong
    
    # ========== COUNT ACTIVITIES ==========
    recent_activities = db.query(func.count(LichSuCanhTac.id)).filter(
        LichSuCanhTac.ngay_thuc_hien >= thirty_days_ago
    ).scalar()
    # Đếm hoạt động 30 ngày gần đây
    
    return {
        "total_farms": total_farms or 0,
        "active_farms": active_farms or 0,
        "total_area_ha": round(float(total_area), 2),
        "total_production": round(float(total_production), 2),
        "recent_activities": recent_activities or 0,
        "chart_data": {}
    }


@router.get("/export-markets", response_model=ChartData)
async def get_export_markets_chart(db: Session = Depends(get_db)):
    """
    ========== Biểu đồ Thị trường Xuất khẩu (Pie Chart) ==========
    
    Endpoint: GET /api/charts/export-markets
    
    Chức năng:
    - Thống kê số lượng cây xuất khẩu theo thị trường
    - Format data cho Chart.js Pie Chart
    - Top 10 thị trường
    
    Response: ChartData schema
    - labels: Danh sách tên thị trường
    - datasets[0].data: Số lượng cây mỗi thị trường
    - datasets[0].backgroundColor: Màu sắc slice
    
    Use case:
    - QuanLyView.vue hiển thị pie chart
    - Phân tích thị trường xuất khẩu chính
    """
    
    # ========== QUERY COUNT BY MARKET ==========
    results = db.query(
        ThiTruong.ten_thi_truong,
        # Tên thị trường (Trung Quốc, Hoa Kỳ, etc.)
        
        func.count(CayThiTruong.id).label('count')
        # Đếm số record trong junction table
        # Mỗi record = 1 loại cây xuất khẩu vào thị trường đó
    ).join(
        CayThiTruong, ThiTruong.id == CayThiTruong.thi_truong_id
        # JOIN thi_truong với cay_thi_truong
        # SQL: FROM thi_truong JOIN cay_thi_truong ON ...
    ).group_by(
        ThiTruong.ten_thi_truong
        # GROUP BY ten_thi_truong để đếm theo thị trường
    ).order_by(
        func.count(CayThiTruong.id).desc()
        # ORDER BY count DESC → thị trường nhiều nhất trước
    ).limit(10).all()
    # Chỉ lấy top 10 thị trường
    
    # ========== HANDLE EMPTY DATA ==========
    if not results:
        # Nếu DB trống → return sample data
        return {
            "labels": ["Trung Quốc", "Hoa Kỳ", "Nhật Bản", "Hàn Quốc", "EU"],
            "datasets": [{
                "data": [35, 25, 18, 12, 10],
                "backgroundColor": [
                    "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"
                ]
            }]
        }
    
    # ========== FORMAT DATA FOR CHART.JS ==========
    labels = [r[0] for r in results]
    # r[0] = ten_thi_truong
    
    data = [r[1] for r in results]
    # r[1] = count
    
    # ========== COLOR PALETTE ==========
    colors = [
        "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF",
        "#FF9F40", "#FF6384", "#C9CBCF", "#4BC0C0", "#FF6384"
    ]
    # Màu sắc cho từng slice (10 màu)
    
    return {
        "labels": labels,
        "datasets": [{
            "data": data,
            "backgroundColor": colors[:len(data)]
            # Cắt array colors theo số lượng data
        }]
    }


@router.get("/crop-production", response_model=ChartData)
async def get_crop_production_chart(db: Session = Depends(get_db)):
    """
    ========== Biểu đồ Sản lượng theo Cây (Bar Chart) ==========
    
    Endpoint: GET /api/charts/crop-production
    
    Chức năng:
    - Thống kê tổng sản lượng dự kiến theo loại cây
    - Format data cho Chart.js Bar Chart
    - Top 10 loại cây sản lượng cao nhất
    
    Response: ChartData schema
    - labels: Tên loại cây
    - datasets[0].data: Sản lượng (tấn)
    - datasets[0].label: "Sản lượng (tấn)"
    
    Use case:
    - QuanLyView.vue hiển thị bar chart
    - So sánh sản lượng các loại cây
    """
    
    # ========== QUERY PRODUCTION BY CROP ==========
    results = db.query(
        LoaiCay.ten_cay,
        # Tên loại cây (Xoài, Thanh Long, etc.)
        
        func.sum(VungCayTrong.san_luong_du_kien).label('total_production')
        # Tổng sản lượng dự kiến (SUM)
        # Aggregate từ tất cả vùng trồng cây đó
    ).join(
        VungCayTrong, LoaiCay.id == VungCayTrong.loai_cay_id
        # JOIN loai_cay với vung_cay_trong
    ).group_by(
        LoaiCay.ten_cay
        # GROUP BY để tổng theo loại cây
    ).order_by(
        func.sum(VungCayTrong.san_luong_du_kien).desc()
        # Sắp xếp từ cao xuống thấp
    ).limit(10).all()
    # Top 10 cây
    
    # ========== HANDLE EMPTY DATA ==========
    if not results:
        # DB trống → return sample data
        return {
            "labels": ["Xoài", "Thanh Long", "Nhãn", "Vải", "Chôm Chôm"],
            "datasets": [{
                "label": "Sản lượng (tấn)",
                "data": [450, 380, 320, 280, 150],
                "backgroundColor": "#10b981"
            }]
        }
    
    # ========== FORMAT DATA ==========
    labels = [r[0] for r in results]
    # r[0] = ten_cay
    
    data = [float(r[1]) if r[1] else 0 for r in results]
    # r[1] = total_production (Decimal)
    # Convert to float, handle NULL → 0
    
    return {
        "labels": labels,
        "datasets": [{
            "label": "Sản lượng (tấn)",
            "data": data,
            "backgroundColor": "#10b981"
            # Màu xanh lá (Tailwind green-500)
        }]
    }


@router.get("/productivity-trend", response_model=ChartData)
async def get_productivity_trend_chart(
    years: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Biểu đồ xu hướng năng suất theo năm (Line Chart)
    """
    current_year = date.today().year
    start_year = current_year - years + 1
    
    # Query productivity by year
    results = db.query(
        VungCayTrong.nam_trong,
        func.avg(
            VungCayTrong.san_luong_du_kien / VungCayTrong.dien_tich_ha
        ).label('productivity')
    ).filter(
        VungCayTrong.nam_trong.isnot(None),
        VungCayTrong.nam_trong >= start_year,
        VungCayTrong.dien_tich_ha > 0
    ).group_by(
        VungCayTrong.nam_trong
    ).order_by(
        VungCayTrong.nam_trong
    ).all()
    
    if not results:
        # Return sample data
        return {
            "labels": ["2020", "2021", "2022", "2023", "2024"],
            "datasets": [{
                "label": "Năng suất (tạ/ha)",
                "data": [38.5, 41.2, 43.8, 45.5, 47.2],
                "borderColor": "#3b82f6",
                "tension": 0.4
            }]
        }
    
    labels = [str(r[0]) for r in results]
    data = [round(float(r[1]), 2) if r[1] else 0 for r in results]
    
    return {
        "labels": labels,
        "datasets": [{
            "label": "Năng suất (tạ/ha)",
            "data": data,
            "borderColor": "#3b82f6",
            "tension": 0.4
        }]
    }


@router.get("/farm-status", response_model=ChartData)
async def get_farm_status_chart(db: Session = Depends(get_db)):
    """
    Biểu đồ phân bổ trạng thái vùng trồng
    """
    today = date.today()
    warning_date = today + timedelta(days=30)
    
    # Count by status
    total = db.query(func.count(VungTrong.id)).scalar()
    con_han = db.query(func.count(VungTrong.id)).filter(
        VungTrong.ngay_het_han > warning_date
    ).scalar()
    sap_het_han = db.query(func.count(VungTrong.id)).filter(
        VungTrong.ngay_het_han.between(today, warning_date)
    ).scalar()
    het_han = db.query(func.count(VungTrong.id)).filter(
        VungTrong.ngay_het_han < today
    ).scalar()
    
    return {
        "labels": ["Còn hạn", "Sắp hết hạn", "Hết hạn"],
        "datasets": [{
            "data": [con_han or 0, sap_het_han or 0, het_han or 0],
            "backgroundColor": ["#10b981", "#f59e0b", "#ef4444"]
        }]
    }


@router.get("/activity-timeline", response_model=ChartData)
async def get_activity_timeline(
    days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db)
):
    """
    Biểu đồ timeline hoạt động canh tác
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=days)
    
    # Query activities by date
    results = db.query(
        LichSuCanhTac.ngay_thuc_hien,
        func.count(LichSuCanhTac.id).label('count')
    ).filter(
        LichSuCanhTac.ngay_thuc_hien.between(start_date, end_date)
    ).group_by(
        LichSuCanhTac.ngay_thuc_hien
    ).order_by(
        LichSuCanhTac.ngay_thuc_hien
    ).all()
    
    if not results:
        return {
            "labels": [],
            "datasets": [{
                "label": "Hoạt động",
                "data": [],
                "borderColor": "#8b5cf6",
                "tension": 0.4
            }]
        }
    
    labels = [r[0].strftime("%d/%m") for r in results]
    data = [r[1] for r in results]
    
    return {
        "labels": labels,
        "datasets": [{
            "label": "Hoạt động",
            "data": data,
            "borderColor": "#8b5cf6",
            "backgroundColor": "#8b5cf620",
            "tension": 0.4
        }]
    }
