#from features import get_feature_vector
from comms.communications import Communicate
from ml.classifier import Classifier
from util.freqHistogram import FreqPredictor
import numpy as np
import sys
import time
from collections import deque
import os


IP_ADDR = ''
PORT_NUM = 8888
GROUP_ID = 2
NUM_DATA_POINTS = 18
first = True
FILE_PATH = ''

# TO BE REMOVED AFTER TESTING
CLASSES = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
        'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
        'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z'
        ]

DANCE_DICT = {
        'doublepump':0,
        'cowboy':0,
        'crab':0,
        'chicken':0,
        'raffles':0,
        'jamesbond':0,
        'runnningman':0,
        'hunchback':0,
        'mermaid':0,
        'snake':0,
        'idle':0,
        'final':0
        }

# TO BE REMOVED AFTER TESTING
def get_feature_vector(raw_data):
    feat_vect = []
    raw_data = np.array(raw_data)
     # print("raw data is : ")
     # print(raw_data)
    feature1 = []
    for i in range(NUM_DATA_POINTS):
        mean = np.mean(raw_data[:,i])
        feature1.append(mean)
    feature2 = []
    for i in range(NUM_DATA_POINTS):
        variance = np.var(raw_data[:,i])
        feature2.append(variance)
    feature3 = []
    for i in range(NUM_DATA_POINTS):
        q75, q25 = np.percentile(raw_data[:,i], [75,25])
        irq_value = q75 - q25
        feature3.append(irq_value)
    feature4 = []
    for i in range(NUM_DATA_POINTS):
        psd_value = np.mean(np.abs(np.fft.fft(raw_data[:,i]))**2)
        feature4.append(psd_value)

    feat_vect = feature1 + feature2 + feature3 + feature4
    return feat_vect

def send_prediction(pred, comm):
    try:
        comm.sendData(action=pred, voltage=0, current=0, power=0,cumpower=0)
    except AttributeError:
        print("Communication client has not been established")

def main():
    comm = Communicate(IP_ADDR)
    print('Handshake started')
    comm.get_handshake()
    print('Handshake completed')
    classifier = Classifier(FILE_PATH)
    print(classifier)
    freqPredict = FreqPredictor()
    dance_dict = DANCE_DICT.copy()
    if comm.has_handshake():
        print("starting a new iteration: ")
    input("Press any key to continue")
    state_queue = deque()

    while True:
        if comm.has_handshake():
            # Get data from IMU
            # raw_data = comm.getData(duration=1)
            # raw_data = comm.getData2(window = 60)
            raw_data = comm.getData2(window = 45)
            if raw_data == None:
                print("Comms Error: None Type")
                break

            # Process data
            feature_vector = get_feature_vector(raw_data)
            predict = classifier.predict_once(feature_vector)
            predict = predict.lower()
        
            freqPredict.store_moves(predict)
            state_queue.append(predict)

            if(len(state_queue) == 2):
                if(predict == state_queue[0]):
                    final_predict = state_queue.popleft()
                    print('Final Prediction (Queue):', final_predict)
                    send_prediction(final_predict, comm)
                    state_queue.clear()
                    freqPredict.clear_hist()
                    continue
                else:
                    if(freqPredict.get_hist_count() == 5):
                        final_predict = freqPredict.get_predict()
                        print('Final Prediction (Hist):', final_predict)
                        send_prediction(final_predict, comm)
                        state_queue.clear()
                        freqPredict.clear_hist()
                        continue
                    else:
                        state_queue.clear()
                        state_queue.append(predict)
                        continue
            else:
                if(freqPredict.get_hist_count() == 5):
                    final_predict = freqPredict.get_predict()
                    print('Final Prediction (Hist):', final_predict)
                    send_prediction(final_predict, comm)
                    state_queue.clear()
                    freqPredict.clear_hist()
                    continue
                else:
                    if(predict == state_queue[0]):
                        continue
                    else:
                        state_queue.clear()
                        state_queue.append(predict)
                        continue
        else:
            print('Handshake broken')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Invalid number of arguments')
        print('python3 main.py <IP_addr> [model]')
        sys.exit()
    IP_ADDR = sys.argv[1]
    FILE_PATH = "/home/pi/cg3002/models/rf.pkl"
    if len(sys.argv) >= 3:
        FILE_PATH = os.path.expanduser(sys.argv[2])
    # PORT_NUM = int(sys.argv[2])
    # Execute the main program
    main()
