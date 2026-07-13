import requests
import time
import random

# URL của API nhận cảnh báo
API_URL = "http://localhost:5000/api/alerts"

# ID của thiết bị# Danh sách ID của các thiết bị có trong CSDL
DEVICE_IDS = [1, 2, 3, 4, 5, 6, 7] 
ALERT_TYPES = ["Sạt lở đất", "Ngập lụt đường ray", "Tàu kẹt ở hầm", "Vượt ẩu đường ngang", "Cây đổ trên đường ray"]
SEVERITIES = ["Thấp", "Trung bình", "Cao", "Nghiêm trọng"]

def send_mock_alert():
    data = {
        "device_id": random.choice(DEVICE_IDS),
        "alert_type": random.choice(ALERT_TYPES),
        "severity": random.choice(SEVERITIES),
        "description": "Cảnh báo tự động tạo ra từ hệ thống mô phỏng (Test)."
    }
    
    try:
        # Gửi request dạng POST giống như form Submit
        response = requests.post(API_URL, json=data)
        if response.status_code == 201:
            print(f"[{time.strftime('%H:%M:%S')}] ✅ Đã gửi cảnh báo: {data['alert_type']} - Mức độ: {data['severity']}")
        else:
            print(f"❌ Lỗi khi gửi cảnh báo: {response.text}")
    except Exception as e:
        print(f"⚠️ Không thể kết nối đến server (Server Flask đã chạy chưa?): {e}")

if __name__ == "__main__":
    print("========================================")
    print("🚂 BẮT ĐẦU MÔ PHỎNG GỬI CẢNH BÁO ĐƯỜNG SẮT")
    print("Nhấn Ctrl+C để dừng lại.")
    print("========================================")
    
    try:
        while True:
            send_mock_alert()
            # Ngủ 5-10 giây rồi lặp lại
            delay = random.randint(5, 10)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng script mô phỏng.")
