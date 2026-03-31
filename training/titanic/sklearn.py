# Cross-validation
from sklearn.model_selection import KFold, GridSearchCV, cross_val_score

# Estimators
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,ExtraTreesClassifier
from sklearn.svm import SVC

# Class is inheriting methods from these classes
from sklearn.base import BaseEstimator, TransformerMixin, ClassifierMixin, clone
# Metrics for measuring our fit
from sklearn.metrics import mean_squared_error, accuracy_score

#data
from training.titanic.data import getTitanicData

import os
import numpy as np
from pathlib import Path

ntrain, ntest, train, test, all_data, target = getTitanicData()

# CV & Metrics

# We need a few functions ways to judge our fit, these are the ones
# I used while trying to find the best result:

# These are for using with CV while testing parameters
def rmse_cv(model):
  kf = KFold(n_folds=5,shuffle=True,random_state=42).get_n_splits(train)
  return np.sqrt(-cross_val_score(model, train, target, scoring='neg_mean_squared_error', cv=kf))

def logloss_cv(model):
  kf = KFold(n_folds=5,shuffle=True,random_state=42).get_n_splits(train)
  return -cross_val_score(model, train, target, scoring='neg_log_loss', cv=kf)

def accuracy_cv(model):
  kf = KFold(n_folds=5,shuffle=True,random_state=42).get_n_splits(train.values)
  return cross_val_score(model, train, target, scoring='accuracy', cv=kf)

# These are for using with predictions and target
def rmse(y_true,y_pred):
    return np.sqrt(mean_squared_error(y_true,y_pred))

def accuracy(y_true,y_pred):
    return accuracy_score(y_true,y_pred)

# Parameters

# After using GridSearchCV, these are the parameters that (so far) have worked
# the best for the data. Also, I did extensive research using other estimators
# such as XGB and LGB classifiers, but to no luck (previously my best score
# was achieved using only LGB)
rf = RandomForestClassifier(n_estimators=700,max_depth=4,
                            min_samples_leaf=1,n_jobs=-1,
                            warm_start=True,
                            random_state=42)

et = ExtraTreesClassifier(n_estimators=550,max_depth=4,
                          min_samples_leaf=1,n_jobs=-1,
                          random_state=42)

ada = AdaBoostClassifier(n_estimators=550,learning_rate=0.001,
                         random_state=42)

svc = SVC(C=2,probability=True,random_state=42)


# Creating Stacking Class

# This is the class/helper I use for stacking. It is
# inspired (and some of the code borrowed) from
# https://www.kaggle.com/serigne/stacked-regressions-top-4-on-leaderboard,
# which is a Kernel from another competition. I learned a LOT about stacking
# from that Kernel so do check it out if you're a beginner:

class StackerLvl1(BaseEstimator, ClassifierMixin, TransformerMixin):

    def __init__(self, base_models, meta_model, n_folds=5):
        self.base_models = base_models
        self.meta_model = meta_model
        self.n_folds = n_folds

    # Get OOF predictions
    def oof_pred(self, X, y):

        self.base_models_ = [list() for x in self.base_models]
        kfold = KFold(n_splits=self.n_folds, shuffle=True, random_state=42)
        out_of_fold_predictions = np.zeros((X.shape[0], len(self.base_models)))

        for i, model in enumerate(self.base_models):

            for train_index, test_index in kfold.split(X, y):

                instance = clone(model)
                self.base_models_[i].append(instance)
                instance.fit(X.loc[train_index], y.loc[train_index])
                y_pred = instance.predict(X.loc[test_index])
                out_of_fold_predictions[test_index, i] = y_pred

        return out_of_fold_predictions

    # Fit meta model using OOF predictions
    def fit(self, X, y):

        self.meta_model_ = clone(self.meta_model)
        self.meta_model_.fit(self.oof_pred(X,y), y)
        return self

    # Predict off of meta features using meta model
    def predict(self, test):
        self.meta_features_ = np.column_stack([
            np.column_stack([model.predict(test) for model in base_models]).mean(axis=1)
            for base_models in self.base_models_ ])
        return self.meta_model_.predict(self.meta_features_)

# Predictions

# Lets first split the data into a train and test set, using the indices we
# saved in the previous section (ntrain). Remember we also saved the target
# feature and the passenger ID for submission

train = all_data[:ntrain]
test = all_data[ntrain:]

# Create our stack object and fit it
stack_model  = StackerLvl1(base_models=(rf,et,svc),meta_model = ada)
stack_model.fit(train,target)

# Get metrics from cv (note that we are fitting to train data and comparing to target!)
print('Accuracy:',accuracy(stack_model.predict(train),target))
print('RMSE:',rmse(stack_model.predict(train),target))

# (.venv)
# activate and install dependencies
# python -m training.titanic.sklearn
