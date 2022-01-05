import requests
import json
import pandas as pd

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'countrycode': '304',
    'authorization': 'Bearer',
    'langcode': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36',
    'content-type': 'application/json',
}

data = '{"soft":"Sw"}'
response_base = requests.post('https://api.battle.pokemon-home.com/cbd/competition/rankmatch/list', headers=headers, data=data)
#response_baseにシーズンごとのデータとなるjsonファイルを取得

#念のため、pokemon.jsonという名前でファイル出力
with open("pokemon.json","w",encoding="UTF-8") as f:
    f.write(response_base.text)

data=json.loads(response_base.text)
num_new_season=len(data["list"])
info_new_season=data["list"][str(num_new_season)]
for i in info_new_season:
    if info_new_season[i]["rule"]==0:
        info_single={"id":i,"rst":str(info_new_season[i]["rst"]),"ts2":str(info_new_season[i]["ts2"])}
    elif info_new_season[i]["rule"]==1:
        info_double={"id":i,"rst":str(info_new_season[i]["rst"]),"ts2":str(info_new_season[i]["ts2"])}

adress = "https://resource.pokemon-home.com/battledata/ranking/"+info_single["id"]+"/"+info_single["rst"]+"/"+info_single["ts2"]+"/pokemon"
headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36',
    'content-type': 'application/json',
}
response = requests.get(adress, headers=headers)
with open("pokemons_ranking.json","w",encoding="UTF-8") as f:
  f.write(response.text)

poke_df = pd.read_csv("poke_id.csv", encoding="UTF-8")
Home_poke =pd.DataFrame()
with open("pokemons_ranking.json","r") as f:
    json_read = json.load(f)
    num = 0
    for x in json_read:
        list=[]
        num = num + 1
        list.append(num)
        id = poke_df[poke_df["id"]==int(x["id"])]
        name = id[id["リージョン"]==int(x["form"])]
        list.append(name.iloc[0,3])
        Home_poke = Home_poke.append([list])

Home_poke.to_csv("pokeHome_ranking.csv",encoding="shift-jis")