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
    # Get everything after the first '#' character
    decryptedString_subslice = decryptedString[decryptedString.find('#') + 1:]
    action = decryptedString_subslice.split('|')[0]
    voltage = decryptedString_subslice.split('|')[1]
    current = decryptedString_subslice.split('|')[2]
    power = decryptedString_subslice.split('|')[3]
    cumpower = decryptedString_subslice.split('|')[4]
    return {'action': action, 'voltage': voltage, 'current': current, 'power': power, 'cumpower': cumpower}


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
