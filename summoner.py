from utils.riot_api_connection import get_response, BASE_URL, PROFILE_ICONS_URL, CHAMPIONS_SPLASH_URL
from database.setup import session, version
from database.models import Champions


def get_summoner_info(summoner_name):
    """
    given a summoner name, retun the following data:

    {
        "profileIconId": 1665,
        "name": "EspinoKiller",
        "summonerLevel": 30,
        "accountId": 228772786,
        "id": 89028317,
        "revisionDate": 1500131820000
    }
    :param summoner_name: the summoner name of a player
    :return a dictionary with the info
    """
    summoner_info = get_response(BASE_URL + 'summoner/v3/summoners/by-name/%s' % summoner_name)
    data = {
        'id': summoner_info['id'],
        'accountId': summoner_info['accountId'],
        'name': summoner_info['name'],
        'lvl': summoner_info['summonerLevel'],
        'icon': PROFILE_ICONS_URL.format(version, summoner_info['profileIconId'])
    }

    return data


def get_summoner_league(summoner_id):
    """
    given a summoner id, return the following data

    {
        "queueType": "RANKED_FLEX_SR",
        "hotStreak": false,
        "wins": 5,
        "veteran": false,
        "losses": 7,
        "playerOrTeamId": "89028317",
        "tier": "BRONZE",
        "playerOrTeamName": "EspinoKiller",
        "inactive": false,
        "rank": "II",
        "freshBlood": false,
        "leagueName": "Cho'Gath's Mercenaries",
        "leaguePoints": 0
    }
    :param summoner_id: the summoner id of a player, found in the returned data of get_summoner_info(summoner_name)
    :return a list of dictionaries with the leagues info
    """
    league_info = get_response(BASE_URL + 'league/v3/positions/by-summoner/%s' % summoner_id)
    leagues = []
    for league in league_info:
        data = {
            'league': league['queueType'],
            'tier': league['tier'],
            'rank': league['rank'],
            'hotStreak': league['hotStreak'],
            'freshBlood': league['freshBlood'],
            'veteran': league['veteran'],
            'wins': league['wins'],
            'losses': league['losses'],
            'points': league['leaguePoints']
        }
        leagues.append(data)

    return leagues


def get_summoner_top_champions(summoner_id):
    """
    given a summoner id, return the following data 5 times
    {
        "championLevel": 7,
        "chestGranted": true,
        "championPoints": 167601,
        "championPointsSinceLastLevel": 146001,
        "playerId": 23880012,
        "championPointsUntilNextLevel": 0,
        "tokensEarned": 0,
        "championId": 119,
        "lastPlayTime": 1497895907000
    }

    :param summoner_id: the summoner id of a player, found in the returned data of get_summoner_info(summoner_name)
    :return: a list of dictionaries with the info of the player's top champions
    """
    """
    url= BASE_URL + 'champion-mastery/v3/champion-masteries/by-summoner/%s' % summoner_id
    print(url)
    exit(1)
    """
    top_champions_info = get_response(BASE_URL + 'champion-mastery/v3/champion-masteries/by-summoner/%s' % summoner_id)
    top_champions = []
    for i in range(5):
        champion = top_champions_info[i]
        extra_info = session.query(Champions).get(champion['championId'])
        data = {
            'lvl': champion['championLevel'],
            'points': champion['championPoints'],
        }
        total_info = {**data, "name": extra_info.name, "title": extra_info.get_title(2), "img_url": CHAMPIONS_SPLASH_URL.format(extra_info.champ_key, 0)}
        top_champions.append(total_info)

    return top_champions


if __name__ == '__main__':
    print(get_summoner_top_champions('24785164'))
