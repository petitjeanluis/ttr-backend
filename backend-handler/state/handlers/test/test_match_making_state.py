import unittest

from state import StateMachineValidationException
from state.handlers import MatchMakingState
from state.actions import PlayerAction

from constants import GameState

from test_utils import createGameDetails

class TestMatchMakingState(unittest.TestCase):

    # General Checks
    def test_invalid_action(self):
        error: StateMachineValidationException = None
        try:
            MatchMakingState.validateInput(PlayerAction.CREATE_GAME, None, None)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r'CREATE_GAME is not a valid input for MATCH_MAKING')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_invalid_player(self):
        gameDetails = createGameDetails(GameState.MATCH_MAKING)
        gameDetails.activePlayerId = 1
        payload = dict()
        payload['id'] = -1

        error: StateMachineValidationException = None
        try:
            MatchMakingState.validateInput(PlayerAction.START_GAME, payload, gameDetails)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r'Player -1 is not part of this game.')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    # Match making errors
    def test_not_started_by_host(self):
        gameDetails = createGameDetails(GameState.MATCH_MAKING)
        gameDetails.activePlayerId = 1
        payload = dict()
        payload['id'] = 2

        error: StateMachineValidationException = None
        try:
            MatchMakingState.validateInput(PlayerAction.START_GAME, payload, gameDetails)
        except StateMachineValidationException as e:
            error = e
            self.assertRegex(str(e), r'Host may only start the game!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    # Successful Test
    def test_successful_game_start(self):
        gameDetails = createGameDetails(GameState.MATCH_MAKING)
        payload = dict()
        payload['id'] = 1

        MatchMakingState.validateInput(PlayerAction.START_GAME, payload, gameDetails)
        MatchMakingState.submitInput(PlayerAction.START_GAME, payload, gameDetails)

        assert gameDetails.gameState == GameState.PICK_INITIAL_DESTINATION_CARDS
        assert gameDetails.activePlayerId != None
        for player in gameDetails.players:
            assert len(player.destinationOptionSet) == 3