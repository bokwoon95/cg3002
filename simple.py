import serial
import struct
import time
import csv

# ser = serial.Serial("/dev/serial1", 115200, timeout=1, bytesize=8, parity='N', stopbits=1)

PACKET_SIZE = 12 * 3

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
DATA_R = b'\x03'

handshake_done = False
#Q what is handshake_done for?


def handshake(handshake_flag):
    "Handshake Between Rasberry Pi and Arduino"
    def sanitize_byte(bt):
        "converts b'1' -> b'x01'"
        return bytes.fromhex(bt.decode('utf-8').rjust(2,'0'))
    while handshake_flag:
        time.sleep(1)
        ser.write(SYN)  # Request for handshake to start
        val = ser.read()
        if (sanitize_byte(val) == SYN_ACK):
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
            unpacked_data = struct.unpack('<HHHHHHHHHHHHHHHHHH', dataBytes)
            print(unpacked_data)
    return unpacked_data


data = getPacket()
with open('data.csv','a') as fd:
    csv.writer(fd).writerow(list(data))
