# https://www.youtube.com/watch?v=1O_BenficgE

import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import pandas as pd
import os

sp500 = yf.Ticker("^GSPC")
sp500 = sp500.history(period="max")

# Assuming sp500 is your DataFrame with a datetime index
plt.figure(figsize=(10, 6)) # Optional: set figure size
plt.plot(sp500.index, sp500["Close"], label="Close")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.title("S&P 500 Close Price")
plt.legend()
plt.grid(True)
# plt.show()

del sp500['Dividends']
del sp500['Stock Splits']

# create a column that show tomorrows closing price by shifting the next days
# close column back one day
sp500["Tomorrow"] = sp500["Close"].shift(-1)
# is Tomorrows closing price greater than todays
sp500["Target"] = (sp500["Tomorrow"] > sp500["Close"]).astype(int)

# remove everything before 1990
sp500 = sp500.loc["1990-01-01":].copy()

# model = RandomForestClassifier(n_estimators=100, min_samples_split=100, random_state=1)
model = RandomForestClassifier(n_estimators=200, min_samples_split=50, random_state=1)

train = sp500.iloc[:-100]
test = sp500.iloc[-100:]

predictors = ["Close", "Volume", "Open", "High", "Low"]
model.fit(train[predictors], train["Target"])

preds = model.predict(test[predictors])
preds = pd.Series(preds, index=test.index)
precision_score(test["Target"], preds)

combined = pd.concat([test["Target"], preds], axis=1)
# combined.plot()

""" def predict(train, test, predictors, model):
  model.fit(train[predictors], train["Target"])
  preds = model.predict(test[predictors])
  preds = pd.Series(preds, index=test.index, name="Predictions")
  combined = pd.concat([test["Target"], preds], axis=1)
  return combined """
def predict(train, test, predictors, model):
  model.fit(train[predictors], train["Target"])
  preds = model.predict_proba(test[predictors])[:,1]
  preds[preds >= .6] = 1
  preds[preds < .6] = 0
  preds = pd.Series(preds, index=test.index, name="Predictions")
  combined = pd.concat([test["Target"], preds], axis=1)
  return combined

def backtest(data, model, predictors, start=2500, step=250):
  all_predictions = []

  for i in range(start, data.shape[0], step):
    train = data.iloc[0:i].copy()
    test = data.iloc[i:(i+step)].copy()
    predictions = predict(train, test, predictors, model)
    all_predictions.append(predictions)

  return pd.concat(all_predictions)

predictions = backtest(sp500, model, predictors)

# print(predictions["Predictions"].value_counts())
# latest output
# Predictions
# 0.0    5514
# 1.0    1126
# Name: count, dtype: int64

# previous outputs
# Predictions
# 0    3960
# 1    2680
# Name: count, dtype: int64

# print(precision_score(predictions["Target"], predictions["Predictions"]))
# latest outputs
# 0.5275310834813499

# previous outputs
# 0.5309701492537313

# print(predictions["Target"].value_counts() / predictions.shape[0])
# outputs
# Target
# 1    0.5375
# 0    0.4625
# Name: count, dtype: float64

# Looking for large drops or ready for a market check
""" horizons = [2,5,60,250,1000]
new_predictors = []

for horizon in horizons:
  rolling_averages = sp500.rolling(horizon).mean()

  ratio_column = f"Close_Ratio_{horizon}"
  sp500[ratio_column] = sp500["Close"] / rolling_averages["Close"]

  trend_column = f"Trend_{horizon}"
  sp500[trend_column] = sp500.shift(1).rolling(horizon).sum()["Target"]

  new_predictors+= [ratio_column, trend_column]

sp500 = sp500.dropna(subset=sp500.columns[sp500.columns != "Tomorrow"]) """

# pip install yfinance
# (.venv)
# activate and install dependencies
# python -m training.stocks.sp500
