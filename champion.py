from database.models import Champions
from database.setup import session
from utils.riot_api_connection import CHAMPIONS_SQUARE_URL


class ChampionRequest:
    """
    Class to send queries to db for champion data
    :cvar language: the id of the desired language i.e. 2 for spanish
    """

    def __init__(self, language):
        self.language = language

    def get_champions_list(self):
        champion_list = []
        for champion in session.query(Champions).all():
            data = {
                "id": champion.id,
                "image": CHAMPIONS_SQUARE_URL.format(champion.version, champion.image_champion),
                "name": champion.name
            }
            champion_list.append(data)

        return champion_list

    def get_champion_info(self, id_champion):
        return session.query(Champions).get(id_champion).toJson(self.language)