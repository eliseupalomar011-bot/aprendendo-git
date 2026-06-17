import socket
import json

HOST = "127.0.0.1"
PORT = 9090


def start_ipc(handler):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"📡 Trinity IPC running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        data = conn.recv(4096).decode()

        try:
            request = json.loads(data)
            response = handler(request)
        except Exception as e:
            response = {"error": str(e)}

        conn.send(json.dumps(response).encode())
        conn.close()
