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

we_puuid = 'u87ngPILQjl0DmYOKApYcGxmIDmbOdQPyYEtnU0uiwgaQuk5AzUUkRah_KwqyboTXQhvyNAp1Mku2A'
Wi_puuid = 'KxCyeGbUMQxRAl1LLaZgTCpo4oPoPiMUuL_0o9Zvz_hY_rG9h9tWRUL7LlyuQruByoH2Ipu0-AwFjA'
n_puuid = '9yRQ7Jo6ZLew0T6ncD3DK4sphF8MMikSusPS_0m3gCSrQlkqmnCOOVSwlbnBIUBXWK8DSDeDmDMJ9g'
g_puuid = '5dHOu8jj81awpqdbJDPl_02XmHbxqVFjBG7osyQFHx_eTPYZkZd3ewx60bYTvZtIZsOwGmobp7syUA'
r_puuid = 'SJewCCsiGM0XIkOM0G6hwoHOJBXcA7KYwo2wGv6rAj0_CuAVo40T3RRmi6HMeo9VAoOYoD5vRu9IBQ'

class player:
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.current_game = None

players = [player('wenox', 'bPhWJ3ijRtBskxzH6-7S13LqlJ1QW3vyZ_6qe4CKitINLSw'),
           player('Wiertek', '3raTIgEJPjozdjALl0k_CnmvW3n_0RQCBGNRl3m5244E6MI'),
           player('Nadzieja', 'vqfKoNKt-OPs7MB1f0mC0hF2iFD--tfQC0lUa5i4D0n1-5Q'),
           player('Gloobus', 'QGJJvkcD6uXdC39XZaQBZmkRRXepLUEpUWw78ALq73kU4CE'),
           player('Ryjek', '4WEc3lvm3xFNMOiUXxuNSrgB-Sc-wycYZIpaUQp5UnB_TXI')]

def check_player_status():
    headers = {
        'X-Riot-Token': config.RIOT_API_KEY
    }
    for p in players:
        url = f'https://eun1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{p.id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200: 
            if p.current_game == None:
                send_facebook_message(f'Powodzenia {p.name}!')
            p.current_game = response.json()['gameId']
            print('wtoś gro')
            print(p.current_game)
        elif response.status_code == 404:
            if p.current_game != None:
                get_info(p.id, p.name, p.current_game)
                p.current_game = None

def get_info(playerId, playerName, gameId):
    headers = {
        'X-Riot-Token': config.RIOT_API_KEY
    }
    url = f'https://europe.api.riotgames.com/lol/match/v5/matches/EUN1_{gameId}'
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code == 200:
        for p in response.json()['info']['participants']:
            if p['summonerId'] == playerId:
                if p['win'] == True:
                    send_facebook_message(f'Gratulacje {playerName}! Dobra robota. :)')
                    print('win msg sent')
                elif p['win'] == False:
                    send_facebook_message(f'{playerName}, następnym razem Ci się uda!')
                    print('lost msg sent')
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
    login_to_facebook(config.email, config.password )
    print('logged in')
    while True:
        check_player_status()
        time.sleep(30)

if __name__ == '__main__':
    main()