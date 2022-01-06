from .player import Player

from constants import PlayerColor

class Opponent:

    def __init__(self, player: Player):
        self.name: str = player.name
        self.color: PlayerColor = player.color
        self.trainCardCount: int = len(player.trainCards)
        self.destinationCardCount: int = len(player.destinationCards)
        self.trainCount: int = player.trainCount
        self.pathScore: int = player.pathScore

    def toDict(self) -> dict:
        return {
            'name': self.name,
            'color': self.color._name_,
            'trainCardCount': self.trainCardCount,
            'destinationCardCount': self.destinationCardCount,
            'trainCount': self.trainCount,
            'pathScore': self.pathScore
        }
