import pandas as pd
import os

class FeatureExtractor:
    def __init__(self, input_dir_path, moves, column_names):
        self.input_dir_path = input_dir_path
        self.moves = moves
        self.column_names = column_names

    def top(self):
        csv_path = os.path.join(self.input_dir_path, 'in.csv')
        features = self.extract(csv_path)

        x = pd.DataFrame(features)

        print(x)
        output_csv_path = os.path.join(self.input_dir_path, 'out.csv')
        self.save(x, output_csv_path)

    def top2(self):
        csv_path = os.path.join(self.input_dir_path, 'in_merge.csv')
        features = self.extract2(csv_path)

        x = pd.DataFrame(features)
        print(x)
        output_csv_path = os.path.join(self.input_dir_path, 'out.csv')
        self.save(x, output_csv_path)

    def extract2(self, input_file_path):
        def slide(size, step, data):
            attributes = self.column_names.copy()
            attributes.pop(0)
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
                    ls.append(rec)
            return ls

        data = pd.read_csv(input_file_path, header=None, names=self.column_names)
        return slide(200, 100, data)

    # returns a list of dicts, each dict being a labeled feature vector
    def extract(self, input_file_path):

        # returns a list of dicts for a single move using sliding window
        def slide(size, step, data, move):
            ls = []
            num_rows = data.shape[0]
            for start in range(0, num_rows-size, step):
                window = data.iloc[start : start + size]
                rec = {}
                rec['move'] = move
                for n in self.column_names:
                    att = window[n]
                    rec['mean_' + n] = att.mean()
                    rec['var_' + n] = att.var()
                    rec['min_' + n] = att.min()
                    rec['max_' + n] = att.max()
                ls.append(rec)
            return ls

        # assume input csv has row labels but no column labels
        data = pd.read_csv(input_file_path, header=None, names=self.column_names)

        # loop through all moves
        ret = []
        for move in self.moves:
            curr = slide(200, 100, data.loc[move], move)
            ret += curr
        return ret

    @staticmethod
    def save(dataframe, path):
        dataframe.to_csv(path, index = False)
