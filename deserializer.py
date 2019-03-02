
import serial

import time

# ser = serial.Serial("/dev/serial1", 115200, timeout=1, bytesize=8, parity='N', stopbits=1)


ser = serial.Serial(
        port='/dev/serial0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 115200,
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

handshake_done = False

# Handshake Beteen Rasberry Pi and Arduino

# Return: None

def handshake(handshake_flag):

    while handshake_flag:
        # print("waiting")
        time.sleep(1)

        ser.write(SYN)

        string = ser.read()
        
        reply = int.from_bytes(string, byteorder='big', signed=True) - 48
        
        print(str(reply))
        print(str(SYN_ACK_int))

        if (reply == SYN_ACK_int):

            handshake_flag = False

            ser.write(ACK)

            print('Handshake completed')

handshake(not handshake_done)