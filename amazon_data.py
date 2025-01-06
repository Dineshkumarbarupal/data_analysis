import requests

url = "https://real-time-amazon-data.p.rapidapi.com/seller-products"

querystring = {"seller_id":"A02211013Q5HP3OMSZC7W","country":"US","page":"1","sort_by":"RELEVANCE"}

headers = {
	"x-rapidapi-key": "9a623cdfcemsh9266ff7a3a527eap14f3d6jsnce6b2e1a1e5d",
	"x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()
print(type(data))
