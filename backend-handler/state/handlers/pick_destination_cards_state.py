from ..state_handler import StateHandler
from ..state_exceptions import StateMachineValidationException
from ..actions import PlayerAction

from ..utils import getNextPlayerId, validateAndGetPlayer, getPlayer, validateTurn
from constants import GameState
from models import GameDetails, Player

class PickDestinationCardsState(StateHandler):

    GAME_STATE = GameState.PICK_DESTINATION_CARDS
    
    VALID_ACTIONS: dict[PlayerAction, list[str]] = {
        PlayerAction.PICK_DESTINATION_CARDS: ['destinationCardIds']
    }
    
    @classmethod
    def validateInput(cls, action: PlayerAction, payload: dict, gameDetails: GameDetails) -> None:
        if action not in cls.VALID_ACTIONS:
            raise StateMachineValidationException(f'{action} is not a valid input for {cls.GAME_STATE}')

        for field in cls.VALID_ACTIONS[action]:
            if field not in payload:
                raise StateMachineValidationException(f'{field} not found in payload for {cls.GAME_STATE} {action}')

        # validate player belongs to this game
        current_player: Player = validateAndGetPlayer(payload, gameDetails)

        validateTurn(payload, gameDetails)

        # validate destination card list provided
        if not isinstance(payload['destinationCardIds'], list):
            raise StateMachineValidationException("Must provide number list of destination card ids!")
        
        # validate at least 1 cards picked
        if len(payload['destinationCardIds']) < 1:
            raise StateMachineValidationException("Must pick at least 1 destination card!")
        
        # validate destination cards picked were part of the option set given
        for id in payload['destinationCardIds']:
            found = False
            for card in current_player.destinationOptionSet:
                if card == id:
                    found = True
                    break
            if not found:
                raise StateMachineValidationException("Picked a destination card not supplied!")

        # validate no dupplicates were given
        cardSet = set()
        for id in payload['destinationCardIds']:
            cardSet.add(id)
        if len(cardSet) != len(payload['destinationCardIds']):
            raise StateMachineValidationException("Picked duplicate cards!")



    @classmethod
    def submitInput(cls, action, payload: dict, gameDetails: GameDetails) -> None:
        selectedCardIds = payload['destinationCardIds']
        player: Player = getPlayer(payload, gameDetails)

        while len(player.destinationOptionSet) > 0:
            destinationCard = player.destinationOptionSet.pop()
            if destinationCard in selectedCardIds:
                player.destinationCards.append(destinationCard)
            else:
                gameDetails.destinationCardPile.append(destinationCard)

        gameDetails.gameState = GameState.TURN
        gameDetails.activePlayerId = getNextPlayerId(gameDetails)
