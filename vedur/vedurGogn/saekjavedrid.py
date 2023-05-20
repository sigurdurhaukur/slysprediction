import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import glob

stodvarlisti = []

with open('stodvalinkar.txt', 'r') as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

for link in soup.find_all('a'):
    stodvarlisti.append(link.get('href'))

for i in range(0, len(stodvarlisti)):
    url = stodvarlisti[i]
    response = requests.get(url)
    data = pd.read_csv(io.StringIO(response.text), delimiter='\t',names=['stöð','ár','mán','t','tx','txx','txxD1','tn','tnn','tnnD1','rh','r','rx','rxD1','p','n','sun','f'])

    # Write to the file
    filename = f'stod{i+1}.csv'
    data[['ár', 'mán', 't']].to_csv(filename, index=False)

# Specify the pattern matching for CSV files
file_pattern = "*.csv" 

# Get a list of all CSV files
csv_files = glob.glob(file_pattern)

for file in csv_files:
    # Read CSV file, skipping the first 2 rows
    df = pd.read_csv(file, skiprows=2)
    
    # Write the data back to CSV
    df.to_csv(file, index=False)
