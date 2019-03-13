import joblib

class Classifier:
    def __init__(self, path):
        self.clf = joblib.load(path)

    def predict(self, Xs):
        return self.clf.predict(Xs)

    def predict_once(self, X):
        return self.clf.predict([X])[0]
