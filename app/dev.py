from flask import render_template, abort

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
