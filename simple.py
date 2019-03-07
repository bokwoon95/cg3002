import serial
import struct
import time
import csv

# ser = serial.Serial("/dev/serial1", 115200, timeout=1, bytesize=8, parity='N', stopbits=1)

IMU_PACKET_SIZE = 15
POWER_PACKET_SIZE = 8

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
DATA_P = b'\x04'

handshake_done = False


def handshake(handshake_flag):
    "Handshake Between Rasberry Pi and Arduino"
    def sanitize_byte(bt):
        "converts b'1' -> b'\x01'"
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


def getIMUPacket():
    ser.write(DATA_R)  # Request for arduino to send data over
    startByte = ser.read().decode("utf-8")
    if (startByte == 'S'):
        dataBytes = ser.read(IMU_PACKET_SIZE)
        endByte = ser.read().decode("utf-8")
        if (endByte == 'E'):
            unpacked_data = struct.unpack('<bHHHHHHH', dataBytes)
            print(unpacked_data)
    return unpacked_data

def getPowerPacket():
    ser.write(DATA_P)  # Request for arduino to send data over
    startByte = ser.read().decode("utf-8")
    if (startByte == 'S'):
        dataBytes = ser.read(POWER_PACKET_SIZE)
        endByte = ser.read().decode("utf-8")
        if (endByte == 'E'):
            unpacked_data = struct.unpack('<HHHH', dataBytes)
            print(unpacked_data)

def getData(label, duration):
        arr_2d = []
        curr_time = time.time()
        while (time.time() - curr_time < duration):
                lst = list(getIMUPacket())
                lst.append(label)
                arr_2d.append(lst)
        return arr_2d

getIMUPacket()
getPowerPacket()
