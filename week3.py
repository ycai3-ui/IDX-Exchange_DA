# IDX Exchange Data Analyst Internship
# Script: week3.py
# Purpose: Fetch FRED 30-year mortgage rate data, merge onto sold and listings
#          datasets by year-month key, validate merge, save enriched CSVs
#
# Deliverable:
# - FRED MORTGAGE30US series fetched and resampled to monthly averages
# - Merged onto both sold and listings datasets using year_month key
# - Validated: 0 null rate values after merge
# - Output: sold_with_rates.csv and listings_with_rates.csv

import pandas as pd
import os

output_folder = "/Users/caiyufei/Desktop/Intern/IDX Exchange Unpaid Intern"

# Load data
print("Loading data...")
listings = pd.read_csv(os.path.join(output_folder, 'listings.csv'), low_memory=False)
sold = pd.read_csv(os.path.join(output_folder, 'sold.csv'), low_memory=False)
print(f"Listings: {listings.shape[0]:,} rows")
print(f"Sold:     {sold.shape[0]:,} rows")

# Fetch FRED Mortgage Rate Data
print("\n── Fetching FRED Mortgage Rate Data ──")
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
mortgage = pd.read_csv(url, parse_dates=['observation_date'])
mortgage.columns = ['date', 'rate_30yr_fixed']

# Resample weekly to monthly average
mortgage['year_month'] = mortgage['date'].dt.to_period('M')
mortgage_monthly = (
    mortgage.groupby('year_month')['rate_30yr_fixed']
    .mean()
    .reset_index()
)
print(f"Mortgage rate data fetched: {len(mortgage_monthly)} months")

# Create year_month key on MLS datasets
sold['year_month'] = pd.to_datetime(sold['CloseDate']).dt.to_period('M')
listings['year_month'] = pd.to_datetime(listings['ListingContractDate']).dt.to_period('M')

# Merge
sold_with_rates = sold.merge(mortgage_monthly, on='year_month', how='left')
listings_with_rates = listings.merge(mortgage_monthly, on='year_month', how='left')

# Validate
print(f"\nNull rates in sold after merge:     {sold_with_rates['rate_30yr_fixed'].isnull().sum()}")
print(f"Null rates in listings after merge: {listings_with_rates['rate_30yr_fixed'].isnull().sum()}")

# Preview
print("\nSample of sold with rates:")
print(sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())

# Save
sold_with_rates.to_csv(os.path.join(output_folder, 'sold_with_rates.csv'), index=False)
listings_with_rates.to_csv(os.path.join(output_folder, 'listings_with_rates.csv'), index=False)
print("\nDone! sold_with_rates.csv and listings_with_rates.csv saved successfully.")
