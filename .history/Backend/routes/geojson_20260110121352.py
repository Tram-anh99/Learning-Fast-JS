"""
GeoJSON API Routes for map visualization
- Polygon/Line rendering
- Click info for regions
- Multi-layer support
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import psycopg2
from config import settings

router = APIRouter(prefix="/geojson", tags=["geojson"])


def get_db():
    """Get database connection"""
    return psycopg2.connect(settings.DATABASE_URL)


class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: Dict[str, Any]


class GeoJSONCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]


@router.get("/provinces", response_model=GeoJSONCollection)
async def get_provinces_geojson(
    tinh_id: Optional[int] = Query(None, description="Filter by province ID")
):
    """
    Get provinces as GeoJSON Polygon features
    Each province has x,y coordinates - we'll create simple bounding boxes
    
    Returns GeoJSON FeatureCollection with properties:
    - id, ma_tinh, ten_tinh, facility_count
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        
        query = """
            SELECT 
                t.id,
                t.ten_tinh,
                t.x,
                t.y,
                COUNT(DISTINCT cs.id) as facility_count,
                COUNT(DISTINCT vt.id) as farm_count
            FROM nongsan.tinh t
            LEFT JOIN nongsan.co_so cs ON t.id = cs.tinh_id
            LEFT JOIN nongsan.vung_trong vt ON t.id = vt.tinh_id
            WHERE 1=1
        """
        params = []
        
        if tinh_id:
            query += " AND t.id = %s"
            params.append(tinh_id)
        
        query += " GROUP BY t.id, t.ten_tinh, t.x, t.y"
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        features = []
        for row in rows:
            tid, ten_tinh, x, y, facility_count, farm_count = row
            
            # Skip if no coordinates
            if x is None or y is None:
                continue
            
            # Create a simple bounding box around the point (±0.5 degrees)
            x_float = float(x)
            y_float = float(y)
            
            polygon_coords = [[
                [x_float - 0.5, y_float - 0.5],  # SW
                [x_float + 0.5, y_float - 0.5],  # SE
                [x_float + 0.5, y_float + 0.5],  # NE
                [x_float - 0.5, y_float + 0.5],  # NW
                [x_float - 0.5, y_float - 0.5]   # Close polygon
            ]]
            
            features.append(GeoJSONFeature(
                type="Feature",
                geometry={
                    "type": "Polygon",
                    "coordinates": polygon_coords
                },
                properties={
                    "id": tid,
                    "ten_tinh": ten_tinh,
                    "center": [x_float, y_float],
                    "facility_count": facility_count,
                    "farm_count": farm_count,
                    "layer": "provinces"
                }
            ))
        
        cur.close()
        conn.close()
        
        return GeoJSONCollection(type="FeatureCollection", features=features)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/districts", response_model=GeoJSONCollection)
