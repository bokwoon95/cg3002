import serial
import struct
import time

# ser = serial.Serial("/dev/serial1", 115200, timeout=1, bytesize=8, parity='N', stopbits=1)

PACKET_SIZE = 12

ser = serial.Serial(
    port='/dev/serial0',  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


# Declare Global Variables

# Hand Shake
ACK = b'\x00'
SYN = b'\x01'
SYN_ACK = b'\x02'
SYN_ACK_int = int.from_bytes(SYN_ACK, byteorder='big', signed=True)
DATA_R = b'\x03'

handshake_done = False

# Handshake Beteen Rasberry Pi and Arduino


def handshake(handshake_flag):
    while handshake_flag:
        time.sleep(1)
        ser.write(SYN)  # Request for handshake to start
        string = ser.read()
        reply = int.from_bytes(string, byteorder='big', signed=True) - 48
        print(type(reply))
        print(str(SYN_ACK_int))
        print(type(string))
        print(str(string))
        print(type(SYN_ACK))
        print(str(SYN_ACK))
        print(string == SYN_ACK)
        if (reply == SYN_ACK_int):
            handshake_flag = False
            ser.write(ACK)
    print('Handshake completed')


handshake(not handshake_done)


def getPacket():
    ser.write(DATA_R)  # Request for arduino to send data over
    startByte = ser.read().decode("utf-8")
    if (startByte == 'S'):
        dataBytes = ser.read(PACKET_SIZE)
        endByte = ser.read().decode("utf-8")
        if (endByte == 'E'):
            print(dataBytes)
            unpacked_data = struct.unpack('<HHHHHH', dataBytes)
            print(unpacked_data)


getPacket()
