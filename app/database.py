from __future__ import print_function  # Python 2/3 compatibility

import boto3

from app import utils


def db_client():
    return boto3.client('sdb')


def create_tables():
    client = db_client()

    seasons = client.create_domain(DomainName='Seasons')
    print(seasons)
    leaders = client.create_domain(DomainName='Leaders')
    print(leaders)
    tournaments = client.create_domain(DomainName='Tournaments')
    print(tournaments)
    players = client.create_domain(DomainName='Players')
    print(players)
    results = client.create_domain(DomainName='Results')
    print(results)

    return "Tables Created"


def list_tables():
    client = db_client()
    response = client.list_domains()
    if 'DomainNames' in response:
        return response["DomainNames"]
    else:
        return "No Tables Exist"


def delete_tables():
    client = db_client()
    tables = list_tables()
    for name in tables:
        print(client.delete_domain(DomainName=name))
    return "Tables Deleted"


def import_provisional_leaders(game, date, players):
    client = db_client()

    # Create Season
    season_id = "#".join([game, date])
    season_attrs = [{'Name': 'game', 'Value': game},
                    {'Name': 'date', 'Value': date},
                    {'Name': 'provisional', 'Value': "1"}]
    season_result = client.put_attributes(DomainName='Seasons', ItemName=season_id, Attributes=season_attrs)
    print(season_result)

    # Create Players
    autoincr_query = 'select itemName() from `Players` where itemName() is not null order by itemName() desc limit 1'
    autoincr_result = client.select(SelectExpression=autoincr_query)
    try:
        new_id = int(autoincr_result["Items"][0]["Name"]) + 1
        print(new_id)
    except:
        new_id = 1


    player_items = []
    leader_items = []

    name_query = 'select * from `Players` where name = "%s"'
    for line in players:
        position = line[0]
        name = line[1]
        f_query = format(name_query % name)
        name_result = client.select(SelectExpression=f_query)

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

    player_result = batch_put(client, 'Players', player_items)
    print(player_result)

    leaders_result = batch_put(client, 'Leaders', leader_items)
    print(leaders_result)

    return "Import Complete. "


def batch_put(client, DomainName, Items):
    res_string = ""
    while len(Items) > 25:
        res_string += str(client.batch_put_attributes(DomainName=DomainName, Items=Items[0:25]))
        Items = Items[25:]
    res_string += str(client.batch_put_attributes(DomainName=DomainName, Items=Items))
    return res_string


if __name__ == "__main__":
    #print(delete_tables())
    #print(create_tables())
    print(list_tables())