async def get_districts_geojson(
    tinh_id: Optional[int] = Query(None, description="Filter by province ID"),
    huyen_id: Optional[int] = Query(None, description="Filter by district ID")
):
    """
    Get districts as GeoJSON Polygon features
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        
        query = """
            SELECT 
                h.id,
                h.ten_huyen,
                h.x,
                h.y,
                h.tinh_id,
                t.ten_tinh,
                COUNT(DISTINCT cs.id) as facility_count,
                COUNT(DISTINCT vt.id) as farm_count
            FROM nongsan.huyen h
            LEFT JOIN nongsan.tinh t ON h.tinh_id = t.id
            LEFT JOIN nongsan.co_so cs ON h.id = cs.huyen_id
            LEFT JOIN nongsan.vung_trong vt ON h.id = vt.huyen_id
            WHERE 1=1
        """
        params = []
        
        if tinh_id:
            query += " AND h.tinh_id = %s"
            params.append(tinh_id)
        
        if huyen_id:
            query += " AND h.id = %s"
            params.append(huyen_id)
        
        query += " GROUP BY h.id, h.ten_huyen, h.x, h.y, h.tinh_id, t.ten_tinh"
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        features = []
        for row in rows:
            hid, ten_huyen, x, y, tinh_id, ten_tinh, facility_count, farm_count = row
            
            if x is None or y is None:
                continue
            
            x_float = float(x)
            y_float = float(y)
            
            # Smaller bounding box for districts (±0.2 degrees)
            polygon_coords = [[
                [x_float - 0.2, y_float - 0.2],
                [x_float + 0.2, y_float - 0.2],
                [x_float + 0.2, y_float + 0.2],
                [x_float - 0.2, y_float + 0.2],
                [x_float - 0.2, y_float - 0.2]
            ]]
            
            features.append(GeoJSONFeature(
                type="Feature",
                geometry={
                    "type": "Polygon",
                    "coordinates": polygon_coords
                },
                properties={
                    "id": hid,
                    "ten_huyen": ten_huyen,
                    "tinh_id": tinh_id,
                    "ten_tinh": ten_tinh,
                    "center": [x_float, y_float],
                    "facility_count": facility_count,
                    "farm_count": farm_count,
                    "layer": "districts"
                }
            ))
        
        cur.close()
        conn.close()
        
        return GeoJSONCollection(type="FeatureCollection", features=features)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/communes", response_model=GeoJSONCollection)
async def get_communes_geojson(
    huyen_id: Optional[int] = Query(None, description="Filter by district ID"),
    xa_id: Optional[int] = Query(None, description="Filter by commune ID")
):
    """
    Get communes as GeoJSON Polygon features
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        
        query = """
            SELECT 
                x.id,
                x.ten_xa,
                x.x,
                x.y,
                x.huyen_id,
                h.ten_huyen,
                h.tinh_id,
                t.ten_tinh,
                COUNT(DISTINCT cs.id) as facility_count,
                COUNT(DISTINCT vt.id) as farm_count
            FROM nongsan.xa x
            LEFT JOIN nongsan.huyen h ON x.huyen_id = h.id
            LEFT JOIN nongsan.tinh t ON h.tinh_id = t.id
            LEFT JOIN nongsan.co_so cs ON x.id = cs.xa_id
            LEFT JOIN nongsan.vung_trong vt ON x.id = vt.xa_id
            WHERE 1=1
        """
        params = []
        
        if huyen_id:
            query += " AND x.huyen_id = %s"
            params.append(huyen_id)
        
        if xa_id:
            query += " AND x.id = %s"
            params.append(xa_id)
        
        query += " GROUP BY x.id, x.ten_xa, x.x, x.y, x.huyen_id, h.ten_huyen, h.tinh_id, t.ten_tinh"
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        features = []
        for row in rows:
            xid, ten_xa, x, y, huyen_id, ten_huyen, tinh_id, ten_tinh, facility_count, farm_count = row
            
            if x is None or y is None:
                continue
            
            x_float = float(x)
            y_float = float(y)
            
            # Even smaller bounding box for communes (±0.1 degrees)
            polygon_coords = [[
                [x_float - 0.1, y_float - 0.1],
                [x_float + 0.1, y_float - 0.1],
                [x_float + 0.1, y_float + 0.1],
                [x_float - 0.1, y_float + 0.1],
                [x_float - 0.1, y_float - 0.1]
            ]]
            
            features.append(GeoJSONFeature(
                type="Feature",
                geometry={
                    "type": "Polygon",
                    "coordinates": polygon_coords
                },
                properties={
                    "id": xid,
                    "ten_xa": ten_xa,
                    "huyen_id": huyen_id,
                    "ten_huyen": ten_huyen,
                    "tinh_id": tinh_id,
                    "ten_tinh": ten_tinh,
                    "center": [x_float, y_float],
                    "facility_count": facility_count,
                    "farm_count": farm_count,
                    "layer": "communes"
                }
            ))
        
        cur.close()
        conn.close()
        
        return GeoJSONCollection(type="FeatureCollection", features=features)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/farms/boundaries", response_model=GeoJSONCollection)
