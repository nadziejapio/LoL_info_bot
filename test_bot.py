import pytest
import requests_mock
import bot_3

def test_load_player():
    with requests_mock.Mocker() as m:
        m.get('https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/test/test', json={'puuid': 'test_puuid'})
        m.get('https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/test_puuid', json={'id': 'test_id'})
        bot_3.load_player('test#test')
        assert len(bot_3.players) == 1
        assert bot_3.players[0].id == 'test_puuid'

def test_check_player_status():
    with requests_mock.Mocker() as m:
        m.get('https://eun1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/test_puuid', json={'gameId': 'test_gameId'})
        player = bot_3.player('test#test', 'test_puuid', 'test_id')
        bot_3.players.append(player)
        bot_3.check_player_status()
        assert bot_3.players[0].current_game == 'test_gameId'

def test_get_info():
    with requests_mock.Mocker() as m:
        m.get('https://europe.api.riotgames.com/lol/match/v5/matches/EUN1_test_gameId', json={
            'info': {
                'participants': [
                    {
                        'summonerId': 'test_id',
                        'championName': 'test_champion',
                        'kills': 10,
                        'deaths': 2,
                        'assists': 8,
                        'win': True
                    }
                ]
            },
            
        })
        m.get('https://eun1.api.riotgames.com/lol/league/v4/entries/by-summoner/test_id', json=[
            {'queueType': 'RANKED_SOLO_5x5',
            'tier': 'test_tier',
            'rank': 'test_rank',
            'leaguePoints': 90
        }])
        player = bot_3.player('test#test', 'test_puuid', 'test_id')
        bot_3.players.append(player)
        bot_3.get_info('test_puuid', 'test#test', 'test_gameId', 'test_id')
        assert bot_3.players[0].current_game == 'justEnded'
    