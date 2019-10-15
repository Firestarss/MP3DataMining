import json
import math

with open("champion.json") as file:
    champion_data = json.load(file)
with open("FullPlayerChampAndWin.txt") as file:
    players = file.readlines()

champion_picks = dict()
champion_wins = dict()
champion_win_rate = dict()
blue_red_advantage = [0,0]

for value in champion_data.keys():
    champion_picks[int(value)] = 0
    champion_wins[int(value)] = 0
    champion_win_rate[int(value)] = 50

def idToChampion(id_number):
    return champion_data[str(id_number)]

def getBlueTeam(match):
    return(match[0][0])

def getRedTeam(match):
    return(match[0][1])

def getWinner(match):
    return(match[1])

def getBlueWinRate(team_wins):
    return team_wins[0]/(team_wins[1]+team_wins[0])

def getRedWinRate(team_wins):
    return team_wins[1]/(team_wins[1]+team_wins[0])

def getCombinedWinrate(champions, team_color, team_wins):
    out = 0
    for champion in champions:
        out += champion_win_rate[champion]
    if team_color == "blue":
        out += getBlueWinRate(team_wins)
    if team_color == "red":
        out += getRedWinRate(team_wins)

    return out


for matches in players:
    matches = eval(matches)
    for match in matches:

        blue_team = getBlueTeam(match)
        red_team = getRedTeam(match)
        winner = getWinner(match)

        if winner == "None":
            continue

        if winner == "Blue":
            blue_red_advantage[0] += 1
            for value in blue_team:
                champion_wins[value] += 1

        if winner == "Red":
            blue_red_advantage[1] += 1
            for value in red_team:
                champion_wins[value] += 1

        for value in red_team:
            champion_picks[value] += 1

        for value in blue_team:
            champion_picks[value] += 1


for key in champion_win_rate:
    if champion_picks[key] > 0 and champion_wins[key] > 0:
        champion_win_rate[key] = (champion_wins[key]/champion_picks[key])*100

for key in champion_data:
    print(champion_data[key] + ": " + str(key))

print("\n\nPlease use the above list to match champions to their corresponding ID numbers.")

blue_input = []
red_input = []
for i in range(5):
    blue_input.append(int(input("Please input the ID number for BLUE side champion #" + str(i+1) + ": ")))
for i in range(5):
    red_input.append(int(input("Please input the ID number for RED side champion #" + str(i+1) + ": ")))

blue_win_chance = getCombinedWinrate(blue_input, "blue", blue_red_advantage)
red_win_chance = getCombinedWinrate(red_input, "red", blue_red_advantage)



if blue_win_chance > red_win_chance:
    print("\n\nI predict that the blue team will win!")
if blue_win_chance < red_win_chance:
    print("\n\nI predict that the red team will win!")
if blue_win_chance == red_win_chance:
    print("\n\nI can not predict this match.")

if input("\n\nDo you wish to see individual champion win rates? (y/n)\n") == "y":
    for key in champion_win_rate.keys():
        print(idToChampion(key) + ": " + str(champion_win_rate[key]) + " %")

    print("\nBlue Side: " + str(getBlueWinRate(blue_red_advantage)*100) + " %")
    print("Red Side: " + str(getRedWinRate(blue_red_advantage)*100) + " %")
