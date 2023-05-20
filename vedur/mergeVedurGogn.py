import pandas as pd
import os
import glob

year = 2007
directory = 'vedurGogn'
if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)

wfilename = 'allarStodvar.csv'

while(year <= 2023):
    for i in range(1, 13):  
        heildarHiti = 0
        cnt = 0
        all_files = glob.glob(os.path.join(directory, "stod*.csv"))
        
        for filename in all_files:
            data = pd.read_csv(filename, delimiter=',', names=['ár', 'mán', 't'])
            
            filtered_data = data[(data['ár'] == year) & (data['mán'] == i)]
            
            if not filtered_data.empty:
                t_values = filtered_data['t'].dropna()
                heildarHiti += t_values.sum()
                cnt += len(t_values)

        avg_temperature = heildarHiti / cnt if cnt > 0 else None
        output_data = pd.DataFrame({'ár': [year], 'mán': [i], 't': [avg_temperature]})
        output_data.to_csv(wfilename, index=False, mode='a', header=False)

    year += 1
