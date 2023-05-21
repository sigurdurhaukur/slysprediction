from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import torch
import requests
from xml.etree import ElementTree as ET
import torch.nn as nn
import joblib
import numpy as np
import requests


def fetch_weather():
    url = "http://xmlweather.vedur.is/?op_w=xml&type=forec&lang=is&view=xml&ids=1;2&params=T;F"
    response = requests.get(url)

    # Check that the request was successful
    if response.status_code != 200:
        print(f"Request failed with status {response.status_code}")
        return

    # Parse the XML response
    tree = ET.fromstring(response.content)

    return tree


def get_temp_and_wind_speed():
    # Call the function to fetch weather data
    root = fetch_weather()

    # Extract the values between <T> and </T> tags
    t_values = [
        int(t.text) for t in root.findall(".//forecast/T") if t.text is not None
    ]
    f_values = [
        int(f.text) for f in root.findall(".//forecast/F") if f.text is not None
    ]  # Added for wind speed

    # Calculate the sum and count for temperature and wind speed
    t_sum = sum(t_values)
    t_count = len(t_values)

    f_sum = sum(f_values)  # Added for wind speed
    f_count = len(f_values)  # Added for wind speed

    # Calculate the average temperature and wind speed, and print the result
    average_temperature = t_sum / t_count if t_count > 0 else 0
    print(f"Average temperature: {average_temperature:.1f}°C")

    average_wind_speed = f_sum / f_count if f_count > 0 else 0  # Added for wind speed
    print(f"Average wind speed: {average_wind_speed:.1f} m/s")  # Added for wind speed

    return average_temperature, average_wind_speed


def get_live_temp_and_wind_speed():
    url = "https://iws.isavia.is/weather/BIRK"

    response = requests.get(url)
    response = response.json()

    temperature = response["data"]["rwyTdz31"]["tempSurface"]["value"]
    wind_speed = response["data"]["rwyTdz31"]["windSpeed"]["value"]
    return temperature, wind_speed


def standardize_input_isl(temperature):
    # standardize input
    x_mean = torch.tensor([4.3893])
    x_std = torch.tensor([4.1323])

    average_temperature = torch.tensor(temperature, dtype=torch.float32).reshape(-1, 1)

    return (average_temperature - x_mean) / x_std


def standardize_input_usa(temperature, wind_speed):
    # standardize input
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

    # Encode the current temperature and wind speed values into one-hot encoding
    temperature_index = next(
        (i for i, bin in enumerate(temperature_bins) if temperature <= bin),
        len(temperature_bins) - 1,
    )
    wind_speed_index = next(
        (i for i, bin in enumerate(wind_speed_bins) if wind_speed <= bin)
    )

    # hacky way to solve out of index error
    if wind_speed_index == len(wind_speed_bins) - 1:
        wind_speed_index -= 1

    encoded_temperature = [0] * len(temperature_labels)
    encoded_temperature[temperature_index] = 1

    encoded_wind_speed = [0] * len(wind_speed_labels)
    encoded_wind_speed[wind_speed_index] = 1

    # Combine the encoded values into a single input tensor
    input_tensor = torch.tensor(
        [encoded_temperature + encoded_wind_speed], dtype=torch.float32
    )

    return input_tensor


# Load the models
usa_model = joblib.load("../models/usa-model.pt")
isl_model = joblib.load("../models/isl-model.pt")


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with appropriate domain(s)
    allow_methods=["*"],
    allow_headers=["*"],
)


# for more frequent updates
@app.get("/prediction/isl/live")
def predict_isl_live():
    live_temperature, live_wind_speed = get_live_temp_and_wind_speed()

    if live_temperature and live_wind_speed:
        standardized_new_data = standardize_input_isl(live_temperature)

        # predict
        prediction = isl_model.predict(standardized_new_data)
        prediction_value = prediction[0].item()

        average_accidents_per_month = 246
        percentage_deviation = (
            (prediction_value - average_accidents_per_month)
            / average_accidents_per_month
            * 100
        )
    else:
        live_temperature = None
        live_wind_speed = None
        prediction_value = None
        percentage_deviation = None
        average_accidents_per_month = None
    return {
        "temp": live_temperature,
        "wind": live_wind_speed,
        "prediction": prediction_value,
        "percentage_deviation": percentage_deviation,
        "average_accidents_per_month": average_accidents_per_month,
    }


# for more frequent updates
@app.get("/prediction/usa/live")
def predict_isl_live():
    live_temperature, live_wind_speed = get_live_temp_and_wind_speed()

    if live_temperature and live_wind_speed:
        input_tensor = standardize_input_usa(live_temperature, live_wind_speed)

        # Make the prediction using the trained model
        prediction = usa_model.predict(input_tensor)  # in log space
        prediction = np.exp(prediction) - 1e-5

        # scale down to 1 month
        predicted = prediction / 48
        average_accidents_per_month = 4216.75
        # Print the predicted amount of accidents
        percentage_deviation = (
            (predicted.item() - average_accidents_per_month)
            / average_accidents_per_month
            * 100
        )

        prediction_value = predicted.item()
    else:
        live_temperature = None
        live_wind_speed = None
        prediction_value = None
        percentage_deviation = None
        average_accidents_per_month = None
    return {
        "temp": live_temperature,
        "wind": live_wind_speed,
        "prediction": prediction_value,
        "percentage_deviation": percentage_deviation,
        "average_accidents_per_month": average_accidents_per_month,
    }


@app.get("/prediction/isl")
def predict_isl():
    current_average_temperature, current_average_wind_speed = get_temp_and_wind_speed()

    standardized_new_data = standardize_input_isl(current_average_temperature)

    # predict
    prediction = isl_model.predict(standardized_new_data)
    prediction_value = prediction[0].item()

    average_accidents_per_month = 246
    percentage_deviation = (
        (prediction_value - average_accidents_per_month)
        / average_accidents_per_month
        * 100
    )
    return {
        "temp": current_average_temperature,
        "wind": current_average_wind_speed,
        "prediction": prediction_value,
        "percentage_deviation": percentage_deviation,
        "average_accidents_per_month": average_accidents_per_month,
    }


@app.get("/prediction/usa")
def predict_isl():
    current_average_temperature, current_average_wind_speed = get_temp_and_wind_speed()

    input_tensor = standardize_input_usa(
        current_average_temperature, current_average_wind_speed
    )

    # Make the prediction using the trained model
    prediction = usa_model.predict(input_tensor)  # in log space
    prediction = np.exp(prediction) - 1e-5

    # scale down to 1 month
    predicted = prediction / 48
    average_accidents_per_month = 4216.75
    # Print the predicted amount of accidents
    print(f"Predicted amount of accidents: {predicted.item():.2f}")
    percentage_deviation = (
        (predicted.item() - average_accidents_per_month)
        / average_accidents_per_month
        * 100
    )
    print(
        "percent deviation from average accidents per month: ",
        str(round(percentage_deviation, 3)) + "%",
    )

    return {
        "temp": current_average_temperature,
        "wind": current_average_wind_speed,
        "prediction": prediction.item(),
        "percentage_deviation": percentage_deviation,
        "average_accidents_per_month": average_accidents_per_month,
    }
