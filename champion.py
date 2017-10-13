from database.models import Champions, Configuration
from database.setup import session
from utils.riot_api_connection import CHAMPIONS_SQUARE_URL

version = session.query(Configuration).filter_by(code="champion version").one().value

def get_champions_list():
    champion_list = []
    for champion in session.query(Champions).all():
        data = {
            "id": champion.id,
            "image": CHAMPIONS_SQUARE_URL.format(version, champion.image_champion),
            "name": champion.name
        }
        champion_list.append(data)

    return champion_list

def get_champion_info(id_champion, id_locale):
    return session.query(Champions).get(id_champion).toJson(id_locale)