import pandas as pd
import os
import time
from ml.random_forest_trainer import RandomForestTrainer
from feature_extractor import FeatureExtractor

curr_path = os.path.abspath(os.path.dirname(__file__))

# supply data directory path
input_dir_path = os.path.join(curr_path, 'data')

moves = ['doublepump', 'cowboy', 'crab', 'chicken', 'raffles', 'jamesbond', 'runningman', 'hunchback', 'mermaid', 'snake', 'idle']
columns = ['acc1_x', 'acc1_y', 'acc1_z', 'acc2_x', 'acc2_y', 'acc2_z', 'acc3_x', 'acc3_y', 'acc3_z', 'gyro1_x', 'gyro1_y', 'gyro1_z', 'gyro2_x', 'gyro2_y', 'gyro2_z', 'gyro3_x', 'gyro3_y', 'gyro3_z']
extractor = FeatureExtractor(input_dir_path, moves, columns)

start_time = time.time()
extractor.top()
stop_time = time.time()
print("Feature extractor ran for %.6f seconds" % (stop_time - start_time))

'''
extractor2 = SpFeatureExtractor(pp4.X_train, pp4.y_train, pp4.X_test, pp4.y_test)
extractor2.top()
'''

#####
# training and evaluation
#####
trainer = RandomForestTrainer(30,14)
#trainer2 = SVMTrainer(5000)
#trainer3 = MLPTrainer()




'''
trainer.train(process.X_train,process.y_train)
trainer2.train(process.X_train,process.y_train)
trainer3.train(process.X_train,process.y_train)
trainer.evaluate(process.X_test,process.y_test)
trainer2.evaluate(process.X_test,process.y_test)
trainer3.evaluate(process.X_test,process.y_test)
trainer.cv(process.X, process.y)
'''

'''
trainer.train(extractor2.X_train,extractor2.y_train)
#trainer2.train(extractor2.X_train,extractor2.y_train)
#trainer3.train(extractor2.X_train,extractor2.y_train)

start_time = time.time()
trainer.evaluate(extractor2.X_test,extractor2.y_test)
stop_time = time.time()
print(stop_time - start_time)
#trainer2.evaluate(extractor2.X_test,extractor2.y_test)
#trainer3.evaluate(extractor2.X_test,extractor2.y_test)
'''

trainer.save("models/random_forest.pkl")
