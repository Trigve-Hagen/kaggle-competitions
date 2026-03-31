# Kaggle Competitions
This site is a combination of both flask and AI scripts. There is a competition section and a training section. The rules state that I cannot share the data files so they are not included. You will have to go to the Kaggle.com site and download the data. For the competitions put the data files(csv, json) in the root of the competition, in the training put them in the dataset folders. I will fix the competitions to have the data files in the dataset folders for continuity.

## Installation
in PS:
  - cd path-to-your-project
  - python -m venv .venv
  - .venv\Scripts\Activate.ps1
  - pip install matplotlib seaborn tensorflow torch numpy pandas scikit-learn Flask Flask-SQLAlchemy
  - python app.py

This app is just to show where I am in hopes of someday getting a position doing AI where I work. More than the position its the fun of solving puzzles and the hopes of writing a paper on some new functionality that advances AI. Thanks to the company I work for. Go USA!

The scripts run separately. I'll try to leave a comment at the bottom to simplify running them.

## File Structure
- competitions
  - arc_prize
  - housing_prices
  - march_madness
- instance - where the sqlite db is stored
- static - images and javascripts
  - img
  - js
- templates - flask templates
  - arc_prize
  - housing_prices
  - includes
  - march_madness
- training - practice for competitions
  - breast
    - dataset
  - housing
    - dataset
  - iris
    - dataset
  - nba
    - dataset
  - salary_prediction
    - dataset
  - titanic
    - dataset
- app.py - entrance to the flash app - for starting the app after installing run 'python app.py'
- columns.py - A script to consolidate multiple csvs into one.
- config.py - The config script mainly for SQL Alchemy database.
- data.py - A script for wrangling March madness data.
- utils.py - A utility script.
