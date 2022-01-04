from enum import Enum, auto

class AutoName(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class PlayerColor(AutoName):
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()
    BLACK = auto()
    