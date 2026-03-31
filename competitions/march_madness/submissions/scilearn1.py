import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from pathlib import Path
from columns import MergeColumns
from data import Data
import os

# 1. Initialize the class
script_dir = Path(__file__).parent.parent
# print(script_dir)

###################################### Data ##########################################
# years_regular_mens_output_path = script_dir / "years" / "regular" / "mens"
# years_tourney_mens_output_path = script_dir / "years" / "tourney" / "mens"
# years_regular_mens_input_csv_path = script_dir / "MRegularSeasonDetailedResults.csv"
# years_tourney_mens_input_csv_path = script_dir / "MNCAATourneyDetailedResults.csv"

# Data.split_csv_by_year(years_regular_mens_input_csv_path, 'Season', years_regular_mens_output_path)
# Data.split_csv_by_year(years_tourney_mens_input_csv_path, 'Season', years_tourney_mens_output_path)

# years_regular_womens_output_path = script_dir / "years" / "regular" / "womens"
# years_tourney_womens_output_path = script_dir / "years" / "tourney" / "womens"
# years_regular_womens_input_csv_path = script_dir / "WRegularSeasonDetailedResults.csv"
# years_tourney_womens_input_csv_path = script_dir / "WNCAATourneyDetailedResults.csv"

# Data.split_csv_by_year(years_regular_womens_input_csv_path, 'Season', years_regular_womens_output_path)
# Data.split_csv_by_year(years_tourney_womens_input_csv_path, 'Season', years_tourney_womens_output_path)

# years_teams_mens_seeds_output_path = script_dir / "years" / "teams" / "mens"
# years_teams_mens_seeds_input_csv_path = script_dir / "MNCAATourneySeeds.csv"

# Data.split_csv_by_year(years_teams_mens_seeds_input_csv_path, 'Season', years_teams_mens_seeds_output_path)

# years_teams_womens_seeds_output_path = script_dir / "years" / "teams" / "womens"
# years_teams_womens_seeds_input_csv_path = script_dir / "WNCAATourneySeeds.csv"

# Data.split_csv_by_year(years_teams_womens_seeds_input_csv_path, 'Season', years_teams_womens_seeds_output_path)

# find the game data for each team in the season data for 2026
# WTeams.csv & MTeams.csv
mens_teams = script_dir / "MTeams.csv"
womens_teams = script_dir / "WTeams.csv"
sample_submissions = script_dir / "SampleSubmissionStage1.csv"
mens_teams_output_path = script_dir / "teams" / "mens"
mens_teams_input_csv_path = script_dir / "MRegularSeasonDetailedResults.csv"
mens_teams_input_cities_csv_path = script_dir / "MGameCities.csv"

df = pd.read_csv(womens_teams)
print(len(df.index))

# Data.split_csv_by_teams(mens_teams_input_cities_csv_path, mens_teams_input_csv_path, mens_teams_output_path)

# iterate through WTeams.csv
# iterate through MGameCities.csv - get every game a team was involved in into a separate team csv file, list in desc order so the last games will be first in the list(build momentum from last 15 games)
  # iterate through MRegularSeasonDetailedResults.csv
    # compare Season, DayNum, WTeamID, LTeamID == Season, DayNum, WTeamID, LTeamID

""" mens_years_merger = MergeColumns(mens_years_output_path)
mens_years_merger.add_file_columns(mens_regular_season_csv_path, ['ID', 'Name'])

mens_output_path = script_dir / "mens_combined_columns.csv"
womens_output_path = script_dir / "womens_combined_columns.csv"

womens_years_output_path = script_dir / "years" / "womens_years_combined_columns.csv"
womens_regular_season_csv_path = script_dir / "WRegularSeasonDetailedResults.csv"
womens_tourney_csv_path = script_dir / "WNCAATourneyDetailedResults.csv" """

# mens_merger = MergeColumns(mens_output_path)

  # 2. Add files and the columns you want from each
  # Example: Take 'ID' and 'Name' from users.csv, 'Salary' from finance.csv
  # merger.add_file_columns('users.csv', ['ID', 'Name'])
  # merger.add_file_columns('finance.csv', ['Salary'])

  # 3. Perform the merge
  # merger.merge_to_csv()

# Load the data, and separate the target
# Get the directory of the current file

# womens_merger = MergeColumns(mens_output_path)

"""
iowa_file_path = script_dir / "train.csv"
home_data = pd.read_csv(iowa_file_path)
y = home_data.SalePrice

# Create X (After completing the exercise, you can return to modify this line!)
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']

# Select columns corresponding to features, and preview the data
X = home_data[features] """
# print(X.head())
# print(y.head())
