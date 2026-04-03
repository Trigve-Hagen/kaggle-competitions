from classes.aai.decisiontree import DecisionTree
from sklearn.model_selection import train_test_split
from sklearn import datasets

import numpy as np
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset" / 'data.csv'

data1 = datasets.load_breast_cancer()
data2 = pd.read_csv(DATASET) # datasets.load_breast_cancer()
# X, y = data.data, data.target

print(data1)
# print(data2.head())

# print(data.columns)
# data.columns = data.columns.str.strip()
# data = data.drop(['Unnamed: 32'], axis=1)

# total_miss = data.isnull().sum()
# percent_miss = (total_miss/data.isnull().count()*100)

# Creating dataframe from dictionary
# missing_data = pd.DataFrame({'Total missing':total_miss,'% missing':percent_miss})
# print(missing_data.sort_values(by='Total missing',ascending=False).head())

# X = data2.drop(columns=['id', 'diagnosis']).values
# y = data2['diagnosis'].map({'B': 0, 'M': 1}) # data['diagnosis'].values

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

# clf = DecisionTree()
# clf.fit(X_train, y_train)
# predictions = clf.predict(X_test)

def accuracy(y_test, y_pred):
  return np.sum(y_test == y_pred) / len(y_test)

# acc = accuracy(y_test, predictions)
# print(acc)

# (.venv)
# activate and install dependencies
# python -m training.breast.decisiontree
