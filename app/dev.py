from flask import render_template, request

from app import app, utils, database
import os

os.environ["TZ"] = "UTC"


@app.route('/dev', methods=["GET"])
def dev_mode(message=""):
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    # get game details
    game_details = {}
    # get game standings
    standings = {}

    title = "Dev Mode"
    return render_template("backend/dev.html", title=title, message=message)


@app.route('/dev/create_tables', methods=["POST"])
def create_tables():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    message = database.create_tables()
    return dev_mode(message=message)


@app.route('/dev/list_tables', methods=["POST"])
def list_tables():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    message = database.list_tables()
    return dev_mode(message=message)


@app.route('/dev/delete_tables', methods=["POST"])
def delete_tables():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    message = database.delete_tables()
    return dev_mode(message=message)


@app.route('/dev/import_leaders', methods=["POST"])
def import_leaders():
    if not utils.is_dev():
        return render_template('webview/404.html'), 404
    game_input = request.form["game"]
    month_input = request.form["month"]
    players_input = request.form["players"]

    game = utils.is_valid_game(game_input)
    date = utils.is_valid_month(month_input)
    players = utils.is_valid_players(players_input)

    message_end = "Game:" + game
    message_end += "; Date:" + date
    message_end += "; Players:" + str(players)

    if not game or not date or not players:
        message = "Import Failed. "
    else:
        message = database.import_provisional_leaders(game, date, players)
    message = message + message_end
    return dev_mode(message=message)
