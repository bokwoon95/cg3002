import time
import csv
import os
import numpy as np
import pandas as pd
import serial
import struct


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


def save_training_data(file_name, data, reset=False):
    if reset:
        os.remove(file_name)
    file_exists = os.path.isfile(file_name)
    if file_exists:
        with open(file_name, 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(data)
    else:
        with open(file_name, 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(data)
    csvFile.close()


def get_training_data(file_path, columns):
    """ This methods splits the label & data given a
        csv file utilising with the following format
        label, accX, accY, accZ, gyroX, gyroY, gyroZ ...
    """
    data_arr = np.genfromtxt(file_path, delimiter=',')

    df = pd.DataFrame(data_arr, columns=columns)
    labels = df['labels'].values
    data = df.drop(['labels'], axis=1).values
    return labels, data


def getIMUData():
    """ This method returns an 18 value array for the IMU data
    """
    unpacked_data = None
    ser.write(DATA_R)  # Request for arduino to send data over
    startByte = ser.read().decode("utf-8")
    if startByte == 'S':
        dataBytes = ser.read(IMU_PACKET_SIZE)
        endByte = ser.read().decode("utf-8")
        if endByte == 'E':
            unpacked_data = struct.unpack('<hhhhhhhhhhhhhhhhhhh', dataBytes)
    return list(unpacked_data)


def main():

    while True:
        TIME = 10
        filename = input("Enter the filename: ")
        filename = filename + '.csv'
        label = int(input("Enter the label: "))
        label = np.reshape(label, (1, 1))
        t_end = time.time() + TIME
        while time.time() < t_end:
            raw_data = getIMUData()
            raw_data = np.hstack((label, raw_data))
            save_training_data(filename, raw_data)
        print('Collection complete')


if __name__ == '__main__':
    main()
