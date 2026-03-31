import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.compose import make_column_transformer
from utils import Utils

class Housing:

  def build_data():
    # Separate target from predictors
    # Read the data
    X = pd.read_csv('Data/Housing/train.csv', index_col='Id')
    X_test = pd.read_csv('Data/Housing/test.csv', index_col='Id')

    # Remove rows with missing target, separate target from predictors
    X.dropna(axis=0, subset=['SalePrice'], inplace=True)
    y = X.SalePrice
    X.drop(['SalePrice'], axis=1, inplace=True)

    # To keep things simple, we'll drop columns with missing values
    cols_with_missing = [col for col in X.columns if X[col].isnull().any()]
    X.drop(cols_with_missing, axis=1, inplace=True)
    X_test.drop(cols_with_missing, axis=1, inplace=True)

    # Break off validation set from training data
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

    input_shape = [X_train.shape[1]]

    return X_train, X_valid, y_train, y_valid, input_shape

  def build_model(X_train, y_train, X_valid, y_valid, input_shape):
    print(X_train.head())
    print(type(X_train))
    print(X_train.shape)

    if isinstance(X_train, pd.Series):
      X_train = X_train.to_frame()

    if isinstance(X_valid, pd.Series):
      X_valid = X_valid.to_frame()

    drop_X_train = X_train.select_dtypes(exclude=['object'])
    drop_X_valid = X_valid.select_dtypes(exclude=['object'])
    # drop_X_train = X_train[[col for col in X_train.columns if X_train[col].dtype != 'object']]
    # drop_X_valid = X_valid[[col for col in X_valid.columns if X_valid[col].dtype != 'object']]

    print("MAE from Approach 1 (Drop categorical variables):")
    print(Utils.score_dataset(drop_X_train, drop_X_valid, y_train, y_valid))

# Data.spotify, Data.concreate, or Data.hotel
X_train, y_train, X_valid, y_valid, input_shape = Housing.build_data()

# Spotify, Concrete or Hotel
Housing.build_model(X_train, y_train, X_valid, y_valid, input_shape)
