import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8888))
client.send("I am CLIENT\n".encode('utf-8'))
from_server = client.recv(4096)
client.close()
print(from_server.decode('utf-8'))
