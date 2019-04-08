from comms.communications import Communicate
from ml.classifier import Classifier
from util.testUtil import TestUtil
import numpy as np

IP_ADDR = ''
PORT_NUM = 123
GROUP_ID = 123
NUM_DATA_POINTS = 19
FILE_PATH_RF = "/home/pi/cg3002/models/rf.pkl"
FILE_PATH_SVM = "/home/pi/cg3002/models/svm.pkl"
FILE_PATH_MLP = "/home/pi/cg3002/models/mlp.pkl"

# max_acc1_x,max_acc1_y,max_acc1_z,max_acc2_x,max_acc2_y,max_acc2_z,max_acc3_x,max_acc3_y,max_acc3_z,max_checksum,max_gyro1_x,max_gyro1_y,max_gyro1_z,max_gyro2_x,max_gyro2_y,max_gyro2_z,max_gyro3_x,max_gyro3_y,max_gyro3_z,mean_acc1_x,mean_acc1_y,mean_acc1_z,mean_acc2_x,mean_acc2_y,mean_acc2_z,mean_acc3_x,mean_acc3_y,mean_acc3_z,mean_checksum,mean_gyro1_x,mean_gyro1_y,mean_gyro1_z,mean_gyro2_x,mean_gyro2_y,mean_gyro2_z,mean_gyro3_x,mean_gyro3_y,mean_gyro3_z,min_acc1_x,min_acc1_y,min_acc1_z,min_acc2_x,min_acc2_y,min_acc2_z,min_acc3_x,min_acc3_y,min_acc3_z,min_checksum,min_gyro1_x,min_gyro1_y,min_gyro1_z,min_gyro2_x,min_gyro2_y,min_gyro2_z,min_gyro3_x,min_gyro3_y,min_gyro3_z,move,var_acc1_x,var_acc1_y,var_acc1_z,var_acc2_x,var_acc2_y,var_acc2_z,var_acc3_x,var_acc3_y,var_acc3_z,var_checksum,var_gyro1_x,var_gyro1_y,var_gyro1_z,var_gyro2_x,var_gyro2_y,var_gyro2_z,var_gyro3_x,var_gyro3_y,var_gyro3_z

CLASSES = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
            'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
            'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z', 'checksum'
]
x_columns = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
            'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
            'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z'
]
def get_feature_vector(raw_data, features):
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
    
    xx = []
    for f in feat_dict:
        xx.append(f)
    xx = (sorted(xx))

    for f in xx:
        feat_vect.append(feat_dict[f])
    #print(feat_dict)
    print(xx) 
    return feat_vect

def most_frequent(List): 
    return max(set(List), key = List.count) 

def main():
    WINDOW = 150
#    comm = Communicate()
#    print('Handshake started')
#    comm.get_handshake()
#    print('Handshake completed')
    
    processor = TestUtil(x_columns)
    raw = np.load('simulate_data.npy')
    raw = processor.strip_checksum(raw)
    label = np.load('simulate_label.npy')
    classifier1 = Classifier(FILE_PATH_RF)
    classifier2 = Classifier(FILE_PATH_SVM)
    classifier3 = Classifier(FILE_PATH_MLP)

    start = 0
    end = start + WINDOW
    print(classifier1)
    print(classifier2)
    print(classifier3)
    while end < len(raw):
        raw_data = raw[start:end]
        l = label[start:end]
        start = end
        end = start + WINDOW
            # Process data
        feature_vector = processor.get_feature_vector(raw)
            # Check if MOVE is idle (TO BE IMPLEMENTED)
        predict1 = classifier1.predict_once(feature_vector)
        predict2 = classifier2.predict_once(feature_vector)
        predict3 = classifier3.predict_once(feature_vector)

        u, indices = np.unique(l, return_inverse=True)
        y_label = u[np.argmax(np.bincount(indices))]

        print(predict1, y_label)
        print(predict2, y_label)
        print(predict3, y_label)

        #comm.sendData(ip_addr=IP_ADDR, port_num=PORT_NUM, groupID=GROUP_ID, action=predict, voltage=0, current=0, power=0, cumpower=0)


if __name__ == "__main__":
    # Execute the main program
    main()
