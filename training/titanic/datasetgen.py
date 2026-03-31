# https://www.youtube.com/watch?v=3giTXZbyf1Q&list=PLh6JMkwECi5HXVJ58ue58jJvL599NFYja&index=2

# Generated the data for the binary classification in logistic regression model.

import pandas as pd
from sklearn.datasets import make_classification
import matplotlib.pyplot as plt
from pathlib import Path

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset"

# 1. Generate the synthetic dataset
# n_features=2: ensures exactly two features
# n_informative=2: ensures both features are useful for prediction
# n_redundant=0, n_repeated=0: ensures no extra, useless features
# n_classes=2: ensures a binary classification problem
# n_clusters_per_class=1: creates a single cluster for each class for clear linear separation
# random_state=42: ensures reproducibility of the data
X, y = make_classification(
    n_samples=1000,
    n_features=2,
    n_informative=2,
    n_redundant=0,
    n_repeated=0,
    n_classes=2,
    n_clusters_per_class=1,
    random_state=42,
    class_sep=1.5 # Adjust class separation for a clearer linear boundary
)

# 2. Convert to a Pandas DataFrame
# Combine the features (X) and the target variable (y) into a single DataFrame
df = pd.DataFrame(X, columns=['Feature_1', 'Feature_2'])
df['Target'] = y

# 3. Save the DataFrame to a CSV file
csv_filename = DATASET / 'binary_classification_dataset.csv'
df.to_csv(csv_filename, index=False) # index=False prevents writing the DataFrame index to the CSV

print(f"Dataset successfully generated and saved to {csv_filename}")

# Optional: Plot the data to visualize the linear separation
plt.scatter(df['Feature_1'], df['Feature_2'], c=df['Target'], cmap='viridis', marker='o', edgecolor='k', s=20)
plt.title('Binary Classification Dataset Visualization')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()
