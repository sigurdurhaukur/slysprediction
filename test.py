import requests
import pandas as pd
import time
#n+1 = 43205
# max_requests = 43205
max_requests = 20 + 1

dates = []
x = requests.get("https://map.is/webservice/proxies/usQueryHTML.php?nid=1")

start_time = time.time()
for i in range(1,max_requests):
    url = "https://map.is/webservice/proxies/usQueryHTML.php?nid=" + str(i)
    x = requests.get(url)
    print("trying", url, "dagsetning" in x.text)
    if ("dagsetning" in x.text):
        texti = x.text

        date = texti[texti.find("dagsetning")+14:texti.find("dagsetning")+21    ] #Slicear út dagsetninguna YYYY-MM

        # print("Date: " + date)

        if (i == 3):
            previous_date = dates[i]
            print(previous_date, date, previous_date == date)
            if(previous_date != date):
                # new date
                accidents_amount = len(dates)
                dates = []

                data = data.append({previous_date: accidents_amount})

                f = open("data.txt", "a")
                f.write(data)
                f.close()

                print("Date: " + date + " Accidents: " + str(accidents_amount))

        dates.append(date)


end_time = time.time()

duration = end_time - start_time
print("Duration: " + str(duration))

