import requests

currency = "btc"
req = requests.get('https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=%s&'
                       'metrics=CapRealUSD,CapMrktCurUSD&limit_per_asset=5' % currency).json()
