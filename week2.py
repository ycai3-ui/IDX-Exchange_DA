# IDX Exchange Data Analyst Internship
# Script: week2.py
# Purpose: Dataset structuring, missing value analysis, and EDA on sold dataset
#
# Deliverable:
# - Unique property types and filtering logic
# - Null count summary table
# - Columns with >90% missing values flagged
# - Numeric distribution summary for ClosePrice, LivingArea, DaysOnMarket
# - EDA questions answered

import pandas as pd
import os

output_folder = "/Users/caiyufei/Desktop/Intern/IDX Exchange Unpaid Intern"

# Load data from listings.py and sold.py output
print("Loading data...")
listings = pd.read_csv(os.path.join(output_folder, 'listings.csv'), low_memory=False)
sold = pd.read_csv(os.path.join(output_folder, 'sold.csv'), low_memory=False)
print(f"Listings: {listings.shape[0]:,} rows, {listings.shape[1]} columns")
print(f"Sold:     {sold.shape[0]:,} rows, {sold.shape[1]} columns")

# Part 1: Data Structure
print("\n── SOLD: Data Types ──")
print(sold.dtypes)

# Part 2: Missing Value Analysis
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

# Part 3: Numeric Distribution Summary
key_fields = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
print("\n── Numeric Distribution Summary (SOLD) ──")
for field in key_fields:
    if field in sold.columns:
        print(f"\n{field}:")
        print(sold[field].describe(percentiles=[.10, .25, .50, .75, .90, .95, .99]))

# Part 4: EDA Questions
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

print("\nDone! week2 analysis complete.")
