# Week 2-3 - Dataset Structuring, Validation and Mortgage Rate Enrichment
# This script:
# 1. Loads listings.csv and sold.csv from Week 1
# 2. Inspects data structure (shape, dtypes, null counts)
# 3. Flags columns with >90% missing values
# 4. Produces numeric distribution summary for key fields
# 5. Answers EDA questions about the dataset
# 6. Fetches FRED 30-year mortgage rate data
# 7. Merges mortgage rates onto both datasets by year-month
# 8. Saves enriched datasets as new CSVs

import pandas as pd
import os
output_folder = "Users/caiyufei/Desktop/Intern/IDX Exchange Unpaid Intern"

#Load data from week1
print("Loading data...")
listings = pd.read_csv(os.path.join(output_folder, 'listings.csv'), low_memory=False)
sold = pd.read_csv(os.path.join(output_folder, 'sold.csv'), low_memory=False)
print(f"Listings: {listings.shape[0]:,} rows, {listings.shape[1]} columns")
print(f"Sold:     {sold.shape[0]:,} rows, {sold.shape[1]} columns")

#Data Structure
print("\n── SOLD: Data Types ──")
print(sold.dtypes)

#Missing Value Analysis
print("\n── SOLD: Missing Value Report ──")
null_counts = sold.isnull().sum()
null_pct = (null_counts / len(sold) * 100).round(2)
missing_report = pd.DataFrame({
    'null_count': null_counts,
    'null_pct': null_pct
})
missing_report = missing_report[missing_report['null_count'] > 0].sort_values('null_pct', ascending=False)
print(missing_report.to_string())

print("\n── Columns with >90% missing (SOLD) ──")
high_missing = missing_report[missing_report['null_pct'] > 90]
print(high_missing.to_string())

#Numeric Distribution Summary
key_fields = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
print("\n── Numeric Distribution Summary (SOLD) ──")
for field in key_fields:
    if field in sold.columns:
        print(f"\n{field}:")
        print(sold[field].describe(percentiles=[.10, .25, .50, .75, .90, .95, .99]))

#EDA Questions
print("\n── EDA: PropertyType breakdown (SOLD) ──")
print(sold['PropertyType'].value_counts())

print("\n── EDA: Median and Mean ClosePrice ──")
print(f"Median ClosePrice: ${sold['ClosePrice'].median():,.0f}")
print(f"Mean ClosePrice:   ${sold['ClosePrice'].mean():,.0f}")

print("\n── EDA: % sold above vs below list price ──")
if 'ClosePrice' in sold.columns and 'ListPrice' in sold.columns:
    above = (sold['ClosePrice'] >= sold['ListPrice']).sum()
    below = (sold['ClosePrice'] < sold['ListPrice']).sum()
    print(f"Sold at or above list price: {above:,} ({above/len(sold)*100:.1f}%)")
    print(f"Sold below list price:       {below:,} ({below/len(sold)*100:.1f}%)")

print("\n── EDA: Top 10 counties by median ClosePrice ──")
if 'CountyOrParish' in sold.columns:
    county_median = sold.groupby('CountyOrParish')['ClosePrice'].median().sort_values(ascending=False)
    print(county_median.head(10))

#Mortgage Rate Enrichment
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
print(f"Null rates in sold after merge:     {sold_with_rates['rate_30yr_fixed'].isnull().sum()}")
print(f"Null rates in listings after merge: {listings_with_rates['rate_30yr_fixed'].isnull().sum()}")

# Preview
print("\nSample of sold with rates:")
print(sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())

# Save enriched datasets
sold_with_rates.to_csv(os.path.join(output_folder, 'sold_with_rates.csv'), index=False)
listings_with_rates.to_csv(os.path.join(output_folder, 'listings_with_rates.csv'), index=False)
print("\nDone! sold_with_rates.csv and listings_with_rates.csv saved successfully.")
