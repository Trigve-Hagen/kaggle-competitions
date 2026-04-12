# https://www.youtube.com/watch?v=oBMzGInnb5g

# what he ^ is doing
# what AI recomends
# what won the golds
# combine all three for next year
# Be ready >>>>>>!!!

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from columns import MergeColumns
from data import Data
import os

# RandomForestClassifier - Predicting discrete outcomes, such as identifying if
# an email is "spam" or "not spam". Using .predict_proba() provides the
# probability of a sample belonging to a class.

# RandomForestRegressor - Returns a continuous number, such as an estimated
# price, age, or quantity. Predicting numerical values, such as estimating the
# price of a house.

# 1. Initialize the class
script_dir = Path(__file__).parent.parent

mens_teams = script_dir / "MTeams.csv"
womens_teams = script_dir / "WTeams.csv"
sample_submissions = script_dir / "SampleSubmissionStage1.csv"
mens_teams_input_cities_csv_path = script_dir / "MGameCities.csv"

mens_seeds = script_dir / "MNCAATourneySeeds.csv"
mens_conferences = script_dir / "MTeamConferences.csv"
mens_regular_season_details = script_dir / "MRegularSeasonDetailedResults.csv"
mens_tourney_compact = script_dir / "MNCAATourneyCompactResults.csv"

mseeds = pd.read_csv(mens_seeds)
mconferences = pd.read_csv(mens_seeds)
mregular_season_details = pd.read_csv(mens_regular_season_details)
mtourney_compact = pd.read_csv(mens_tourney_compact)

win_teams = pd.DataFrame()
loose_teams = pd.DataFrame()

columns = [ 'Season', 'TeamID', 'Points', 'OppPoints', 'Loc', 'NumOT', 'FGM',
  'FGA', 'FGM3', 'FGA3', 'FTM', 'FTA', 'OR', 'DR', 'Ast', 'TO', 'Stl', 'Blk',
  'PF', 'OppFGM', 'OppFGA', 'OppFGM3', 'OppFGA3', 'OppFTM', 'OppFTA', 'OppOR',
  'OppDR', 'OppAst', 'OppTO', 'OppStl', 'OppBlk', 'OppPF' ]

win_teams[columns] = mregular_season_details[[ 'Season', 'WTeamID', 'WScore',
  'LScore', 'WLoc', 'NumOT', 'WFGM', 'WFGA', 'WFGM3', 'WFGA3', 'WFTM', 'WFTA',
  'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF', 'LFGM', 'LFGA', 'LFGM3',
  'LFGA3', 'LFTM', 'LFTA', 'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF' ]]

win_teams['Wins'] = 1
win_teams['Losses'] = 0

loose_teams[columns] = mregular_season_details[[ 'Season', 'LTeamID', 'LScore',
  'WScore', 'WLoc', 'NumOT', 'LFGM', 'LFGA', 'LFGM3', 'LFGA3', 'LFTM', 'LFTA',
  'LOR', 'LDR', 'LAst', 'LTO', 'LStl', 'LBlk', 'LPF', 'WFGM', 'WFGA', 'WFGM3',
  'WFGA3', 'WFTM', 'WFTA', 'WOR', 'WDR', 'WAst', 'WTO', 'WStl', 'WBlk', 'WPF' ]]

def change_loc(loc):
  if loc == 'H':
    return 'A'
  elif loc == 'A':
    return 'H'
  else:
    return 'N'

loose_teams['Loc'] = loose_teams['Loc'].apply(change_loc)

loose_teams['Wins'] = 0
loose_teams['Losses'] = 1

win_loose_teams = pd.concat([win_teams, loose_teams])
combined_teams = win_loose_teams.groupby(['Season', 'TeamID']).sum()
combined_teams['NumGames'] = combined_teams['Wins'] + combined_teams['Losses']

regular_season_input = pd.DataFrame()

regular_season_input['WinRatio'] = combined_teams['Wins'] / combined_teams['NumGames']
regular_season_input['PointPerGame'] = combined_teams['Points'] / combined_teams['NumGames']
regular_season_input['PointsAllowedPerGame'] = combined_teams['OppPoints'] / combined_teams['NumGames']
regular_season_input['PointsRatio'] = combined_teams['Points'] / combined_teams['OppPoints']
regular_season_input['OtsPerGame'] = combined_teams['NumOT'] / combined_teams['NumGames']

# Field Goals Made
# Field Goal Attempts
regular_season_input['FGPerGame'] = combined_teams['FGM'] / combined_teams['NumGames']
regular_season_input['FGRatio'] = combined_teams['FGM'] / combined_teams['FGA']
regular_season_input['FGAllowedPerGame'] = combined_teams['OppFGM'] / combined_teams['NumGames']

# Field Goals Made 3 pointers
# Field Goal Attempts 3 pointers
regular_season_input['FG3PerGame'] = combined_teams['FGM3'] / combined_teams['NumGames']
regular_season_input['FG3Ratio'] = combined_teams['FGM3'] / combined_teams['FGA3']
regular_season_input['FG3AllowedPerGame'] = combined_teams['OppFGM3'] / combined_teams['NumGames']

