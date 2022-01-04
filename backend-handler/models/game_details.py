from .player import Player
from .destination import Destination

from constants import TrainColor, GameState

class GameDetails:

    def __init__(self, 
            gameId: int, 
            players: list[Player], 
            gameState: GameState,
            hostId: int,
            pathOwnership: dict = None, # pathId : playerId
            availableCards: list[TrainColor] = None,
            trainCardPile: list[TrainColor] = None,
            destinationCardPile: list[int] = None,
            discardTrainCardPile: list[TrainColor] = None,
            activePlayerId: int = None):
        self.gameId: int = gameId
        self.players: list[Player] =  players
        self.gameState: GameState = gameState
        self.hostId: int = hostId

        self.pathOwnership: dict = dict() if pathOwnership == None else pathOwnership

        self.availableCards: list[TrainColor] = [] if availableCards == None else availableCards
        self.trainCardPile: list[TrainColor] = [] if trainCardPile == None else trainCardPile
        self.destinationCardPile: list[int] = [] if destinationCardPile == None else destinationCardPile
        self.discardTrainCardPile: list[TrainColor] = [] if discardTrainCardPile == None else discardTrainCardPile

        self.activePlayerId: int = activePlayerId

    def toDict(self) -> dict:
        return {
            'gameId': self.gameId,
            'pathOwnership': pathOwnershipToStrDict(self.pathOwnership),
            'players': [player.toDict() for player in self.players],
            'availableCards': [card._name_ for card in self.availableCards],
            'trainCardPile': [card._name_ for card in self.trainCardPile],
            'destinationCardPile': self.destinationCardPile,
            'discardTrainCardPile': [card._name_ for card in self.discardTrainCardPile],
            'gameState': self.gameState._name_,
            'hostId': self.hostId,
            'activePlayerId': self.activePlayerId,
        }

    
    
    def fromDict(item: dict):
        return GameDetails(
            gameId=item['gameId'],
            pathOwnership=pathOwnershipToIntDict(item['pathOwnership']),
            players=[Player.fromDict(player) for player in item['players']],
            availableCards=[TrainColor[card] for card in item['availableCards']],
            trainCardPile=[TrainColor[card] for card in item['trainCardPile']],
            destinationCardPile=item['destinationCardPile'],
            discardTrainCardPile=[TrainColor[card] for card in item['discardTrainCardPile']],
            gameState=GameState[item['gameState']],
            hostId=item['hostId'],
            activePlayerId=item['activePlayerId']
        )

def pathOwnershipToStrDict(intDict: dict) -> dict:
    print(intDict)
    stringDict = dict()
    for key, value in intDict.items():
        stringDict[str(key)] = value
    return stringDict

def pathOwnershipToIntDict(stringDict: dict) -> dict:
    intDict = dict()
    for key, value in stringDict.items():
        intDict[int(key)] = value
    return intDict
    
