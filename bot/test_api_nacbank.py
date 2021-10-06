import requests
import json


col = ('Cur_Abbreviation','Cur_Name','Cur_OfficialRate','Cur_Scale','Date')
s = requests.Session()
r = s.get("https://www.nbrb.by/api/exrates/rates?periodicity=0")
r = json.loads(r.text)
print(r)

for i in r:
    for j in col:
        if j in i:
            print(i[j])

