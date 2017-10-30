from flask import Flask, jsonify, abort, request
from database.setup import session
from database.models import Configuration
#from summoner import SummonerRequest
import match, champion, summoner
from requests import HTTPError


app = Flask(__name__)


@app.route('/smartLoL/summoner/<summoner_name>')
def get_summoner(summoner_name):
    try:
        summoner_request = summoner.SummonerRequest(request.args['platform'], request.args['language'])
        summoner_data = summoner_request.get_summoner_info(summoner_name)
        summoner_data['leagues'] = summoner_request.get_summoner_league(summoner_data['id'])
        summoner_data['top_champions'] = summoner_request.get_summoner_top_champions(summoner_data['id'])
    except HTTPError as err:
        print(err.args[0].status_code)
        return abort(err.args[0].status_code)
    else:
        return jsonify(summoner_data)


@app.route('/smartLoL/recentgames/<account_id>')
def get_recent_games(account_id):
    try:
        match_request = match.MatchRequest(request.args['platform'], request.args['language'])
        recent_games = match_request.get_summoner_recent_matches(account_id)
    except HTTPError as err:
        return abort(err.args[0].status_code)
    else:
        return jsonify(recent_games)


@app.route('/smartLoL/recentrankeds/<account_id>')
def get_recent_rankeds(account_id):
    try:
        match_request = match.MatchRequest(request.args['platform'], request.args['language'])
        recent_rankeds = match_request.get_summoner_recent_rankeds(account_id)
    except HTTPError as err:
        return abort(err.args[0].status_code)
    else:
        return jsonify(recent_rankeds)


@app.route('/smartLoL/currentgame/<summoner_id>')
def get_current_game(summoner_id):
    try:
        match_request = match.MatchRequest(request.args['platform'], request.args['language'])
        current_game = match_request.get_current_game_info(summoner_id)
    except HTTPError as err:
        return abort(err.args[0].status_code)
    else:
        return jsonify(current_game)


@app.route('/smartLoL/champions/')
def get_champions_list():
    champion_request = champion.ChampionRequest(request.args['language'])
    return jsonify(champion_request.get_champions_list())


@app.route('/smartLoL/champion/<champion_id>')
def get_champion_info(champion_id):
    champion_request = champion.ChampionRequest(request.args['language'])
    return jsonify(**champion_request.get_champion_info(champion_id))



@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


#TODO surround with try except .one() calls
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
