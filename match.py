from utils.riot_api_connection import get_response, BASE_URL
from database.models import Champions, Masteries, Runes, SummonerSpells
from database.setup import session

class MatchRequest:
    """
    Class to send request to riot games api for matches data
    :cvar platform: the objective region i.e. euw1
    :cvar language: the id of the desired language i.e. 2 for spanish
    """

    def __init__(self, platform, language):
        self.platform = platform
        self.language = language

    def get_summoner_recent_matches(self, account_id):
        """
        given an account id, return the following data

         "matches": [
            {
                "lane": "MID",
                "gameId": 3265138942,
                "champion": 50,
                "platformId": "EUW1",
                "timestamp": 1500130368205,
                "queue": 65,
                "role": "NONE",
                "season": 9
            },
        "endIndex": 20,
        "startIndex": 0,
        "totalGames": 20

        :param account_id: the account id of a summoner, found in the returned data of get_summoner_info(summoner_name)
        :return: a list of dictionaries with info about the last 20 games of a summoner
        """

        recent_games_info = get_response(BASE_URL.format(self.platform) + 'match/v3/matchlists/by-account/%s/recent' % account_id)['matches']
        recent_games = []
        for game in recent_games_info:
            data = {
                'lane': game['lane'],
                'gameId': game['gameId'],
                'championId': game['champion'],
                'queue': game['queue'],
                'season': game['season']
            }
            recent_games.append(data)

        return recent_games


    def get_summoner_recent_rankeds(self, account_id):
        """
        given an account id, return the following data
        "matches": [
            {
                "lane": "TOP",
                "gameId": 3258236269,
                "champion": 106,
                "platformId": "EUW1",
                "timestamp": 1499692802391,
                "queue": 420,
                "role": "SOLO",
                "season": 9
            },
        "endIndex": 20,
        "startIndex": 0,
        "totalGames": 1568

        :param account_id: the account id of a summoner, found in the returned data of get_summoner_info(summoner_name)
        :return: a list of dictionaries with info about the last 20 games of a summoner
        """

        recent_games_info = get_response(BASE_URL.format(self.platform) + 'match/v3/matchlists/by-account/%s?endIndex=20&beginIndex=0' % account_id)['matches']
        recent_games = []
        for game in recent_games_info:
            data = {
                'lane': game['lane'],
                'gameId': game['gameId'],
                'championId': game['champion'],
                'queue': game['queue'],
                'season': game['season']
            }
            recent_games.append(data)

        return recent_games


    def get_several_matches_info(self, games_list):
        """
        given a match id, return the data written in "match_info" file as an example.
        this function returns the summoner match data from several of his recent rankeds or unrankeds games

        :param games_list: a sublist of games receive from function "get_summoner_recent_games" or "get_summoner_recent_rankeds"
        :return: a list of dictionaries with info about the games
        """
        info_list = []
        for game in games_list:
            game_info = get_response(BASE_URL.format(self.platform) + 'match/v3/matches/%s' % game['gameId'])

            for participant in game_info['participants']:
                if participant['championId'] == game['championId']:
                    stats = participant['stats']
                    info = {
                        'win': stats['win'],
                        'kills': stats['kills'],
                        'goldEarned': stats['goldEarned'],
                        'deaths': stats['deaths'],
                        'assists': stats['assists'],
                        'champLvl': stats['champLevel'],
                        'cs': stats['totalMinionsKilled'],
                        'spell1': participant['spell1Id'],
                        'spell2': participant['spell2Id']
                    }
                    info_list.append(info)
                    break

        return info_list


    def get_current_game_info(self, summoner_id):
        """
        given a summoner id, return the data written in current_game_info if that summoner is currently playing or
        starting a match up

        :param summoner_id: the id of the summoner
        :return: a dictionary with the desired data
        """
        current_game = {}
        current_game_info = get_response(BASE_URL.format(self.platform) + "spectator/v3/active-games/by-summoner/%s" % summoner_id)
        current_game['gameId'] = current_game_info['gameId']
        banned_champs = []
        for champ in current_game_info['bannedChampions']:
            query = session.query(Champions).get(champ['championId'])
            champion_info = {"id": query.id, "image": query.image_champion}
            banned_champs.append(champion_info)

        current_game['bannedChamps'] = banned_champs
        participants = []
        for participant in current_game_info['participants']:
            participant_data = {
                "champion": session.query(Champions).get(participant['championId']).toJson(2),
                "summoner_name": participant['summonerName'],
                "summonerId": participant['summonerId'],
                "runes": [session.query(Runes).get(rune['runeId']).toJson(self.language, count=rune["count"]) for rune in participant['runes']],
                "masteries": [session.query(Masteries).get(mastery['masteryId']).toJson(self.language, count=mastery["rank"]) for mastery in participant['masteries']],
                "spell1": session.query(SummonerSpells).get(participant['spell1Id']).toJSon(self.language),
                "spell2": session.query(SummonerSpells).get(participant['spell2Id']).toJSon(self.language),
                "team": participant['teamId']
            }
            participants.append(participant_data)

        current_game['participants'] = participants

        return current_game


if __name__ == '__main__':
    pass
