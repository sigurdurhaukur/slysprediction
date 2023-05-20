import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_accidents_vs_temp():
    (a, b) = np.loadtxt("accidents\\hiti.csv", delimiter=",", dtype=int).T
    hiti = a.tolist()
    slys = b.tolist()
    plt.plot(hiti, slys)
    plt.xlabel("Hitastig í °C")
    plt.ylabel("Fjöldi slysa")
    plt.show()


def plot_accidents_vs_wind():
    data = pd.read_csv(
        "./vindur.csv",
        delimiter=",",
        names=["wind speed", "amount of accidents"],
        skiprows=1,
    )

    # drop empty wind speed
    data = data.dropna()

    print(data)
    wind_speed = data["wind speed"]
    amount_of_accidents = data["amount of accidents"]
    # reverse the order of the data
    wind_speed = wind_speed[::-1]
    amount_of_accidents = amount_of_accidents[::-1]

    plt.plot(wind_speed, amount_of_accidents)
    plt.xlabel("Vindur í m/s")
    plt.ylabel("Fjöldi slysa")
    plt.show()


plot_accidents_vs_wind()
