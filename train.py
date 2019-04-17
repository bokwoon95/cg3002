import pandas as pd
import os
import time
from ml.random_forest_trainer import RandomForestTrainer
from feature_extractor import FeatureExtractor
from data.process import Loader

model = 'rf'
if len(sys.argv) >= 2:
    model = sys.argv[1]
# else:
#     print('Please provide a name for the output model (e.g. "rf")')
#     os.exit(1)

curr_path = os.path.abspath(os.path.dirname(__file__))

moves = ['doublepump', 'cowboy', 'crab', 'chicken', 'raffles', 'jamesbond', 'runningman', 'hunchback', 'mermaid', 'snake', 'idle', 'logout']
moves_upper = ['Doublepump', 'Cowboy', 'Crab', 'Chicken', 'Raffles', 'Jamesbond', 'Runningman', 'Hunchback', 'Mermaid', 'Snake', 'Idle', 'Final']
columns_raw = ['move','acc1_x', 'acc1_y', 'acc1_z', 
        'gyro1_x', 'gyro1_y', 'gyro1_z', 
        'acc2_x', 'acc2_y', 'acc2_z', 
        'gyro2_x', 'gyro2_y', 'gyro2_z', 
        'acc3_x', 'acc3_y', 'acc3_z', 
        'gyro3_x', 'gyro3_y', 'gyro3_z','checksum']

feature_prefix = ["mean_", "var_", "iqr_", "psd_"]
x_columns = ["acc1_x", "acc1_y", "acc1_z", 
        "gyro1_x", "gyro1_y", "gyro1_z",
        "acc2_x", "acc2_y", "acc2_z",
        "gyro2_x", "gyro2_y", "gyro2_z",
        "acc3_x", "acc3_y", "acc3_z",
        "gyro3_x", "gyro3_y", "gyro3_z"]

headers = []
for prefix in feature_prefix:
    for x in x_columns:
        headers.append(prefix + x)

print("headers passed to loader are:")
print(headers)
print("headers passed to featureEx are: ")
print(columns_raw)
y_column = "move"

trainer = RandomForestTrainer(30,14)

def top(moves, columns, dir_name, dir_path, file_name, trainer, model_name): 
    loader = Loader(dir_name, headers, y_column)
    extractor = FeatureExtractor(dir_path, file_name, moves, columns)
    
    start_time = time.time()
    extractor.top()
    stop_time = time.time()
    print("Feature extractor ran for %.6f seconds" % (stop_time - start_time))
    
    loader.top()

    trainer.train(loader.X_train,loader.y_train)
    trainer.evaluate(loader.X_test,loader.y_test)
    trainer.save("models/"+ model_name + ".pkl")

dir_name = input("Enter directory name: ")
input_dir_path = os.path.join(curr_path, dir_name)
file_name = input("Enter training file name: ")
top(moves, columns_raw, dir_name, input_dir_path, file_name, trainer, model)
