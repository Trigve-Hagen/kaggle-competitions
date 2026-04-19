# https://www.youtube.com/watch?v=h-LGjJ_oANs

import os
from pathlib import Path
import pandas as pd

script_dir = Path(__file__).parent
DATASET = script_dir / "dataset" / "stock_data.csv"
df = pd.read_csv(DATASET)

print(df.head())

# (.venv)
# activate and install dependencies
# python -m training.stocks.newssentiment
