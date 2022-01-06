from ..state_handler import StateHandler
from ..state_exceptions import StateMachineValidationException
from ..actions import PlayerAction
from ..utils import getAllPlayerColors, getAllTrainCards, getAllDestinationCards, validateAndGetPlayer

from models import GameDetails, Player
from constants import TrainColor, PlayerColor, GameState
from random import randint

class MatchMakingState(StateHandler):

    GAME_STATE = GameState.MATCH_MAKING

    VALID_ACTIONS: dict = {
        PlayerAction.START_GAME: []
    }
    
    @classmethod
    def validateInput(cls, action: PlayerAction, payload: dict, gameDetails: GameDetails) -> None:
        if action not in cls.VALID_ACTIONS:
            raise StateMachineValidationException(f'{action} is not a valid input for {cls.GAME_STATE}')

        for field in cls.VALID_ACTIONS[action]:
            if field not in payload:
                raise StateMachineValidationException(f'{field} not found in payload for {cls.GAME_STATE} {action}')

        player: Player = validateAndGetPlayer(payload, gameDetails)

        if player.id != gameDetails.hostId:
            raise StateMachineValidationException("Host may only start the game!")

    @classmethod
    def submitInput(cls, action: PlayerAction, payload: dict, gameDetails: GameDetails) -> None:
        '''
            Initialize:
                get shuffled train cards
                get shuffled destination cards
                assign player colors
                give train cards to players
                give destination card option set to players
                set available cards (check for three wild card case TODO)
                set train card and destination card piles
                pick first player
                transition state
                update
        '''

        trainCards: list[TrainColor] = getAllTrainCards()
        destinationTrainCards: list[list] = getAllDestinationCards()
        playerColors: list[PlayerColor] = getAllPlayerColors()

        for player in gameDetails.players:
            player.color = playerColors.pop()
            player.trainCount = 45
            for _ in range(4):
                player.trainCards.append(trainCards.pop())

            for _ in range(3):
                player.destinationOptionSet.append(destinationTrainCards.pop(0))

        for _ in range(5):
            gameDetails.availableCards.append(trainCards.pop())
        
        gameDetails.trainCardPile = trainCards
        gameDetails.destinationCardPile = destinationTrainCards

        randomIndex = randint(0,len(gameDetails.players)-1)
        gameDetails.activePlayerId = gameDetails.players[randomIndex].id

        gameDetails.gameState = GameState.PICK_INITIAL_DESTINATION_CARDS
