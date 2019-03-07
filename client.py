import socket
from Crypto.Cipher import AES
from Crypto import Random
import base64
import time
import sys


def decryptText(b64ascii, secret_key):
    # decrypt base64 ascii into byte array
    bytearr = base64.b64decode(b64ascii)
    # Extract initialization vector iv (first 16 bytes) from byte array
    iv = bytearr[0:16]
    # Initialize cipher with secret_key and iv
    cipher = AES.new(secret_key.encode('utf-8'), AES.MODE_CBC, iv)
    # Decrypt string
    decryptedString = cipher.decrypt(bytearr[16:]).decode('utf-8')
    # Get the rest of the string after the first '#' character and split by '|'
    values = decryptedString[decryptedString.find('#') + 1:].split('|')
    return {'action': values[0], 'voltage': values[1], 'current': values[2], 'power': values[3], 'cumpower': values[4]}


def encryptText(dictt, secret_key):
    def pad(s):
        "pads string to a multiple of 16 chars"
        return s.rjust(len(s) + 16 - len(s) % 16, "0")
    strarray = list(map(str, dictt.values()))
    payload = pad("#" + "|".join(strarray) + "|")
    # Generate random 16 byte initialization vector
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(secret_key.encode('utf-8'), AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(payload))


if len(sys.argv) != 4:
    print('Invalid number of arguments')
    print('python server.py [IP address] [Port] [groupID]')
    sys.exit()
ip_addr = sys.argv[1]
port_num = int(sys.argv[2])
groupID = sys.argv[3]
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip_addr, port_num))
strr = encryptText({'action': "chicken", 'voltage': 0, 'current': 0, 'power': 0, 'cumpower': 0}, "0123456789ABCDEF")
time.sleep(60)
client.send(strr)
# from_server = client.recv(4096)
# print(from_server.decode('utf-8'))
client.close()
