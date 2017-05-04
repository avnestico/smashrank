from flask import Flask

app = Flask(__name__)

from app import database, dev, utils, webview
