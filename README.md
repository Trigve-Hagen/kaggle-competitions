# Kaggle Competitions
This site is a combination of both flask and AI. There is a compitition section and a training section.

## Installation
Each script has a list of pip installs and instructions using .venv and Powershell in a comment. For all scripts including the flask app the process is the same. Create your .venv, activate it, pip install your packages, and run the script using the comment.

## File Structure
- competitions
  - housing_prices
  - march_madness
- instance - where the sqlite db is stored
- static - images and javascripts
  - img
  - js
- templates - flask templates
  - housing_prices
  - includes
  - march_madness
- training - practice for competitions
  - breast
    - dataset
  - iris
    - dataset
  - nba
    - dataset
      - Salary_Data.csv
  - salary_prediction
    - dataset
  - titanic
    - dataset
- app.py - entrance to the flash app - for starting the app after installing run 'python app.py'
- columns.py - A script to consolidate multiple csvs into one.
- config.py - The config script mainly for SQL Alchemy database.
- data.py - A script for wrangling March madness data.
- utils.py - A utility script.
