CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE railways (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    geom geometry(LineString, 4326)
);

CREATE TABLE stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    geom geometry(Point, 4326)
);

CREATE TABLE warning_devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    geom geometry(Point, 4326)
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    device_id INTEGER REFERENCES warning_devices(id),
    alert_type VARCHAR(100),
    severity VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Mới',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dữ liệu Tuyến phía Bắc
INSERT INTO railways (name, geom) VALUES
('Tuyến Hà Nội - Lào Cai', ST_GeomFromText('LINESTRING(105.84 21.02, 105.32 21.32, 104.97 21.70, 103.97 22.48)', 4326)),
('Tuyến Hà Nội - Hải Phòng', ST_GeomFromText('LINESTRING(105.84 21.02, 106.18 20.93, 106.68 20.85)', 4326)),
('Tuyến Hà Nội - Đồng Đăng', ST_GeomFromText('LINESTRING(105.84 21.02, 106.02 21.18, 106.27 21.60, 106.70 21.93)', 4326));

-- Dữ liệu Ga phía Bắc
INSERT INTO stations (name, geom) VALUES
('Ga Hà Nội', ST_GeomFromText('POINT(105.84117 21.0245)', 4326)),
('Ga Long Biên', ST_GeomFromText('POINT(105.848 21.040)', 4326)),
('Ga Gia Lâm', ST_GeomFromText('POINT(105.875 21.050)', 4326)),
('Ga Đông Anh', ST_GeomFromText('POINT(105.86 21.14)', 4326)),
('Ga Vĩnh Yên', ST_GeomFromText('POINT(105.59 21.31)', 4326)),
('Ga Việt Trì', ST_GeomFromText('POINT(105.43 21.29)', 4326)),
('Ga Phú Thọ', ST_GeomFromText('POINT(105.21 21.37)', 4326)),
('Ga Yên Bái', ST_GeomFromText('POINT(104.97 21.70)', 4326)),
('Ga Lào Cai', ST_GeomFromText('POINT(103.977 22.485)', 4326)),
('Ga Cẩm Giàng', ST_GeomFromText('POINT(106.21 20.94)', 4326)),
('Ga Hải Dương', ST_GeomFromText('POINT(106.31 20.94)', 4326)),
('Ga Phú Thái', ST_GeomFromText('POINT(106.49 20.92)', 4326)),
('Ga Thượng Lý', ST_GeomFromText('POINT(106.65 20.86)', 4326)),
('Ga Hải Phòng', ST_GeomFromText('POINT(106.682 20.858)', 4326)),
('Ga Bắc Ninh', ST_GeomFromText('POINT(106.05 21.18)', 4326)),
('Ga Bắc Giang', ST_GeomFromText('POINT(106.19 21.27)', 4326)),
('Ga Kép', ST_GeomFromText('POINT(106.28 21.41)', 4326)),
('Ga Lạng Sơn', ST_GeomFromText('POINT(106.75 21.84)', 4326)),
('Ga Đồng Đăng', ST_GeomFromText('POINT(106.703 21.935)', 4326));

-- Thiết bị dọc tuyến phía Bắc
INSERT INTO warning_devices (name, type, geom) VALUES
('Cảm biến sạt lở Yên Bái', 'Sạt lở', ST_GeomFromText('POINT(104.97 21.70)', 4326)),
('Cảm biến ngập lụt Hải Dương', 'Ngập lụt', ST_GeomFromText('POINT(106.31 20.93)', 4326)),
('Camera chắn tàu Bắc Giang', 'Camera', ST_GeomFromText('POINT(106.19 21.27)', 4326)),
('Thiết bị rào chắn Vĩnh Yên', 'Vật cản', ST_GeomFromText('POINT(105.59 21.31)', 4326)),
('Cảm biến lún đường ray Gia Lâm', 'Sụt lún', ST_GeomFromText('POINT(105.875 21.050)', 4326)),
('Cảm biến ngập lụt Lạng Sơn', 'Ngập lụt', ST_GeomFromText('POINT(106.75 21.84)', 4326)),
('Camera đường ngang Đông Anh', 'Camera', ST_GeomFromText('POINT(105.86 21.14)', 4326));

INSERT INTO alerts (device_id, alert_type, severity, description) VALUES
(2, 'Ngập lụt đường ray', 'Cao', 'Nước ngập trên 20cm tại Km12+300'),
(4, 'Sạt lở đất đá', 'Nghiêm trọng', 'Khối lượng lớn đất đá chắn ngang đường ray'),
(8, 'Lún nền đường', 'Cao', 'Phát hiện lún sụt bất thường 5cm');

-- Tự động nắn chỉnh (snap) tất cả các nhà ga và thiết bị cảnh báo 
-- bám chính xác vào đường ray gần nhất để hiển thị chuẩn trên bản đồ
UPDATE stations SET geom = (SELECT ST_ClosestPoint(r.geom, stations.geom) FROM railways r ORDER BY ST_Distance(r.geom, stations.geom) LIMIT 1);
UPDATE warning_devices SET geom = (SELECT ST_ClosestPoint(r.geom, warning_devices.geom) FROM railways r ORDER BY ST_Distance(r.geom, warning_devices.geom) LIMIT 1);
