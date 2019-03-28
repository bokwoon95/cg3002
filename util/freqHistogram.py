import numpy as np

DANCE_MOVES = ['Doublepump', 'Cowboy', 'Crab', 'Chicken', 'Raffles', 'Jamesbond', 'Runningman', 'Hunchback', 'Mermaid', 'Snake', 'Idle']

class FreqPredictor:
    def __init__(self):
        self.hist = [0 for i in range(len(DANCE_MOVES))]
    
    def store_moves(self, predict):
        self.hist[DANCE_MOVES.index(predict)] += 1

    def clear_hist(self):
        self.hist = [0 for i in range(len(DANCE_MOVES))]

    def get_predict(self):
        return DANCE_MOVES[np.argmax(self.hist)]

    def get_hist_count(self):
        return sum(self.hist)

