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
        print(f'Updating connection {connectionId} with {stateUpdates[connectionId].toDict()}\n')
    #     client.post_to_connection(Data=stateUpdate.toDict(), ConnectionId=connectionId)

def updatePlayer(connectionId: str, gameDetails: GameDetails) -> None:
    client.post_to_connection(Data=gameDetails.toDict(), ConnectionId=connectionId)

    