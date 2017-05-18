import sys
from datetime import datetime

from werkzeug.routing import BaseConverter, ValidationError


def is_dev():
    return "dev" in sys.argv


def strip_game(game):
    return game.replace("_", "").replace("-", "").replace(" ", "")


def pad_int_to_str(i, padding):
    return format(i, '0%dd' % padding)


def is_valid_game(game):
    games = ['melee', 'wii-u']
    game = game.lower()
    if game in games:
        return game
    else:
        return None


def is_valid_month(date):
    try:
        datetime.strptime(date, '%Y-%m')
        return date
    except ValueError:
        return None


def is_valid_players(players_input):
    try:
        players = []
        lines = players_input.splitlines()
        for line in lines:
            record = line.split("\t")
            if len(record) != 2:
                raise TypeError
            record[0] = int(record[0])  # confirm that position is integer
            record[0] = pad_int_to_str(record[0], 3)
            players.append(record)
        return players
    except:
        return None


def is_valid_tournament(tournament_input):
    return tournament_input


class GameConverter(BaseConverter):
    """Validates that an input is a game."""

    def to_python(self, value):
        if not is_valid_game(value):
            raise ValidationError()
        return value

    def to_url(self, value):
        return is_valid_game(value)
