import joblib

class Classifier:
    def __init__(self, path):
        self.clf = joblib.load(path)
        print("path is: " + path)
        print(joblib.load("/home/pi/cg3002/models/rf.pkl"))

    def predict(self, Xs):
        return self.clf.predict(Xs)

    def predict_once(self, X):
        result = self.clf.predict([X])[0]
        print(result)
        # print('acc:', self.clf.predict_proba([X]))
        return result

if __name__ == "__main__":
    clf = Classifier("../models/random_forest.pkl")
    clf.predict_once()
