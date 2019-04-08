from comms.communications import Communicate
from ml.classifier import Classifier
from util.freqHistogram import FreqPredictor
import numpy as np
import sys
import time

IP_ADDR = ''
PORT_NUM = 8888
GROUP_ID = 2
NUM_DATA_POINTS = 18
first = True
FILE_PATH = "/home/pi/cg3002/models/rf.pkl"

# max_acc1_x,max_acc1_y,max_acc1_z,max_acc2_x,max_acc2_y,max_acc2_z,max_acc3_x,max_acc3_y,max_acc3_z,max_checksum,max_gyro1_x,max_gyro1_y,max_gyro1_z,max_gyro2_x,max_gyro2_y,max_gyro2_z,max_gyro3_x,max_gyro3_y,max_gyro3_z,mean_acc1_x,mean_acc1_y,mean_acc1_z,mean_acc2_x,mean_acc2_y,mean_acc2_z,mean_acc3_x,mean_acc3_y,mean_acc3_z,mean_checksum,mean_gyro1_x,mean_gyro1_y,mean_gyro1_z,mean_gyro2_x,mean_gyro2_y,mean_gyro2_z,mean_gyro3_x,mean_gyro3_y,mean_gyro3_z,min_acc1_x,min_acc1_y,min_acc1_z,min_acc2_x,min_acc2_y,min_acc2_z,min_acc3_x,min_acc3_y,min_acc3_z,min_checksum,min_gyro1_x,min_gyro1_y,min_gyro1_z,min_gyro2_x,min_gyro2_y,min_gyro2_z,min_gyro3_x,min_gyro3_y,min_gyro3_z,move,var_acc1_x,var_acc1_y,var_acc1_z,var_acc2_x,var_acc2_y,var_acc2_z,var_acc3_x,var_acc3_y,var_acc3_z,var_checksum,var_gyro1_x,var_gyro1_y,var_gyro1_z,var_gyro2_x,var_gyro2_y,var_gyro2_z,var_gyro3_x,var_gyro3_y,var_gyro3_z

CLASSES = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
        'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
        'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z'
        ]

def get_feature_vector(raw_data):
    feat_vect = []
    raw_data = np.array(raw_data)
    print("raw data is : ")
    print(raw_data)
    feature1 = []
    for i in range(NUM_DATA_POINTS):
        mean = np.mean(raw_data[:,i])
        feature1.append(mean)
    feature2 = []
    for i in range(NUM_DATA_POINTS):
        variance = np.var(raw_data[:,i])
        feature2.append(variance)

    feat_vect = feature1 + feature2
    return feat_vect


def main():
    comm = Communicate(IP_ADDR)
    print('Handshake started')
    comm.get_handshake()
    print('Handshake completed')
    classifier = Classifier(FILE_PATH)
    print(classifier)
    freqPredict = FreqPredictor()
    if comm.has_handshake():
        print("starting a new iteration: ")
    while True:
        if comm.has_handshake():
            # Get data from IMU
            # raw_data = comm.getData(duration=1)
            raw_data = comm.getData2(window = 60)
            if raw_data == None:
                print("Comms Error: None Type")
                break

            is_skip = False
            for data in raw_data:
                if data is None:
                    is_skip = True
                    print("None inside ")
                    break
            if is_skip:
                continue
            # raw_data = [list(raw_data[i]) for i in range(90)]
            # Process data
            feature_vector = get_feature_vector(raw_data)
            # Check if MOVE is idle (TO BE IMPLEMENTED)
            predict = classifier.predict_once(feature_vector)
            if(predict != "idle" and first):
                first = False
                freqPredict.clear_hist()
            if freqPredict.get_hist_count() < 4:
                freqPredict.store_moves(predict)
            else:
                final_predict = freqPredict.get_predict()
                freqPredict.clear_hist()
                print('Final Prediction', final_predict)
                time.sleep(1)
                try:
                    comm.sendData(action=final_predict, voltage=0, current=0, power=0, cumpower=0)
                except AttributeError:
                    # print("Communicate(): client has not been initialized")
                    continue
        # Send Data
            # For Testing (REMOVE DURING DEPLOYMENT)

        else:
            print('Handshake broken')


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Invalid number of arguments')
        print('python3 main.py [IP address]')
        sys.exit()
    IP_ADDR = sys.argv[1]
    # PORT_NUM = int(sys.argv[2])
    # Execute the main program
    main()