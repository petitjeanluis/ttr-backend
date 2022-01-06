import os
import boto3

from models import GameDetails, Player

REGION = os.environ['REGION']
GAME_DETAILS_TABLE = os.environ['GAME_DETAILS_TABLE']
CONNECTION_TABLE = os.environ['CONNECTION_TABLE']

dynamodb = boto3.resource('dynamodb', region_name=REGION)

game_details_table = dynamodb.Table(GAME_DETAILS_TABLE)
connection_table = dynamodb.Table(CONNECTION_TABLE)

def getGameDetails(gameId: int) -> GameDetails:
    result = game_details_table.get_item(
        Key={'gameId': gameId},
        ReturnConsumedCapacity='NONE')
    
    if 'Item' not in result:
        return None
    
    return GameDetails.fromDict(result['Item'])

def updateGameDetails(gameDetails: GameDetails):
    game_details_table.put_item(
        Item=gameDetails.toDict()
    )

def addConnection(connectionId: str, playerId: int, gameId: int):
    connection_table.put_item(
        Item={
            "connectionId": connectionId,
            "playerId": playerId,
            "gameId": gameId
        }
    )

def removeConnection(connectionId: str):
    result = connection_table.delete_item(
        Key={
            'connectionId': connectionId
        },
        ReturnValues='ALL_OLD'
    )

    gameDetails: GameDetails = getGameDetails(result['Attributes']['gameId'])

    if gameDetails != None:
        for player in gameDetails.players:
            if player.id == result['Attributes']['playerId']:
                player.connectionId = None
                updateGameDetails(gameDetails)
                break
    
    