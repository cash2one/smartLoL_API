from flask import Flask, jsonify, abort
from database.setup import session
from database.models import Configuration
import summoner, match, champion
from requests import HTTPError


app = Flask(__name__)


@app.route('/smartLoL/summoner/<summoner_name>')
def get_summoner(summoner_name):
    try:
        summoner_data = summoner.get_summoner_info(summoner_name)
        summoner_data['leagues'] = summoner.get_summoner_league(summoner_data['id'])
        summoner_data['top_champions'] = summoner.get_summoner_top_champions(summoner_data['id'])
    except HTTPError as err:
        print(err.args[0].status_code)
        return abort(err.args[0].status_code)
    else:
        return jsonify(summoner_data)


@app.route('/smartLoL/recentgames/<account_id>')
def get_recent_games(account_id):
    try:
        recent_games = match.get_summoner_recent_matches(account_id)
    except HTTPError as err:
        return abort(err.args[0].status_code)
    else:
        return jsonify(recent_games)


@app.route('/smartLoL/recentrankeds/<account_id>')
def get_recent_rankeds(account_id):
    try:
        recent_rankeds = match.get_summoner_recent_rankeds(account_id)
    except HTTPError as err:
        return abort(err.args[0].status_code)
    else:
        return jsonify(recent_rankeds)


@app.route('/smartLoL/currentgame/<summoner_id>')
def get_current_game(summoner_id):
    try:
        current_game = match.get_current_game_info(summoner_id)
    except HTTPError as err:
        return abort(err.args[0].status_code)
    else:
        return jsonify(current_game)


@app.route('/smartLoL/champions/')
def get_champions_list():
    return jsonify(champion.get_champions_list())


@app.route('/smartLoL/champion/<champion_id>')
def get_champion_info(champion_id):
    return jsonify(**champion.get_champion_info(champion_id, 2))



@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


def get_champion_version():
    version = session.query(Configuration).filter_by(code="champion version").one()
    return version.value

def get_mastery_version():
    version = session.query(Configuration).filter_by(code="mastery version").one()
    return version.value

def get_runes_version():
    version = session.query(Configuration).filter_by(code="rune version").one()
    return version.value

def get_summoner_version():
    version = session.query(Configuration).filter_by(code="summoner version").one()
    return version.value


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5001)
