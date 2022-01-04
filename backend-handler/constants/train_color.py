from enum import Enum, auto

class AutoName(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

class TrainColor(AutoName):
    BLACK = auto()
    WHITE = auto()
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()
    PINK = auto()
    ORANGE = auto()
    WILD = auto()
    