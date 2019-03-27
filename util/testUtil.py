import pandas as pd
import numpy as np

class TestUtil:
    def __init__(self, x_columns):
        self.x_columns = x_columns

    def get_feature_vector(self, raw_data):
        df = pd.DataFrame(raw_data, columns=self.x_columns)
        ret = []
        for i in range(len(self.x_columns)):
            column = pd.Series(raw_data[:,i])
            ret.append(column.mean())
        return ret

    def strip_checksum(self, vector):
        stripped = np.delete(vector, -1, 1)
        return stripped