async def get_farm_boundaries_geojson(
    tinh_id: Optional[int] = Query(None, description="Filter by province ID"),
    vung_id: Optional[int] = Query(None, description="Filter by farm ID")
):
    """
    Get farm boundaries as GeoJSON Polygon features
    Creates polygons from farm area (dien_tich)
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        
        query = """
            SELECT 
                vt.id,
                vt.ma_vung,
                vt.ten_vung,
                vt.dien_tich,
                vt.tinh_id,
                t.ten_tinh,
                t.x as tinh_x,
                t.y as tinh_y,
                tch.ten_to_chuc as chu_so_huu,
                tt.ten_trang_thai as trang_thai
            FROM nongsan.vung_trong vt
            LEFT JOIN nongsan.tinh t ON vt.tinh_id = t.id
            LEFT JOIN nongsan.to_chuc_ca_nhan tch ON vt.chu_so_huu_id = tch.id
            LEFT JOIN nongsan.trang_thai_vung tt ON vt.trang_thai_id = tt.id
            WHERE 1=1
        """
        params = []
        
        if tinh_id:
            query += " AND vt.tinh_id = %s"
            params.append(tinh_id)
        
        if vung_id:
            query += " AND vt.id = %s"
            params.append(vung_id)
        
        cur.execute(query, params)
        rows = cur.fetchall()
        
        features = []
        for row in rows:
            vid, ma_vung, ten_vung, dien_tich, tinh_id, ten_tinh, tinh_x, tinh_y, chu_so_huu, trang_thai = row
            
            if tinh_x is None or tinh_y is None or dien_tich is None:
                continue
            
            # Create polygon based on area (simplified square)
            # area = side^2, so side = sqrt(area)
            # Convert hectares to approximate degrees (very rough: 1 ha ≈ 0.003° × 0.003°)
            import math
            side_km = math.sqrt(float(dien_tich)) / 10  # rough conversion
            side_deg = side_km * 0.009  # 1 km ≈ 0.009 degrees at Vietnam latitude
            
            center_x = float(tinh_x) + (vid % 10 - 5) * 0.05  # offset from province center
            center_y = float(tinh_y) + ((vid // 10) % 10 - 5) * 0.05
            
            half_side = side_deg / 2
            polygon_coords = [[
                [center_x - half_side, center_y - half_side],
                [center_x + half_side, center_y - half_side],
                [center_x + half_side, center_y + half_side],
                [center_x - half_side, center_y + half_side],
                [center_x - half_side, center_y - half_side]
            ]]
            
            features.append(GeoJSONFeature(
                type="Feature",
                geometry={
                    "type": "Polygon",
                    "coordinates": polygon_coords
                },
                properties={
                    "id": vid,
                    "ma_vung": ma_vung,
                    "ten_vung": ten_vung,
                    "dien_tich": float(dien_tich),
                    "tinh_id": tinh_id,
                    "ten_tinh": ten_tinh,
                    "chu_so_huu": chu_so_huu,
                    "trang_thai": trang_thai,
                    "center": [center_x, center_y],
                    "layer": "farms"
                }
            ))
        
        cur.close()
        conn.close()
        
        return GeoJSONCollection(type="FeatureCollection", features=features)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/routes/lines", response_model=GeoJSONCollection)
async def get_routes_as_lines():
    """
    Get routes/connections as GeoJSON LineString features
    Creates lines between provinces that share farms
    Note: thi_truong table doesn't have location data, so we create simplified province-to-province connections
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        
        # Get province-to-province connections based on farm locations
        # Create example lines between adjacent provinces (simplified)
        query = """
            WITH province_coords AS (
                SELECT 
                    id, 
                    ten_tinh, 
                    x, 
                    y,
                    ROW_NUMBER() OVER (ORDER BY id) as rn
                FROM nongsan.tinh
                WHERE x IS NOT NULL AND y IS NOT NULL
            )
            SELECT 
                p1.id as from_id,
                p1.ten_tinh as from_tinh,
                p1.x as from_x,
                p1.y as from_y,
                p2.id as to_id,
                p2.ten_tinh as to_tinh,
                p2.x as to_x,
                p2.y as to_y
            FROM province_coords p1
            JOIN province_coords p2 ON p2.rn = p1.rn + 1
            LIMIT 20
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        features = []
        for idx, row in enumerate(rows):
            from_tid, from_tinh, from_x, from_y, to_tid, to_tinh, to_x, to_y, conn_count = row
            
            # Create LineString between provinces
            line_coords = [
                [float(from_x), float(from_y)],
                [float(to_x), float(to_y)]
            ]
            
            features.append(GeoJSONFeature(
                type="Feature",
                geometry={
                    "type": "LineString",
                    "coordinates": line_coords
                },
                properties={
                    "id": idx,
                    "from_tinh_id": from_tid,
                    "from_tinh": from_tinh,
                    "to_tinh_id": to_tid,
                    "to_tinh": to_tinh,
                    "connection_count": conn_count,
                    "layer": "routes"
                }
            ))
        
        cur.close()
        conn.close()
        
        return GeoJSONCollection(type="FeatureCollection", features=features)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/info/{layer}/{feature_id}")
async def get_feature_info(layer: str, feature_id: int):
    """
    Get detailed information for a clicked feature
    
    Layers:
    - provinces: Province info
    - districts: District info  
    - communes: Commune info
    - farms: Farm details with crops
    - routes: Route/connection details
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        
        if layer == "provinces":
            cur.execute("""
                SELECT 
                    t.id, t.ten_tinh, t.x, t.y,
                    COUNT(DISTINCT cs.id) as facilities,
                    COUNT(DISTINCT vt.id) as farms,
                    COUNT(DISTINCT h.id) as districts,
                    COUNT(DISTINCT x.id) as communes
                FROM nongsan.tinh t
                LEFT JOIN nongsan.co_so cs ON t.id = cs.tinh_id
                LEFT JOIN nongsan.vung_trong vt ON t.id = vt.tinh_id
                LEFT JOIN nongsan.huyen h ON t.id = h.tinh_id
                LEFT JOIN nongsan.xa x ON h.id = x.huyen_id
                WHERE t.id = %s
                GROUP BY t.id, t.ten_tinh, t.x, t.y
            """, (feature_id,))
            
        elif layer == "districts":
            cur.execute("""
                SELECT 
                    h.id, h.ten_huyen, h.x, h.y, h.tinh_id, t.ten_tinh,
                    COUNT(DISTINCT cs.id) as facilities,
                    COUNT(DISTINCT vt.id) as farms,
                    COUNT(DISTINCT x.id) as communes
                FROM nongsan.huyen h
                LEFT JOIN nongsan.tinh t ON h.tinh_id = t.id
                LEFT JOIN nongsan.co_so cs ON h.id = cs.huyen_id
                LEFT JOIN nongsan.vung_trong vt ON h.id = vt.huyen_id
                LEFT JOIN nongsan.xa x ON h.id = x.huyen_id
                WHERE h.id = %s
                GROUP BY h.id, h.ten_huyen, h.x, h.y, h.tinh_id, t.ten_tinh
            """, (feature_id,))
            
        elif layer == "communes":
            cur.execute("""
                SELECT 
                    x.id, x.ten_xa, x.x, x.y, x.huyen_id, h.ten_huyen,
                    h.tinh_id, t.ten_tinh,
                    COUNT(DISTINCT cs.id) as facilities,
                    COUNT(DISTINCT vt.id) as farms
                FROM nongsan.xa x
                LEFT JOIN nongsan.huyen h ON x.huyen_id = h.id
                LEFT JOIN nongsan.tinh t ON h.tinh_id = t.id
                LEFT JOIN nongsan.co_so cs ON x.id = cs.xa_id
                LEFT JOIN nongsan.vung_trong vt ON x.id = vt.xa_id
                WHERE x.id = %s
                GROUP BY x.id, x.ten_xa, x.x, x.y, x.huyen_id, h.ten_huyen, h.tinh_id, t.ten_tinh
            """, (feature_id,))
            
        elif layer == "farms":
            cur.execute("""
                SELECT 
                    vt.id, vt.ma_vung, vt.ten_vung, vt.dien_tich,
                    vt.tinh_id, t.ten_tinh,
                    tch.ten_to_chuc as chu_so_huu,
                    tt.ten_trang_thai as trang_thai,
                    STRING_AGG(DISTINCT lc.ten_cay, ', ') as crops
                FROM nongsan.vung_trong vt
                LEFT JOIN nongsan.tinh t ON vt.tinh_id = t.id
                LEFT JOIN nongsan.to_chuc_ca_nhan tch ON vt.chu_so_huu_id = tch.id
                LEFT JOIN nongsan.trang_thai_vung tt ON vt.trang_thai_id = tt.id
                LEFT JOIN nongsan.vung_cay_trong vct ON vt.id = vct.vung_trong_id
                LEFT JOIN nongsan.loai_cay lc ON vct.loai_cay_id = lc.id
                WHERE vt.id = %s
                GROUP BY vt.id, vt.ma_vung, vt.ten_vung, vt.dien_tich, vt.tinh_id, 
                         t.ten_tinh, tch.ten_to_chuc, tt.ten_trang_thai
            """, (feature_id,))
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown layer: {layer}")
        
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Feature not found: {layer}/{feature_id}")
        
        # Build response based on layer
        columns = [desc[0] for desc in cur.description]
        result = dict(zip(columns, row))
        
        cur.close()
        conn.close()
        
        return {
            "layer": layer,
            "feature_id": feature_id,
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