# Free Throws Made
# Free Throws Attempts
regular_season_input['FTPerGame'] = combined_teams['FTM'] / combined_teams['NumGames']
regular_season_input['FTRatio'] = combined_teams['FTM'] / combined_teams['FTA']
regular_season_input['FTAllowedPerGame'] = combined_teams['OppFTM'] / combined_teams['NumGames']

# Offensive Rebound
# Defensive Rebound
regular_season_input['ORRatio'] = combined_teams['OR'] / combined_teams['OR'] + combined_teams['OppDR']
regular_season_input['DRRatio'] = combined_teams['DR'] / combined_teams['DR'] + combined_teams['OppOR']

# Assists
regular_season_input['AstPerGame'] = combined_teams['Ast'] / combined_teams['NumGames']

# Turnovers
# Steals
# Blocks
# Personal Fouls
regular_season_input['TOPerGame'] = combined_teams['TO'] / combined_teams['NumGames']
regular_season_input['StlPerGame'] = combined_teams['Stl'] / combined_teams['NumGames']
regular_season_input['BlkPerGame'] = combined_teams['Blk'] / combined_teams['NumGames']
regular_season_input['PFPerGame'] = combined_teams['PF'] / combined_teams['NumGames']
# print(regular_season_input.describe())
# print(regular_season_input.isna().sum())

# four conferences
#   kaggle labeled them W X Y Z
#   for each conferences there is a ranking of 1 through 16
#   there is a chance that two 1s or 16s may compete. they are labeled A B
# 16 teams per conference
# winners of each conference compete
# final champion is the winner of the two conference titles
seed_dict = mseeds.set_index(['Season', 'TeamID'])
# print(seed_dict)

tourney_input = pd.DataFrame()

win_ids = mtourney_compact['WTeamID']
loss_ids = mtourney_compact['LTeamID']
season = mtourney_compact['Season']

winners = pd.DataFrame()
winners[['Season', 'Team1', 'Team2']] = mtourney_compact[['Season', 'WTeamID', 'LTeamID']]
winners['Result'] = 1

losers = pd.DataFrame()
losers[['Season', 'Team1', 'Team2']] = mtourney_compact[['Season', 'LTeamID', 'WTeamID']]
losers['Result'] = 0

tourney_input = pd.concat([winners, losers])

# we only have data in the season details starting
# from 2003 so we need to remove the rest
tourney_input = tourney_input[tourney_input['Season'] >= 2003].reset_index(drop=True)

# if 1 seed is playing 16 seed theres a good chance 1 seed will win
team1seeds = []
team2seeds = []

for x in range(len(tourney_input)):
  idx = (tourney_input['Season'][x], tourney_input['Team1'][x])
  seed = seed_dict.loc[idx].values[0]
  if len(seed) == 4:
    seed = int(seed[1:-1])
  else:
    seed = int(seed[1:])
  team1seeds.append(seed)

  idx = (tourney_input['Season'][x], tourney_input['Team2'][x])
  seed = seed_dict.loc[idx].values[0]
  if len(seed) == 4:
    seed = int(seed[1:-1])
  else:
    seed = int(seed[1:])
  team2seeds.append(seed)

tourney_input['Team1Seed'] = team1seeds
tourney_input['Team2Seed'] = team2seeds

# combine regular season with tounament data
# we need to compare team1 and team2 to predict the winner
# one way to compare is to subtract team2 from team1
# this is the input into the model
outscores = []
for x in range(len(tourney_input)):
  idx = (tourney_input['Season'][x], tourney_input['Team1'][x])
  team1score = regular_season_input.loc[idx]
  team1score['Seed'] = tourney_input['Team1Seed'][x]

  idx = (tourney_input['Season'][x], tourney_input['Team2'][x])
  team2score = regular_season_input.loc[idx]
  team2score['Seed'] = tourney_input['Team2Seed'][x]

  outscore = team1score - team2score
  outscore['Result'] = tourney_input['Result'][x]
  outscores.append(outscore)

outscores = pd.DataFrame(outscores)
# print(seed_dict.index.values)
# print(outscores)
# print(outscores.describe())

# correlate how effective the feature is when predicting
# High = good, Low = bad
corrs = round(outscores.corr(), 2)
# print(np.abs(corrs['Result']))
# plt.figure(figsize=(15,10))
# sns.heatmap(corrs)
# plt.show()

X = outscores[outscores.columns[:-1]].values
y = outscores['Result'].values

# can pull out by year here
np.random.seed(1)
idx = np.random.permutation(len(X))
train_idx = idx[:int(-.2*len(X))]
test_idx = idx[int(-.2*len(X)):]

X_train = X[train_idx]
X_test = X[test_idx]
y_train = y[train_idx]
y_test = y[test_idx]

mins = X_train.min(axis=0)
maxs = X_train.max(axis=0)

X_train = (X_train - mins) / (maxs - mins)
X_test = (X_test - mins) / (maxs - mins)

# print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

model = RandomForestClassifier(random_state=1)
model = model.fit(X_train, y_train)
print(model.score(X_test, y_test))
