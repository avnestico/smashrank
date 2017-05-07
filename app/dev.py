from flask import render_template, request, jsonify, json

from app import app, utils, database
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
        pass
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
