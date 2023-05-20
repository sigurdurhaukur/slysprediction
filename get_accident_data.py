import requests
import pandas as pd
import time


def save_data(dates):
    try:
        # Create a list of dates and counts
        date_list = []
        count_list = []
        for item in dates:
            date = list(item.keys())[0]
            count = item[date]
            date_list.append(date)
            count_list.append(count)

        # Create a DataFrame from the lists
        df = pd.DataFrame({"Date": date_list, "Amount of accidents": count_list})

        # Save data to CSV
        df.to_csv("data.csv", index=False)
    except Exception as e:
        print("Error saving data", e)


def get_date(text):
    date = text[
        text.find("dagsetning") + 14 : text.find("dagsetning") + 21
    ]  # Slicear út dagsetninguna YYYY-MM
    return date


def main():
    max_requests = 43205
    dates = []
    url = "https://map.is/webservice/proxies/usQueryHTML.php?nid="
    start_time = time.time()

    for id in range(1, max_requests + 1):
        try:
            print("getting data with id:", id)
            response = requests.get(url + str(id))
            response = response.text

            if "dagsetning" in response:
                date = get_date(response)

                # if new date
                if date not in [list(d.keys())[0] for d in dates]:
                    data = {date: 1}
                    dates.append(data)
                    print("new date", date)

                    # save data to csv whenever a new date is found
                    save_data(dates)

                # if date already exists
                else:
                    for d in dates:
                        if date in d.keys():
                            d[date] += 1
                    print("incrementing date", date, "count:", d[date])

        except Exception as e:
            if e == KeyboardInterrupt:
                save_data(dates)
                break

            print("Error", e)

    end_time = time.time()
    duration = end_time - start_time
    print("Duration:", duration)
    print(dates)


if __name__ == "__main__":
    main()
