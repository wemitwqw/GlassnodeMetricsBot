import requests
import pandas as pd
import json

req = requests.get('https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&'
                   'metrics=CapRealUSD,CapMrktCurUSD&limit_per_asset=2').json()
print(req)
req = str(req['data'])
req = req.replace("\'", "\"")
req = req.replace("[", "")
req = req.replace("]", "")
print(req)
req = json.loads(req)
#print(req['time'])
#nupl = int(req['CapMrktCurUSD'])


'''json.loads(req)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df = pd.DataFrame.from_dict(req)

df.columns = ['Asset', 'Time', 'Realized Cap', 'Market Cap']
print(df.to_string(index=False))'''