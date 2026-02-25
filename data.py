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
    files = glob.glob(os.path.join('competitions', competition, '*.csv'))
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
    for file_path in glob.glob(os.path.join('competitions', competition, '*.csv')):
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
    csv_path = os.path.join('competitions', competition, item)

    # Read the data from the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path, nrows=500)

    # Convert the DataFrame to an HTML table string
    # index=False prevents pandas from adding an extra column for the index
    return df.to_html(index=False, classes="table table-striped", justify='unset')

  # Takes the columns results and separates the results by the distinct years.
  def years():
    pass

  # Takes the years results and separates the results by the distinct teams.
  def teams():
    pass
