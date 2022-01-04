import unittest
from unittest.mock import patch

from state.handlers import PickSecondTrainCardState
from state import StateMachineValidationException
from state.actions import PlayerAction

from constants import GameState, TrainColor

from test_utils import createGameDetails

class TestPickSecondTrainState(unittest.TestCase):

    # General Checks
    def test_invalid_action(self):
        error: StateMachineValidationException = None
        try:
            PickSecondTrainCardState.validateInput(PlayerAction.CREATE_GAME, None, None)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r'CREATE_GAME is not a valid input for PICK_SECOND_TRAIN_CARD')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_invalid_player(self):
        gameDetails = createGameDetails(GameState.PICK_SECOND_TRAIN_CARD)
        payload = dict()
        payload['id'] = -1

        error: StateMachineValidationException = None
        try:
            PickSecondTrainCardState.validateInput(PlayerAction.PICK_RANDOM_TRAIN_CARD, payload, gameDetails)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r'Player -1 is not part of this game.')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_not_turn(self):
        gameDetails = createGameDetails(GameState.PICK_SECOND_TRAIN_CARD)
        payload = dict()
        payload['id'] = 2

        error: StateMachineValidationException = None
        try:
            PickSecondTrainCardState.validateInput(PlayerAction.PICK_RANDOM_TRAIN_CARD, payload, gameDetails)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r'It is not your turn!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_pick_train_card_invalid_index(self):
        gameDetails = createGameDetails(GameState.PICK_SECOND_TRAIN_CARD)
        payload = dict()
        payload['id'] = 1
        payload['trainCardIndex'] = 5

        error: StateMachineValidationException = None
        try:
            PickSecondTrainCardState.validateInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r"Invalid train card index provided!")
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_bad_pick_wild_train_card(self, ):
        gameDetails = createGameDetails(GameState.PICK_SECOND_TRAIN_CARD)
        gameDetails.availableCards[0] = TrainColor.WILD
        payload = dict()
        payload['id'] = 1
        payload['trainCardIndex'] = 0

        error: StateMachineValidationException = None
        try:
            PickSecondTrainCardState.validateInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r'Cannot pick wild card as second pick!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    @patch('state.handlers.pick_second_train_card_state.updateGameDetails')
    @patch('state.handlers.pick_second_train_card_state.updatePlayers')
    def test_successful_pick_color_train_card(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.PICK_SECOND_TRAIN_CARD)
        gameDetails.availableCards = [TrainColor.GREEN for i in range(5)]
        payload = dict()
        payload['id'] = 1
        payload['trainCardIndex'] = 0
        trainCardCount = len(gameDetails.trainCardPile)

        PickSecondTrainCardState.validateInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)
        PickSecondTrainCardState.submitInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert len(gameDetails.trainCardPile) == trainCardCount - 1
        assert len(gameDetails.players[0].trainCards) == 1
        assert gameDetails.activePlayerId == 2

    @patch('state.handlers.pick_second_train_card_state.updateGameDetails')
    @patch('state.handlers.pick_second_train_card_state.updatePlayers')
    def test_successful_pick_random_train_card(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.PICK_SECOND_TRAIN_CARD)
        payload = dict()
        payload['id'] = 1
        trainCardCount = len(gameDetails.trainCardPile)

        PickSecondTrainCardState.validateInput(PlayerAction.PICK_RANDOM_TRAIN_CARD, payload, gameDetails)
        PickSecondTrainCardState.submitInput(PlayerAction.PICK_RANDOM_TRAIN_CARD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert len(gameDetails.trainCardPile) == trainCardCount - 1
        assert len(gameDetails.players[0].trainCards) == 1
        assert gameDetails.activePlayerId == 2
        