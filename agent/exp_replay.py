from collections import deque
import random, pickle
import numpy as np


class ExpReplay(object):
    def __init__(self, size):
        self.size = size
        self.replay = deque()

    def add(self, sample):
        self.replay.append(sample)
        if len(self.replay) > self.size:
            self.replay.popleft()

    def batch(self, batch_size):
        mini_batch = random.sample(self.replay, batch_size)
        return mini_batch

    def is_full(self):
        return len(self.replay) == self.size

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def __len__(self):
        return len(self.replay)
