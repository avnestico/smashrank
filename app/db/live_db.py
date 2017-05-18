import boto3


def db_client():
    return boto3.client('sdb')


client = db_client()


def create_tables():
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
    response = client.list_domains()
    if 'DomainNames' in response:
        return response["DomainNames"]
    else:
        return "No Tables Exist"


def delete_tables():
    tables = list_tables()
    for name in tables:
        print(client.delete_domain(DomainName=name))
    return "Tables Deleted"


def search_by_name(name):
    name_query = 'select * from `Players` where name = "%s"'
    f_query = format(name_query % name)
    name_result = client.select(SelectExpression=f_query)
    return name_result


def search_for_leader(date, game, player_id):
    leader_id = "#".join([game, date, player_id])
    leader_result = client.get_attributes(DomainName="Leaders", ItemName=leader_id)
    return leader_result


def get_autoincr_id():
    autoincr_query = 'select itemName() from `Players` where itemName() is not null order by itemName() desc limit 1'
    autoincr_result = client.select(SelectExpression=autoincr_query)
    try:
        new_id = int(autoincr_result["Items"][0]["Name"]) + 1
    except:
        new_id = 1
    print(new_id)
    return new_id


def create_season(date, game, months):
    months = str(months)
    season_id = "#".join([game, date])
    season_attrs = [{'Name': 'game', 'Value': game},
                    {'Name': 'date', 'Value': date},
                    {'Name': 'months', 'Value': months}]
    season_result = client.put_attributes(DomainName='Seasons', ItemName=season_id, Attributes=season_attrs)
    print(season_result)
    return season_id


def simpledb_json_to_compact_json(query_items):
    query_dict = {}
    for item in query_items:
        attributes = {}
        if "Attributes" in item:
            for attribute in item["Attributes"]:
                attributes[attribute["Name"]] = attribute["Value"]
        query_dict[item["Name"]] = attributes
    return query_dict


def batch_put(DomainName, Items):
    MAX_ITEMS = 25

    res_string = ""
    while len(Items) > MAX_ITEMS:
        res_string += str(client.batch_put_attributes(DomainName=DomainName, Items=Items[:MAX_ITEMS]))
        Items = Items[MAX_ITEMS:]
    res_string += str(client.batch_put_attributes(DomainName=DomainName, Items=Items))
    return res_string


def batch_query(query_string):
    query_items = []
    query_result = client.select(SelectExpression=query_string)

    while True:
        if "Items" in query_result:
            query_items += query_result["Items"]
            if "NextToken" in query_result:
                query_result = client.select(SelectExpression=query_string, NextToken=query_result["NextToken"])
            else:
                break
        else:
            break

    return simpledb_json_to_compact_json(query_items)


def batch_query_with_tests(query, tests):
    MAX_TESTS = 20

    query_dict = {}
    while len(tests) > MAX_TESTS:
        f_query = format(query % str(tuple(tests[:MAX_TESTS])))
        query_dict.update(batch_query(f_query))
        tests = tests[MAX_TESTS:]
    f_query = format(query % str(tuple(tests)))
    query_dict.update(batch_query(f_query))
    return query_dict


def get_players_without_smashgg_id():
    players_query = 'select * from `Players` where smashgg_id is null'
    return batch_query(players_query)


if __name__ == "__main__":
    print(list_tables())
