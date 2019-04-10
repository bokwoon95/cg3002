import pandas as pd
import os
import time
from ml.random_forest_trainer import RandomForestTrainer
from ml.svm_trainer import SVMTrainer
from ml.mlp_trainer import MLPTrainer
from feature_extractor import FeatureExtractor
from sp_feature_extractor import SpFeatureExtractor
from data.process import Loader

curr_path = os.path.abspath(os.path.dirname(__file__))
input_dir_path = os.path.join(curr_path, 'data')

moves = ['doublepump', 'cowboy', 'crab', 'chicken', 'raffles', 'jamesbond', 'runningman', 'hunchback', 'mermaid', 'snake', 'idle', 'logout']
moves1 = ['Doublepump', 'Cowboy', 'Crab', 'Chicken', 'Raffles', 'Jamesbond',
        'Runningman', 'Hunchback', 'Mermaid', 'Snake', 'Idle', 'Final']
moves2 = ['runningman']

columns1 = ['move','acc1_x', 'acc1_y', 'acc1_z', 
        'gyro1_x', 'gyro1_y', 'gyro1_z', 
        'acc2_x', 'acc2_y', 'acc2_z', 
        'gyro2_x', 'gyro2_y', 'gyro2_z', 
        'acc3_x', 'acc3_y', 'acc3_z', 
        'gyro3_x', 'gyro3_y', 'gyro3_z','checksum']

feature_prefix = ["mean_", "var_"]
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
print(columns1)
y_column = "move"

trainer1 = RandomForestTrainer(30,14)
trainer2 = SVMTrainer(100)
trainer3 = MLPTrainer()

def top(moves, columns, dir_path, trainer, model_name):
    loader = Loader("data", headers, y_column)
  
    extractor = FeatureExtractor(input_dir_path, moves, columns)
    start_time = time.time()
    extractor.top()
    stop_time = time.time()
    print("Feature extractor ran for %.6f seconds" % (stop_time - start_time))
    loader.top()

    trainer.train(loader.X_train,loader.y_train)
    trainer.evaluate(loader.X_test,loader.y_test)
    trainer.save("models/"+ model_name + ".pkl")

top(moves1, columns1, input_dir_path, trainer1, 'rf')
