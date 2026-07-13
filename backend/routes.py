from flask import Blueprint, jsonify, request, render_template, send_from_directory
from models import db, Railway, Station, WarningDevice, Alert
from socket_events import socketio
import os
import json

api = Blueprint('api', __name__)
web = Blueprint('web', __name__)

# --- WEB ROUTES (Giao diện) ---
@web.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

# --- API ROUTES (Cung cấp dữ liệu) ---
from sqlalchemy import func

@api.route('/api/railways', methods=['GET'])
def get_railways():
    railways = db.session.query(Railway.id, Railway.name, func.ST_AsGeoJSON(Railway.geom).label('geom')).all()
    features = []
    for r in railways:
        features.append({
            "type": "Feature",
            "properties": {"id": r.id, "name": r.name},
            "geometry": json.loads(r.geom) if r.geom else None
        })
    return jsonify({"type": "FeatureCollection", "features": features})

@api.route('/api/stations', methods=['GET'])
def get_stations():
    stations = db.session.query(Station.id, Station.name, func.ST_AsGeoJSON(Station.geom).label('geom')).all()
    features = []
    for s in stations:
        features.append({
            "type": "Feature",
            "properties": {"id": s.id, "name": s.name},
            "geometry": json.loads(s.geom) if s.geom else None
        })
    return jsonify({"type": "FeatureCollection", "features": features})

@api.route('/api/devices', methods=['GET'])
def get_devices():
    devices = db.session.query(WarningDevice.id, WarningDevice.name, WarningDevice.type, func.ST_AsGeoJSON(WarningDevice.geom).label('geom')).all()
    features = []
    for d in devices:
        features.append({
            "type": "Feature",
            "properties": {"id": d.id, "name": d.name, "type": d.type},
            "geometry": json.loads(d.geom) if d.geom else None
        })
    return jsonify({"type": "FeatureCollection", "features": features})

@api.route('/api/alerts', methods=['GET'])
def get_alerts():
    try:
        alerts = Alert.query.order_by(Alert.created_at.desc()).all()
        return jsonify([a.to_dict() for a in alerts])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/api/alerts', methods=['POST'])
def create_alert():
    try:
        data = request.json
        new_alert = Alert(
            device_id=data.get('device_id'),
            alert_type=data.get('alert_type'),
            severity=data.get('severity'),
            description=data.get('description', '')
        )
        db.session.add(new_alert)
        db.session.commit()
        
        alert_data = new_alert.to_dict()
        # Gửi sự kiện realtime tới tất cả client đang kết nối
        socketio.emit('new_alert', alert_data)
        
        return jsonify(alert_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/api/alerts/<int:id>', methods=['PUT'])
def update_alert(id):
    try:
        alert = Alert.query.get_or_404(id)
        data = request.json
        if 'status' in data:
            alert.status = data['status']
        db.session.commit()
        return jsonify(alert.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/api/alerts/<int:id>', methods=['DELETE'])
def delete_alert(id):
    try:
        alert = Alert.query.get_or_404(id)
        db.session.delete(alert)
        db.session.commit()
        return jsonify({"message": "Đã xóa thành công"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
