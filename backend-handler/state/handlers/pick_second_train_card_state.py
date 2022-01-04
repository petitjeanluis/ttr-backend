from ..state_handler import StateHandler
from ..state_exceptions import StateMachineValidationException
from ..actions import PlayerAction

from ..utils import validateAndGetPlayer, validateTurn, getPlayer, makeCountDict, getNextPlayerId
from services import updateGameDetails, updatePlayers
from constants import TrainColor, GameState
from models import GameDetails, Player

class PickSecondTrainCardState(StateHandler):

    GAME_STATE = GameState.PICK_SECOND_TRAIN_CARD
    
    VALID_ACTIONS: dict = {
        PlayerAction.PICK_TRAIN_CARD: ['trainCardIndex'],
        PlayerAction.PICK_RANDOM_TRAIN_CARD: []
    }
    
    @classmethod
    def validateInput(cls, action: PlayerAction, payload: dict, gameDetails: GameDetails) -> None:
        if action not in cls.VALID_ACTIONS:
            raise StateMachineValidationException(f'{action} is not a valid input for {cls.GAME_STATE}')

        for field in cls.VALID_ACTIONS[action]:
            if field not in payload:
                raise StateMachineValidationException(f'{field} not found in payload for {cls.GAME_STATE} {action}')

        validateAndGetPlayer(payload, gameDetails)

        validateTurn(payload, gameDetails)

        if action == PlayerAction.PICK_TRAIN_CARD:
            trainCardIndex = payload['trainCardIndex']

            # validate valid index
            if trainCardIndex < 0 or trainCardIndex >= 5:
                raise StateMachineValidationException(f"Invalid train card index provided!")

            # not a wild card
            if gameDetails.availableCards[trainCardIndex] == TrainColor.WILD:
                raise StateMachineValidationException("Cannot pick wild card as second pick!")


    @classmethod
    def submitInput(cls, action, payload: dict, gameDetails: GameDetails) -> None:
        if action == PlayerAction.PICK_TRAIN_CARD:
            cls.submitPickTrainCardInput(payload, gameDetails)
        elif action == PlayerAction.PICK_RANDOM_TRAIN_CARD:
            cls.submitPickRandomTrainCardInput(payload, gameDetails)
        
        updateGameDetails(gameDetails)
        updatePlayers(gameDetails)

    @classmethod
    def submitPickTrainCardInput(cls, payload: dict, gameDetails: GameDetails):
        trainCardIndex = payload['trainCardIndex']
        player: Player = getPlayer(payload, gameDetails)

        # give player the card
        pickedCard: TrainColor = gameDetails.availableCards[trainCardIndex]
        player.trainCards.append(pickedCard)

        # TODO: handle reshuffle for empty train card pile
        # update available cards and check for triple wild
        nextCard: TrainColor = gameDetails.trainCardPile.pop()
        gameDetails.availableCards[trainCardIndex] = nextCard
        trainCardCount = makeCountDict(gameDetails.availableCards)
        while TrainColor.WILD in trainCardCount and trainCardCount[TrainColor.WILD] >= 3:
            for i in range(5):
                gameDetails.discardTrainCardPile.append(gameDetails.availableCards.pop())
            for i in range(5):
                gameDetails.availableCards.append(gameDetails.trainCardPile.pop())
            trainCardCount = makeCountDict(gameDetails.availableCards)
        
        gameDetails.gameState = GameState.TURN
        gameDetails.activePlayerId = getNextPlayerId(gameDetails)


    @classmethod
    def submitPickRandomTrainCardInput(cls, payload: dict, gameDetails: GameDetails):
        player: Player = getPlayer(payload, gameDetails)

        nextCard: TrainColor = gameDetails.trainCardPile.pop()
        player.trainCards.append(nextCard)

        gameDetails.gameState = GameState.TURN
        gameDetails.activePlayerId = getNextPlayerId(gameDetails)