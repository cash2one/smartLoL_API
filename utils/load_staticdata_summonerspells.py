from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.riot_api_connection import get_response
from database.models import Configuration, SummonerSpells, SummonerSpellsTranslations
from database.setup import session

import json

LOCALES = {
    1: "en_GB",
    2: "es_ES",
    4: "fr_FR",
    3: "it_IT",
    5: "de_DE"
}
URL = "https://euw1.api.riotgames.com/lol/static-data/v3/summoner-spells?locale={}&dataById=false&tags=all"


def write_files():
    """
    writes the json response from the api into several files
    :return: None
    """
    for id_locale, locale in LOCALES.items():
        response = get_response(URL.format(locale))
        with open("summspells{}.json".format(locale), "w") as outfile:
            json.dump(response, outfile)


def main():
    """
    for each locale json file reads the file parsing it to json and insert the data into the database
    :return: None
    """
    first_time = True
    for id_locale, locale in LOCALES.items():
        with open("summspells{}.json".format(locale)) as inputfile:
            response = json.load(inputfile)

        try:
            summspell_version = session.query(Configuration).filter_by(code="{} version".format(response['type'])).one()
        except:
            configdata = {
                "code": "{} version".format(response['type']),
                "value": response['version']
            }
            print("añadiendo versión summoner spells")
            summspell_version = Configuration(**configdata)
            session.add(summspell_version)

        if summspell_version.value != response['version']:
            summspell_version.version = response['version']
            session.add(summspell_version)

        summspells_data = response['data']

        for spell in summspells_data.values():
            if first_time:
                data = {
                    "id": spell['id'],
                    "summspell_key": spell['key'],
                    "image": spell['image']['full']
                }
                newSummSpell = SummonerSpells(**data)
                session.add(newSummSpell)

            translation = {
                "id_spell": spell['id'],
                "id_language": id_locale,
                "name": spell['name'],
                "description": spell['sanitizedDescription']
            }
            newTranslation = SummonerSpellsTranslations(**translation)
            session.add(newTranslation)

        first_time = False
        print("todos los datos insertados con éxito para {}".format(locale))

    session.commit()

if __name__ == '__main__':
    main()
