from .destination import Destination

from constants import PlayerColor, TrainColor

class Player:
    
    def __init__(self, 
            id: int, 
            name: str, 
            connectionId: str,
            color: PlayerColor = PlayerColor.BLACK, 
            trainCards: list[TrainColor] = None, 
            destinationCards: list[int] = None, 
            trainCount: int = 0, 
            pathScore: int = 0,
            destinationOptionSet: list[int] = None) -> None:
        self.id: int = id
        self.name: str = name
        self.connectionId: str = connectionId
        self.color: PlayerColor = color
        self.trainCards: list[TrainColor] = [] if trainCards == None else trainCards
        self.destinationCards: list[int] = [] if destinationCards == None else destinationCards
        self.trainCount: int = trainCount
        self.pathScore: int = pathScore
        self.destinationOptionSet: list[int] = [] if destinationOptionSet == None else destinationOptionSet

    def toDict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'connectionId': self.connectionId,
            'color': self.color._name_,
            'trainCards': [card._name_ for card in self.trainCards],
            'destinationCards': self.destinationCards,
            'trainCount': self.trainCount,
            'pathScore': self.pathScore,
            'destinationOptionSet': self.destinationOptionSet
        }

    def fromDict(item: dict):
        return Player(
            id=item['id'],
            name=item['name'],
            connectionId=item['connectionId'],
            color=PlayerColor[item['color']],
            trainCards=[TrainColor[card] for card in item['trainCards']],
            destinationCards=item['destinationCards'],
            trainCount=item['trainCount'],
            pathScore=item['pathScore'],
            destinationOptionSet=item['destinationOptionSet']
        )