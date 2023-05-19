import requests
import pandas as pd
#n+1 = 43205
x = requests.get("https://map.is/webservice/proxies/usQueryHTML.php?nid=1")
for i in range(1,43205):
    x = requests.get("https://map.is/webservice/proxies/usQueryHTML.php?nid=" + str(i))
    if ("dagsetning" in x.text):
        texti = x.text
        (texti[texti.find("dagsetning")+14:texti.find("dagsetning")+24]) #Slicear út dagsetninguna YYYY-MM

