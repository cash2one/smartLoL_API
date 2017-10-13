import requests
import os.path



CHAMPIONS_SQUARE_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}' #version_name
CHAMPIONS_SPLASH_URL = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_{}.jpg' #champkey_skinum
PROFILE_ICONS_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/profileicon/{}.png' #version_id
CHAMPIONS_LOADING_URL = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_{}.jpg' #champkey_skinum
PASSIVE_ABILITIES_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/passive/{} ' #version_name
ABILITIES_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}' #version_name
MASTERIES_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/mastery/{}' #version_id
RUNES_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/rune/{}' #version_id

BASE_URL ="https://euw1.api.riotgames.com/lol/"


def get_response(url):
    """
    HTTP Request header example:
    {
        "Origin": "https://developer.riotgames.com",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Riot-Token": "RGAPI-660b2c5b-3ff0-447c-b676-e8c61cc60b28",
        "Accept-Language": "es-ES,es;q=0.8,en;q=0.6",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
    }
    """
    key = open(os.path.abspath("api-key")).readline()[:-1]
    headers = {"X-Riot-Token": key}

    data = requests.get(url, headers=headers)
    if data.status_code == 200:
        return data.json()
    else:
        raise requests.HTTPError(data)


if __name__ == '__main__':
    pass
