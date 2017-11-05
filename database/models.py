from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import SET, ENUM
from database.setup import Base, session
import utils.riot_api_connection as riot_urls


class Languages(Base):
    __tablename__ = 'Languages'

    id = Column(Integer, primary_key=True)
    locale = Column(String(5), nullable=False)


class Configuration(Base):
    __tablename__ = 'Configuration'

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    value = Column(String(50), nullable=False)

    @staticmethod
    def get_version(element):
        version = session.query(Configuration).filter_by(code=element).one().value
        return version


class Champions(Base):
    __tablename__ = 'Champions'

    version = Configuration.get_version("champion version")

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50), nullable=False)
    champ_key = Column(String(50), nullable=False)
    rols = Column(SET("Fighter", "Assassin", "Mage", "Support", "Tank", "Marksman"), nullable=False)
    image_champion = Column(String(100), nullable=False)
    image_passive = Column(String(100), nullable=False)

    title = relationship("ChampionsTitles", lazy="dynamic")
    passive = relationship("PassivesTranslations", lazy="dynamic")
    spells = relationship("ChampionsSpells")
    skins = relationship("ChampionsSkins", lazy="dynamic")
    info = relationship("ChampionsInfo", uselist=False)
    ally_tips = relationship("ChampionAllyTips", lazy="dynamic")
    enemy_tips = relationship("ChampionEnemyTips", lazy="dynamic")

    def toJson(self, id_locale):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image_champion,
            "rols": list(self.rols),
            "title": self.get_title(id_locale),
            "passive": self.get_passive(id_locale),
            "spells": self.get_spells(id_locale),
            "skins": self.get_skins(id_locale),
            "info": self.get_info(),
            "ally_tips": self.get_ally_tips(id_locale),
            "enemy_tips": self.get_enemy_tips(id_locale)
        }

    def get_ally_tips(self, id_locale):
        """
        :param id_locale: id of the desired language
        :return: return a list of tips as strings
        """
        return [item.tip for item in self.ally_tips.filter_by(id_language=id_locale)]

    def get_enemy_tips(self, id_locale):
        """
        :param id_locale: id of the desired language
        :return: return a list of tips as strings
        """
        return [item.tip for item in self.enemy_tips.filter_by(id_language=id_locale)]

    def get_spells(self, id_locale):
        """
        :param id_locale: id of the desired language
        :return: return a list of spells as dictionaries
        """
        spells = []
        for spell in self.spells:
            item = spell.translations.filter_by(id_language=id_locale).one()
            data = {
                "image": riot_urls.ABILITIES_URL.format(self.version, spell.image),
                "name": item.name,
                "descripion": item.description
            }
            spells.append(data)

        return spells

    def get_skins(self, id_locale):
        """
        :param id_locale: id of the desired language
        :return: a list of skins as dictionaries
        """
        skins = []
        for skin in self.skins:
            data = {
                "image": riot_urls.CHAMPIONS_SPLASH_URL.format(self.champ_key, skin.num),
                "name": skin.translations.filter_by(id_language=id_locale).one().name
            }
            skins.append(data)

        return skins

    def get_passive(self, id_locale):
        passive = self.passive.filter_by(id_language=id_locale).one()
        return {
            "name": passive.name,
            "description": passive.description,
            "image": riot_urls.PASSIVE_ABILITIES_URL.format(self.version, self.image_passive)
        }

    def get_title(self, id_locale):
        return self.title.filter_by(id_language=id_locale).one().title

    def get_info(self):
        return {
            "difficulty": self.info.difficulty,
            "attack": self.info.attack,
            "defense": self.info.defense,
            "magic": self.info.magic
        }


class ChampionsTitles(Base):
    __tablename__ = 'ChampionsTitles'

    id_champion = Column(Integer, ForeignKey("Champions.id"), primary_key=True)
    id_language = Column(Integer, ForeignKey("Languages.id"), primary_key=True)
    title = Column(String(50), nullable=False)


class PassivesTranslations(Base):
    __tablename__ = 'PassivesTranslations'

    id_champion = Column(Integer, ForeignKey("Champions.id"), primary_key=True)
    id_language = Column(Integer, ForeignKey("Languages.id"), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(800), nullable=False)


class ChampionsSpells(Base):
    __tablename__ = 'ChampionsSpells'

    id = Column(Integer, primary_key=True)
    id_champion = Column(Integer, ForeignKey("Champions.id"))
    spell_key = Column(String(50), nullable=False, unique=True)
    image = Column(String(100), nullable=False)

    translations = relationship("SpellsTranslations", lazy="dynamic")


