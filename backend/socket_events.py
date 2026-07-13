from flask_socketio import SocketIO, emit

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")

@socketio.on('connect')
def handle_connect():
    print("Một client (trình duyệt) vừa kết nối thành công.")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client đã ngắt kết nối.")
