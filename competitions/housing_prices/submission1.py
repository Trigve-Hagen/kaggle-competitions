import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from pathlib import Path
import matplotlib.pyplot as plt
import os

# Load the data, and separate the target
# Get the directory of the current file
script_dir = Path(__file__).parent
print(script_dir)
iowa_file_path = script_dir / "dataset" / "train.csv"
home_data = pd.read_csv(iowa_file_path)

oe = OrdinalEncoder()
# Create new encoded column
home_data['LandContour_encoded'] = oe.fit_transform(home_data[['LandContour']])
y = home_data.SalePrice

# Create X (After completing the exercise, you can return to modify this line!)
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd', 'LandContour_encoded']

# 1. Ordinal Encoding Example
mapping = {'Low': 0, 'HLS': 1, 'Bnk': 2, 'Lvl': 3}

# Select columns corresponding to features, and preview the data
X = home_data[features]
# print(X.head())
# print(y.head())

# plt.xlabel('Area')
# plt.ylabel('Price')
# sqft = home_data['1stFlrSF'] + home_data['2ndFlrSF']
# plt.scatter(sqft, home_data.SalePrice, color='red', marker='+')
# plt.show()

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Define a random forest model
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(train_X, train_y)
rf_val_predictions = rf_model.predict(val_X)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))

# To improve accuracy, create a new Random Forest model which you will train on all training data
rf_model_on_full_data = RandomForestRegressor()

# fit rf_model_on_full_data on all data from the training data
rf_model_on_full_data.fit(X, y)

# path to file you will use for predictions
test_data_path = script_dir / "dataset" / "test.csv"

# read test data file using pandas
test_data = pd.read_csv(test_data_path)
test_data['LandContour_encoded'] = oe.fit_transform(test_data[['LandContour']])

# create test_X which comes from test_data but includes only the columns you used for prediction.
# The list of columns is stored in a variable called features
test_X = test_data[features]

# make predictions which we will submit.
test_preds = rf_model_on_full_data.predict(test_X)

output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})

# path to submissions
submissions_path = script_dir / "submissions"

output.to_csv(submissions_path / "submission.csv", index=False)

# (.venv)
# activate and install dependencies
# python -m competitions.housing_prices.submissions.submission1


# submission 1
# Validation MAE for Random Forest Model: 21,857
