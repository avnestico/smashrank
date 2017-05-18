import operator
from flask import render_template, request, jsonify, json

import app.db.live_db
from app import app, utils, database, scrape, compute
import os

os.environ["TZ"] = "UTC"


@app.route('/dev', methods=["GET"])
def dev_mode():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    title = "Dev Mode"
    return render_template("backend/dev.html", title=title)


# Run commands which don't have any input
@app.route('/dev/<command>', methods=["POST"])
def dev_command(command):
    if hasattr(database, command):
        message = getattr(database, command)()
    else:
        message = "Invalid Command."
    return jsonify(message=message)


@app.route('/dev/import_provisional_leaders', methods=["POST"])
def import_leaders():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    game_input = request.json["game"]
    month_input = request.json["month"]
    players_input = request.json["players"]

    game = utils.is_valid_game(game_input)
    date = utils.is_valid_month(month_input)
    players = utils.is_valid_players(players_input)

    message_end = "Game:" + str(game)
    message_end += "; Date:" + str(date)
    message_end += "; Players:" + str(players)

    if not game or not date or not players:
        message = "Import Failed. "
    else:
        message = database.import_provisional_leaders(game, date, players)
    message = message + message_end
    return jsonify(message=message)


@app.route('/dev/import_smashgg_tournament', methods=["POST"])
def import_sgg_tournament():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    game_input = request.json["game"]
    tournament_input = request.json["tournament"]

    game = utils.is_valid_game(game_input)
    tournament = utils.is_valid_tournament(tournament_input)

    if not game or not tournament:
        message = "Import Failed. "
    else:
        tournament_dict, attendees_dict = scrape.dump_tournament(tournament, game)
        message = "Tournament: " + str(tournament_dict) + " Attendees:"

        tournament_value = 0

        leader_string = "#".join([game, "2016-01"])
        leader_query = 'SELECT * FROM `Leaders` where ItemName() like "%s%%" limit 200'
        f_leader_query = format(leader_query % leader_string)
        leaders = app.db.live_db.batch_query(f_leader_query)
        print(leaders)

        players_join = []
        for key in leaders.keys():
            players_join.append(key.split("#")[2])
        player_query = 'SELECT * FROM `Players` where ItemName() in %s'
        players = app.db.live_db.batch_query_with_tests(player_query, players_join)
        print(players)

        value_dict = {}
        for player in range(len(attendees_dict)):
            player_name = attendees_dict[player]["name"]
            value = compute.get_player_value(players, leaders, player_name, leader_string)
            value_dict[player_name] = value
            if value:
                tournament_value += value
        message += str(sorted(value_dict.items(), key=operator.itemgetter(1), reverse=True))

        message += " Tournament Value: " + str(tournament_value)
    return jsonify(message=message)


@app.route('/dev/search_player_smashgg', methods=["POST"])
def search_player_smashgg():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    player = request.json["player"]
    message = scrape.search_player_smashgg(player)
    return jsonify(message=message)
