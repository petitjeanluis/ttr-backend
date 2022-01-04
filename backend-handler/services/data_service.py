import os
import boto3

from models import GameDetails

REGION = os.environ['REGION']
TABLE_NAME = os.environ['TABLE_NAME']

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def getGameDetails(gameId: int) -> GameDetails:
    result = table.get_item(
        Key={'gameId': gameId},
        ReturnConsumedCapacity='NONE')
    
    if 'Item' not in result:
        return None
    
    return GameDetails.fromDict(result['Item'])

def updateGameDetails(gameDetails: GameDetails):
    table.put_item(
        Item=gameDetails.toDict()
    )
