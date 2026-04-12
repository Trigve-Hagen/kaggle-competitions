import pandas as pd
import glob
import os

class Data:

  def get_subdirectories(directory):
    subdirs = []
    if os.path.isdir(directory):
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                subdirs.append(entry)
    return subdirs

  # Reads all CSV files in a directory and returns a set of unique column names.
  def get_all_column_names(competition):
    # Use glob to find all files ending with .csv in the specified directory
    files = glob.glob(os.path.join('competitions', competition, 'dataset', '*.csv'))
    all_columns = set()

    # Iterate through each file
    for file in files:
        # Read only the header (nrows=0) for efficiency
        df = pd.read_csv(file, nrows=0)
        # Add column names to the set to ensure uniqueness
        all_columns.update(df.columns.tolist())

    # Convert the set back to a list for standard use
    return sorted(list(all_columns))

  def get_all_columns_and_names(competition, category):
    # Initialize an empty dictionary to store the results
    csv_columns_map = {}
    # Use glob to find all CSV files in the current directory
    # Change '*.csv' to the specific path if your files are in another folder
    for file_path in glob.glob(os.path.join('competitions', competition, 'dataset', '*.csv')):
      # Read only the header (first row) of the CSV file
      try:
          df_header = pd.read_csv(file_path, nrows=0)
          # Extract column names and convert to a list
          column_names = list(df_header.columns)
          # Get just the filename (without the path) for the dictionary key
          filename = os.path.basename(file_path)
          # Add to the dictionary
          if category == filename[0] or category == 'all':
            csv_columns_map[filename] = column_names
      except Exception as e:
          print(f"Error reading {file_path}: {e}")

    # Return the resulting dictionary
    return csv_columns_map

  def get_data(competition, item):
    # Construct the path to the CSV file
    csv_path = os.path.join('competitions', competition, 'dataset', item)

    # Read the data from the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path, nrows=15)

    # Convert the DataFrame to an HTML table string
    # index=False prevents pandas from adding an extra column for the index
    return df.to_html(index=False, classes="table table-striped", justify='unset')

  # Takes the columns results and separates the results by the distinct years.
  def split_csv_by_year(input_file, column_name, output_path):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Ensure the year column is treated as a string to extract the year correctly if it's a date object
    # If the column contains only 4-digit integers, this step can be skipped
    # Example for date formats (adjust the format string if needed):
    # df[column_name] = pd.to_datetime(df[column_name]).dt.year.astype(str)

    # Get unique years from the specified column
    unique_years = df[column_name].unique()

    # Create a separate CSV for each unique year
    for year in unique_years:
        # Filter the DataFrame for the current year
        df_filtered = df[df[column_name] == year]

        # Define the output file name
        output_file = output_path / f"{column_name}_{year}.csv"

        # Write the filtered data to a new CSV file
        df_filtered.to_csv(output_file, index=False)
        print(f"Created: {output_file} with {len(df_filtered)} rows")

  # Takes the teams and details and separates them by the distinct teams.
  def split_csv_by_teams(teams_file, details_file, output_dir="team_games"):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. Read the CSV files into pandas DataFrames
    try:
        teams_df = pd.read_csv(teams_file)
        details_df = pd.read_csv(details_file)
    except FileNotFoundError as e:
        print(e)
        return

    # 2. Merge the DataFrames on the common 'team_id' column
    # Assuming the team ID column is named 'team_id' in both CSVs.
    # Adjust 'how' parameter as needed (e.g., 'inner', 'left')
    merged_df = pd.merge(teams_df, details_df, on='team_id', how='inner')

    # 3. Group the merged data by team name (or team_id)
    # Assuming there is a 'team_name' column in the teams file
    team_groups = merged_df.groupby('team_name')

    # 4. Iterate through each group and save to a separate CSV file
    for team_name, group_df in team_groups:
        # Sanitize team name for filename (e.g., replace spaces with underscores)
        filename = f"{team_name.replace(' ', '_')}_games.csv"
        filepath = os.path.join(output_dir, filename)

        # Save the group DataFrame to a CSV file
        # index=False prevents pandas from writing the DataFrame index as a column
        group_df.to_csv(filepath, index=False)
        print(f"Saved game details for {team_name} to {filepath}")
        # check_connection(website["name"], website["url"])


    # Create a separate CSV for each unique year
    """ for year in unique_years:
        # Filter the DataFrame for the current year
        df_filtered = df[df[column_name] == year]

        # Define the output file name
        output_file = output_path / f"{column_name}_{year}.csv"

        # Write the filtered data to a new CSV file
        df_filtered.to_csv(output_file, index=False)
        print(f"Created: {output_file} with {len(df_filtered)} rows") """


# 1. Initialize the class
  # merger = MergeColumns('final_destination.csv')

  # 2. Add files and the columns you want from each
  # Example: Take 'ID' and 'Name' from users.csv, 'Salary' from finance.csv
  # merger.add_file_columns('users.csv', ['ID', 'Name'])
  # merger.add_file_columns('finance.csv', ['Salary'])

  # 3. Perform the merge
  # merger.merge_to_csv()
