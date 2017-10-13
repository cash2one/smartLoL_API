from utils.riot_api_connection import get_response
from database.setup import session
from database.models import Configuration, Champions, ChampionEnemyTips, ChampionAllyTips, ChampionsInfo, ChampionsSkins, ChampionsSpells, ChampionsTitles, PassivesTranslations, SpellsTranslations, SkinsTranslations
import json

LOCALES = {
    1: "en_GB",
    2: "es_ES",
    4: "fr_FR",
    3: "it_IT",
    5: "de_DE"
}
URL = "https://euw1.api.riotgames.com/lol/static-data/v3/champions?locale={}&tags=allytips&tags=enemytips&tags=image&tags=info&tags=passive&tags=skins&tags=spells&tags=tags&dataById=false"

def write_files():
    """
    writes the json response from the api into several files
    :return: None
    """
    for id_locale, locale in LOCALES.items():
        response = get_response(URL.format(locale))
        with open("{}.json".format(locale), "w") as outfile:
            json.dump(response, outfile)


def main():
    """
    for each locale json file reads the file parsing it to json and insert the data into the database
    :return: None
    """
    first_time = True
    for id_locale, locale in LOCALES.items():
        with open("champs{}.json".format(locale)) as inputfile:
            response = json.load(inputfile)

        try:
            version = session.query(Configuration).filter_by(code="{} version".format(response['type'])).one()
        except:
            configdata = {
                "code": "{} version".format(response['type']),
                "value": response['version']
            }
            if not version:
                print("añadiendo versión campeones")
                championversion = Configuration(**configdata)
                session.add(championversion)
        if championversion.value != response['version']:
            print("actualizando versión campeones")
            championversion.value = response['version']
            session.add(championversion)

        champions_data = response['data']

        for champion in champions_data.values():
            #champion, champion spells, champions skins and champions info are locale independant
            if first_time:
                get_champion(champion)
                get_Champion_spells(champion, id_locale)
                get_champion_skins(champion, id_locale)
                get_champion_info(champion)

            get_champion_title(champion, id_locale)
            get_passive_translations(champion, id_locale)
            get_spell_translations(champion, id_locale)
            get_skin_translation(champion, id_locale)
            get_champion_allytips(champion, id_locale)
            get_champion_enemytips(champion, id_locale)

        first_time = False
        print("todos los datos insertados con éxito para {}".format(locale))
    session.commit()


def get_champion(champion):
    championdata = {
        "id": champion['id'],
        "name": champion['name'],
        "champ_key": champion['key'],
        "rols": ','.join(champion['tags']),
        "image_champion": champion['image']['full'],
        "image_passive": champion['passive']['image']['full']
    }
    newChampion = Champions(**championdata)
    session.add(newChampion)

def get_champion_title(champion, language):
    titledata = {
        "id_champion": champion['id'],
        "id_language": language,
        "title": champion['title']
    }
    newChampionTitle = ChampionsTitles(**titledata)
    session.add(newChampionTitle)

def get_passive_translations(champion, language):
    translationdata = {
        "id_champion": champion['id'],
        "id_language": language,
        "name": champion['passive']['name'],
        "description": champion['passive']['sanitizedDescription']
    }
    newPassiveTranslation = PassivesTranslations(**translationdata)
    session.add(newPassiveTranslation)

def get_Champion_spells(champion, language):
    id_champion = champion['id']
    for spell in champion['spells']:
        spelldata = {
            "id_champion": id_champion,
            "image": spell['image']['full'],
            "spell_key": spell['key']
        }
        newChampionSpell = ChampionsSpells(**spelldata)
        session.add(newChampionSpell)

def get_spell_translations(champion, language):

    for spell in champion['spells']:
        spell_id = session.query(ChampionsSpells).filter_by(spell_key=spell['key']).one().id
        translationdata = {
            "id_spell": spell_id,
            "id_language": language,
            "name": spell['name'],
            "description": spell['sanitizedDescription']
        }
        newSpellTranslation = SpellsTranslations(**translationdata)
        session.add(newSpellTranslation)

def get_champion_skins(champion, language):
    id_champion = champion['id']
    for skin in champion['skins']:
        skindata = {
            "id": skin['id'],
            "id_champion": id_champion,
            "num": skin['num']
        }
        newChampionSkin = ChampionsSkins(**skindata)
        session.add(newChampionSkin)

def get_skin_translation(champion, language):
    for skin in champion['skins']:
        translationdata = {
            "id_skin": skin['id'],
            "id_language": language,
            "name": skin['name']
        }
        newSkinTranslation = SkinsTranslations(**translationdata)
        session.add(newSkinTranslation)

def get_champion_info(champion):
    infodata = {
        "id_champion": champion['id'],
        "difficulty": champion['info']['difficulty'],
        "attack": champion['info']['attack'],
        "defense": champion['info']['defense'],
        "magic": champion['info']['magic']
    }
    newChampionInfo = ChampionsInfo(**infodata)
    session.add(newChampionInfo)

def get_champion_allytips(champion, language):
    id_champion = champion['id']
    for tip in champion['allytips']:
        tipdata = {
            "id_champion": id_champion,
            "id_language": language,
            "tip": tip
        }
        newChampionAllyTip = ChampionAllyTips(**tipdata)
        session.add(newChampionAllyTip)

def get_champion_enemytips(champion, language):
    id_champion = champion['id']
    for tip in champion['enemytips']:
        tipdata = {
            "id_champion": id_champion,
            "id_language": language,
            "tip": tip
        }
        newChampionEnemyTip = ChampionEnemyTips(**tipdata)
        session.add(newChampionEnemyTip)


if __name__ == '__main__':
    pass