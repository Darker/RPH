#from __future__ import print_function
from board import Board
from player_abstract import MyPlayer as AbstractPlayer
from player_predictive_weighted import MyPlayer as PlayerPredictiveWeighted
from player_greedy_weighted import MyPlayer as PlayerGreedyWeighted

class MyPlayer(AbstractPlayer):
    '''Tento hrac nacita pouziva ruzne hrace v zavislosti na poctu tahu'''
    def __init__(self, my_color,opponent_color, neutral_color=-1):
        AbstractPlayer.__init__(self, my_color,opponent_color, neutral_color=-1)
        self.turns = 0
        self.greedy = PlayerGreedyWeighted(my_color,opponent_color)
        self.predictive = PlayerPredictiveWeighted(my_color,opponent_color)
    
    def find_position(self, board):
        self.turns+=1
        if self.turns>22:
            print("Predictive mode")
            return self.predictive.find_position(board)
        else:
            print("Greedy mode")
            return self.greedy.find_position(board)
