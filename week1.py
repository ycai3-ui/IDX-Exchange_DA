# Week 1 - Monthly Dataset Aggregation
# IDX Exchange Data Analyst Internship
#
# This script:
# 1. Loads all available monthly CRMLSListing and CRMLSSold CSV files
# 2. Concatenates them into two combined datasets
# 3. Filters both to PropertyType == 'Residential' only
# 4. Saves the filtered datasets as listings.csv and sold.csv

import pandas as pd
import os

# folder path
folder = "/Users/caiyufei/Desktop/Intern/IDX Exchange Unpaid Intern/File Data"

# filled version is preferred if available, otherwise use original version
def get_best_files(folder, prefix):
    all_files = [f for f in os.listdir(folder) if f.startswith(prefix) and f.endswith('.csv')]
    # find all months
    months = set()
    for f in all_files:
        name = f.replace(prefix, '').replace('_filled.csv', '').replace('.csv', '')
        if name.isdigit():
            months.add(name)
    # for each month, prefer filled version
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
sold_files = get_best_files(folder, 'CRMLSSold')

print(f"found {len(listing_files)} Listing files")
print(listing_files)
print(f"found {len(sold_files)} Sold files")
print(sold_files)

# integrate all Listing files
listing_dfs = []
for f in listing_files:
    df = pd.read_csv(os.path.join(folder, f), low_memory=False)
    listing_dfs.append(df)
listings = pd.concat(listing_dfs, ignore_index=True)
print(f"\nintegrated Listing total rows: {len(listings)}")

# integrate all Sold files
sold_dfs = []
for f in sold_files:
    df = pd.read_csv(os.path.join(folder, f), low_memory=False)
    sold_dfs.append(df)
sold = pd.concat(sold_dfs, ignore_index=True)
print(f"integrated Sold total rows: {len(sold)}")

# filter to Residential only
listings_residential = listings[listings['PropertyType'] == 'Residential']
sold_residential = sold[sold['PropertyType'] == 'Residential']

print(f"\nListing before filter: {len(listings)} rows → after filter: {len(listings_residential)} rows")
print(f"Sold before filter: {len(sold)} rows → after filter: {len(sold_residential)} rows")

# save to CSV
output_folder = "/Users/caiyufei/Desktop/Intern/IDX Exchange Unpaid Intern"
listings_residential.to_csv(os.path.join(output_folder, 'listings.csv'), index=False)
sold_residential.to_csv(os.path.join(output_folder, 'sold.csv'), index=False)

print("\nDone! listings.csv and sold.csv saved successfully.")
