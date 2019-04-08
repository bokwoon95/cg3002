import numpy as np

CLASSES = ['acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
            'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
            'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z']

def get_enhance_feature_extraction(raw_data):
    """ data comes in the form :
    'acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
    'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
    'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z',
    Features to be used: 32 DWT coefficients for ax, ay, az abd bacc
    32 DWT coecients for ax , az and bacc
    """
    # A 18 value list that stores all sensor data from acc1_x, acc2_x .... gyro3_z
    imu_data = []
    for i in range(len(CLASSES)):
        imu_data.append(raw_data[:,i])

    # Calculate the average power specturm density 
    feat_vectors = []
    for data in imu_data:
        feat_vectors.append(np.mean(data))         # get mean value
        feat_vectors.append(np.var(data))          # get var value
        feat_vectors.append(np.min(data))          # get min value
        feat_vectors.append(np.max(data))          # get max value
        q75, q25 = np.percentile(data, [75 ,25])
        feat_vectors.append(q75 - q25)             # get interquantile range (measure of variability)
        psd = np.abs(np.fft.fft(data))**2
        feat_vectors.append(np.mean(psd))          # get average power spectral density
        

    return feat_vectors     # returns a list of mean, var, min, max, iqr & psd for acc1_x, acc2_x, ...., gyro3_z
    

def get_acceleration(raw_data):
    """ Returns the average acceleratopm
    
    data comes in the form :
    'acc1_x', 'acc1_y', 'acc1_z', 'gyro1_x', 'gyro1_y', 'gyro1_z',
    'acc2_x', 'acc2_y', 'acc2_z', 'gyro2_x', 'gyro2_y', 'gyro2_z',
    'acc3_x', 'acc3_y', 'acc3_z', 'gyro3_x', 'gyro3_y', 'gyro3_z',
    """
    # A 18 value list that stores all sensor data from acc1_x, acc2_x .... gyro3_z
    imu_data = []
    for i in range(len(CLASSES)):
        imu_data.append(raw_data[:,i])

    acceleration1 = np.mean(np.sqrt(imu_data[0]**2 + imu_data[1]**2 + imu_data[2]**2))
    acceleration2 = np.mean(np.sqrt(imu_data[6]**2 + imu_data[7]**2 + imu_data[8]**2))
    acceleration3 = np.mean(np.sqrt(imu_data[12]**2 + imu_data[13]**2 + imu_data[14]**2))

    return acceleration1, acceleration2, acceleration3


def get_feature_vector2(raw_data):
    """ This method takes in the raw data (list of IMU sensor data) 
        and returns a dict with the mean, var min max of each IMU sensor data
    """
    feat_vect = []
    raw_data = np.array(raw_data)
    feat_dict = {}
    for i in range(len(CLASSES)):
        #print(raw_data[:,i])
        mean = np.mean(raw_data[:,i])                               # get mean value
        variance = np.var(raw_data[:,i])                            # get var value
        min_value = np.min(raw_data[:,i])                           # get min value
        max_value = np.max(raw_data[:,i])                           # get max value
        q75, q25 = np.percentile(raw_data[:,i], [75 ,25])
        iqr_value = q75 - q25                                       # get interquantile range (measure of variability)
        psd_value = np.mean(np.abs(np.fft.fft(raw_data[:,i]))**2)   # get average power spectral density

        feat_dict['mean_' + CLASSES[i]] = mean
        feat_dict['var_' + CLASSES[i]] = variance
        feat_dict['min_' + CLASSES[i]] = min_value
        feat_dict['max_' + CLASSES[i]] = max_value
        feat_dict['iqr_' + CLASSES[i]] = iqr_value
        feat_dict['psd_' + CLASSES[i]] = psd_value
    
    for f in sorted(feat_dict):
        feat_vect.append(feat_dict[f])
    
    return feat_vect


def get_feature_vector(raw_data):
    """ This method takes in the raw data (list of IMU sensor data) 
        and returns a dict with the mean, var min max of each IMU sensor data
    """
    feat_vect = []
    raw_data = np.array(raw_data)
    feat_dict = {}
    for i in range(len(CLASSES)):
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