from models import GameDetails, Player, Destination
from constants import TrainColor, PlayerColor, DESTINATION_CARDS, TRAIN_CARDS
from .state_exceptions import StateMachineValidationException
from random import randint

def validateAndGetPlayer(payload: dict, gameDetails: GameDetails) -> Player:
        current_player: Player = None

        for player in gameDetails.players:
            if player.id == payload['id']:
                current_player = player

        if not current_player:
            raise StateMachineValidationException(f"Player {payload['id']} is not part of this game.")

        return current_player

def getPlayer(payload: dict, gameDetails: GameDetails) -> Player:
        current_player: Player = None

        for player in gameDetails.players:
            if player.id == payload['id']:
                current_player = player

        return current_player

def validateTurn(payload: dict, gameDetails: GameDetails):
    if gameDetails.activePlayerId != payload['id']:
        raise StateMachineValidationException('It is not your turn!')

def getNextPlayerId(gameDetails: GameDetails) -> int:
    activePlayerId = gameDetails.activePlayerId
    nextIndex: int
    for i, player in enumerate(gameDetails.players):
        if player.id == activePlayerId:
            nextIndex = (i+1)%len(gameDetails.players)
            break
    return gameDetails.players[nextIndex].id

def makeCountDict(array: list[any]) -> dict[any, int]:
    countDict = dict()
    for item in array:
        if item in countDict:
            countDict[item] = countDict[item] + 1
        else:
            countDict[item] = 1
    return countDict

def getAllPlayerColors() -> list[PlayerColor]:
    colors: list[PlayerColor] = []
    for color in PlayerColor:
        colors.append(color)

    shuffle(colors)
    return colors

def getAllTrainCards() -> list[TrainColor]:
    trainCards: list[TrainColor] = []
    
    for card in TRAIN_CARDS:
        for i in range(card['count']):
            trainCards.append(card['trainColor'])
    
    shuffle(trainCards)

    return trainCards

def getAllDestinationCards() -> list[int]:
    destinationCards: list[Destination] = []

    for card in DESTINATION_CARDS:
        destinationCards.append(card['id'])

    shuffle(destinationCards)

    return destinationCards
    

def shuffle(array: list):
    n: int = len(array)

    for i in range(n-2):
        j = randint(i,n-1)
        temp = array[i]
        array[i] = array[j]
        array[j] = temp