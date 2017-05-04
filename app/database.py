from __future__ import print_function  # Python 2/3 compatibility

from app import utils


def create_tables():
    dynamodb = utils.dynamodb()

    seasons = dynamodb.create_table(
        TableName='Seasons',
        KeySchema=[
            {
                'AttributeName': 'game',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'date',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'game',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'date',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    leaders = dynamodb.create_table(
        TableName='Leaders',
        KeySchema=[
            {
                'AttributeName': 'season_id',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'position',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'season_id',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'position',
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    tournaments = dynamodb.create_table(
        TableName='Tournaments',
        KeySchema=[
            {
                'AttributeName': 'game',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'tournament_id',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'game',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'tournament_id',
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    players = dynamodb.create_table(
        TableName='Players',
        KeySchema=[
            {
                'AttributeName': 'game',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'player_id',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'game',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'player_id',
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    results = dynamodb.create_table(
        TableName='Results',
        KeySchema=[
            {
                'AttributeName': 'player_id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'tournament_id',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'player_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'tournament_id',
                'AttributeType': 'N'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    #print("Seasons table status:", seasons.table_status)
    #print("Leaders table status:", leaders.table_status)
    #print("Tournaments table status:", tournaments.table_status)
    #print("Players table status:", players.table_status)
    #print("Results table status:", results.table_status)

    return "Tables Created"


def table_status():
    client = utils.dynamodb_client()
    tables = list_tables()
    response = []
    for name in tables:
        response.append(client.describe_table(TableName=name))
    return response


def list_tables():
    client = utils.dynamodb_client()
    return client.list_tables()["TableNames"]


def delete_tables():
    dynamodb = utils.dynamodb()
    tables = list_tables()
    for name in tables:
        table = dynamodb.Table(name)
        table.delete()
    return "Tables Deleted"


if __name__ == "__main__":
    #print(delete_tables())
    #print(create_tables())
    print(list_tables())