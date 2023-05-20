import pandas as pd

# Load the data
data = pd.read_csv("./US-data.csv")

# Preprocess the data
data["Start_Time"] = pd.to_datetime(data["Start_Time"])  # Convert to datetime if needed
data = data.dropna()
temperature = data["Temperature(C)"].round()
wind_speed = data["Wind_Speed(m/s)"].round()

# Define the bins for temperature and wind speed
temperature_bins = [-float("inf"), -5, 0, 5, 10, 15, 20, 25, 30, 35, float("inf")]
wind_speed_bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, float("inf")]

# Assign labels to each bin
temperature_labels = [
    "Extremely Cold",
    "Very Cold",
    "Cold",
    "Slightly Cold",
    "Moderate Cold",
    "Moderate Hot",
    "Slightly Hot",
    "Hot",
    "Very Hot",
    "Extremely Hot",
]
wind_speed_labels = [
    "No Wind",
    "Very Low",
    "Low",
    "Slightly Low",
    "Moderate Low",
    "Moderate High",
    "Slightly High",
    "High",
    "Very High",
    "Extremely High",
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

# Save as a CSV file
grouped_data.to_csv("processed-usa-data.csv", index=False)
