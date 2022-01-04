from models import GameDetails, Player
from constants import GameState
from state import getAllTrainCards, getAllDestinationCards

def createGameDetails(gameState: GameState = GameState.MATCH_MAKING) -> GameDetails:
    player1 = Player(
            id=1,
            name='Boots',
            connectionId='connection1'
        )

    player2 = Player(
            id=2,
            name='Squirrel',
            connectionId='connection2'
        )

    gameId = 2
    gameDetails = GameDetails(
        gameId=gameId,
        players=[player1, player2],
        gameState=gameState,
        hostId=player1.id,
        destinationCardPile=getAllDestinationCards(),
        trainCardPile=getAllTrainCards(),
        activePlayerId=player1.id
    )

    for count in range(5):
        gameDetails.availableCards.append(gameDetails.trainCardPile.pop())
    
    return gameDetails
