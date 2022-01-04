from enum import Enum, auto

class AutoName(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class GameState(AutoName):
    MATCH_MAKING = auto()

    PICK_INITIAL_DESTINATION_CARDS = auto()

    TURN = auto()
    PICK_SECOND_TRAIN_CARD = auto()
    PICK_DESTINATION_CARDS = auto()

    END = auto()