import requests
import pandas as pd
import json

req = requests.get('https://community-api.coinmetrics.io/v4/timeseries/asset-metrics?assets=btc&'
                   'metrics=CapRealUSD,CapMrktCurUSD&limit_per_asset=10').json()
req = str(req['data'])
req = req.replace("\'", "\"")
#req = req.replace("[", "")
#req = req.replace("]", "")
req = json.loads(req)
print(req)
#nupl = int(req['CapMrktCurUSD'])

nupl = []
for i in range(len(req)):
    #nupl = nupl.append(float(req[i]['CapMrktCurUSD']) - float(req[i]['CapRealUSD']))/float(req[i]['CapMrktCurUSD'])
    nupl.append((float(req[i]['CapMrktCurUSD'])-float(req[i]['CapRealUSD']))/float(req[i]['CapMrktCurUSD']))
    #print(req[i]['time'])
nupl = json.loads(str(nupl))

df = pd.DataFrame.from_dict(req)

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

df.columns = ['Asset', 'Time', 'Realized Cap', 'Market Cap']
df = (df[['Time', 'Realized Cap', 'Market Cap']])
#print(df.to_string(index=False))
#print(req['CapMrktCurUSD'])