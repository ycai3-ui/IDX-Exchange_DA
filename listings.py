# IDX Exchange Data Analyst Internship
# Script: listings.py
# Purpose: Load and concatenate all monthly CRMLSListing CSV files,
#          filter to Residential only, and save as listings.csv
#
# Row counts:
# Before concat: 29 files
# After concat: 930,308 rows
# After Residential filter: 591,976 rows

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

listing_files = get_best_files(folder, 'CRMLSListing')
print(f"Found {len(listing_files)} Listing files")

listing_dfs = []
for f in listing_files:
    df = pd.read_csv(os.path.join(folder, f), low_memory=False)
    listing_dfs.append(df)
listings = pd.concat(listing_dfs, ignore_index=True)
print(f"After concat: {listings.shape[0]:,} rows")

listings_residential = listings[listings['PropertyType'] == 'Residential']
print(f"After Residential filter: {listings_residential.shape[0]:,} rows")

listings_residential.to_csv(os.path.join(output_folder, 'listings.csv'), index=False)
print("Done! listings.csv saved successfully.")
