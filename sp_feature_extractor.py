import sklearn.model_selection as ms
import os
import numpy as np

class SpFeatureExtractor:
    def __init__(self, X, y):
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []
        self.X = X
        self.y = np.array(y)

    def top(self):
        self.X = np.array([ SpFeatureExtractor.extract(mtx) for mtx in self.X])
        self.y = self.y.reshape(-1,1)
        tmp = np.append(self.X, self.y, axis=1)
        print(tmp)
        train,test = ms.train_test_split(tmp, test_size=0.33, random_state=0)


        self.X_train = train[:,:-1].copy()
        self.X_test = test[:,:-1].copy()
        self.y_train = train[:,-1]
        self.y_test = test[:,-1]
    @staticmethod
    def extract(mtx):
        ret = []
        for col in mtx.T:
            ret += [np.mean(col), np.var(col), np.max(col), np.min(col)]
        return ret
