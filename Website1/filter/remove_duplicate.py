import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrape.private import file_path_to_save, mergeFile, unfilteredFolder, filteredFolder

folder_path_read = file_path_to_save + unfilteredFolder + mergeFile
folder_path_save = file_path_to_save + filteredFolder

merged_data = pd.read_csv(folder_path_read)
filtered_data = merged_data.drop_duplicates(subset=['Title', 'Image'], keep='first')
filtered_data.to_csv(folder_path_save + "filtered_data.csv", index=False)

print("Filtered data saved to 'filtered_data.csv'")