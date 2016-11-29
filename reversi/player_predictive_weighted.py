#from __future__ import print_function
from board import Board
from player_predictive import MyPlayer as PredictivePlayer

class MyPlayer(PredictivePlayer):
    '''State space search, vazi si hodnoty.'''
    # Finds the most suitable position for placing a stone
    # best position is such that yields most turned stones after execution
    #
    def find_position(self, board):
        board.weighted = True
        return PredictivePlayer.find_position(self, board)
