import time
import config
import requests
import plyer
class player:
    def __init__(self, name, id, summoner_id):
        self.id = id
        self.name = name
        self.summoner_id = summoner_id
        self.current_game = None

headers = {'X-Riot-Token': config.RIOT_API_KEY}

def get_nicknames():
    is_ended = False
    nicks = []
    while is_ended == False:
        nick = input('Enter nickname: ')
        tag = input('Enter tag: ')
        nicks.append(f'{nick}#{tag}')
        is_last = False
        while is_last == False:
            check = input('Do you want to add more?(y/n) ')
            if check == 'y':
                is_last = True
            elif check == 'n':
                print(nicks)
                return nicks

players = []

def load_player(players_Name):
    players_nick = players_Name.split('#')[0]
    players_tag = players_Name.split('#')[1]
    url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{players_nick}/{players_tag}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        summoner_id =  requests.get(f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{response.json()["puuid"]}', headers=headers).json()['id']
        print(response.json().get('puuid'))
        players.append(player(players_Name, response.json().get('puuid'), summoner_id))
        print(f'{players_Name} loaded - {response.json()["puuid"]} - {summoner_id}')
        plyer.notification.notify(title='LoL', message=f'{players_Name} loaded', app_name='Lol_Checker', app_icon='/Users/piotrgorny/Downloads/lol.png')
        return None
    else:
        raise Exception('Something is wrong')

def check_player_status():
    for p in players:
        if p.current_game == 'justEnded':
            p.current_game = None
            continue
        url = f'https://eun1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{p.id}'
        response = requests.get(url, headers=headers)
        print(p.current_game)
        if response.status_code == 200:
            if p.current_game == None:
                plyer.notification.notify(title='LoL', message=f'{p.name} is playing LoL', app_name='Lol_Checker')
            p.current_game = response.json()['gameId']
        elif response.status_code == 404:
            if p.current_game != None:
                get_info(p.id, p.name, p.current_game, p.summoner_id)
                p.current_game = None
    return 'checked'

def get_info(playerId, playerName, gameId, summonerId):
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/EUN1_{gameId}'
    response = requests.get(url, headers=headers)
    r2 = requests.get(f'https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}', headers=headers)
    tier = ''
    rank = ''
    lp = ''
    for i in r2.json():
        if i['queueType'] == 'RANKED_SOLO_5x5':
            tier = i['tier']
            rank = i['rank']
            lp = i['leaguePoints']
    if response.status_code == 200:
        for p in response.json()['info']['participants']:
            if p['summonerId'] == summonerId:
                champ = p['championName']
                k = p['kills']
                d = p['deaths']
                a = p['assists']
                if p['win'] == True:
                    plyer.notification.notify(title='LoL', message=f'{playerName} won! ({tier} {rank} - {lp}LP)! {k}/{d}/{a} - {champ}', app_name='Lol_Checker')
                    print('win msg sent')
                elif p['win'] == False:
                    plyer.notification.notify(title='LoL', message=f'{playerName} lost! ({tier} {rank} - {lp}LP)! {k}/{d}/{a} - {champ}', app_name='Lol_Checker')
                    print('lost msg sent')
                for p in players:
                    if p.id == playerId:
                        p.current_game = 'justEnded'
                        break
                return
            else:
                print('something is not working')
    else:
        time.sleep(30)
        get_info(playerId, playerName, gameId, summonerId)

def main():
    nicks = get_nicknames()
    for n in nicks:
        load_player(n)
    while True:
        check_player_status()
        print('checked')
        time.sleep(15)

if __name__ == '__main__':
    main()
