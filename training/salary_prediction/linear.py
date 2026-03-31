# Linear Regression from scratch - https://www.youtube.com/watch?v=Jj7WD71qQWE&list=PLh6JMkwECi5HXVJ58ue58jJvL599NFYja

# Linear Regression is a foundational supervised machine learning algorithm
# used for predictive modeling. It models the relationship between a dependent
# variable (target) and one or more independent variables (features) by fitting
# a straight line (or hyperplane) to the data. Its primary purpose is to predict
# continuous numerical outcome.

# Used to predict numbers, such as house prices, stock prices, or temperatures,
# rather than categories.

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset" / "Salary_Data.csv"

df = pd.read_csv(DATASET)
x_train = df['YearsExperience'].values
y_train = df['Salary'].values

# plt.xlabel('YearsExperience')
# plt.ylabel('Salary')
# plt.scatter(x_train, y_train)
# plt.show()

def cost_function(x, y, w, b):
  m = len(x)
  cost_sum = 0

  for i in range(m):
    f = w * x[i] + b
    cost = (f - y[i]) ** 2
    cost_sum += cost

  total_cost = (1/(2*m)) * cost_sum
  return total_cost

def gradient_function(x, y, w, b):
  m = len(x)
  dc_dw = 0
  dc_db = 0

  for i in range(m):
    f = w * x[i] + b

    dc_dw += (f - y[i]) * x[i]
    dc_db += (f - y[i])

  dc_dw = (1/m) * dc_dw
  dc_db = (1/m) * dc_db

  return dc_dw, dc_db

def gradient_decent(x, y, alpha, iterations):
  w = 0
  b = 0

  for i in range(iterations):
    dc_dw, dc_db = gradient_function(x, y, w, b)

    w = w - alpha * dc_dw
    b = b- alpha * dc_db

    print(f"Iteration {i}: Cost {cost_function(x, y, w, b)}")

  return w, b

learning_rate = 0.01
iterations = 1000

final_w, final_b = gradient_decent(x_train, y_train, learning_rate, iterations)
print(f"w: {final_w:.4f}, b: {final_b:.4f}")

plt.scatter(x_train, y_train, label="Data Points")
x_vals = np.linspace(min(x_train), max(x_train), 100)
y_vals = final_w * x_vals + final_b
plt.plot(x_vals, y_vals, color='red', label='Regression Line')
plt.xlabel('YearsExperience')
plt.ylabel('Salary')
plt.legend()
plt.show()
