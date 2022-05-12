#!/usr/bin/env python
# coding: utf-8

# In[20]:


import requests
import json
import os
import time
import pickle
from pathlib import Path


# In[21]:


api_key = "RGAPI-18f77fdf-3e3b-487a-b3e1-ea9027d243df"


# In[22]:


end_point = "league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5"


# In[23]:


url = "https://na1.api.riotgames.com/lol/"+ end_point +"?api_key=" + api_key
x = requests.get(url)
print(x)


# In[24]:


json_object = json.loads(x.text)

json_formatted_str = json.dumps(json_object, indent=2)
players = json_object["entries"]
print((players[0]))
sorted_players = sorted(players, key=lambda k: k['leaguePoints'])


# In[27]:


# count = 0
# last_time = 0
def make_call(url):
#     delta_time = (time.time() - last_time)
#     if count == 19 and delta_time < 20:
        
#     if count == 99 and delta_time < 120:   
    response = requests.get(url)
    time.sleep(1)
    while response.status_code != 200:
        print('sleepy time')
        response = requests.get(url)
        time.sleep(2)
    return response


# In[28]:


# convert to list of puuids
good_puuids = []
for player in sorted_players:
    summonerName = player['summonerName']
    end_point = "/lol/summoner/v4/summoners/by-name/"+(summonerName).replace(" ", "%20")
    url = "https://na1.api.riotgames.com"+ end_point +"?api_key=" + api_key
    x = make_call(url)
    print(x)
    json_object = json.loads(x.text)
    puuid = json_object["puuid"]
    good_puuids.append(puuid)


# In[29]:


good_player_path = Path('data/') / 'good_players.pkl'
with open(good_player_path, 'wb') as f:
    pickle.dump(good_puuids, f)


# In[30]:


good_players = pickle.load(open(good_player_path, 'rb')); 


# In[31]:


good_players[:10]


# In[35]:


num_matches = 5
requests_per_summoner = 1 + num_matches # summonerToID + matchList + numMatches

def get_games_by_id(puuid):
    data_path = f'data/{puuid}'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    match_end = f"/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num_matches}&type=ranked"
    url = "https://americas.api.riotgames.com"+ match_end +"&api_key=" + api_key
    x = make_call(url)
    print(url, x)
    matchIds = x.json()
    for matchId in matchIds:
        print(matchId)
        match = f"/lol/match/v5/matches/{matchId}"
        url = "https://americas.api.riotgames.com"+ match +"?api_key=" + api_key
        
        match_request = make_call(url)
        with open(data_path + "/" + matchId +".json", 'w') as js:
            json.dump(match_request.json(), js)


# In[36]:


get_games_by_id(good_puuids[0])


# In[ ]:


for player in good_puuids:
    print(player)
    get_games(player['summonerName'])


# In[ ]:


import shutil
data_path = Path('data/')
count = 0
for summoner_folder in data_path.iterdir():
    if str(summoner_folder.name).startswith('.') or summoner_folder.name == 'good_players.pkl':
        continue
    # user_id = summoner_folder.name
    # if user_id not in sorted_player_ids:
    #     shutil.rmtree(summoner_folder)
    for game_file in summoner_folder.iterdir():
        with open(game_file, 'r') as f:
            game_json = json.load(f)

            metadata = game_json['metadata']
            participants = metadata['participants']
            for p in participants:
                if p not in good_puuids:
                    count += 1
                    get_games_by_id(p)


# In[ ]:


count


# In[ ]:




