# https://www.youtube.com/watch?v=rTEtEy5o3X0&list=PLcWfeUsAys2k_xub3mHks85sBHZvg24Jd&index=2

import numpy as np
from collections import Counter

def euclidean_distance(a, b):
  return np.sqrt(np.sum((b - a) ** 2))

class KNN:
  def __init__(self, k):
    self.k = k

  def fit(self, X, y):
    self.X_train = X
    self.y_train = y

  def predict(self, X):
    predictions = [self._predict(x) for x in X]
    return np.array(predictions)

  def _predict(self, x):
    distances = [euclidean_distance(x, x_train) for x_train in self.X_train]

    k_indices = np.argsort(distances)[:self.k]
    k_nearest_labels = [self.y_train[i] for i in k_indices]

    most_common = Counter(k_nearest_labels).most_common(1)[0][0]
    return most_common
