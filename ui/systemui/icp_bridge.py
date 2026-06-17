import socket
import json

HOST = "127.0.0.1"
PORT = 9090


def ipc_call(payload):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.send(json.dumps(payload).encode())
    data = client.recv(4096).decode()
    client.close()
    return json.loads(data)
