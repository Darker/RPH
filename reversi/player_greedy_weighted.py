#from __future__ import print_function
from board import Board
from player_abstract import MyPlayer as AbstractPlayer

class MyPlayer(AbstractPlayer):
    '''Tento hrac vzdy sebere tolik kamenu, kolik muze, vazi si hodnoty.'''
    # Finds the most suitable position for placing a stone
    # best position is such that yields most turned stones after execution
    #
    def find_position(self, board):
        board.weighted = True
        coords, scores = board.get_positions_and_scores(self, False)
        if len(scores) > 0:
            values = []
            
            for i in range(len(scores)):
                values.append(board.stones_value(scores[i]) + board.stones_value([coords[i]]))
            best_score = values.index(max(values))
            return coords[best_score]
        else: 
            return None
