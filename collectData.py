import requests
import json
import time
import math


api_key = "RGAPI-319b0dc4-9951-4f47-b325-f72048b36636"

"""
TEST FILES:
with open("match1.json") as file:
    match = json.load(file)
with open("champion.json") as file:
    champion_data = json.load(file)
with open("diamond1League1.json") as file:
    diamond_1 = json.load(file)
with open("MatchHistory.json") as file:
    match_history = json.load(file)
"""

def getLeague(division, page=1):
    if division == "d":
        URL = "https://na1.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/DIAMOND/I?page=" + str(page) + "&api_key=" + api_key
        out = requests.get(URL)

    if division == "m":
        URL = "https://na1.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
        out = requests.get(URL)

    if division == "g":
        URL = "https://na1.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
        out = requests.get(URL)

    if division == "c":
        URL = "https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=" + api_key
        out = requests.get(URL)

    return out.json()

def getSummonerData(summoner_name):
    URL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + str(summoner_name) + "?api_key=" + api_key
    out = requests.get(URL)
    return out.json()

def getMatchHistory(account_id):
    URL = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + str(account_id) + "?api_key=" + api_key
    out = requests.get(URL)
    return out.json()

def getMatch(game_id):
    URL = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(game_id) + "?api_key=" + api_key
    out = requests.get(URL)
    return out.json()

def getChampionsPicked(match_json):
    blue_side = []
    red_side = []

    for i in range(len(match_json['participants'])):
        if i < (len(match_json['participants'])/2):
            blue_side.append(match_json["participants"][i]["championId"])
        else:
            red_side.append(match_json["participants"][i]["championId"])

    out = [blue_side] + [red_side]
    return out

def getTeamsAndWinner(match_json):
    winner = "None"
    if match_json["teams"][0]["win"] == "Win":
        winner = "Blue"
    elif match_json["teams"][1]["win"] == "Win":
        winner = "Red"

    return ([getChampionsPicked(match_json),winner])

def appendLeague(league_json):
    with open("Challenger.txt", "a+") as file:
        for summoner in league_json["entries"]:
            player = getSummonerData(str(summoner["summonerName"]))
            file.write(str(player["accountId"]) + "\n")
            print("summoner: " + str(player["name"]))
            time.sleep(2)


def getTeamsLast4Games(account_id):
    history = getMatchHistory(account_id)
    games = []
    for i in range(4):
        game_id = history["matches"][i]["gameId"]
        match = getMatch(game_id)
        if "teams" not in match.keys():
            continue
        games.append(getTeamsAndWinner(match))

    return (games)

with open("Challenger.txt") as infile, open("ChallengerChampAndWin.txt", "a+") as outfile:
    file = infile.readlines()
    count = 0
    threshold = 0
    length = len(file)
    for lines in file:

        if count < threshold:
            print("Skipping Summoner " + str(count))
            count += 1
            continue


        teams = getTeamsLast4Games(lines[0:-1])
        outfile.write(str(teams) + "\n")
        print("Summoner " + str(count) + "        " + lines[0:-1])
        count += 1
        time.sleep(10)
