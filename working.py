import serial
import struct
import time
import csv
import binascii

# ser = serial.Serial("/dev/serial1", 115200, timeout=1, bytesize=8, parity='N', stopbits=1)

IMU_PACKET_SIZE = 40
POWER_PACKET_SIZE = 8

ser = serial.Serial(
    port='/dev/serial0',  # Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
    baudrate=38400,
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
EMPTY = b'\x05'

handshake_done = False


def handshake():
    "Handshake Between Rasberry Pi and Arduino"
    global handshake_done

    print('Handshake started')

    def sanitize_byte(bt):
        "converts b'1' -> b'\x01'"
        return bytes.fromhex(bt.decode('utf-8').rjust(2, '0'))

    while True:
        time.sleep(1)
        ser.write(SYN)  # Request for handshake to start
        val = ser.read()
        if sanitize_byte(val) == SYN_ACK:
            ser.write(ACK)
            handshake_done = True
            break
    print('Handshake completed')


handshake()


def getIMUPacket():
    unpacked_data = None
    ser.write(DATA_R)  # Request for arduino to send data over
    rawData = ser.read() 
    if (rawData == EMPTY):
        print("Empty Buffer")
        return None
    startByte = rawData.decode("utf-8")
    if startByte == 'S':
        dataBytes = ser.read(IMU_PACKET_SIZE)
        endByte = ser.read().decode("utf-8")
        if endByte == 'E':
            unpacked_data = struct.unpack('<hhhhhhhhhhhhhhhhhhI', dataBytes)
            # print(unpacked_data)
            #import pdb; pdb.set_trace(
            print("Received 'E'")
        else:
            print("Did not receive 'E' byte")
    return unpacked_data


def getPowerPacket():
    unpacked_data = None
    ser.write(DATA_P)  # Request for arduino to send data over
    startByte = ser.read().decode("utf-8")
    if startByte == 'S':
        dataBytes = ser.read(POWER_PACKET_SIZE)
        endByte = ser.read().decode("utf-8")
        if endByte == 'E':
            unpacked_data = struct.unpack('<HHHH', dataBytes)
            # print(unpacked_data)
    return unpacked_data


def getData(label, duration):
    dataCount = 0
    errCount = 0
    print("Collecting data for move %s for %d seconds" % (label, duration))
    arr_2d = []
    curr_time = time.time()
    while time.time() - curr_time < duration:
        packet = getIMUPacket()
        print(packet)
        if packet is not None:
            lst = list(packet)
            lst.insert(0, label)
            lst.pop(len(lst) - 1)
            arr_2d.append(lst)
            #time.sleep(5 / 1000)
        else:
            print("packet received is None")
            errCount += 1
        
        dataCount += 1
        #with open('training.csv', 'a') as fd:
        #    csv.writer(fd).writerows(arr_2d)
    print("Err/Data: %d/%d" % (errCount, dataCount))
    return arr_2d

sensordata = getIMUPacket()
powerdata  = getPowerPacket()

print("Sensor data: " + str(sensordata))
print("Power data: " + str(powerdata))


sensordata = getData("Doublepump", 60)

with open('data.csv', 'a') as fd:
    sensordata = ("no data") if sensordata is None else sensordata
    csv.writer(fd).writerows(sensordata)
