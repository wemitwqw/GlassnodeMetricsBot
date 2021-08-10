import requests

glassAPI = "1wOnIiKwiAZ03yVSoJjUsm4J1gA"
req = requests.get('https://api.glassnode.com/v1/metrics/addresses/sending_to_exchanges_count',
    params={'a': 'BTC', 's': 1483228801, 'u': 1485004801, 'i': '24h', 'api_key': glassAPI})