import pandas as pd
import numpy as np
import os


class FeatureExtractor:
    def __init__(self, input_dir_path, file_name, moves, column_names):
        self.input_dir_path = input_dir_path
        self.moves = moves
        self.column_names = column_names
        self.file_name = file_name

    def top(self):
        csv_path = os.path.join(self.input_dir_path, self.file_name+'.csv')
        features = self.extract(csv_path)

        x = pd.DataFrame(features)
        print("feature dataframe dimension is: ")
        print(x.shape)
        output_csv_path = os.path.join(self.input_dir_path, 'out.csv')
        self.save(x, output_csv_path)

    def extract(self, input_file_path):
        def slide(size, step, data):
            attributes = self.column_names.copy()
            #discount first item in header
            attributes.pop(0)
            print(self.moves)
            ls = []
            num_rows = data.shape[0]
            for start in range(0, num_rows-size, step):
                window = data.iloc[start: start + size]
                rec = {}
                moves = window['move'].copy()
                modes = window['move'].mode().copy()
                freq = moves.value_counts()
                if freq[0] > size * 0.8:
                    move = modes[0]
                    rec['move'] = move
                    for n in attributes:
                        att = window[n]
                        rec['mean_' + n] = att.mean()
                        rec['var_' + n] = att.var()
                        rec['min_' + n] = att.min()
                        rec['max_' + n] = att.max()
                        q75, q25 = np.percentile(att.data,[75,25])
                        rec['iqr_' + n] = q75-q25
                        rec['psd_' + n] = np.mean(np.abs(np.fft.fft(att.data))**2)
                    ls.append(rec)
            return ls

        data = pd.read_csv(input_file_path, header=None, names=self.column_names)
        print(type(data['move']))
        print(data.dtypes)
        return slide(45, 10, data)

    @staticmethod
    def save(dataframe, path):
        dataframe.to_csv(path, index = False)
