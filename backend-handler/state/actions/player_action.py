from enum import Enum, auto

class AutoName(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class PlayerAction(AutoName):
    PICK_RANDOM_TRAIN_CARD = auto()
    PICK_TRAIN_CARD = auto()
    GET_DESTINATION_CARDS = auto()
    PICK_DESTINATION_CARDS = auto()
    BUILD = auto()

    JOIN_GAME = auto()
    CREATE_GAME = auto()
    START_GAME = auto()
    