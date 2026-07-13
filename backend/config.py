import os

class Config:
    # Lấy thông tin kết nối từ biến môi trường
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+pg8000://postgres:Kiendang2207%40@localhost:5432/railway_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret-key-do-an')
