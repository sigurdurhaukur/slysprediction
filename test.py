import requests
import pandas as pd
import time
#n+1 = 43205
# max_requests = 43205
max_requests = 1000 + 1

dates = []

start_time = time.time()
for i in range(140,max_requests):
    try:
        url = "https://map.is/webservice/proxies/usQueryHTML.php?nid=" + str(i)
        x = requests.get(url)
        print("trying", url, "dagsetning" in x.text)

        if ("dagsetning" in x.text):
            texti = x.text

            date = texti[texti.find("dagsetning")+14:texti.find("dagsetning")+21    ] #Slicear út dagsetninguna YYYY-MM

            # print("Date: " + date)

            dates.append(date)

            previous_date = dates[i - 1]
            print(i, previous_date, date, previous_date != date)
            if(previous_date != date):
                # new date
                accidents_amount = len(dates)
                # dates = []

                data = data.append({previous_date: accidents_amount})

                f = open("data.txt", "a")
                f.write(data)
                f.close()

                print("Date: " + date + " Accidents: " + str(accidents_amount))
    except Exception as e:
        if e == KeyboardInterrupt:
            break
        print("Error")
        pass


end_time = time.time()

duration = end_time - start_time
print("Duration: " + str(duration))

