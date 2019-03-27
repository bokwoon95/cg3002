from comms.communications import Communicate
from ml.classifier import Classifier
import numpy as np

IP_ADDR = ''
PORT_NUM = 123
GROUP_ID = 123
NUM_DATA_POINTS = 19
FILE_PATH = "/home/pi/cg3002/models/rf.pkl"

# max_acc1_x,max_acc1_y,max_acc1_z,max_acc2_x,max_acc2_y,max_acc2_z,max_acc3_x,max_acc3_y,max_acc3_z,max_checksum,max_gyro1_x,max_gyro1_y,max_gyro1_z,max_gyro2_x,max_gyro2_y,max_gyro2_z,max_gyro3_x,max_gyro3_y,max_gyro3_z,mean_acc1_x,mean_acc1_y,mean_acc1_z,mean_acc2_x,mean_acc2_y,mean_acc2_z,mean_acc3_x,mean_acc3_y,mean_acc3_z,mean_checksum,mean_gyro1_x,mean_gyro1_y,mean_gyro1_z,mean_gyro2_x,mean_gyro2_y,mean_gyro2_z,mean_gyro3_x,mean_gyro3_y,mean_gyro3_z,min_acc1_x,min_acc1_y,min_acc1_z,min_acc2_x,min_acc2_y,min_acc2_z,min_acc3_x,min_acc3_y,min_acc3_z,min_checksum,min_gyro1_x,min_gyro1_y,min_gyro1_z,min_gyro2_x,min_gyro2_y,min_gyro2_z,min_gyro3_x,min_gyro3_y,min_gyro3_z,move,var_acc1_x,var_acc1_y,var_acc1_z,var_acc2_x,var_acc2_y,var_acc2_z,var_acc3_x,var_acc3_y,var_acc3_z,var_checksum,var_gyro1_x,var_gyro1_y,var_gyro1_z,var_gyro2_x,var_gyro2_y,var_gyro2_z,var_gyro3_x,var_gyro3_y,var_gyro3_z

CLASSES = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
            'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
            'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z',
]
def get_feature_vector(raw_data):
    feat_vect = []
    raw_data = np.array(raw_data)
    feat_dict = {}
    for i in range(NUM_DATA_POINTS):
        #print(raw_data[:,i])
        mean = np.mean(raw_data[:,i])
        variance = np.var(raw_data[:,i])
        min_value = np.min(raw_data[:,i])
        max_value = np.max(raw_data[:,i])        
        feat_dict['mean_' + CLASSES[i]] = mean
        feat_dict['var_' + CLASSES[i]] = variance
        feat_dict['min_' + CLASSES[i]] = min_value
        feat_dict['max_' + CLASSES[i]] = max_value
    
    for f in sorted(feat_dict):
        feat_vect.append(feat_dict[f])
    
    return feat_vect


def main():
    comm = Communicate()
    print('Handshake started')
    comm.get_handshake()
    print('Handshake completed')
    classifier = Classifier(FILE_PATH)
    print(classifier)
    while True:
        if comm.has_handshake():
            # Get data from IMU
            raw_data = comm.getData(duration=2)
            raw_data = [list(x) for x in raw_data]
            # Process data
            feature_vector = get_feature_vector(raw_data)
            # Check if MOVE is idle (TO BE IMPLEMENTED)
            predict = classifier.predict_once(feature_vector)
            # Send Data
            # For Testing (REMOVE DURING DEPLOYMENT)
            # print(predict)
        else:
            print('Handshake broken')
        #comm.sendData(ip_addr=IP_ADDR, port_num=PORT_NUM, groupID=GROUP_ID, action=predict, voltage=0, current=0, power=0, cumpower=0)


if __name__ == "__main__":
    # Execute the main program
    main()
