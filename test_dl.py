import numpy as np
from keras.utils import to_categorical
from keras import models
from keras import layers
from keras.datasets import imdb


(training_data, training_targets), (testing_data, testing_targets) = imdb.load_data(num_words=10000)
data = np.concatenate((training_data, testing_data), axis=0)
targets = np.concatenate((training_targets, testing_targets), axis=0)
