from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.riot_api_connection import get_response
from database.models import Configuration, Masteries, MasteriesTranslations
from database.setup import session

import json

LOCALES = {
    1: "en_GB",
    2: "es_ES",
    4: "fr_FR",
    3: "it_IT",
    5: "de_DE"
}
URL = "https://euw1.api.riotgames.com/lol/static-data/v3/masteries?locale={}&tags=all"



def write_files():
    """
    writes the json response from the api into several files
    :return: None
    """
    for id_locale, locale in LOCALES.items():
        response = get_response(URL.format(locale))
        with open("masteries{}.json".format(locale), "w") as outfile:
            json.dump(response, outfile)


def main():
    """
    for each locale json file reads the file parsing it to json and insert the data into the database
    :return: None
    """
    first_time = True
    for id_locale, locale in LOCALES.items():
        with open("{}.json".format(locale)) as inputfile:
            response = json.load(inputfile)

        try:
            masteryversion = session.query(Configuration).filter_by(code="{} version".format(response['type'])).one()
        except:
            configdata = {
                "code": "{} version".format(response['type']),
                "value": response['version']
            }
            print("añadiendo versión maestrias")
            masteryversion = Configuration(**configdata)
            session.add(masteryversion)

        if masteryversion.value != response['version']:
            masteryversion.version = response['version']
            session.add(masteryversion)

        masteries_data = response['data']

        for mastery in masteries_data.values():
            # champion, champion spells, champions skins and champions info are locale independant
            if first_time:
                mastery_data = {
                    "id": mastery['id'],
                    "ranks": mastery['ranks'],
                    "image": mastery['image']['full'],
                    "tree": mastery['masteryTree']
                }
                newMastery = Masteries(**mastery_data)
                session.add(newMastery)

            translation_data = {
                "id_mastery": mastery['id'],
                "id_language": id_locale,
                "name": mastery['name'],
                "description": ','.join(mastery['sanitizedDescription'])
            }
            newTranslation = MasteriesTranslations(**translation_data)
            session.add(newTranslation)

        first_time = False
        print("todos los datos insertados con éxito para {}".format(locale))

    session.commit()

if __name__ == '__main__':
    main()
