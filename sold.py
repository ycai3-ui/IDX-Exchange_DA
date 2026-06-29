# IDX Exchange Data Analyst Internship
# Script: sold.py
# Purpose: Load and concatenate all monthly CRMLSSold CSV files,
#          filter to Residential only, and save as sold.csv
#
# Row counts:
# Before concat: 29 files
# After concat: 613,842 rows
# After Residential filter: 412,131 rows

import pandas as pd
import os

folder = "/Users/caiyufei/Desktop/Intern/IDX Exchange Unpaid Intern/File Data"
output_folder = "/Users/caiyufei/Desktop/Intern/IDX Exchange Unpaid Intern"

def get_best_files(folder, prefix):
    all_files = [f for f in os.listdir(folder) if f.startswith(prefix) and f.endswith('.csv')]
    months = set()
    for f in all_files:
        name = f.replace(prefix, '').replace('_filled.csv', '').replace('.csv', '')
        if name.isdigit():
            months.add(name)
    best = []
    for month in sorted(months):
        filled = f"{prefix}{month}_filled.csv"
        original = f"{prefix}{month}.csv"
        if filled in all_files:
            best.append(filled)
        elif original in all_files:
            best.append(original)
    return best

sold_files = get_best_files(folder, 'CRMLSSold')
print(f"Found {len(sold_files)} Sold files")

sold_dfs = []
for f in sold_files:
    df = pd.read_csv(os.path.join(folder, f), low_memory=False)
    sold_dfs.append(df)
sold = pd.concat(sold_dfs, ignore_index=True)
print(f"After concat: {sold.shape[0]:,} rows")

sold_residential = sold[sold['PropertyType'] == 'Residential']
print(f"After Residential filter: {sold_residential.shape[0]:,} rows")

sold_residential.to_csv(os.path.join(output_folder, 'sold.csv'), index=False)
print("Done! sold.csv saved successfully.")
