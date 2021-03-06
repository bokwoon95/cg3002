import time
import datetime
import csv
import os
import numpy as np
import pandas as pd
from comms.communications import Communicate
import sys
import uuid

def save_training_data(file_name, data, label, reset=False):
    if reset:
        os.remove(file_name)
    file_exists = os.path.isfile(file_name)
    if file_exists:
        print('ERROR, FILE ALREADY EXISTS')
   
    with open(file_name, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for d in data:
            d= list(d)
            d.insert(0,label)
            writer.writerow(d)
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


def main():
    if len(sys.argv) != 2:
        print('Invalid number of arguments')
        print('python3 data_collect.py [IP address]')
        sys.exit()
    IP_ADDR = sys.argv[1]
    comm = Communicate(IP_ADDR)
    comm.get_handshake()
    while True:
        if comm.has_handshake():
            label = input("Enter the label: ")
            timenow = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', label + '_' + timenow + '.csv')
            raw_data = comm.getData(duration=10)
            print("len of raw data is %d" % len(raw_data))
            save_training_data(filename, raw_data, label)
            print('Collection complete')
        else:
            print('Handshake broken')

if __name__ == '__main__':
    main()
