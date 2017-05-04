from flask import render_template

from app import app


@app.route('/')
def main():
    return render_template("webview/index.html", title="SmashRank")


@app.route('/<game>', methods=["GET"])
def game_standings(game):
    # get game details
    game_details = {}
    # get game standings
    standings = {}

    title = game + " Standings"
    return render_template("webview/game.html", game=game_details, standings=standings, title=title)


@app.route('/<game>/tournaments', methods=["GET"])
def game_tournaments(game):
    # get game details
    game_details = {}
    # get game's tournaments in the past 12 months, sorted by value
    tournaments = {}

    title = game + " Tournaments"
    return render_template("webview/tournaments.html", game=game_details, tournaments=tournaments, title=title)


@app.route('/<game>/tournament/<tournament_id>', methods=["GET"])
def tournament_details(game, tournament_id):
    # get game details
    game_details = {}
    # get tournament details
    tournament_details = {}

    title = game + " " + tournament_id
    return render_template("webview/tournament_id.html", game=game_details, tournament_details=tournament_details, title=title)


@app.route('/<game>/player/<player_id>', methods=["GET"])
def player_details(game, player_id):
    # get game details
    game_details = {}
    # get player details
    player_details = {}

    title = game + " " + player_id
    return render_template("webview/player_id.html", game=game_details, player_details=player_details, title=title)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('webview/404.html', title="Page Not Found"), 404
