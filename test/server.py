import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 8888))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data: break
        data = data.decode('utf-8')
        from_client += data
        print(from_client)
        conn.send("I am SERVER\n".encode('utf-8'))
    conn.close()
    print('client disconnected')
