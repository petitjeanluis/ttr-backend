from .game_details import GameDetails
from .opponent import Opponent
from .player import Player

from constants import TrainColor, GameState

class StateUpdate:

    def __init__(self, 
            pathOwnership: dict,
            opponents: list[Opponent],
            availableCards: list[TrainColor],
            player: Player,
            activePlayerId: str,
            gameState: GameState) -> None:
        self.pathOwnership: dict = pathOwnership
        self.opponents: list[Opponent] = opponents
        self.availableCards: list[TrainColor] = availableCards
        self.player: Player = player
        self.activePlayerId: str = activePlayerId
        self.gameState: GameState = gameState
    
    def toDict(self) -> dict:
        return {
            'pathOwnership': self.pathOwnership,
            'opponents': [opponent.toDict() for opponent in self.opponents],
            'availableCards': [card._name_ for card in self.availableCards],
            'player': self.player.toDict(),
            'activePlayerId': self.activePlayerId,
            'gameState': self.gameState._name_
        }


def buildStateUpdates(gameDetails: GameDetails) -> dict[str, StateUpdate]:
    stateUpdates: dict[str, StateUpdate] = {}

    opponents: dict[str, list[Opponent]] = {}

    for player in gameDetails.players:
        tempOpponents = []
        for player2 in gameDetails.players:
            if player2.id == player.id:
                continue
            else:
                tempOpponents.append(Opponent(player2))
        opponents[player.id] = tempOpponents

    

    for player in gameDetails.players:
        stateUpdate = StateUpdate(
            pathOwnership=gameDetails.pathOwnership,
            opponents=opponents[player.id],
            availableCards=gameDetails.availableCards,
            player=player,
            activePlayerId=gameDetails.activePlayerId,
            gameState=gameDetails.gameState
        )
        stateUpdates[player.connectionId] = stateUpdate

    return stateUpdates