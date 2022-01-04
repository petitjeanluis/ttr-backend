import logging
from logging import StreamHandler
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(StreamHandler())

from engine import GameEngine, PlayerAction, GameEngineValidationException, GameEngineException

log = logging.getLogger(__name__)

def handler(event, context):

    connectionId = event['requestContext']['connectionId']
    
    # body = json.loads(event['body'])
    body = event['body']
    
    payload = body['payload']
    action = PlayerAction[body['action']]
    
    try:
        GameEngine.processAction(action, payload, connectionId)
    except GameEngineValidationException as error:
        return {
            "statusCode": 400,
            "errorMessage": str(error)
        }

    return {
        "statusCode": 200
    }


if __name__ == '__main__':

    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    # event = {
    #     "body": {
    #         "action": "CREATE_GAME",
    #         "payload": {
    #             'id': '1111',
    #             'name': 'Luis'
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(pp.pprint(handler(event, None)))

    # event = {
    #     "body": {
    #         "action": "JOIN_GAME",
    #         "payload": {
    #             'id': '2222',
    #             'name': 'Squirrel',
    #             'gameId': '0000'
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection2'
    #     }
    # }

    # print(pp.pprint(handler(event, None)))

    # event = {
    #     "body": {
    #         "action": "START_GAME",
    #         "payload": {
    #             'id': '1111',
    #             'gameId': '0000'
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(pp.pprint(handler(event, None)))

    # event = {
    #     "body": {
    #         "action": "PICK_DESTINATION_CARDS",
    #         "payload": {
    #             'destinationCards': [20,21],
    #             'id': '1111',
    #             'gameId': '0000'
    #         }
    #     },
    #     "requestContext": {
    #         "connectionId": 'testConnection1'
    #     }
    # }

    # print(pp.pprint(handler(event, None)))

    event = {
        "body": {
            "action": "BUILD",
            "payload": {
                'destinationCards': [16,17,29],
                'id': '2222',
                'gameId': '0000'
            }
        },
        "requestContext": {
            "connectionId": 'testConnection1'
        }
    }

    print(pp.pprint(handler(event, None)))
