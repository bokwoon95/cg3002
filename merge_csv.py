import os
import pandas as pd


FILE_PATH = input("Enter directory name: ")

files = os.listdir(FILE_PATH)
li = []
print(files)
with open(FILE_PATH+'/in.csv', 'w') as outfile:
    for f in files:
        if f.endswith('.csv'):
            fp = os.path.join(FILE_PATH, f)
            with open(fp) as infile:
                outfile.write(infile.read())

