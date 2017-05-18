from flask import Flask

app = Flask(__name__)

from app import utils

app.url_map.converters['game'] = utils.GameConverter

from app import compute, database, scrape, webview

if utils.is_dev():
    from app import dev
