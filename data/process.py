import sklearn.model_selection as ms
import pandas as pd

file_train = open("data/HAR3_0/out.csv")
#f = open("out.csv")

#dataframe = pd.read_csv(f, index_col=False)
dataframe = pd.read_csv(file_train, index_col=False)
train, test = ms.train_test_split(dataframe,test_size=0.33,random_state=0)

X = dataframe.loc[:,dataframe.columns != 'move'].copy()
y = dataframe['move'].copy()

X_train = train.loc[:,dataframe.columns != 'move'].copy()
X_test = test.loc[:,dataframe.columns != 'move'].copy()
y_train = train['move'].copy()
y_test = test['move'].copy()
