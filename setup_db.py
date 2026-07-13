import os
from sqlalchemy import create_engine, text

print("========================================")
print("Đang tự động cài đặt Cơ sở dữ liệu...")

# 1. Connect to postgres to create DB
try:
    engine1 = create_engine('postgresql+pg8000://postgres:Kiendang2207%40@localhost:5432/postgres', isolation_level="AUTOCOMMIT")
    with engine1.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS railway_db"))
        conn.execute(text("CREATE DATABASE railway_db"))
    print("✅ Đã tạo database railway_db thành công!")
except Exception as e:
    print(f"❌ Lỗi khi tạo DB: {e}")

# 2. Connect to railway_db to run init_db.sql
try:
    engine2 = create_engine('postgresql+pg8000://postgres:Kiendang2207%40@localhost:5432/railway_db')
    with engine2.begin() as conn:
        sql_path = os.path.join(os.path.dirname(__file__), 'database', 'init_db.sql')
        with open(sql_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        # Chạy từng lệnh SQL
        statements = sql.split(';')
        for statement in statements:
            stmt = statement.strip()
            if stmt:
                conn.execute(text(stmt))
    print("✅ Đã khởi tạo các bảng và dữ liệu mẫu xong!")
except Exception as e:
    print(f"❌ Lỗi khi khởi tạo bảng: {e}")
