"""
API Routes for enhanced facilities with coordinates and views
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
import psycopg2
from config import settings

router = APIRouter(prefix="/enhanced", tags=["enhanced"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


# Response Models
class FacilityLocation(BaseModel):
    id: int
    ma_co_so: str
    ten_co_so: str
    loai_hinh: Optional[str]
    dia_chi: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    ten_tinh: Optional[str]
    ten_huyen: Optional[str]
    ten_xa: Optional[str]

    class Config:
        from_attributes = True


class FarmCrop(BaseModel):
    vung_trong_id: int
    ma_vung: str
    ten_vung: str
    loai_cay_id: int
    ten_cay: str
    dien_tich: Optional[float]
    nam_trong: Optional[int]
    ten_tinh: Optional[str]

    class Config:
        from_attributes = True


class FacilityStats(BaseModel):
    total_facilities: int
    with_coordinates: int
    with_province: int
    by_type: dict
    by_province: dict


@router.get("/facilities", response_model=List[FacilityLocation])
async def get_facilities_enhanced(
    tinh_id: Optional[int] = Query(None, description="Filter by province ID"),
    has_coordinates: Optional[bool] = Query(
        None, description="Filter facilities with coordinates"),
    loai_hinh_id: Optional[int] = Query(
        None, description="Filter by facility type"),
    limit: int = Query(100, le=1000, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination")
):
    """
    Get facilities with full location information including coordinates
    Uses v_co_so_full view for efficient querying
    """
    try:
        conn = get_db()
        cur = conn.cursor()

        # Build query
        query = """
            SELECT 
                cs.id,
                cs.ma_co_so,
                cs.ten_co_so,
                lh.ten_loai as loai_hinh,
                cs.dia_chi,
                cs.latitude,
                cs.longitude,
                t.ten_tinh,
                h.ten_huyen,
                x.ten_xa
            FROM nongsan.co_so cs
            LEFT JOIN nongsan.loai_hinh_co_so lh ON cs.loai_hinh_id = lh.id
            LEFT JOIN nongsan.tinh t ON cs.tinh_id = t.id
            LEFT JOIN nongsan.huyen h ON cs.huyen_id = h.id
            LEFT JOIN nongsan.xa x ON cs.xa_id = x.id
            WHERE 1=1
        """
        params = []

        # Apply filters
        if tinh_id is not None:
            query += " AND cs.tinh_id = %s"
            params.append(tinh_id)

        if has_coordinates is not None:
            if has_coordinates:
                query += " AND cs.latitude IS NOT NULL AND cs.longitude IS NOT NULL"
            else:
                query += " AND (cs.latitude IS NULL OR cs.longitude IS NULL)"

        if loai_hinh_id is not None:
            query += " AND cs.loai_hinh_id = %s"
            params.append(loai_hinh_id)

        query += " ORDER BY cs.id LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cur.execute(query, params)
        rows = cur.fetchall()

        facilities = []
        for row in rows:
            facilities.append(FacilityLocation(
                id=row[0],
                ma_co_so=row[1],
                ten_co_so=row[2],
                loai_hinh=row[3],
                dia_chi=row[4],
                latitude=row[5],
                longitude=row[6],
                ten_tinh=row[7],
                ten_huyen=row[8],
                ten_xa=row[9]
            ))

        cur.close()
        conn.close()

        return facilities

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@router.get("/facilities/map")
async def get_facilities_for_map(
    tinh_id: Optional[int] = Query(None, description="Filter by province ID"),
    bounds: Optional[str] = Query(
        None, description="Bounding box: lat_min,lon_min,lat_max,lon_max")
):
    """
    Get facilities with coordinates for map display
    Returns only essential data for performance
    """
    try:
        conn = get_db()
        cur = conn.cursor()

        query = """
            SELECT 
                cs.id,
                cs.ma_co_so,
                cs.ten_co_so,
                cs.latitude,
                cs.longitude,
                lh.ten_loai as loai_hinh,
                t.ten_tinh
            FROM nongsan.co_so cs
            LEFT JOIN nongsan.loai_hinh_co_so lh ON cs.loai_hinh_id = lh.id
            LEFT JOIN nongsan.tinh t ON cs.tinh_id = t.id
            WHERE cs.latitude IS NOT NULL 
            AND cs.longitude IS NOT NULL
        """
        params = []

        if tinh_id is not None:
            query += " AND cs.tinh_id = %s"
            params.append(tinh_id)

        if bounds:
            try:
                lat_min, lon_min, lat_max, lon_max = map(
                    float, bounds.split(','))
                query += """ 
                    AND cs.latitude BETWEEN %s AND %s
                    AND cs.longitude BETWEEN %s AND %s
                """
                params.extend([lat_min, lat_max, lon_min, lon_max])
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid bounds format")

        cur.execute(query, params)
        rows = cur.fetchall()

        markers = []
        for row in rows:
            markers.append({
                "id": row[0],
                "ma_co_so": row[1],
                "ten_co_so": row[2],
                "lat": float(row[3]),
                "lon": float(row[4]),
                "loai_hinh": row[5],
                "ten_tinh": row[6]
            })

        cur.close()
        conn.close()

        return {
            "total": len(markers),
            "markers": markers
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@router.get("/farms/crops", response_model=List[FarmCrop])
async def get_farms_with_crops():
    """
    Get farms with their crops information
    Uses v_vung_cay_trong view
    """
    try:
        conn = get_db()
        cur = conn.cursor()

        query = """
            SELECT 
                vct.vung_trong_id,
                vt.ma_vung,
                vt.ten_vung,
                lc.id as loai_cay_id,
                lc.ten_cay,
                vct.dien_tich,
                vct.nam_trong,
                t.ten_tinh
            FROM nongsan.vung_cay_trong vct
            JOIN nongsan.vung_trong vt ON vct.vung_trong_id = vt.id
            JOIN nongsan.loai_cay lc ON vct.loai_cay_id = lc.id
            LEFT JOIN nongsan.tinh t ON vt.tinh_id = t.id
            ORDER BY vt.id, lc.ten_cay
        """

        cur.execute(query)
        rows = cur.fetchall()

        farms = []
        for row in rows:
            farms.append(FarmCrop(
                vung_trong_id=row[0],
                ma_vung=row[1],
                ten_vung=row[2],
                loai_cay_id=row[3],
                ten_cay=row[4],
                dien_tich=row[5],
                nam_trong=row[6],
                ten_tinh=row[7]
            ))

        cur.close()
        conn.close()

        return farms

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@router.get("/stats", response_model=FacilityStats)
async def get_facility_stats():
    """
    Get statistics about facilities
    """
    try:
        conn = get_db()
        cur = conn.cursor()

        # Total facilities
        cur.execute("SELECT COUNT(*) FROM nongsan.co_so")
        total = cur.fetchone()[0]

        # With coordinates
        cur.execute("""
            SELECT COUNT(*) FROM nongsan.co_so 
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
        """)
        with_coords = cur.fetchone()[0]

        # With province
        cur.execute(
            "SELECT COUNT(*) FROM nongsan.co_so WHERE tinh_id IS NOT NULL")
        with_province = cur.fetchone()[0]

        # By type
        cur.execute("""
            SELECT lh.ten_loai, COUNT(*) 
            FROM nongsan.co_so cs
            LEFT JOIN nongsan.loai_hinh_co_so lh ON cs.loai_hinh_id = lh.id
            GROUP BY lh.ten_loai
            ORDER BY COUNT(*) DESC
        """)
        by_type = {row[0] or "Unknown": row[1] for row in cur.fetchall()}

        # By province
        cur.execute("""
            SELECT t.ten_tinh, COUNT(*) 
            FROM nongsan.co_so cs
            LEFT JOIN nongsan.tinh t ON cs.tinh_id = t.id
            WHERE cs.tinh_id IS NOT NULL
            GROUP BY t.ten_tinh
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """)
        by_province = {row[0]: row[1] for row in cur.fetchall()}

        cur.close()
        conn.close()

        return FacilityStats(
            total_facilities=total,
            with_coordinates=with_coords,
            with_province=with_province,
            by_type=by_type,
            by_province=by_province
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@router.get("/provinces")
async def get_provinces_with_counts():
    """
    Get all provinces with facility counts
    """
    try:
        conn = get_db()
        cur = conn.cursor()

        query = """
            SELECT 
                t.id,
                t.ma_tinh,
                t.ten_tinh,
                COUNT(cs.id) as facility_count,
                COUNT(CASE WHEN cs.latitude IS NOT NULL THEN 1 END) as with_coords_count
            FROM nongsan.tinh t
            LEFT JOIN nongsan.co_so cs ON t.id = cs.tinh_id
            GROUP BY t.id, t.ma_tinh, t.ten_tinh
            ORDER BY facility_count DESC
        """

        cur.execute(query)
        rows = cur.fetchall()

        provinces = []
        for row in rows:
            provinces.append({
                "id": row[0],
                "ma_tinh": row[1],
                "ten_tinh": row[2],
                "facility_count": row[3],
                "with_coords_count": row[4]
            })

        cur.close()
        conn.close()

        return {"total": len(provinces), "provinces": provinces}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")
