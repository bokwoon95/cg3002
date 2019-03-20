import serial
import struct
import time
import csv

IMU_PACKET_SIZE = 38
POWER_PACKET_SIZE = 8

# Hand Shake
ACK = b'\x00'
SYN = b'\x01'
SYN_ACK = b'\x02'
DATA_R = b'\x03'
DATA_P = b'\x04'

class Communicate:
    def __init__(self):
        self.serial = serial.Serial(
                port='/dev/serial0',  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        self.handshake_done = False

    def get_handshake(self):
        def sanitize_byte(bt):
            "converts b'1' -> b'\x01'"
            return bytes.fromhex(bt.decode('utf-8').rjust(2, '0'))

        while True:
            time.sleep(1)
            self.serial.write(SYN)  # Request for handshake to start
            val = self.serial.read()
            if sanitize_byte(val) == SYN_ACK:
                self.serial.write(ACK)
                self.handshake_done = True
                break
        print('Handshake completed')

    def has_handshake(self):
        return self.handshake_done

    def getIMUPacket(self):
        """ Returns a list of len 19 """
        unpacked_data = None
        self.serial.write(DATA_R)  # Request for arduino to send data over
        startByte = self.serial.read().decode("utf-8")
        if startByte == 'S':
            dataBytes = self.serial.read(IMU_PACKET_SIZE)
            endByte = self.serial.read().decode("utf-8")
            if endByte == 'E':
                unpacked_data = struct.unpack('<hhhhhhhhhhhhhhhhhhh', dataBytes)
                # print(unpacked_data)
        return unpacked_data

    def getPowerPacket(self):
        unpacked_data = None
        self.serial.write(DATA_P)  # Request for arduino to send data over
        startByte = self.serial.read().decode("utf-8")
        if startByte == 'S':
            dataBytes = self.serial.read(POWER_PACKET_SIZE)
            endByte = self.serial.read().decode("utf-8")
            if endByte == 'E':
                unpacked_data = struct.unpack('<HHHH', dataBytes)
                # print(unpacked_data)
        return unpacked_data

    def getData(self, duration=1000):
        """ Duration in seconds """
        window_data = []
        curr_time = time.time()
        while time.time() - curr_time < duration:
            window_data.append(self.getIMUPacket())
        return window_data
        