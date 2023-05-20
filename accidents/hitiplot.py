import matplotlib.pyplot as plt
import numpy as np

def main():
    (a,b) = np.loadtxt('accidents\\hiti.csv',delimiter=",",dtype=int).T
    hiti = a.tolist()
    slys = b.tolist()
    plt.plot(hiti,slys)
    plt.xlabel("Hitastig í °C")
    plt.ylabel("Fjöldi slysa")
    plt.show()

main()