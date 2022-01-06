import unittest

from state.handlers import PickInitialDestinationCardsState
from state.actions import PlayerAction
from state import StateMachineValidationException
from constants import GameState

from test_utils import createGameDetails

class TestPickInitialDestinationCards(unittest.TestCase):

    # General Checks

    def test_invalid_action(self):
        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.CREATE_GAME, None, None)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'CREATE_GAME is not a valid input for PICK_INITIAL_DESTINATION_CARDS')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_invalid_player(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        payload = dict()
        payload['id'] = -1
        payload['destinationCardIds'] = []

        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Player -1 is not part of this game.')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_no_destination_card_list_passed(self):
        gameDetails = createGameDetails()
        gameDetails.players[0].destinationOptionSet = [0, 1, 2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = 0

        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Must provide number list of destination card ids!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_no_destination_cards_picked(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = [0, 1, 2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = []

        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Must pick at least 2 destination cards!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_one_destination_cards_picked(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = [0, 1, 2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0]

        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Must pick at least 2 destination cards!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_destination_cards_not_in_option_set(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = [0, 1, 2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0,4]

        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Picked a destination card not supplied!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_duplicates_given(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = [0,1,2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0, 0]

        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Picked duplicate cards!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_already_picked_cards(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = []
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0,4]

        error: StateMachineValidationException = None
        try:
            PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Player already selected initial destination cards')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_successful_initial_pick(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = [0,1,2]
        gameDetails.players[1].destinationOptionSet = [3,4,5]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0, 2]
        destinationCardPileCount = len(gameDetails.destinationCardPile)
        
        PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        PickInitialDestinationCardsState.submitInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        
        assert gameDetails.gameState == GameState.PICK_INITIAL_DESTINATION_CARDS
        assert len(gameDetails.players[0].destinationOptionSet) == 0
        assert len(gameDetails.players[0].destinationCards) == 2
        assert len(gameDetails.destinationCardPile) == destinationCardPileCount + 1

    def test_successful_initial_pick_and_transition(self):
        gameDetails = createGameDetails(GameState.PICK_INITIAL_DESTINATION_CARDS)
        gameDetails.players[0].destinationOptionSet = [0,1,2]
        payload = dict()
        payload['id'] = 1
        payload['destinationCardIds'] = [0, 2]
        destinationCardPileCount = len(gameDetails.destinationCardPile)
        
        PickInitialDestinationCardsState.validateInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        PickInitialDestinationCardsState.submitInput(PlayerAction.PICK_DESTINATION_CARDS, payload, gameDetails)
        
        assert gameDetails.gameState == GameState.TURN
        assert len(gameDetails.players[0].destinationOptionSet) == 0
        assert len(gameDetails.players[0].destinationCards) == 2
        assert len(gameDetails.destinationCardPile) == destinationCardPileCount + 1
