from .destination import Destination

class DestinationSet:

    def __init__(self, id: str, destinationCards: list[Destination]) -> None:
        self.id: str = id
        self.destinationCards: list[Destination] = destinationCards
