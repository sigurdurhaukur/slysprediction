import requests
from xml.etree import ElementTree as ET
from datetime import date


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
