from comms.communications import Communicate
from ml.classifier import Classifier
import numpy as np

IP_ADDR = ''
PORT_NUM = 123
GROUP_ID = 123
NUM_DATA_POINTS = 18
FILE_PATH = 'MODEL FILE PATH'

def get_feature_vector(raw_data):
    feat_vect = []
    raw_data = np.array(raw_data)
    for i in range(NUM_DATA_POINTS):
        mean = np.mean(raw_data[:i])
        variance = np.var(raw_data[:i])
        min_value = np.min(raw_data[:i])
        max_value = np.max(raw_data[:i])
        feat_vect.append(mean)
        feat_vect.append(variance)
        feat_vect.append(min_value)
        feat_vect.append(max_value)
    return feat_vect


def main():
    comm = Communicate()
    comm.get_handshake()
    while True:
        # Get data from IMU
        raw_data = comm.getData(duration=10)
        # Process data
        feature_vector = get_feature_vector(raw_data)
        # Check if MOVE is idle (TO BE IMPLEMENTED)
        classifier = Classifier(FILE_PATH)
        predict = classifier.predict_once(feature_vector)
        # Send Data
        # For Testing (REMOVE DURING DEPLOYMENT)
        print(predict)
        comm.sendData(ip_addr=IP_ADDR, port_num=PORT_NUM, groupID=GROUP_ID, action=predict, 
            voltage=0, current=0, power=0, cumpower=0)
    
    
if __name__ == "__main__":
    # Execute the main program
    main()