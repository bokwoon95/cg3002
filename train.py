import pandas as pd
import os
import time
from ml.random_forest_trainer import RandomForestTrainer
from ml.svm_trainer import SVMTrainer
from ml.mlp_trainer import MLPTrainer
from feature_extractor import FeatureExtractor
from sp_feature_extractor import SpFeatureExtractor
from data.process import Loader
import data.preprocess as preprocess

curr_path = os.path.abspath(os.path.dirname(__file__))
input_dir_path = os.path.join(curr_path, 'data')

moves1 = ['Doublepump', 'Cowboy', 'Crab', 'Chicken', 'Raffles', 'Jamesbond', 'Runningman', 'Hunchback', 'Mermaid', 'Snake', 'Idle']
moves1_2 = ['Snake', 'Crab', 'Raffles', 'Jamesbond', 'Mermaid', 'Idle']
columns1 = ['move','acc1_x', 'acc1_y', 'acc1_z', 'acc2_x', 'acc2_y', 'acc2_z', 'acc3_x', 'acc3_y', 'acc3_z', 'gyro1_x', 'gyro1_y', 'gyro1_z', 'gyro2_x', 'gyro2_y', 'gyro2_z', 'gyro3_x', 'gyro3_y', 'gyro3_z','checksum']

moves2 = ['Walking', 'Jogging', 'Upstairs', 'Downstairs', 'Sitting', 'Standing']
columns2 = ['x', 'y', 'z']


trainer1 = RandomForestTrainer(30,14)
trainer2 = SVMTrainer(100)
trainer3 = MLPTrainer()

def top(moves, columns, dir_path, trainer, model_name):
    loader = Loader("data")
    extractor = FeatureExtractor(input_dir_path, moves, columns)
    start_time = time.time()
    extractor.top2()
    stop_time = time.time()
    print("Feature extractor ran for %.6f seconds" % (stop_time - start_time))

    loader.top()

    trainer.train(loader.X_train,loader.y_train)
    trainer.evaluate(loader.X_test,loader.y_test)
    trainer.save("models/"+ model_name + ".pkl")

    trainer.cv(loader.X, loader.y)

def top2(trainer, model_name):
    extractor = SpFeatureExtractor(preprocess.X, preprocess.y)
    extractor.top()
    trainer.train(extractor.X_train, extractor.y_train)
    trainer.evaluate(extractor.X_test, extractor.y_test)
    trainer.save("models/"+model_name + ".pkl")

top(moves1_2, columns1, input_dir_path, trainer1, 'rf')
#top(moves1_2, columns1, input_dir_path, trainer2, 'svm')
#top(moves1_2, columns1, input_dir_path, trainer3, 'mlp')

#top2(trainer1, 'rf')
