from .state_handler import StateHandler
from .actions import PlayerAction
from .handlers import MatchMakingState, TurnState, PickInitialDestinationCardsState, PickSecondTrainCardState, PickDestinationCardsState, EndState

from services import getGameDetails, updateGameDetails, updatePlayers

from models import GameDetails, Player
from constants import GameState

from random import randint

class StateEngine:

    STATE_HANDLER_MAP: dict[GameState, StateHandler] = {
        GameState.MATCH_MAKING: MatchMakingState,
        GameState.TURN: TurnState,
        GameState.PICK_INITIAL_DESTINATION_CARDS: PickInitialDestinationCardsState,
        GameState.PICK_SECOND_TRAIN_CARD: PickSecondTrainCardState,
        GameState.PICK_DESTINATION_CARDS: PickDestinationCardsState,
        GameState.END: EndState
    }

    @classmethod
    def processAction(cls, action: PlayerAction, payload: dict, connectionId: str):
        if action == PlayerAction.CREATE_GAME:
            cls.createGame(payload, connectionId)
        elif action == PlayerAction.JOIN_GAME:
            cls.joinGame(payload, connectionId)
        else:
            cls.updateGame(action, payload, connectionId)

    @classmethod
    def createGame(cls, payload: dict, connectionId: str):
        validatePayload(payload, 'id', 'name')

        hostPlayer = Player(
            id=payload['id'],
            name=payload['name'],
            connectionId=connectionId
        )

        # gameId = '0000'
        gameId = str(randint(111111,999999))
        gameDetails = GameDetails(
            gameId=gameId,
            players=[hostPlayer],
            gameState=GameState.MATCH_MAKING,
            hostId=hostPlayer.id,
        )

        updateGameDetails(gameDetails)
        updatePlayers(gameDetails)

    @classmethod
    def joinGame(cls, payload: dict, connectionId: str):
        validatePayload(payload, 'id', 'name', 'gameId')

        gameDetails = getGameDetails(payload['gameId'])

        if not gameDetails:
            raise GameEngineValidationException(f"Game: {payload['gameId']} not found")

        if gameDetails.gameState != GameState.MATCH_MAKING:
            raise GameEngineValidationException(f"Game {gameDetails.gameId} already started, can't join game.")

        for player in gameDetails.players:
            if player.id == payload['id']:
                raise GameEngineValidationException(f"Player id {player.id} already exist in game {payload['gameId']}")

        if len(gameDetails.players) >= 4:
            raise GameEngineValidationException(f"Game roster is full for game {payload['gameId']}")

        player = Player(
            id=payload['id'],
            name=payload['name'],
            connectionId=connectionId
        )

        gameDetails.players.append(player)

        updateGameDetails(gameDetails)
        updatePlayers(gameDetails)

    @classmethod
    def updateGame(cls, action: PlayerAction, payload: dict, connectionId: str):
        validatePayload(payload, 'id', 'gameId')

        gameDetails = getGameDetails(payload['gameId'])

        stateHandler = cls.STATE_HANDLER_MAP[gameDetails.gameState]

        stateHandler.validateInput(action, payload, gameDetails)

        stateHandler.submitInput(action, payload, gameDetails)


def validatePayload(payload: dict, *fields: str):
    for field in fields:
        if field not in payload:
            raise GameEngineException(f"{field} not found in payload")

class GameEngineValidationException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f'GameEngineValidationException: {msg}')

class GameEngineException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f'GameEngineException: {msg}')
