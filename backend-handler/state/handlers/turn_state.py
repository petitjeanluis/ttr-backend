from ..state_handler import StateHandler
from ..state_exceptions import StateMachineValidationException
from ..actions import PlayerAction

from ..utils import validateAndGetPlayer, validateTurn, getPlayer, getNextPlayerId, makeCountDict

from constants import PATH_MAP, Path, TrainColor, GameState, PATH_VALUE
from models import GameDetails, Player

class TurnState(StateHandler):

    GAME_STATE = GameState.TURN

    VALID_ACTIONS: dict = {
        PlayerAction.BUILD: ['pathId', 'trainCards'],
        PlayerAction.GET_DESTINATION_CARDS: [],
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

        player: Player = validateAndGetPlayer(payload, gameDetails)

        validateTurn(payload, gameDetails)
        
        if action == PlayerAction.BUILD:
            cls.validateBuildInput(payload, gameDetails, player)
        elif action == PlayerAction.PICK_TRAIN_CARD:
            cls.validatePickTrainCardInput(payload)

    @classmethod
    def validateBuildInput(cls, payload: dict, gameDetails: GameDetails, player: Player):
        if payload['pathId'] < 0 or payload['pathId'] >= 100:
            raise StateMachineValidationException(f"Invalid path id selected!")

        if payload['pathId'] in gameDetails.pathOwnership:
            raise StateMachineValidationException(f"Selected path is already owned!")

        path: Path = PATH_MAP[payload['pathId']]

        if path.length > player.trainCount:
            raise StateMachineValidationException(f"Player does not have enough trains!")
        
        if len(payload['trainCards']) != path.length:
            raise StateMachineValidationException(f"Player did not provide the correct number of cards!")

        tempCards: list[TrainColor] = player.trainCards[:]
        for card in payload['trainCards']:
            if TrainColor[card] not in tempCards:
                raise StateMachineValidationException(f'Some or all provided cards did not belong to the player.')
            tempCards.remove(TrainColor[card])

        for card in payload['trainCards']:
            cardCountDict = makeCountDict([TrainColor[card] for card in payload['trainCards']])

            if len(cardCountDict) > 2:
                raise StateMachineValidationException("Provided more than 2 types of cards, can't build!")

            if len(cardCountDict) == 2 and TrainColor.WILD not in cardCountDict:
                    raise StateMachineValidationException("Provided two different colors, can't build!")

            if path.trainColor != TrainColor.WILD:
                if path.trainColor not in cardCountDict and TrainColor.WILD not in cardCountDict:
                    raise StateMachineValidationException("Provided the wrong color for path, can't build!")
    
    @classmethod
    def validatePickTrainCardInput(cls, payload: dict):
        trainCardIndex = payload['trainCardIndex']

        if trainCardIndex < 0 or trainCardIndex >= 5:
            raise StateMachineValidationException(f"Invalid train card index provided!")
    

    @classmethod
    def submitInput(cls, action: PlayerAction, payload: dict, gameDetails: GameDetails) -> None:
        if action == PlayerAction.BUILD:
            cls.submitBuildInput(payload, gameDetails)
        elif action == PlayerAction.GET_DESTINATION_CARDS:
            cls.submitGetDestinationCardsInput(payload, gameDetails)
        elif action == PlayerAction.PICK_TRAIN_CARD:
            cls.submitPickTrainCardInput(payload, gameDetails)
        elif action == PlayerAction.PICK_RANDOM_TRAIN_CARD:
            cls.submitPickRandomTrainCardInput(payload, gameDetails)

    @classmethod
    def submitBuildInput(cls, payload: dict, gameDetails: GameDetails):
        path: Path = PATH_MAP[payload['pathId']]
        selectedCards: list[TrainColor] = [TrainColor[card] for card in payload['trainCards']]
        player: Player = getPlayer(payload, gameDetails)

        player.trainCount = player.trainCount - path.length
        player.pathScore = player.pathScore + PATH_VALUE[path.length]

        for card in selectedCards:
            player.trainCards.remove(card)
            gameDetails.discardTrainCardPile.append(card)

        gameDetails.pathOwnership[path.id] = player.id

        gameDetails.activePlayerId = getNextPlayerId(gameDetails)
        
        
    @classmethod
    def submitGetDestinationCardsInput(cls, payload: dict, gameDetails: GameDetails):
        player: Player = getPlayer(payload, gameDetails)

        destinationCards: list[int] = []
        for i in range(3):
            destinationCards.append(gameDetails.destinationCardPile.pop(0))
        
        player.destinationOptionSet = destinationCards
        
        gameDetails.gameState = GameState.PICK_DESTINATION_CARDS

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
        
        # transtion state only if non-wild card is picked, else switch to next player
        if pickedCard != TrainColor.WILD:
            gameDetails.gameState = GameState.PICK_SECOND_TRAIN_CARD
        else:
            gameDetails.activePlayerId = getNextPlayerId(gameDetails)


    @classmethod
    def submitPickRandomTrainCardInput(cls, payload: dict, gameDetails: GameDetails):
        player: Player = getPlayer(payload, gameDetails)

        nextCard: TrainColor = gameDetails.trainCardPile.pop()
        player.trainCards.append(nextCard)

        gameDetails.gameState = GameState.PICK_SECOND_TRAIN_CARD

    
        