class SpellsTranslations(Base):
    __tablename__ = 'SpellsTranslations'

    id_spell = Column(Integer, ForeignKey("ChampionsSpells.id"), primary_key=True)
    id_language = Column(Integer, ForeignKey("Languages.id"), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(800), nullable=False)


class ChampionsSkins(Base):
    __tablename__ = 'ChampionsSkins'

    id = Column(Integer, primary_key=True, autoincrement=False)
    id_champion = Column(Integer, ForeignKey("Champions.id"), primary_key=True)
    num = Column(Integer, nullable=False)

    translations = relationship("SkinsTranslations", lazy="dynamic")


class SkinsTranslations(Base):
    __tablename__ = 'SkinsTranslations'

    id_skin = Column(Integer, ForeignKey("ChampionsSkins.id"), primary_key=True)
    id_language = Column(Integer, ForeignKey("Languages.id"), primary_key=True)
    name = Column(String(100), nullable=False)


class ChampionsInfo(Base):
    __tablename__ = 'ChampionsInfo'

    id_champion = Column(Integer, ForeignKey("Champions.id"), primary_key=True)
    difficulty = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    magic = Column(Integer, nullable=False)


class ChampionAllyTips(Base):
    __tablename__ = 'ChampionAllyTips'

    id = Column(Integer, primary_key=True)
    id_champion = Column(Integer, ForeignKey("Champions.id"))
    id_language = Column(Integer, ForeignKey("Languages.id"))
    tip = Column(String(500))


class ChampionEnemyTips(Base):
    __tablename__ = 'ChampionEnemyTips'

    id = Column(Integer, primary_key=True)
    id_champion = Column(Integer, ForeignKey("Champions.id"))
    id_language = Column(Integer, ForeignKey("Languages.id"))
    tip = Column(String(500))


class Masteries(Base):
    __tablename__ = 'Masteries'

    id = Column(Integer, primary_key=True)
    tree = Column(ENUM("Ferocity", "Resolve", "Cunning"), nullable=False)
    ranks = Column(Integer, nullable=False)
    image = Column(String(50), nullable=False)

    translations = relationship("MasteriesTranslations", lazy="dynamic")

    def toJson(self, id_locale, **kwargs):
        data = {
            "translation": self.get_translation(id_locale),
            "tree": self.tree,
            "ranks": self.ranks,
            "image": self.image
        }
        for key, value in kwargs.items():
            data[key] = value

        return data

    def get_translation(self, id_locale):
        data = self.translations.filter_by(id_language=id_locale).one()
        return {
            "name": data.name,
            "description": data.description
        }


class MasteriesTranslations(Base):
    __tablename__ = 'MasteriesTranslations'

    id_mastery = Column(Integer, ForeignKey("Masteries.id"), primary_key=True)
    id_language = Column(Integer, ForeignKey("Languages.id"), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(1500), nullable=False)


class SummonerSpells(Base):
    __tablename__ = "SummonerSpells"

    id = Column(Integer, primary_key=True, autoincrement=False)
    summspell_key = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False)

    translations = relationship("SummonerSpellsTranslations", lazy="dynamic")

    def toJson(self, id_locale):
        return {
            "translation": self.get_translation(id_locale),
            "image": self.image
        }

    def get_translation(self, id_locale):
        data = self.translations.filter_by(id_language=id_locale).one()
        return {
            "name": data.name,
            "description": data.description
        }


class SummonerSpellsTranslations(Base):
    __tablename__ = "SummonerSpellsTranslations"

    id_spell = Column(Integer, ForeignKey("SummonerSpells.id"), primary_key=True)
    id_language = Column(Integer, ForeignKey("Languages.id"), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)


class Runes(Base):
    __tablename__ = "Runes"

    id = Column(Integer, primary_key=True, autoincrement=False)
    tier = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    tags = Column(String(500), nullable=False)
    image = Column(String(100), nullable=False)

    translations = relationship("RunesTranslations", lazy="dynamic")

    def toJson(self, id_locale, **kwargs):
        data = {
            "translation": self.get_translation(id_locale),
            "tier": self.tier,
            "type": self.type,
            "tags": self.tags,
            "image": self.image
        }
        for key, value in kwargs.items():
            data[key] = value

        return data

    def get_translation(self, id_locale):
        data = self.translations.filter_by(id_language=id_locale).one()
        return {
            "name": data.name,
            "description": data.description
        }


class RunesTranslations(Base):
    __tablename__ = "RunesTranslations"

    id_rune = Column(Integer, ForeignKey("Runes.id"), primary_key=True)
    id_language = Column(Integer, ForeignKey("Languages.id"), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
