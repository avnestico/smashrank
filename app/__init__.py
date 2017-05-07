from flask import Flask

app = Flask(__name__)

from app import compute, database, dev, scrape, utils, webview
