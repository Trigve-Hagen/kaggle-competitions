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
DATASET = script_dir / "dataset" / 'train.csv'

data = pd.read_csv(DATASET)

data.drop(["Cabin","Name","PassengerId","Ticket"],axis=1,inplace=True)
data['Sex'] = data['Sex'].replace(["female", "male"], [0, 1])
data['Embarked'] = data['Embarked'].replace(['S', 'C', 'Q'], [1, 2, 3])
data.dropna(inplace=True)

X = data.drop(columns=['Survived']).values
y = data['Survived'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

class NaiveBayesClassifier():
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels
        self.log_py = self.log_prior()
        self.mu,self.sigma = self.get_mean_std()

    def log_prior(self):
        class_counts = np.unique(self.labels,return_counts=True)[1]
        log_py = np.log(class_counts/class_counts.sum()).reshape(2,1)
        return log_py

    def get_mean_std(self):
        x_feature_subset = self.features[np.nonzero(self.labels == 0)].astype(np.float64)
        x = np.mean(x_feature_subset, axis=0)
        y_feature_subset = self.features[np.nonzero(self.labels == 1)].astype(np.float64)
        y = np.mean(y_feature_subset, axis=0)
        mu = np.column_stack((x,y))

        x_feature_subset = self.features[np.nonzero(self.labels == 0)].astype(np.float64)
        x = np.std(x_feature_subset, axis=0)
        y_feature_subset = self.features[np.nonzero(self.labels == 1)].astype(np.float64)
        y = np.std(y_feature_subset, axis=0)
        sigma = np.column_stack((x,y))

        return mu,sigma

    def predict(self, features):
        N, d = features.shape
        x = (np.log(((self.sigma.transpose()[0].reshape(1,d))*np.sqrt(np.pi*2))**-1))- (((features-self.mu.transpose()[0].reshape(1,d))**2)/(2*(self.sigma.transpose()[0].reshape(1,d))**2))
        y = (np.log(((self.sigma.transpose()[1].reshape(1,d))*np.sqrt(np.pi*2))**-1))-(((features-self.mu.transpose()[1].reshape(1,d))**2)/(2*(self.sigma.transpose()[1].reshape(1,d))**2))
        naive_prob = np.column_stack((np.sum(x,axis=1)+self.log_py[0],np.sum(y,axis=1)+self.log_py[1]))
        return naive_prob.argmax(axis=1)

titanic_classifier = NaiveBayesClassifier(X_train, y_train)
train_pred = titanic_classifier.predict(X_train)
test_pred = titanic_classifier.predict(X_test)

train_acc_cust_model = (train_pred==y_train).mean()
test_acc_cust_model = (test_pred==y_test).mean()
print(f'The training accuracy of our custom model is {train_acc_cust_model}')
print(f'The testing accuracy of our custom model is {test_acc_cust_model}')

# (.venv)
# activate and install dependencies
# python -m training.titanic.bayes

