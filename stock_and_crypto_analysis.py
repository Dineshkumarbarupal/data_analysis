import requests

url = "https://tradingview-ta-api-technical-analysis.p.rapidapi.com/get_symbols_from_exchange"

querystring = {"exchange":"NASDAQ"}

headers = {
	"x-rapidapi-key": "9a623cdfcemsh9266ff7a3a527eap14f3d6jsnce6b2e1a1e5d",
	"x-rapidapi-host": "tradingview-ta-api-technical-analysis.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())