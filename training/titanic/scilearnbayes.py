from sklearn.naive_bayes import GaussianNB
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

clf = GaussianNB()
clf.fit(X_train,y_train)
train_pred_sklearn = clf.predict(X_train)
test_pred_sklearn = clf.predict(X_test)

train_acc_skl_model = (train_pred_sklearn==y_train).mean()
test_acc_skl_model = (test_pred_sklearn==y_test).mean()
print(f'The training accuracy of out of the box sklearn model is {train_acc_skl_model}')
print(f'The testing accuracy of out of the box sklearn model is {test_acc_skl_model}')

# (.venv)
# activate and install dependencies
# python -m training.titanic.scilearnbayes
