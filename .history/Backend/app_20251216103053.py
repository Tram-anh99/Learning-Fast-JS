"""
========== FastAPI Backend Application ==========
Purpose: API server cho ứng dụng nông nghiệp
Author: Learning-Fast-JS
Date: 2025-12-16
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for Frontend connection
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# ========== API ROUTES ==========

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Backend API is running",
        "version": "1.0.0"
    })


@app.route('/api/charts/export-markets', methods=['GET'])
def get_export_markets():
    """
    Lấy dữ liệu thị trường xuất khẩu
    Returns: JSON data for export market chart
    """
    data = {
        "labels": ["Trung Quốc", "Hoa Kỳ", "Nhật Bản", "Hàn Quốc", "EU"],
        "datasets": [{
            "data": [35, 25, 18, 12, 10],
            "backgroundColor": [
                "#FF6384",
                "#36A2EB", 
                "#FFCE56",
                "#4BC0C0",
                "#9966FF"
            ]
        }]
    }
    return jsonify(data)


@app.route('/api/charts/crop-production', methods=['GET'])
def get_crop_production():
    """
    Lấy dữ liệu sản lượng cây trồng
    Returns: JSON data for crop production chart
    """
    data = {
        "labels": ["Xoài", "Thanh Long", "Nhãn", "Vải", "Chôm Chôm"],
        "datasets": [{
            "label": "Sản lượng (tấn)",
            "data": [450, 380, 320, 280, 150],
            "backgroundColor": "#10b981"
        }]
    }
    return jsonify(data)


@app.route('/api/charts/productivity-trend', methods=['GET'])
def get_productivity_trend():
    """
    Lấy dữ liệu xu hướng năng suất
    Returns: JSON data for productivity trend chart
    """
    data = {
        "labels": ["2020", "2021", "2022", "2023", "2024"],
        "datasets": [{
            "label": "Năng suất (tạ/ha)",
            "data": [38.5, 41.2, 43.8, 45.5, 47.2],
            "borderColor": "#3b82f6",
            "tension": 0.4
        }]
    }
    return jsonify(data)


@app.route('/api/farms', methods=['GET'])
def get_farms():
    """
    Lấy danh sách vùng trồng
    Returns: List of farm areas
    """
    # TODO: Kết nối database và query dữ liệu thực
    farms = []
    return jsonify(farms)


@app.route('/api/diary', methods=['GET', 'POST'])
def handle_diary():
    """
    GET: Lấy danh sách nhật ký
    POST: Tạo nhật ký mới
    """
    if request.method == 'GET':
        # TODO: Lấy từ database
        return jsonify([])
    
    elif request.method == 'POST':
        data = request.json
        # TODO: Lưu vào database
        return jsonify({
            "success": True,
            "message": "Đã lưu nhật ký thành công",
            "data": data
        }), 201


# ========== ERROR HANDLERS ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Not Found",
        "message": "Endpoint không tồn tại"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal Server Error", 
        "message": "Lỗi server"
    }), 500


# ========== RUN APPLICATION ==========

if __name__ == '__main__':
    print("🚀 Starting Backend API Server...")
    print("📡 API running at: http://localhost:5000")
    print("🔗 Frontend should connect to: http://localhost:5000/api/...")
    app.run(debug=True, host='0.0.0.0', port=5000)
