import time
import csv
import os
import numpy as np
import pandas as pd
from comms.communications import Communicate

def save_training_data(file_name, data, label, reset=False):
    if reset:
        os.remove(file_name)
    file_exists = os.path.isfile(file_name)
    if not file_exists:
        with open(file_name, 'w') as csvFile:
            writer = csv.writer(csvFile)
            for d in data:
                d.insert(0,label)
                writer.writerow(d)
    else:
        print('ERROR, File already exists')
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
    comm = Communicate()
    comm.get_handshake()
    while True:
        if comm.has_handshake():
            filename = input("Enter the filename: ")
            filename = filename + '.csv'
            label = int(input("Enter the label: "))
            raw_data = comm.getData(duration=10)
            save_training_data(filename, raw_data, label)
            print('Collection complete')
        else:
            print('Handshake broken')

if __name__ == '__main__':
    main()
