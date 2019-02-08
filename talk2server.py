import os
import sys
import socket
import threading
from Crypto.Cipher import AES

class RpiServer(threading.Thread):
    def __init__(self, ip_addr, port_num):
        threading.Thread.__init__(self)
        self.shutdown = threading.Event()
        # init server
        # self.auth = server_auth()
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the port
        server_address = (ip_addr, port_num)
        print('starting up on %s port %s' % server_address, file=sys.stderr)
        self.sock.bind(server_address)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Invalid number of arguments')
        print('python server.py [IP address] [Port] [groupID]')
        sys.exit()
    ip_addr = sys.argv[1]
    port_num = int(sys.argv[2])
    groupID = sys.argv[3]
    # my_server = RpiServer(ip_addr, port_num)
    # my_server.start()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))
    client.send("I am CLIENT\n")
    from_server = client.recv(4096)
