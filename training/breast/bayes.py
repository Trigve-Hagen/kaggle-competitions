# https://www.youtube.com/watch?v=3giTXZbyf1Q&list=PLh6JMkwECi5HXVJ58ue58jJvL599NFYja&index=2

# Naive Bayes is a simple, fast, and highly effective probabilistic classification
# algorithm in machine learning that uses Bayes' Theorem with a strong, "naive"
# assumption that all features are independent of each other used for
# classification and regression. In machine learning, a probabilistic classifier
# is a classifier that is able to predict, given an observation of an input,
# a probability distribution over a set of classes.

from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from collections import Counter

import os
import numpy as np
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset" / 'data_kaggle.csv'

data = pd.read_csv(DATASET)

X = data.drop(columns=['id', 'diagnosis'])
y = data['diagnosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

class NaiveBayes:
  def fit(self, X_train, y_train):
    # In the context of the sentence provided, a class (often denoted as)
    # refers to a specific, predefined category or label into which data points
    # are sorted.
    self.classes = np.unique(y_train)
    # P(y) is called the Prior. Its independent of X and is usually calculated
    # by counting the frequency of each class from the data.
    self.priors = [len(y_train[y_train == c]) / len(y_train) for c in self.classes]

    self.means = [X_train[y_train == c].mean() for c in self.classes]
    self.stds = [X_train[y_train == c].std() for c in self.classes]

  def compute_likelihood(self, row, class_idx):
    likelihood = 1
    for feature in row.index:
      mean = self.means[class_idx][feature]
      std = self.stds[class_idx][feature]
      likelihood *= (1 / (np.sqrt(2 * np.pi) * std)) * np.exp((-(row[feature] - mean)**2) / (2 * std**2))

    return likelihood

  def predict(self, X):
    y_pred = []
    for _, row in X.iterrows():
      posteriors = []
      for i in range(len(self.classes)):
        likelihood = self.compute_likelihood(row, i)
        posteriors.append(likelihood * self.priors[i])

      y_pred.append(self.classes[np.argmax(posteriors)])

    return np.array(y_pred)

nb = NaiveBayes()
nb.fit(X_train, y_train)
predictions = nb.predict(X_test)

accuracy = np.mean(predictions == y_test) * 100
print(f"Accuracy: {accuracy:.2f}%")

# (.venv)
# activate and install dependencies
# python -m training.breast.bayes
