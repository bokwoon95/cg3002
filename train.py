import pandas as pd
import os
import time
from ml.random_forest_trainer import RandomForestTrainer
from feature_extractor import FeatureExtractor
from data.process import Loader

curr_path = os.path.abspath(os.path.dirname(__file__))
input_dir_path = os.path.join(curr_path, 'data')

moves1 = ['doublepump', 'cowboy', 'crab', 'chicken', 'raffles', 'jamesbond', 'runningman', 'hunchback', 'mermaid', 'snake', 'idle']
columns1 = ['acc1_x', 'acc1_y', 'acc1_z', 'acc2_x', 'acc2_y', 'acc2_z', 'acc3_x', 'acc3_y', 'acc3_z', 'gyro1_x', 'gyro1_y', 'gyro1_z', 'gyro2_x', 'gyro2_y', 'gyro2_z', 'gyro3_x', 'gyro3_y', 'gyro3_z']

moves2 = ['Walking', 'Jogging', 'Upstairs', 'Downstairs', 'Sitting', 'Standing']
columns2 = ['x', 'y', 'z']

trainer1 = RandomForestTrainer(30,14)

def top(moves, columns, dir_path, trainer):
    loader = Loader("data")
    extractor = FeatureExtractor(input_dir_path, moves, columns)
    start_time = time.time()
    extractor.top()
    stop_time = time.time()
    print("Feature extractor ran for %.6f seconds" % (stop_time - start_time))

    loader.top()

    trainer.train(loader.X_train,loader.y_train)
    trainer.evaluate(loader.X_test,loader.y_test)
    trainer.save("models/random_forest.pkl")

top(moves2, columns2, input_dir_path, trainer1)

