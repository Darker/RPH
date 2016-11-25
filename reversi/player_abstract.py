#from __future__ import print_function
from board import Board
import sys
if sys.version_info < (3, 0):
    def console_input(prompt):
        return raw_input(prompt)
else:
    def console_input(prompt):
        return input(prompt)
class MyPlayer:
    '''Tento hrac vzdy sebere tolik kamenu, kolik muze. Bez planovani.'''
    MY_COLOR = 0
    HIS_COLOR = 1;
    NEUTRAL = 2
    def __init__(self, my_color,opponent_color, neutral_color=-1):
        self.name = 'maredjak' #username studenta
        self.colors = [my_color, opponent_color, neutral_color]
        self.enemy_ = None
    @property
    def color(self):
        return self.colors[self.MY_COLOR]
    @property
    def opponent_color(self):
        return self.colors[self.HIS_COLOR]
    @property
    def neutral_color(self):
        return self.colors[self.NEUTRAL]
    @property
    def enemy(self):
        if self.enemy_ is not None:
            return self.enemy_
        self.enemy_ = MyPlayer(self.opponent_color, self.color, self.neutral_color)
        self.enemy_.enemy_ = self
        return self.enemy_
    # This just casts algorithm output to required format of 
    # tuple
    def move(self,board):
        board = self.wrap_board_if_needed(board)
        coords = self.find_position(board)
        return tuple(coords) if coords is not None else None
    # This is not very efficient, because it lists
    # all stones instead of just finding if a move is valid
    def can_play(self, board):
        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                if(board[row][col] == self.colors[self.NEUTRAL]):
                    #print("Testing ["+str(row)+", "+str(col)+"]")
                    score = len(board.get_claim_stones([row, col], self, True))
                    if score>0:
                        return True
        return False
    # prompts player to make a move via standard input
    # todo: remove this after debug
    def move_via_console(self, board):
        board = self.wrap_board_if_needed(board)
        zeman = "kunda"
        fails = 3
        while zeman=="kunda":
            i,j = console_input("Enter two values:  ").split()
            i = int(i)
            j = int(j)
            if board.is_valid_move([i, j], self):
                return [i, j]
            else:
                fails-=1
                if fails>0:
                    print("Invalid move! Enter valid values - "+str(fails)+" attempts remaining.")
                else:
                    raise ValueError("Too many invalid move attempts!")  
        #note: zeman still "kunda" tho, even after loop ends
        
    # Finds the most suitable position for placing a stone
    # best position is such that yields most turned stones after execution
    #
    def find_position(self, board):
        raise NotImplementedError("This is abstract player. It cannot play.")

    #wraps raw list into more convenient Board class
    def wrap_board_if_needed(self, board):
        if isinstance(board, Board):
            return board
        else:
            return Board(board)
            

