import pandas as pd
import os
import glob

year = 2007
directory = 'vedurGogn'
os.makedirs(directory, exist_ok=True)

wfilename = 'allarStodvar.csv'

all_files = glob.glob("stod*.csv")

# Concatenate all the CSV files into a single DataFrame
data_list = []
for filename in all_files:
    data = pd.read_csv(filename, delimiter=',', names=['ár', 'mán', 't'], skiprows=1)
    data_list.append(data)
all_data = pd.concat(data_list)

output_data = pd.DataFrame(columns=['ár', 'mán', 't'],)  # Create an empty DataFrame for output

while year < 2024:
    yearly_data = []
    for month in range(1, 13):
        # Filter data by year and month and calculate the average temperature
        filtered_data = all_data.query('ár == @year and mán == @month')
        avg_temperature = filtered_data['t'].mean()
        yearly_data.append({'ár': year, 'mán': month, 't': avg_temperature})

    year_data_df = pd.DataFrame(yearly_data, columns=['ár', 'mán', 't'])
    output_data = pd.concat([output_data, year_data_df], ignore_index=True)

    year += 1

output_data.to_csv(wfilename, index=False, mode='a', header=False)
