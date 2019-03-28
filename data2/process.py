import sklearn.model_selection as ms
import pandas as pd
import os

class Loader:
    def __init__(self, path_to_dir, x_columns, y_column):
        self.path = os.path.join(path_to_dir, 'out.csv')
        self.x_columns = x_columns
        self.y_column = y_column
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []
        self.X = []
        self.y = []

    def top(self):
        file_train = open(self.path)
        #dataframe = pd.read_csv(f, index_col=False)
        dataframe = pd.read_csv(file_train, index_col=False)

        self.X, self.y = self.extract_columns(dataframe)
        print("extracted columns are(ordered):")
        print(list(self.X))
        self.X_train, self.X_test, self.y_train, self.y_test = ms.train_test_split(self.X,self.y,test_size=0.3,random_state=0)

        #print(list(self.X))
        #print(self.y)
    def extract_columns(self, df):
        data_x = df[self.x_columns].copy()
        data_y = df[self.y_column].copy()
        return data_x, data_y

