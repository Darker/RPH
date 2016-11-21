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
        coords, scores = self.get_positions_and_scores(board)
        if len(scores) > 0:
            best_score = scores.index(max(scores))
            return coords[best_score]
        else: 
            return None
    # This gives number of valid moves and
    # lists of stones which will change color (placed stone not included)
    # by default, second list just contains count of those stones
    def get_positions_and_scores(self, board, score_as_len=True):
        board = self.wrap_board_if_needed(board)
        coords = []
        # contains list lists o stone coordinates
        # length of values can be used to calculate score
        scores = []
        for row in range(0, len(board)):
            for col in range(0, len(board[row])):
                if(board[row][col] == self.colors[self.NEUTRAL]):
                    #print("Testing ["+str(row)+", "+str(col)+"]")
                    score = board.get_claim_stones([row, col], self)
                    if len(score)>0:
                        coords.append([row, col])
                        scores.append(len(score) if score_as_len else score)
                        #print("Placing stone at ["+str(row)+", "+str(col)+"] yields "+str(score))
        return (coords, scores)
    #wraps raw list into more convenient Board class
    def wrap_board_if_needed(self, board):
        if isinstance(board, Board):
            return board
        else:
            return Board(board)
            

if __name__ == "__main__":
    board = [
     #   0 1 2 3 4 5 6 7
        [0,0,0,0,0,0,0,0],# 0
        [0,0,0,0,0,0,0,0],# 1
        [0,0,0,0,0,0,0,0],# 2
        [0,0,0,1,2,0,0,0],# 3
        [0,0,0,2,1,0,0,0],# 4
        [0,0,0,0,0,0,0,0],# 5
        [0,0,0,0,0,0,0,0],# 6
        [0,0,0,0,0,0,0,0] # 7
    ]
    board = Board(board)
    player = MyPlayer(1, 2, 0)
    from predictive_player import MyPlayer as OtherPlayer
    console_player = OtherPlayer(2, 1, 0)
    console_player.enemy_ = player
    player_enemy = console_player
    
    board.printMe(1, 2, 0)
    while True:
        move = player.move(board)
        moves = 0;
        #if move is not None:
        #    print("[" + ", ".join( str(x) for x in move) + "]")
        #else:
        #    print("No valid move...")
        if move is not None:
            board.place(list(move), player)
            print("Computer (simple) played:")
            board.printMe(1, 2, 0)
            moves+=1
        if  console_player.can_play(board):
            #move = console_player.move_via_console(board) 
            move = list(console_player.move(board))
            board.place(move, console_player)
            print("Advanced opponent played:")
            board.printMe(1, 2, 0)
            moves+=1
        if moves==0:
            break
    result = board.balance(player)
    if result>0:
        print("Base player wins!")
    elif result==0:
        print("Nobody wins!")
    else:
        print("Guest player wins!")
    #print '[%s]' % ', '.join(map(str, p))