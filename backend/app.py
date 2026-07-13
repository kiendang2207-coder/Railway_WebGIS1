from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()

from config import Config
from models import db
from routes import api, web
from socket_events import socketio

def create_app():
    # Cấu hình Flask để tìm file HTML ở thư mục frontend
    template_dir = os.path.abspath('../frontend')
    app = Flask(__name__, template_folder=template_dir)
    app.config.from_object(Config)
    
    # Cho phép gọi API từ nhiều nguồn (Cross-Origin)
    CORS(app)
    
    # Khởi tạo Database
    db.init_app(app)
    
    # Đăng ký các routes
    app.register_blueprint(api)
    app.register_blueprint(web)
    
    # Khởi tạo WebSocket
    socketio.init_app(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Server đang khởi động tại http://localhost:5000 ...")
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
