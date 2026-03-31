from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from collections import Counter

import os
import numpy as np
from pathlib import Path
import pandas as pd
from classes.aai.knn import KNN

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset" / 'iris.csv'

data = pd.read_csv(DATASET)

X = data.drop(columns=["Id", "Species"]).values
y = data["Species"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

clf = KNN(k=5)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)

# print(predictions)

acc = np.sum(predictions == y_test) / len(y_test)
print(acc)

# (.venv)
# activate and install dependencies
# python -m training.iris.knn
