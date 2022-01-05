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

#最新シーズンのシングルとダブルのbaseデータのうち、次のAPIをたたくのに必要なid,rst,ts2を出力dictに保存
data=json.loads(response_base.text)
num_new_season=len(data["list"])
info_new_season=data["list"][str(num_new_season)]
for i in info_new_season:
    if info_new_season[i]["rule"]==0:
        info_single={"id":i,"rst":str(info_new_season[i]["rst"]),"ts2":str(info_new_season[i]["ts2"])}
    elif info_new_season[i]["rule"]==1:
        info_double={"id":i,"rst":str(info_new_season[i]["rst"]),"ts2":str(info_new_season[i]["ts2"])}

#ポケモンのデータは5つのjsonファイルに保存されるのでそれらをpokemons_filex.jsonとして保存。
for x in range(1,6):
    adress = "https://resource.pokemon-home.com/battledata/ranking/"+info_single["id"]+"/"+info_single["rst"]+"/"+info_single["ts2"]+"/pdetail-"+str(x)
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36',
        'content-type': 'application/json',
    }

    response = requests.get(adress, headers=headers)
    with open("pokemons_file"+str(x)+".json","w",encoding="UTF-8") as f:
        f.write(response.text)

#技、ポケモン名、アイテムのNoと名称の対応表を読み込み。(なぜかpoke_idだけUTF-8でcsvファイル作りました。)
move_df = pd.read_csv("move_id.csv",encoding="shift-jis")
poke_df = pd.read_csv("poke_id.csv", encoding="UTF-8")
item_df = pd.read_csv("item_id.csv",encoding="shift-jis")

#先ほど保存したjsonファイルを読み込み、jsonファイルを展開してpandasデータフレームに格納。
Home_poke =pd.DataFrame()
Home_poke2 = pd.DataFrame()
for y in range(1,6):
    with open("pokemons_file"+str(y)+".json","r") as f:
        json_read = json.load(f)
        #ポケモンidで展開
        for x in json_read:
            id = poke_df[poke_df["id"]==int(x)]
            #リージョンで展開してポケモン名をlistとlist2に格納
            for y in json_read[x]:
                list=[]
                list2=[]
                name = id[id["リージョン"]==int(y)]
                list.append(name.iloc[0,3])
                list2.append(name.iloc[0,3])
                #技名で展開しlistに格納。全技を格納したら、Home_pokeに格納
                for z in json_read[x][y]["temoti"]["waza"]:
                    move = move_df[move_df["id"]==int(z["id"])]
                    list.append(move.iloc[0,2])
                    list.append(z["val"])
                Home_poke = Home_poke.append([list])
                #持ち物で展開し、list2に格納。全持ち物を格納したら、Home_poke2に格納
                for z in json_read[x][y]["temoti"]["motimono"]:
                    item = item_df[item_df["id"]==int(z["id"])]
                    list2.append(item.iloc[0,2])
                    list2.append(z["val"])
                Home_poke2 = Home_poke2.append([list2])

            
#Home_pokeとHome_poke2のカラムに名称を付けてcsvとして保存。
Home_poke.columns = ["ポケモン名","技1","割合1","技2","割合2","技3","割合3","技4","割合4","技5","割合5","技6","割合6","技7","割合7","技8","割合8","技9","割合9","技10","割合10"]
Home_poke.to_csv("pokeHome_move.csv",encoding="shift-jis")
Home_poke2.columns = ["ポケモン名","アイテム1","割合1","アイテム2","割合2","アイテム3","割合3","アイテム4","割合4","アイテム5","割合5","アイテム6","割合6","アイテム7","割合7","アイテム8","割合8","アイテム9","割合9","アイテム10","割合10"]
Home_poke2.to_csv("pokeHome_item.csv",encoding="shift-jis")