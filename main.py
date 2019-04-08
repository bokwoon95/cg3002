from features import get_feature_vector
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


# TO BE REMOVED AFTER TESTING
# CLASSES = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
#         'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
#         'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z'
#         ]


# TO BE REMOVED AFTER TESTING
# def get_feature_vector(raw_data):
#     feat_vect = []
#     raw_data = np.array(raw_data)
#     # print("raw data is : ")
#     # print(raw_data)
#     feature1 = []
#     for i in range(NUM_DATA_POINTS):
#         mean = np.mean(raw_data[:,i])
#         feature1.append(mean)
#     feature2 = []
#     for i in range(NUM_DATA_POINTS):
#         variance = np.var(raw_data[:,i])
#         feature2.append(variance)

#     feat_vect = feature1 + feature2
#     return feat_vect


def main():
    global first
    comm = Communicate(IP_ADDR)
    print('Handshake started')
    comm.get_handshake()
    print('Handshake completed')
    classifier = Classifier(FILE_PATH)
    print(classifier)
    freqPredict = FreqPredictor()
    time.sleep(57)
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

            # TO BE REMOVED. 
            # is_skip = False
            # for data in raw_data:
            #     if data is None:
            #         is_skip = True
            #         print("None inside ")
            #         break
            # if is_skip:
            #     continue

            # TO BE REMOVED
            # raw_data = [list(raw_data[i]) for i in range(90)]


            # Process data
            feature_vector = get_feature_vector(raw_data)
            # Check if MOVE is idle (TO BE IMPLEMENTED)
            predict = classifier.predict_once(feature_vector)

            # TO BE REMOVED
            #if(predict == "idle" and first):
                #first = False
                #freqPredict.clear_hist()
             #   continue


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
