from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
import json
from datetime import datetime

db = SQLAlchemy()

class Railway(db.Model):
    __tablename__ = 'railways'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    geom = db.Column(Geometry(geometry_type='LINESTRING', srid=4326))

    def to_geojson(self):
        shape = to_shape(self.geom)
        return {
            "type": "Feature",
            "properties": {"id": self.id, "name": self.name},
            "geometry": shape.__geo_interface__
        }

class Station(db.Model):
    __tablename__ = 'stations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    def to_geojson(self):
        shape = to_shape(self.geom)
        return {
            "type": "Feature",
            "properties": {"id": self.id, "name": self.name},
            "geometry": shape.__geo_interface__
        }

class WarningDevice(db.Model):
    __tablename__ = 'warning_devices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100))
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))

    def to_geojson(self):
        shape = to_shape(self.geom)
        return {
            "type": "Feature",
            "properties": {"id": self.id, "name": self.name, "type": self.type},
            "geometry": shape.__geo_interface__
        }

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('warning_devices.id'))
    alert_type = db.Column(db.String(100))
    severity = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Mới')
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    device = db.relationship('WarningDevice', backref='alerts')

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_name": self.device.name if self.device else "Không xác định",
            "alert_type": self.alert_type,
            "severity": self.severity,
            "status": self.status,
            "description": self.description,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
