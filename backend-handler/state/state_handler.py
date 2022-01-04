from .actions import PlayerAction
from .state_exceptions import StateMachineException

from models import GameDetails

class StateHandler:
    
    def validateInput(self, action: PlayerAction, payload: dict, gameDetails: GameDetails) -> None:
        raise StateMachineException('Must implement StateMachine.validateInput()!')

    def submitInput(self, action: PlayerAction, payload: dict, gameDetails: GameDetails) -> None:
        raise StateMachineException('Must implement StateMachine.submitInput()!')
