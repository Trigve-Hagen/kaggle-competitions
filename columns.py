import pandas as pd
import os

class MergeColumns:

  def __init__(self, output_file='subdata/combined.csv'):
    self.output_file = output_file
    self.dataframes = []

  # Reads a CSV file, selects specific columns, and prepares them for merging.
  def add_file_columns(self, file_path, columns_to_keep=None):

    try:
      # Read only the necessary columns to save memory
      if columns_to_keep is None:
        df = pd.read_csv(file_path)
      else:
        df = pd.read_csv(file_path, usecols=columns_to_keep)

      # Optional: Rename columns to include source file if needed
      # df = df.rename(columns={col: f"{os.path.basename(file_path)}_{col}" for col in df.columns})

      self.dataframes.append(df)
      print(f"Successfully processed: {file_path}")
    except ValueError as e:
      print(f"Error processing {file_path}: {e}. Columns might not exist.")
    except FileNotFoundError:
      print(f"File not found: {file_path}")

  # Merges all processed columns and saves to the destination file.
  # axis=1 (default) for horizontal stacking, 0 for vertical.
  def merge_to_csv(self, axis=1):

    if not self.dataframes:
      print("No dataframes to merge.")
      return

    # Combine the dataframes horizontally
    final_df = pd.concat(self.dataframes, axis=axis)

    # Save to CSV
    final_df.to_csv(self.output_file, index=False)
    print(f"Successfully created: {self.output_file}")

# --- Example Usage ---
# if __name__ == "__main__":
  # 1. Initialize the class
  # merger = MergeColumns('final_destination.csv')

  # 2. Add files and the columns you want from each
  # Example: Take 'ID' and 'Name' from users.csv, 'Salary' from finance.csv
  # merger.add_file_columns('users.csv', ['ID', 'Name'])
  # merger.add_file_columns('finance.csv', ['Salary'])

  # 3. Perform the merge
  # merger.merge_to_csv()
