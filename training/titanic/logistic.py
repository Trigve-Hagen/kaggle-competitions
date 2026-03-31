# https://www.youtube.com/watch?v=3giTXZbyf1Q&list=PLh6JMkwECi5HXVJ58ue58jJvL599NFYja&index=2

# Logistic regression is a fundamental supervised machine learning algorithm
# used primarily for classification tasks. Unlike linear regression, which
# predicts continuous numerical values, logistic regression predicts the
# probability of a discrete, categorical outcome
# (e.g., yes/no, spam/not spam, disease/no disease).

from training.titanic.data import getTitanicData
import matplotlib.pyplot as plt

import os
import numpy as np
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset" / 'binary_classification_dataset.csv'

# ntrain, ntest, train, test, all_data, target = getTitanicData()

# X_train = all_data[['Pclass', 'Sex', 'Age', 'Fare', 'Deck', 'Embarked', 'FamSize', 'Alone']].values
data = pd.read_csv(DATASET)

X_train = data[['Feature_1', 'Feature_2']].values
y_train = data['Target'].values

# print(type(all_data)) # <class 'pandas.DataFrame'>
# print(type(X_train)) # <class 'numpy.ndarray'>
# print(type(target)) # <class 'pandas.Series'>
# print(type(y_train)) # <class 'numpy.ndarray'>
# print(X_train.shape) # (1309, 8)

m, n = X_train.shape
# plt.scatter(all_data[target == 0, 0], all_data[target == 0, 1], color='tab:blue', label='Class 0', s=20)
# plt.scatter(all_data[target == 1, 0], all_data[target == 1, 1], color='tab:orange', label='Class 1', s=20)
# plt.xlabel('Feature1')
# plt.ylabel('Feature2')

def sigmoid(z):
  return 1 / (1 + np.exp(-z))

def cost_function(X, y, w, b):
  cost_sum = 0

  for i in range(m):
    z = np.dot(w, X[i]) + b
    g = sigmoid(z)

    cost_sum += -y[i] * np.log(g) - (1 - y[i]) * np.log(1 - g)

  return (1/m) * cost_sum

def gradient_function(X, y, w, b):
  grad_w = np.zeros(n)
  grad_b = 0

  for i in range(m):
    z = np.dot(w, X[i]) + b
    g = sigmoid(z)

    grad_b += (g - y[i])
    for j in range(n):
      grad_w[j] += (g - y[i]) * X[i, j]

  grad_b = (1/m) * grad_b
  grad_w = (1/m) * grad_w

  return grad_b, grad_w

def gradient_decent(X, y, alpha, iterations):
  w = np.zeros(n)
  b = 0

  for i in range(iterations):
    grad_b, grad_w = gradient_function(X, y, w, b)

    w = w - alpha * grad_w
    b = b - alpha * grad_b

    if i % 1000 == 0:
      print(f"Iteration {i}: Cost {cost_function(X, y, w, b)}")

  return w, b

def predict(X, w, b):
  preds = np.zeros(m)

  for i in range(m):
    z = np.dot(w, X[i]) + b
    g = sigmoid(z)

    preds[i] = 1 if g >= 0.5 else 0

  return preds

learning_rate = 0.01
iterations = 10000

final_w, final_b = gradient_decent(X_train, y_train, learning_rate, iterations)
predictions = predict(X_train, final_w, final_b)
accuracy = np.mean(predictions == y_train) * 100
print(f"Training Accuracy: {accuracy:.2f}%")

# (.venv)
# activate and install dependencies
# python -m training.titanic.logistic
