import boto3
import os

from models import GameDetails, StateUpdate, buildStateUpdates

API_ID = os.environ['API_ID']
STAGE = os.environ['STAGE']
REGION = os.environ['REGION']

ENDPOINT = f'https://{API_ID}.execute-api.{REGION}.amazonaws.com/{STAGE}'

client = boto3.client('apigatewaymanagementapi', endpoint_url=ENDPOINT)

def updatePlayers(gameDetails: GameDetails):
    stateUpdates: dict[str, StateUpdate] =  buildStateUpdates(gameDetails)

    for connectionId in stateUpdates:
        # print(f'Notification: {stateUpdates[connectionId].toDict()}\n')
        client.post_to_connection(Data=stateUpdates[connectionId].toDict(), ConnectionId=connectionId)

    