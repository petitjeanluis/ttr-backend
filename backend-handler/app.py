import json
from state import StateEngine, StateMachineValidationException
from state.actions import PlayerAction
from services import removeConnection

import logging

log = logging.getLogger(__name__)

def handler(event, context):

    connectionId = event['requestContext']['connectionId']
    routeKey = event['requestContext']['routeKey']

    if routeKey == '$disconnect':
        removeConnection(connectionId)
    else:
        body = json.loads(event['body'])
        
        payload = body['payload']
        action = PlayerAction[body['action']]
        
        try:
            StateEngine.processAction(action, payload, connectionId)
        except StateMachineValidationException as error:
            log.error(error)
            return {
                "statusCode": 400,
                "errorMessage": str(error)
            }

    return {
        "statusCode": 200
    }


if __name__ == '__main__':
    event = {
        "requestContext": {
            "connectionId": 'testConnection1',
            "routeKey": "$disconnect"
        }
    }

    print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "CREATE_GAME",
    #         "payload": {
    #             'id': 1111,
    #             'name': 'Luis'
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1',
    #         "routeKey": "$default"
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "JOIN_GAME",
    #         "payload": {
    #             'id': 2222,
    #             'name': 'Squirrel',
    #             'gameId': 0
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection2',
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "START_GAME",
    #         "payload": {
    #             'id': 1111,
    #             'gameId': 0
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "PICK_DESTINATION_CARDS",
    #         "payload": {
    #             'destinationCardIds': [9,4],
    #             'id': 1111,
    #             'gameId': 0000
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "PICK_DESTINATION_CARDS",
    #         "payload": {
    #             'destinationCardIds': [2,18],
    #             'id': 2222,
    #             'gameId': 0000
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "BUILD",
    #         "payload": {
    #             'trainCards': ['WHITE','WILD'],
    #             'pathId': 95,
    #             'id': 1111,
    #             'gameId': 0000
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "PICK_RANDOM_TRAIN_CARD",
    #         "payload": {
    #             'id': 2222,
    #             'gameId': 0000
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "GET_DESTINATION_CARDS",
    #         "payload": {
    #             'id': 1111,
    #             'gameId': 0000
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(handler(event, None))

    # event = {
    #     "body": {
    #         "action": "PICK_DESTINATION_CARDS",
    #         "payload": {
    #             'id': 1111,
    #             'gameId': 0000,
    #             "destinationCardIds": [1]
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(handler(event, None))
    pass
