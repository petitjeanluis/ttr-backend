import unittest
from unittest.mock import patch

from state import StateMachineValidationException
from state.handlers import PickDestinationCardsState
from state.actions import PlayerAction

from constants import GameState

from test_utils import createGameDetails

class TestPickDestinationCardsState(unittest.TestCase):

    # General Checks

    def test_invalid_action(self):
        error: StateMachineValidationException = None
        try:
            PickDestinationCardsState.validateInput(PlayerAction.CREATE_GAME, None, None)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'CREATE_GAME is not a valid input for PICK_DESTINATION_CARDS')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_invalid_player(self):
        gameDetails = createGameDetails(GameState.PICK_DESTINATION_CARDS)
        payload = dict()
        payload['id'] = -1
        payload['destinationCardIds'] = []

        error: StateMachineValidationException = None
        try:
            PickDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Player -1 is not part of this game.')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_not_turn(self):
        gameDetails = createGameDetails(GameState.PICK_DESTINATION_CARDS)
        payload = dict()
        payload['id'] = 2
        payload['destinationCardIds'] = []

        error: StateMachineValidationException = None
        try:
            PickDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'It is not your turn!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    # Error Tests

    def test_no_destination_card_list_passed(self):
        gameDetails = createGameDetails(GameState.PICK_DESTINATION_CARDS)
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = 0

        error: StateMachineValidationException = None
        try:
            PickDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Must provide number list of destination card ids!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_no_destination_cards_picked(self):
        gameDetails = createGameDetails(GameState.PICK_DESTINATION_CARDS)
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = []

        error: StateMachineValidationException = None
        try:
            PickDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Must pick at least 1 destination card!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_destination_cards_not_in_option_set(self):
        gameDetails = createGameDetails(GameState.PICK_DESTINATION_CARDS)
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0]

        error: StateMachineValidationException = None
        try:
            PickDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Picked a destination card not supplied!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_duplicates_given(self):
        gameDetails = createGameDetails(GameState.PICK_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = [0,1,2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0, 0]

        error: StateMachineValidationException = None
        try:
            PickDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Picked duplicate cards!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    @patch('state.handlers.pick_destination_cards_state.updateGameDetails')
    @patch('state.handlers.pick_destination_cards_state.updatePlayers')
    def test_successful_destination_cards_picked(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.PICK_DESTINATION_CARDS)
        gameDetails.destinationCardPile = [3,4,5,6]
        gameDetails.players[0].destinationOptionSet = [0,1,2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0]
        destinationPileCount = len(gameDetails.destinationCardPile)
        
        PickDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        PickDestinationCardsState.submitInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert gameDetails.activePlayerId == 2
        assert len(gameDetails.destinationCardPile) == destinationPileCount + 2
        assert len(gameDetails.players[0].destinationCards) == 1
        assert gameDetails.players[0].destinationCards[0] == 0

