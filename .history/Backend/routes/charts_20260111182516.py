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
    - Lấy các chỉ số KPI cho dashboard từ VIEW v_dashboard_stats
    - Tổng số vùng trồng, diện tích, sản lượng
    - Đếm hoạt động gần đây
    
    Response: DashboardStats schema
    """
    
    # ========== QUERY FROM VIEW ==========
    # Query từ view v_dashboard_stats đã tính sẵn
    query = """
        SELECT 
            total_farms,
            active_farms,
            total_area,
            total_activities,
            activities_last_30_days,
            farms_with_activities
        FROM nongsan.v_dashboard_stats
    """
    result = db.execute(query).fetchone()
    
    if not result:
        # Fallback nếu view không có data
        return {
            "total_farms": 0,
            "active_farms": 0,
            "total_area_ha": 0.0,
            "total_production": 0.0,
            "recent_activities": 0,
            "chart_data": {}
        }
    
    return {
        "total_farms": result.total_farms or 0,
        "active_farms": result.active_farms or 0,
        "total_area_ha": float(result.total_area or 0),
        "total_production": 0.0,  # TODO: Add to view later
        "recent_activities": result.activities_last_30_days or 0,
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
    # years: Số năm hiển thị (default 5, min 1, max 10)
    # Query param: /api/charts/productivity-trend?years=5
    
    db: Session = Depends(get_db)
):
    """
    ========== Biểu đồ Xu hướng Năng suất (Line Chart) ==========
    
    Endpoint: GET /api/charts/productivity-trend
    
    Chức năng:
    - Thống kê năng suất trung bình theo năm
    - Năng suất = san_luong_du_kien / dien_tich_ha (tấn/ha)
    - Hiển thị xu hướng tăng/giảm qua các năm
    
    Query Parameters:
    - years: Số năm hiển thị (1-10, default 5)
    
    Response: ChartData schema
    - labels: Năm (2020, 2021, etc.)
    - datasets[0].data: Năng suất trung bình (tạ/ha)
    - datasets[0].tension: 0.4 (smooth curve)
    
    Use case:
    - Phân tích hiệu quả sản xuất qua thời gian
    - Dự đoán xu hướng tương lai
    """
    
    # ========== CALCULATE DATE RANGE ==========
    current_year = date.today().year
    # Năm hiện tại (2026)
    
    start_year = current_year - years + 1
    # Ví dụ: years=5 → start_year = 2026 - 5 + 1 = 2022
    # Hiển thị 5 năm: 2022, 2023, 2024, 2025, 2026
    
    # ========== QUERY PRODUCTIVITY BY YEAR ==========
    results = db.query(
        VungCayTrong.nam_trong,
        # Năm trồng
        
        func.avg(
            VungCayTrong.san_luong_du_kien / VungCayTrong.dien_tich_ha
        ).label('productivity')
        # Năng suất = Sản lượng / Diện tích
        # AVG: Trung bình năng suất trong năm
        # Unit: tấn/hecta
    ).filter(
        VungCayTrong.nam_trong.isnot(None),
        # Loại bỏ NULL
        
        VungCayTrong.nam_trong >= start_year,
        # Chỉ lấy data từ start_year
        
        VungCayTrong.dien_tich_ha > 0
        # Tránh chia cho 0
    ).group_by(
        VungCayTrong.nam_trong
        # GROUP BY năm
    ).order_by(
        VungCayTrong.nam_trong
        # Sắp xếp theo thứ tự thời gian
    ).all()
    
    # ========== HANDLE EMPTY DATA ==========
    if not results:
        # DB trống → sample data
        return {
            "labels": ["2020", "2021", "2022", "2023", "2024"],
            "datasets": [{
                "label": "Năng suất (tạ/ha)",
                "data": [38.5, 41.2, 43.8, 45.5, 47.2],
                "borderColor": "#3b82f6",
                "tension": 0.4
            }]
        }
    
    # ========== FORMAT DATA ==========
    labels = [str(r[0]) for r in results]
    # Convert year to string (2023 → "2023")
    
    data = [round(float(r[1]), 2) if r[1] else 0 for r in results]
    # r[1] = productivity (AVG result)
    # Round 2 chữ số thập phân
    
    return {
        "labels": labels,
        "datasets": [{
            "label": "Năng suất (tạ/ha)",
            "data": data,
            "borderColor": "#3b82f6",
            # Màu xanh dương (Tailwind blue-500)
            
            "tension": 0.4
            # Bezier curve tension (0 = straight, 1 = very curved)
            # 0.4 = smooth curve
        }]
    }


@router.get("/farm-status", response_model=ChartData)
async def get_farm_status_chart(db: Session = Depends(get_db)):
    """
    ========== Biểu đồ Trạng thái Vùng (Pie Chart) ==========
    
    Endpoint: GET /api/charts/farm-status
    
    Chức năng:
    - Thống kê vùng trồng theo trạng thái hạn giấy chứng nhận
    - 3 nhóm: Còn hạn, Sắp hết hạn, Hết hạn
    - Warning threshold: 30 ngày
    
    Response: ChartData schema
    - labels: ["Còn hạn", "Sắp hết hạn", "Hết hạn"]
    - datasets[0].data: Số lượng vùng mỗi nhóm
    - datasets[0].backgroundColor: Màu (xanh, vàng, đỏ)
    
    Note: Dùng field cũ ngay_het_han
    """
    
    # ========== DATE THRESHOLDS ==========
    today = date.today()
    # Ngày hiện tại
    
    warning_date = today + timedelta(days=30)
    # 30 ngày từ nay (ngưỡng cảnh báo)
    
    # ========== COUNT TOTAL ==========
    total = db.query(func.count(VungTrong.id)).scalar()
    # Tổng số vùng (không dùng, reserved)
    
    # ========== COUNT CON HAN ==========
    # TODO: Field ngay_het_han không tồn tại trong DB mới
    con_han = db.query(func.count(VungTrong.id)).filter(
        VungTrong.ngay_het_han > warning_date
        # ngay_het_han > (today + 30 days)
        # Còn hạn > 30 ngày
    ).scalar()
    
    # ========== COUNT SAP HET HAN ==========
    sap_het_han = db.query(func.count(VungTrong.id)).filter(
        VungTrong.ngay_het_han.between(today, warning_date)
        # ngay_het_han BETWEEN today AND (today + 30 days)
        # Sắp hết hạn trong vòng 30 ngày
    ).scalar()
    
    # ========== COUNT HET HAN ==========
    het_han = db.query(func.count(VungTrong.id)).filter(
        VungTrong.ngay_het_han < today
        # Đã hết hạn (quá khứ)
    ).scalar()
    
    # ========== RETURN PIE CHART DATA ==========
    return {
        "labels": ["Còn hạn", "Sắp hết hạn", "Hết hạn"],
        "datasets": [{
            "data": [con_han or 0, sap_het_han or 0, het_han or 0],
            # Đảm bảo không NULL
            
            "backgroundColor": ["#10b981", "#f59e0b", "#ef4444"]
            # Xanh lá (OK), Vàng (Warning), Đỏ (Danger)
            # Tailwind: green-500, amber-500, red-500
        }]
    }


@router.get("/activity-timeline", response_model=ChartData)
async def get_activity_timeline(
    days: int = Query(30, ge=7, le=90),
    # days: Số ngày hiển thị (default 30, min 7, max 90)
    
    db: Session = Depends(get_db)
):
    """
    ========== Biểu đồ Timeline Hoạt động (Line Chart) ==========
    
    Endpoint: GET /api/charts/activity-timeline
    
    Chức năng:
    - Hiển thị số lượng hoạt động canh tác theo ngày
    - Timeline: 7-90 ngày gần đây
    - Giúp theo dõi tần suất hoạt động
    
    Query Parameters:
    - days: Số ngày hiển thị (7-90, default 30)
    
    Response: ChartData schema
    - labels: Ngày (dd/mm format)
    - datasets[0].data: Số hoạt động mỗi ngày
    
    Use case:
    - Xác định ngày nào có nhiều hoạt động
    - Phân tích patterns (weekend vs weekday, etc.)
    """
    
    # ========== DATE RANGE ==========
    end_date = date.today()
    # Ngày kết thúc = hôm nay
    
    start_date = end_date - timedelta(days=days)
    # Ngày bắt đầu = days ngày trước
    # Ví dụ: days=30 → 30 ngày gần đây
    
    # ========== QUERY ACTIVITIES BY DATE ==========
    results = db.query(
        LichSuCanhTac.ngay_thuc_hien,
        # Ngày thực hiện hoạt động
        
        func.count(LichSuCanhTac.id).label('count')
        # Đếm số hoạt động trong ngày
    ).filter(
        LichSuCanhTac.ngay_thuc_hien.between(start_date, end_date)
        # Chỉ lấy data trong khoảng [start_date, end_date]
    ).group_by(
        LichSuCanhTac.ngay_thuc_hien
        # GROUP BY ngày
    ).order_by(
        LichSuCanhTac.ngay_thuc_hien
        # Sắp xếp theo thời gian
    ).all()
    
    # ========== HANDLE EMPTY DATA ==========
    if not results:
        # DB trống → empty chart
        return {
            "labels": [],
            "datasets": [{
                "label": "Hoạt động",
                "data": [],
                "borderColor": "#8b5cf6",
                "tension": 0.4
            }]
        }
    
    # ========== FORMAT DATA ==========
    labels = [r[0].strftime("%d/%m") for r in results]
    # r[0] = ngay_thuc_hien (date object)
    # strftime: Convert to "dd/mm" format
    # Ví dụ: date(2026, 1, 1) → "01/01"
    
    data = [r[1] for r in results]
    # r[1] = count (số hoạt động)
    
    return {
        "labels": labels,
        "datasets": [{
            "label": "Hoạt động",
            "data": data,
            
            "borderColor": "#8b5cf6",
            # Màu tím (Tailwind violet-500)
            
            "backgroundColor": "#8b5cf620",
            # Màu tím nhạt (20% opacity) cho fill area
            
            "tension": 0.4
            # Smooth curve
        }]
    }
