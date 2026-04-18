import random
from micrograd.engine import Value
from micrograd.nn import MLP
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# 4 inputs (sepal length/width, petal length/width),
# 2 hidden layers (e.g., 10 nodes each), 3 outputs (species)
model = MLP(4, [10, 10, 3])
# print(model.parameters())

# Load data
iris = load_iris()
X = iris.data
y = iris.target

# Convert y to one-hot encoding for 3-class classification
y_onehot = np.zeros((y.size, 3))
y_onehot[np.arange(y.size), y] = 1

# Normalize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y_onehot, test_size=0.2)

for k in range(100): # 100 epochs
    # Forward pass
    total_loss = 0
    for i in range(len(X_train)):
        inputs = [Value(x) for x in X_train[i]]
        pred = model(inputs)

        # Loss calculation (MSE)
        target = y_train[i]
        loss = sum((p - t)**2 for p, t in zip(pred, target))
        total_loss += loss

        # Backward pass
        model.zero_grad()
        loss.backward()

        # Update weights (SGD)
        learning_rate = 0.01
        for p in model.parameters():
          p.data -= learning_rate * p.grad

    print(f"Epoch {k}, Loss: {total_loss.data / len(X_train)}")


# (.venv)
# activate and install dependencies
# python -m training.micrograd.iris
