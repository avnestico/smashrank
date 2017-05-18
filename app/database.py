from __future__ import print_function  # Python 2/3 compatibility

from app import utils, compute
from app.db import live_db


def import_provisional_leaders(game, date, players):
    # Create Season
    provisional_months = 12
    season_id = live_db.create_season(date, game, provisional_months)

    # Create Players
    new_id = live_db.get_autoincr_id()

    player_items = []
    leader_items = []

    for line in players:
        position = line[0]
        name = line[1]
        name_result = live_db.search_by_name(name)

        if "Items" in name_result:
            if len(name_result["Items"]) == 1:
                player_id = name_result["Items"][0]["Name"]
            else:
                return "Error: " + name + " exists multiple times in database. " + str(name_result["Items"])
        else:
            player_id = utils.pad_int_to_str(new_id, 6)
            new_id += 1
            player_attrs = [{'Name': 'name', 'Value': name}]
            player_item = {'Name': player_id, 'Attributes': player_attrs}
            player_items.append(player_item)

        # Create Leaders
        leader_id = "#".join([season_id, player_id])
        leader_attrs = [{'Name': 'position', 'Value': position}]
        leader_item = {'Name': leader_id, 'Attributes': leader_attrs}
        leader_items.append(leader_item)

    player_result = live_db.batch_put('Players', player_items)
    print(player_result)

    leaders_result = live_db.batch_put('Leaders', leader_items)
    print(leaders_result)

    return "Import Complete. "


def lookup_player_points_by_name(game, date, name):
    name_result = live_db.search_by_name(name)

    if "Items" not in name_result:
        return None

    if len(name_result["Items"]) == 1:
        player_id = name_result["Items"][0]["Name"]
        print("Player ID: " + player_id)
    else:
        return "Error: " + name + " exists multiple times in database. " + str(name_result["Items"])

    leader_result = live_db.search_for_leader(date, game, player_id)

    if "Attributes" in leader_result:
        print("Position: " + str(leader_result["Attributes"][0]["Value"]))

        return compute.get_position_points(leader_result["Attributes"][0]["Value"])
    else:
        return None
