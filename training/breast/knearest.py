# https://www.youtube.com/watch?v=3giTXZbyf1Q&list=PLh6JMkwECi5HXVJ58ue58jJvL599NFYja&index=2

# K-Nearest Neighbors (KNN) is a simple, non-parametric, lazy learning algorithm
# used for classification and regression. It predicts the label of a data point
# based on the majority vote of its closest neighbors in the training set,
# commonly using Euclidean distance. It is versatile, easy to implement, and
# requires no training step, but can be slow on large datasets.

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from collections import Counter

import os
import numpy as np
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset" / 'data.csv'

data = pd.read_csv(DATASET)

# print(data.columns)
data.columns = data.columns.str.strip()
data = data.drop(['Unnamed: 32'], axis=1)

# total_miss = data.isnull().sum()
# percent_miss = (total_miss/data.isnull().count()*100)

# Creating dataframe from dictionary
# missing_data = pd.DataFrame({'Total missing':total_miss,'% missing':percent_miss})
# print(missing_data.sort_values(by='Total missing',ascending=False).head())

X = data.drop(columns=['id', 'diagnosis']).values
y = data['diagnosis'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

# X_train_np = X_train.values
# y_train_np = y_train.values

# plt.scatter(X_train_np[y_train_np == 'B', 0], X_train_np[y_train_np == 'B', 1], color='tab:green', label='Benign')
# plt.scatter(X_train_np[y_train_np == 'M', 0], X_train_np[y_train_np == 'M', 1], color='tab:red', label='Malignant')
# plt.xlabel('Radius Mean')
# plt.ylabel('Texture Mean')
# plt.legend()
# plt.show()

def euclidean_distance(a, b):
  return np.sqrt(np.sum((b - a) ** 2))

class KNN:
  def __init__(self, k):
    self.k = k

  def fit(self, X, y):
    self.X_train = X
    # print(self.X_train.dtypes)
    self.y_train = y

  def predict(self, new_points):
    predictions = [self.predict_class(new_point) for new_point in new_points]
    return np.array(predictions)

  def predict_class(self, new_point):
    distances = [euclidean_distance(point, new_point) for point in self.X_train]

    k_nearest_indices = np.argsort(distances)[:self.k]
    k_nearest_labels = [self.y_train[i] for i in k_nearest_indices]

    most_common = Counter(k_nearest_labels).most_common(1)[0][0]
    return most_common


knn = KNN(7)
knn.fit(X_train, y_train)

# print(data['radius_mean'].unique())
predictions = knn.predict(X_test)
accuracy = np.mean(predictions == y_test) * 100
print(f"Accuracy: {accuracy:.2f}%")

# (.venv)
# activate and install dependencies
# python -m training.breast.knearest
