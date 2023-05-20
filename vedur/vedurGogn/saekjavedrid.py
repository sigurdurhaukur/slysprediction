import pandas as pd
import requests
from bs4 import BeautifulSoup
import io
import os

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
