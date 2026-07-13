# Railway WebGIS Monitoring System

Hệ thống cảnh báo và quản lý đường sắt trực tuyến sử dụng công nghệ Bản đồ số (WebGIS).
Đồ án tập trung vào việc số hóa hạ tầng mạng lưới đường sắt (nhà ga, đường ray) và cảnh báo các sự cố khẩn cấp (cháy nổ, sạt lở) theo thời gian thực (Real-time).

## Công nghệ sử dụng
- **Frontend:** HTML, CSS, JavaScript, LeafletJS (WebGIS).
- **Backend:** Python, Flask, Flask-SocketIO (WebSockets).
- **Cơ sở dữ liệu:** PostgreSQL kết hợp thư viện không gian PostGIS (GeoAlchemy2).
- **Mô phỏng (Simulator):** Script Python tự động sinh các cảnh báo sự cố IoT.

## Cấu trúc thư mục
- `/backend/`: Chứa mã nguồn máy chủ API và WebSockets.
  - `app.py`: Khởi chạy Web Server Flask.
  - `routes.py`: Xử lý API cấp phát dữ liệu bản đồ.
  - `socket_events.py`: Truyền tải tín hiệu khẩn cấp thời gian thực.
  - `simulate_alert.py`: Công cụ giả lập cảnh báo.
- `/frontend/`: Chứa giao diện người dùng Web.
  - `index.html`: Bản đồ số theo dõi toàn hệ thống.
  - `admin.html`: Bảng điều khiển quản lý lịch sử sự cố.
- `/database/`: Chứa các script SQL khởi tạo.
  - `init_db.sql`: Dữ liệu không gian (tọa độ các nhà ga phía Bắc).

## Hướng dẫn Cài đặt & Chạy dự án

### 1. Yêu cầu hệ thống
- Python 3.8+
- PostgreSQL cài sẵn Extension PostGIS.

### 2. Thiết lập cơ sở dữ liệu
Bạn có thể tự chạy file `database/init_db.sql` trong pgAdmin4, hoặc chạy script tự động bằng Python:
```bash
python setup_db.py
```

### 3. Cài đặt thư viện Backend
Vào thư mục `backend` và cài các gói thư viện:
```bash
cd backend
pip install -r requirements.txt
```

### 4. Khởi chạy hệ thống
Mở 2 Terminal (Cmd/PowerShell) riêng biệt:

**Terminal 1 (Chạy Máy chủ Web):**
```bash
cd backend
python app.py
```
*(Truy cập `http://localhost:5000` để xem bản đồ và `http://localhost:5000/admin` để xem trang quản trị).*

**Terminal 2 (Chạy bộ giả lập phát cảnh báo sự cố):**
```bash
cd backend
python simulate_alert.py
```

**Tác giả:** Đặng Trung Kiên (MSSV: 20233473)
**Trường:** Đại học Bách Khoa Hà Nội - Viện Điện - Điện tử.
