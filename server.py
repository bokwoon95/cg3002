import socket
from Crypto.Cipher import AES
from Crypto import Random
import base64


def betterDecryptText(b64ascii, secret_key):
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


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 8888))
serv.listen(5)

while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        data = conn.recv(4096)
        try:
            decodedmsg = betterDecryptText(data.decode('utf-8'), "0123456789ABCDEF")
            print(decodedmsg)
        except Exception:
            break
        conn.send("I RECEIVED YOUR MESSAGE\n".encode('utf-8'))
    conn.close()
    print('client disconnected')
