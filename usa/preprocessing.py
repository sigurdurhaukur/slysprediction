import pandas as pd

# Load the data
data = pd.read_csv(
    "./US-data.csv"
)  # Replace "your_data.csv" with the path to your dataset

# Preprocess the data
data["Start_Time"] = pd.to_datetime(data["Start_Time"])  # Convert to datetime if needed
data = data.dropna()
temperature = data["Temperature(C)"].round()
wind_speed = data["Wind_Speed(m/s)"].round()

# Define the bins for temperature and wind speed
temperature_bins = [-float("inf"), 0, 5, 10, 15, 20, 25, 30, 35, float("inf")]
wind_speed_bins = [-float("inf"), 0, 5, 10, 15, 20, 25, 30, 35, float("inf")]

# Assign labels to each bin
temperature_labels = [
    "Extremely Cold",
    "Very Cold",
    "Slightly Cold",
    "Cold",
    "Moderate",
    "Slightly Hot",
    "Very Hot",
    "Extremely Hot",
]
wind_speed_labels = [
    "Extremely low",
    "Very low",
    "Slightly low",
    "low",
    "Moderate",
    "Slightly high",
    "Very high",
    "Extremely high",
]

# Group the data by binned temperature and wind speed and count the number of accidents
data["Temperature_Bin"] = pd.cut(
    data["Temperature(C)"], bins=temperature_bins, labels=temperature_labels
)
data["Wind_Speed_Bin"] = pd.cut(
    data["Wind_Speed(m/s)"], bins=wind_speed_bins, labels=wind_speed_labels
)

grouped_data = (
    data.groupby(["Temperature_Bin", "Wind_Speed_Bin"])
    .size()
    .reset_index(name="Amount_of_Accidents")
)

print(grouped_data)

# save as csv file
grouped_data.to_csv("processed-usa-data.csv", index=False)
