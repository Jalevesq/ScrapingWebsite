import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrape.private import file_path_to_save, unfilteredFolder, mergeFile

folder_path = file_path_to_save + unfilteredFolder

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

merged_data = pd.DataFrame()

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    merged_data = merged_data._append(df, ignore_index=True)

merged_data.to_csv(folder_path + mergeFile, index=False)

print(f"Merged data saved to '{mergeFile}'")