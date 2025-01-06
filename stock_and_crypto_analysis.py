# exceeded monthly quota

import requests
import csv

url = "https://tradingview-ta-api-technical-analysis.p.rapidapi.com/get_symbols_from_exchange"
querystring = {"exchange": "NASDAQ"}

headers = {
    "x-rapidapi-key": "9a623cdfcemsh9266ff7a3a527eap14f3d6jsnce6b2e1a1e5d",
    "x-rapidapi-host": "tradingview-ta-api-technical-analysis.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()
print(data)
print(type(data))


# with open('output.txt', 'w') as file:   # Save data into text file
#     for key, value in data.items():
#         file.write(f'{key}: {value}\n')

# with open('output.txt', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for key, value in data.items():
#         writer.writerow([key, value])


file_name = "nasdaq_symbols.csv"

with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Code", "Name"]) 

    for item in data:
        writer.writerow([item.get("code", ""), item.get("name", "")])






