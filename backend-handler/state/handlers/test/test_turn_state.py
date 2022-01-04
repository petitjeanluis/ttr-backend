import unittest
from unittest.mock import patch

from test_utils import createGameDetails
from state.actions import PlayerAction
from state.handlers import TurnState
from state import StateMachineValidationException
from constants import GameState, TrainColor

class TestTurnState(unittest.TestCase):

    # General Checks
    def test_invalid_action(self):
        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.CREATE_GAME, None, None)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'CREATE_GAME is not a valid input for TURN')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_invalid_player(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = -1
        payload['pathId'] = 96
        payload['trainCards'] = ['GREEN','GREEN']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.GET_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Player -1 is not part of this game.')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_not_turn(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = 2
        payload['pathId'] = 96
        payload['trainCards'] = ['GREEN','GREEN']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.GET_DESTINATION_CARDS, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'It is not your turn!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    # Build Tests

    def test_build_missing_pathid(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = 1
        payload['trainCards'] = ['GREEN','GREEN']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'pathId not found in payload')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_invalid_path_id(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 100
        payload['trainCards'] = ['GREEN','GREEN']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Invalid path id selected!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_build_path_already_owned(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.pathOwnership[96] = 0
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96
        payload['trainCards'] = ['GREEN','GREEN']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Selected path is already owned!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)
    
    def test_build_not_enough_trains_pieces(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 0
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96
        payload['trainCards'] = ['GREEN','GREEN']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Player does not have enough trains!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_build_not_enough_train_cards(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 0
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96
        payload['trainCards'] = ['GREEN','GREEN']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r'Player does not have enough trains!')
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_build_three_types_given(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','RED','BLUE']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 0
        payload['trainCards'] = ['GREEN','RED','BLUE']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r"Provided more than 2 types of cards, can't build!")
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    # Path combinations

    def test_build_bad_wild_path_with_no_wild(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','BLUE','BLUE']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 0 # 3 wild
        payload['trainCards'] = ['GREEN','BLUE','BLUE']

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r"Provided two different colors, can't build!")
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_build_bad_color_path_with_non_wild_mix(self): #
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','BLUE']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96 # 2 green
        payload['trainCards'] = ['GREEN','BLUE']
        
        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r"Provided two different colors, can't build!")
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    def test_build_color_path_bad_color(self):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['BLUE','BLUE']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96 # 2 green
        payload['trainCards'] = ['BLUE','BLUE']
        
        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r"Provided the wrong color for path, can't build!")
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    # Invalid Pick Train Card

    def test_pick_train_card_invalid_index(self):
        gameDetails = createGameDetails(GameState.TURN)
        payload = dict()
        payload['id'] = 1
        payload['trainCardIndex'] = 5

        error: StateMachineValidationException = None
        try:
            TurnState.validateInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)
        except Exception as e:
            error = e
            self.assertRegex(str(e), r"Invalid train card index provided!")
            self.assertTrue(isinstance(e, StateMachineValidationException))
        self.assertFalse(error == None)

    # SUCCCESSFUL BUILDS

    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_build_wild_path_with_some_wild(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','WILD','WILD']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 0
        payload['trainCards'] = ['GREEN','WILD','WILD']

        TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.BUILD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert gameDetails.activePlayerId == 2
        assert gameDetails.pathOwnership[0] == 1
        assert gameDetails.players[0].pathScore == 4
        assert gameDetails.players[0].trainCount == 7
        assert len(gameDetails.players[0].trainCards) == 0
        assert len(gameDetails.discardTrainCardPile) == 3
    
    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_build_wild_path_with_all_wild(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['WILD','WILD','WILD']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 0
        payload['trainCards'] = ['WILD','WILD','WILD']

        TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.BUILD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert gameDetails.activePlayerId == 2
        assert gameDetails.pathOwnership[0] == 1
        assert gameDetails.players[0].pathScore == 4
        assert gameDetails.players[0].trainCount == 7
        assert len(gameDetails.players[0].trainCards) == 0
        assert len(gameDetails.discardTrainCardPile) == 3
    
    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_build_wild_path_with_no_wild(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','GREEN','GREEN']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 0
        payload['trainCards'] = ['GREEN','GREEN','GREEN']

        TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.BUILD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert gameDetails.activePlayerId == 2
        assert gameDetails.pathOwnership[0] == 1
        assert gameDetails.players[0].pathScore == 4
        assert gameDetails.players[0].trainCount == 7
        assert len(gameDetails.players[0].trainCards) == 0
        assert len(gameDetails.discardTrainCardPile) == 3

    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_build_color_path_with_some_wild(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','WILD','BLUE']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96
        payload['trainCards'] = ['GREEN','WILD']

        TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.BUILD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert gameDetails.activePlayerId == 2
        assert gameDetails.pathOwnership[96] == 1
        assert gameDetails.players[0].pathScore == 2
        assert gameDetails.players[0].trainCount == 8
        assert len(gameDetails.players[0].trainCards) == 1
        assert len(gameDetails.discardTrainCardPile) == 2

    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_build_color_path_with_all_wild(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['WILD','WILD']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96
        payload['trainCards'] = ['WILD','WILD']

        TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.BUILD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert gameDetails.activePlayerId == 2
        assert gameDetails.pathOwnership[96] == 1
        assert gameDetails.players[0].pathScore == 2
        assert gameDetails.players[0].trainCount == 8
        assert len(gameDetails.players[0].trainCards) == 0
        assert len(gameDetails.discardTrainCardPile) == 2

    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_build_color_path_no_wildcards(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.players[0].trainCount = 10
        gameDetails.players[0].trainCards = ['GREEN','GREEN']
        payload = dict()
        payload['id'] = 1
        payload['pathId'] = 96
        payload['trainCards'] = ['GREEN','GREEN']

        TurnState.validateInput(PlayerAction.BUILD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.BUILD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert gameDetails.activePlayerId == 2
        assert gameDetails.pathOwnership[96] == 1
        assert gameDetails.players[0].pathScore == 2
        assert gameDetails.players[0].trainCount == 8
        assert len(gameDetails.players[0].trainCards) == 0
        assert len(gameDetails.discardTrainCardPile) == 2

    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_pick_train_card(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.availableCards = [TrainColor.GREEN for i in range(5)]
        payload = dict()
        payload['id'] = 1
        payload['trainCardIndex'] = 4
        trainCardCount = len(gameDetails.trainCardPile)


        TurnState.validateInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)

        assert len(gameDetails.trainCardPile) == trainCardCount - 1
        assert len(gameDetails.players[0].trainCards) == 1
        assert gameDetails.gameState == GameState.PICK_SECOND_TRAIN_CARD
        assert gameDetails.activePlayerId == 1
        
    
    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_pick_wild_train_card(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.availableCards = [TrainColor.GREEN for i in range(5)]
        gameDetails.availableCards[4] = TrainColor.WILD
        payload = dict()
        payload['id'] = 1
        payload['trainCardIndex'] = 4
        trainCardCount = len(gameDetails.trainCardPile)


        TurnState.validateInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.PICK_TRAIN_CARD, payload, gameDetails)

        assert gameDetails.gameState == GameState.TURN
        assert len(gameDetails.trainCardPile) == trainCardCount - 1
        assert len(gameDetails.players[0].trainCards) == 1
        assert gameDetails.activePlayerId == 2

    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_pick_random_train_card(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        payload = dict()
        payload['id'] = 1
        trainCardCount = len(gameDetails.trainCardPile)

        TurnState.validateInput(PlayerAction.PICK_RANDOM_TRAIN_CARD, payload, gameDetails)
        TurnState.submitInput(PlayerAction.PICK_RANDOM_TRAIN_CARD, payload, gameDetails)

        assert gameDetails.gameState == GameState.PICK_SECOND_TRAIN_CARD
        assert len(gameDetails.trainCardPile) == trainCardCount - 1
        assert len(gameDetails.players[0].trainCards) == 1
        assert gameDetails.activePlayerId == 1

    @patch('state.handlers.turn_state.updateGameDetails')
    @patch('state.handlers.turn_state.updatePlayers')
    def test_successful_get_destination_cards(self, updateGameDetails, updatePlayers):
        gameDetails = createGameDetails(GameState.TURN)
        gameDetails.destinationCardPile = [0,0,0]
        payload = dict()
        payload['id'] = 1
        destinationCardCount = len(gameDetails.destinationCardPile)

        TurnState.validateInput(PlayerAction.GET_DESTINATION_CARDS, payload, gameDetails)
        TurnState.submitInput(PlayerAction.GET_DESTINATION_CARDS, payload, gameDetails)

        assert gameDetails.gameState == GameState.PICK_DESTINATION_CARDS
        assert len(gameDetails.destinationCardPile) == destinationCardCount - 3
        assert len(gameDetails.players[0].destinationOptionSet) == 3
        assert gameDetails.activePlayerId == 1
    