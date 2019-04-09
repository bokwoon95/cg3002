import serial
from Crypto.Cipher import AES
from Crypto import Random
import base64
import socket
import struct
import time
import csv
import binascii

IMU_PACKET_SIZE = 40
POWER_PACKET_SIZE = 8

# Hand Shake
ACK = b'\x00'
SYN = b'\x01'
SYN_ACK = b'\x02'
DATA_R = b'\x03'
DATA_P = b'\x04'
EMPTY = b'\x05'

class Communicate:
    def __init__(self, ip_addr='192.168.43.206', port_num=8888):
        self.serial = serial.Serial(
                port='/dev/serial0',  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
                baudrate=38400,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        if ip_addr != '-':
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((ip_addr, port_num))
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
        unpacked_data = None
        self.serial.write(DATA_R)  # Request for arduino to send data over
        rawData = self.serial.read() 
        if (rawData == EMPTY):
            print("Empty Buffer")
            return None
        startByte = rawData.decode("utf-8")
        if startByte == 'S':
            dataBytes = self.serial.read(IMU_PACKET_SIZE)
            endByte = self.serial.read().decode("utf-8")
            if endByte == 'E':
                unpacked_data = struct.unpack('<hhhhhhhhhhhhhhhhhhI', dataBytes)
                # print(unpacked_data)
                #import pdb; pdb.set_trace()
        # return unpacked_data, dataBytes[:-4]
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
        """ This method returns a list of IMU sensor data
            Duration in seconds """
            
        window_data = []
        curr_time = time.time()
        while time.time() - curr_time < duration:
            # packet, rawdata = self.getIMUPacket()
            packet = self.getIMUPacket()
            # if packet is not None && packet[-1] == binascii.crc32(rawdata):
            if packet is not None:
                if True: # ignore the checksum for now
                # if packet[-1] == binascii.crc32(rawdata):
                    window_data.append(packet)
                else:
                    print("--------------------------------------------------------------------------------")
                    print("checksum no match:")
                    print(packet[-1], checksum)
                    print(packet)
                    print("--------------------------------------------------------------------------------")
        return window_data

    def getData2(self, window=90):
        window_data = []
        for i in range(window):
            packet = self.getIMUPacket()
            done = False
            while not done:
                if packet is not None:
                    window_data.append(self.getIMUPacket())
                    done = True
                else:
                    packet = self.getIMUPacket()
        # print(window_data)
        return window_data

    def getData3(self, duration=1000):
      dataCount = 0
      errCount = 0
      print("Collecting data for %d seconds" % duration)
      arr_2d = []
      curr_time = time.time()
      while time.time() - curr_time < duration:
        packet = self.getIMUPacket()
        print(packet)
        if packet is not None:
           lst = list(packet)
           arr_2d.append(lst)
           #time.sleep(5 / 1000)
        else:
           print("packet received is None")
           errCount += 1 
        dataCount += 1
        #with open('training.csv', 'a') as fd:
        #    csv.writer(fd).writerows(arr_2d)
      print("Err/Data: %d/%d" % (errCount, dataCount))
      print("Freq: %d" % (dataCount / duration))
      return arr_2d


    def encryptText(self, listt, secret_key):
        def pad(s):
            "pads string to a multiple of 16 chars"
            return s.rjust(len(s) + 16 - len(s) % 16, "0")
        strarray = list(map(str, listt))
        payload = pad("#" + "|".join(strarray) + "|")
        # Generate random 16 byte initialization vector
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(secret_key.encode('utf-8'), AES.MODE_CBC, iv)
        print(payload)
        print("========================================")
        print()
        return base64.b64encode(iv + cipher.encrypt(payload))

    def sendData(self, action, voltage=0, current=0, power=0, cumpower=0, secret_key='0123456789ABCDEF'):
        """ Send data to the server """
        # dictionary = {
        #     'action': action, 
        #     'voltage': voltage,
        #     'current': current,
        #     'power': power,
        #     'cumpower': cumpower
        # }
        listt = [action, voltage, current, power, cumpower]
        encrypted_msg = self.encryptText(listt, secret_key)
        # time.sleep(60)
        self.client.send(encrypted_msg)
        # self.client.close()
