import requests
import pandas as pd
import time
#n+1 = 43205
max_requests = 43205
# max_requests = 10 + 1
dates = []
x = requests.get("https://map.is/webservice/proxies/usQueryHTML.php?nid=1")

start_time = time.time()
for i in range(1,max_requests):
    try:
        x = requests.get("https://map.is/webservice/proxies/usQueryHTML.php?nid=" + str(i))
        if ("dagsetning" in x.text):
            texti = x.text

            date = texti[texti.find("dagsetning")+14:texti.find("dagsetning")+21    ] #Slicear út dagsetninguna YYYY-MM

            # print("Date: " + date)
            dates.append(date)
    except:
        pass

end_time = time.time()

duration = end_time - start_time
print("Duration: " + str(duration))
# dates = sorted(dates, key=lambda x: pd.to_datetime(x))

print("Length:", len(dates))
# print(dates)

def count_occurrences(lst):
    occurrences = {}
    for item in lst:
        occurrences[item] = occurrences.get(item, 0) + 1
    return occurrences

print()
result = count_occurrences(dates)
print(result)

