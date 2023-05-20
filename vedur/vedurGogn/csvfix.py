import pandas as pd
import glob

# Specify the pattern matching for CSV files
file_pattern = "*.csv" 

# Get a list of all CSV files
csv_files = glob.glob(file_pattern)

for file in csv_files:
    # Read CSV file, skipping the first 2 rows
    df = pd.read_csv(file, skiprows=2)
    
    # Write the data back to CSV
    df.to_csv(file, index=False)
