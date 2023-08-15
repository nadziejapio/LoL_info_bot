import time
import config
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

option = Options()
option.add_argument('--disable-notifications')
driver = webdriver.Chrome(options = option)

class player:
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.current_game = None

headers = {'X-Riot-Token': config.RIOT_API_KEY}

#enter nicknames here
nicks = ['wenox', 'Nadzieja', 'Gloobus', 'Wiertek', 'Ryjek']

players = []

def load_player(players_Name):
    url = f'https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{players_Name}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        players.append(player(players_Name, response.json()['id']))


def check_player_status():
    for p in players:
        if p.current_game == 'justEnded':
            p.current_game = None
            continue
        url = f'https://eun1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{p.id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200: 
            if p.current_game == None:
                send_facebook_message(f'Powodzenia {p.name}!')
                print('wtoś gro')
                print(p.current_game)
            p.current_game = response.json()['gameId']
        elif response.status_code == 404:
            if p.current_game != None:
                get_info(p.id, p.name, p.current_game)
                p.current_game = None

def get_info(playerId, playerName, gameId):
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/EUN1_{gameId}'
    response = requests.get(url, headers=headers)
    r2 = requests.get(f'https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/{playerId}', headers=headers)
    for i in r2.json():
        if i['queueType'] == 'RANKED_SOLO_5x5':
            tier = i['tier']
            rank = i['rank']
            lp = i['leaguePoints']
    print(response)
    if response.status_code == 200:
        for p in response.json()['info']['participants']:
            if p['summonerId'] == playerId:
                champ = p['championName']
                k = p['kills']
                d = p['deaths']
                a = p['assists']
                if p['win'] == True:
                    send_facebook_message(f'Gratulacje {playerName} ({tier} {rank} - {lp}LP)! Dobra robota :) {k}/{d}/{a} - {champ}')
                    print('win msg sent')
                elif p['win'] == False:
                    send_facebook_message(f'{playerName}, następnym razem Ci się uda!')
                    print('lost msg sent')
                for p in players:
                    if p.id == playerId:
                        p.current_game = 'justEnded'
                        break
                return
            else:
                print('coś nie pykło')
    else:
        time.sleep(30)
        get_info(playerId, playerName, gameId)

def login_to_facebook(email, password):
    driver.get("https://www.facebook.com/")
    time.sleep(2)
    
    cookies = driver.find_element(By.CSS_SELECTOR, "button[data-cookiebanner='accept_button']")
    cookies.click()

    email_box = driver.find_element(By.ID, "email")
    email_box.send_keys(email)
    
    password_box = driver.find_element(By.ID, "pass")
    password_box.send_keys(password)
    
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()

    time.sleep(5)  # Wait for login

def send_facebook_message(message):
    driver.get(config.threadUrl)
    time.sleep(10)
    message_box = driver.find_element(By.CSS_SELECTOR, "div[role='textbox']")
    message_box.click()
    message_box.send_keys(message)
    message_box.send_keys(Keys.RETURN)

def main():
    for n in nicks:
        load_player(n)
    login_to_facebook(config.email, config.password )
    print('logged in')
    while True:
        check_player_status()
        time.sleep(5)

if __name__ == '__main__':
    main()