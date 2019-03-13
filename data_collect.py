import time
import csv
import os
import argparse
import numpy as np
import pandas as pd


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
    # Generate Dummy Data
    dummy_data = np.random.rand(1,18)
    return dummy_data

def main():
    
    while True:
        TIME = 10
        filename = input("Enter the filename: ")
        filename = filename + '.csv'
        label = int(input("Enter the label: "))
        label = np.reshape(label, (1,1))
        t_end = time.time() + TIME 
        while time.time() < t_end:
            raw_data = getIMUData()
            raw_data = np.hstack((label, raw_data))
            save_training_data(filename, raw_data)
        print('Collection complete')    


if __name__ == '__main__':
    main()