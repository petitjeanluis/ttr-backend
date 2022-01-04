from ..state_handler import StateHandler
from constants import GameState

class EndState(StateHandler):

    GAME_STATE = GameState.END
    
    def validateInput(self, action, payload: dict) -> None:
        pass

    def submitInput(self, action, payload: dict) -> None:
        pass