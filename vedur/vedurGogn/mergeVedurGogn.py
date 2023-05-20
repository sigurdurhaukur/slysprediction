import pandas as pd
import os
import glob

year = 2007
directory = "vedurGogn"
os.makedirs(directory, exist_ok=True)

wfilename = "allarStodvar.csv"

all_files = glob.glob("stod*.csv")
output_data = pd.DataFrame(
    columns=["ár", "mán", "t"], dtype=int
)  # Create an empty DataFrame for output

while year < 2024:
    yearly_data = []
    for month in range(1, 13):
        total_temp = 0
        count = 0

        for filename in all_files:
            data = pd.read_csv(
                filename, delimiter=",", names=["ár", "mán", "t"], skiprows=1
            )

            filtered_data = data.query("ár == @year and mán == @month")
            # print(filtered_data)
            t_values = data["t"].dropna()

            total_temp += float(t_values.sum())
            count += len(t_values)

        avg_temperature = total_temp / count if count > 0 else None
        print(avg_temperature)
        yearly_data.append({"ár": year, "mán": month, "t": avg_temperature})

    year_data_df = pd.DataFrame(yearly_data, columns=["ár", "mán", "t"])
    output_data = pd.concat([output_data, year_data_df], ignore_index=True)

    year += 1

output_data.to_csv(wfilename, index=False, mode="a", header=False)
