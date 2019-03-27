import numpy as np
import csv

X = np.load("data/x_data.npy")
y = np.load("data/y_data.npy")
y = [np.where(y_vector==1)[0][0] for y_vector in y]
