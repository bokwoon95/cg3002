from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics as metrics
import sklearn.model_selection as ms
import joblib

class RandomForestTrainer:
    def __init__(self, numEst, maxDepth):
        self.numEst = numEst
        self.maxDepth = maxDepth
        self.clf = RandomForestClassifier(n_estimators=numEst, max_depth=maxDepth, random_state=0)

    def train(self, X, y):
        self.clf.fit(X,y)

    def evaluate(self, X, y):
        res = self.clf.predict(X)
        score = metrics.accuracy_score(y,res)
        print("RF with %d estimators and max depth of %d" % (self.numEst,self.maxDepth))
        print("confusion matrix:\n%s" % metrics.confusion_matrix(y,res))
        print("accuracy score:\n%s" % score)
        return score

    def cv(self, X, y):
        scores = ms.cross_val_score(self.clf, X, y, cv=30)
        print("cross val score: %f" % scores.mean())

    def save(self, model_path):
        print("saving model...")
        joblib.dump(self.clf, model_path)
        print("Model successfully saved at %s" % model_path)
