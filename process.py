import sklearn.model_selection as ms
import pandas as pd
import os

class Loader:
    def __init__(self, path_to_dir):
        self.path = os.path.join(path_to_dir, 'out.csv')
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

        train, test = ms.train_test_split(dataframe,test_size=0.33,random_state=0)
        self.X = dataframe.loc[:,dataframe.columns != 'move'].copy()
        self.y = dataframe['move'].copy()

        self.X_train = train.loc[:,dataframe.columns != 'move'].copy()
        self.X_test = test.loc[:,dataframe.columns != 'move'].copy()
        self.y_train = train['move'].copy()
        self.y_test = test['move'].copy()


