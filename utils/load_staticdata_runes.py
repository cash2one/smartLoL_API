from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.riot_api_connection import get_response
from database.models  import Configuration, Runes, RunesTranslations
from database.setup import session

import json

LOCALES = {
    1: "en_GB",
    2: "es_ES",
    4: "fr_FR",
    3: "it_IT",
    5: "de_DE"
}
URL = "https://euw1.api.riotgames.com/lol/static-data/v3/runes?locale={}&tags=all"


def write_files():
    """
    writes the json response from the api into several files
    :return: None
    """
    for id_locale, locale in LOCALES.items():
        response = get_response(URL.format(locale))
        with open("runes{}.json".format(locale), "w") as outfile:
            json.dump(response, outfile)


def main():
    """
    for each locale json file reads the file parsing it to json and insert the data into the database
    :return: None
    """
    first_time = True
    for id_locale, locale in LOCALES.items():
        with open("runes{}.json".format(locale)) as inputfile:
            response = json.load(inputfile)

        try:
            runes_version = session.query(Configuration).filter_by(code="{} version".format(response['type'])).one()
        except:
            configdata = {
                "code": "{} version".format(response['type']),
                "value": response['version']
            }
            print("añadiendo versión runas")
            runes_version = Configuration(**configdata)
            session.add(runes_version)

        if runes_version.value != response['version']:
            runes_version.version = response['version']
            session.add(runes_version)

        runes_data = response['data']

        for runes in runes_data.values():
            if first_time:
                data = {
                    "id": runes['id'],
                    "tier": runes['rune']['tier'],
                    "type": runes['rune']['type'],
                    "tags": ','.join(runes['tags']),
                    "image": runes['image']['full']
                }
                newSummSpell = Runes(**data)
                session.add(newSummSpell)

            translation = {
                "id_rune": runes['id'],
                "id_language": id_locale,
                "name": runes['name'],
                "description": runes['sanitizedDescription']
            }
            newTranslation = RunesTranslations(**translation)
            session.add(newTranslation)

        first_time = False
        print("todos los datos insertados con éxito para {}".format(locale))

    session.commit()

if __name__ == '__main__':
    main()
