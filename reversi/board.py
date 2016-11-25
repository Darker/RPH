#from __future__ import print_function
# for copying boards 
import copy

class Board:
    EMPTY_ARRAY = []
    WEIGHTS = [
        [99, -8,  8, 6, 6, 8, -8,99],
        [-8,-24, -4,-3,-3,-4,-24,-8],
        [ 8, -4,  7, 4, 4, 7, -4, 8],
        [ 6, -3,  4, 0, 0, 4, -3, 6],
        [ 6, -3,  4, 0, 0, 4, -3, 6],
        [ 8, -4,  7, 4, 4, 7, -4, 8],
        [-8,-24, -4,-3,-3,-4,-24,-8],
        [99, -8,  8, 6, 6, 8, -8,99]
    ]
    def __init__(self, board):
        self.board = board
        self.players = [None, None]
        self.currentTurn = -1
        # These are lazy calculated
        # the numbers mean [player 1 stones, player 2 stones, empty stones]
        self.stones = [-1, -1, -1]
        # number of stones, cached both for performance and readability reasons
        self.rows = len(board)
        self.cols = len(board[0])
        self.no_stones = self.rows*self.cols
    def set_players(self, a, b):
        self.players[0] = a
        self.players[1] = b
        self.currentTurn = 0
    def isValidPos(self, row, col=-1):
        if isinstance(row, list):
            col = row[1]
            row = row[0]
        #print("CHECK POS ["+str(row)+", "+str(col)+"]")
        return row>=0 and col>=0 and row<self.rows and col<self.cols
    def strpos(self, row, col=-1):
        if isinstance(row, list):
            col = row[1]
            row = row[0]
        return "["+str(row)+", "+str(col)+"]"
    # guaranteed to return NEW list containing the two coordinates
    def coord(self, row, col=-1, copy=True):
        if isinstance(row, list):
            return [row[0], row[1]] if copy else row
        elif isinstance(row, tuple):
            return [row[0], row[1]]
        else:
            return [row, col]
    # Performs complete move with placing and reversing stones
    # `turned_fields` argument can be used if you already have a list
    #     of fields to be turned when a stone is placed
    #     given list is not checked for correctness
    def place(self, pos, player, turned_fields = None):
        #pos = self.coord(pos, -1, False)
        if turned_fields is None:
            turned_fields = self.get_claim_stones(pos, player)
        if len(turned_fields)==0:
            raise ValueError("Invalid move at "+self.strpos(pos))
        for field in turned_fields:
            self.board[field[0]][field[1]]=player.color
        # do not forget to also actually place the stone
        self.board[pos[0]][pos[1]] = player.color
        # switch turn if possible
        if self.players[0] is None:
            self.players[0]=player
        if self.players[1] is None and self.players[0] is not player:
            self.players[1]=player
        cur_player_index = self.player_index(player)
        # opposing player index
        self.currentTurn = 0 if cur_player_index==1 else 1
        
        # add fields to balance
        if self.stones[0]>=0:
            turned_stones = len(turned_fields)
            self.stones[cur_player_index] += turned_stones + 1
            self.stones[self.currentTurn] -= turned_stones
            # one stone was placed, therefore removed from free stones count
            self.stones[2] -= 1
        #self.cached_balance += (1 if player is self.players[0] else -1)*(len(turned_fields)+1)
    def opponent(self, player):
        return self.players[0] if player==self.players[1] else self.players[1]
    def player_index(self, player):
        if player is self.players[0]:
            return 0
        if player is self.players[1]:
            return 1
        return -1
    def cur_playa(self):
        return self.players[self.currentTurn]
    def is_valid_move(self, pos, player):
        turned_fields = self.get_claim_stones(pos, player)
        return len(turned_fields)!=0
    # This gives number of valid moves and
    # lists of stones which will change color (placed stone not included)
    # by default, second list just contains count of those stones
    def get_positions_and_scores(self, player, score_as_len=True):
        coords = []
        # contains list lists o stone coordinates
        # length of values can be used to calculate score
        scores = []
        board = self.board
        row = 0
        while row<self.rows:
            col = 0
            while col<self.cols:
                if(board[row][col] == player.colors[player.NEUTRAL]):
                    #print("Testing ["+str(row)+", "+str(col)+"]")
                    score = self.get_claim_stones([row, col], player)
                    if len(score)>0:
                        coords.append([row, col])
                        scores.append(len(score) if score_as_len else score)
                        #print("Placing stone at ["+str(row)+", "+str(col)+"] yields "+str(score))
                col+=1
            row+=1
        return (coords, scores)
    # Returns list of stones turned by placing stone at `stone_pos`
    # if empty list is returned that move is not valid!
    #@profile
    def get_claim_stones(self, stone_pos, player, terminate_asap=False):
        #stone_pos = self.coord(stone_pos, -1, False)
        #print(stone_pos)
        directions = [[0, 1], [1,1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
        reverse_fields = []
        opponent_color = player.opponent_color
        for direction in directions:
            pos = [stone_pos[0]+direction[0], stone_pos[1]+direction[1]]
            #if not (pos[0]>=0 and pos[1]>=0 and pos[0]<self.rows and pos[1]<self.cols) or self.board[pos[0]][pos[1]]!=opponent_color:
            #    continue
            fields_tmp = self.find_opponent_stones(direction, pos, player)
            # It is noteworthy, that no duplicates need removal
            # because the 'beams' of search never intersect
            reverse_fields += fields_tmp
            if terminate_asap and len(reverse_fields) >0:
                break
            #print(fields_tmp)
        #print(reverse_fields)
        #for field in reverse_fields:
        #    print("  - claims ["+str(field[0])+", "+str(field[1])+"]")
        return reverse_fields
    # returns score of both players in a tuple
    # that can be used for simple assignment
    def score(self, player):
        counts = [0, 0, 0]
        roles = [player.color, player.opponent_color,player.neutral_color]
        for row in self.board:
            for number in row:
                index = roles.index(number)
                counts[index] += 1
        self.stones[2] = counts[2]
        # helper var that says that the player order was crossed
        crossed = player is self.players[1]
        self.stones[0] = counts[0] if not crossed else counts[1]
        self.stones[1] = counts[1] if not crossed else counts[0]
        return tuple(counts)
    def score_from_cache(self, player):
        if self.stones[0]<0:
            self.score(self.players[0])
        result = [0,0,self.stones[2]]
        crossed = player is self.players[1]
        result[0] = self.stones[0] if not crossed else self.stones[1]
        result[1] = self.stones[1] if not crossed else self.stones[0]
        return result
    def balance_from_cache(self, player):
        if self.stones[0]<0:
            self.score(self.players[0])
        # testing block
        #uncached_score = list(self.score(self.players[0]))
        #assert(uncached_score==self.stones)
        # if player 1 wins
        if self.stones[0]-self.stones[1]>0:
            return 1 if player is self.players[0] else -1
        # draw
        elif self.stones[0]==self.stones[1]:
            return 0
        # if player 2 wins
        else:
            return 1 if player is self.players[1] else -1
    # returns +1 0 or -1 based on whether given player
    # winsor loses right now
    def balance(self, player):
        plrscore, enemyscore, empty = self.score(player)
        if plrscore==enemyscore:
            return 0
        return 1 if plrscore>enemyscore else -1
    def clone(self):
        board = [row[:] for row in self.board]
        
        #for row in self.board:
            #tmp = []
            #for number in row:
            #   tmp.append(number)
        #    board.append(row[:])
            
        result =  Board(board)
        result.stones = self.stones[:]
        result.players = self.players[:]
        result.currentTurn = self.currentTurn
        return result
        
    # returns list of stones that will change color if 
    # stone is placed on start
    # for performance reasons, it is expected that you DID already increment START once
    #@profile
    def find_opponent_stones(self, direction, start, player):
        #print("   Finding enemy stones at "+self.strpos(start)+" in direction "+self.strpos(direction))
        # starting directly at 'next' field.
        # btw it made this algorithm WAY faster when I put 
        # the addition in the list ctor instead of incrememting it later
        #pos = [start[0]+direction[0], start[1]+direction[1]]
        pos = [start[0], start[1]]
        #row = start[0]+direction[0]
        #col = start[1]+direction[1]
        #if not (pos[0]>=0 and pos[1]>=0 and pos[0]<self.rows and pos[1]<self.cols):
        #    return []
        first_iteration = True
        # several variables are defined inside the loop so they're only defined
        # when needed
        # these:
        #   fields = []
        ended_properly = False
        board = self.board
        #while self.isValidPos(pos):
        # While condition replaced with inline
        # because just as any other interpreted language
        # python sucks at inlining
        while pos[0]>=0 and pos[1]>=0 and pos[0]<self.rows and pos[1]<self.cols:
            #current_color = self[pos];
            current_color = board[pos[0]][pos[1]]
            if first_iteration:
                #opponent_color = player.opponent_color
                if current_color != player.opponent_color:
                    #print("     First stone not enemies' at "+self.strpos(pos))
                    break
                fields = []
                
            else:
                if current_color == player.color:
                    ended_properly = True
                    break;
                elif current_color == player.neutral_color:
                    #ending if free space was reached
                    break;
            first_iteration = False
            fields.append([pos[0], pos[1]])
            #print("Adding "+self.strpos(pos)+" to list of claimed points.")
            pos[0]+=direction[0]
            pos[1]+=direction[1]
        if(ended_properly):
            #print("   These fields can be claimed: ", end="")
            #print(fields)
            return fields
        else:
            #if len(fields)>0:
            #    print("   Throwing away "+str(len(fields))+" because last field wasn't mine.")
            return []
    def __getitem__(self, key):
        if isinstance(key, list):
            if self.isValidPos(key):
                return self.board[key[0]][key[1]]
            else:
                return None
        else:
            return self.board[key]
    def __setitem__(self, key, value):
        if isinstance(key, list):
            if self.isValidPos(key):
                self.board[key[0]][key[1]] = value
            else:
                raise IndexError("Invalid offset in game board.")
        else:
            if isinstance(value, list) and len(value)==len(self.board[key]):
                self.board[key]=value
            else:
                raise ValueError("Assignment to game board row. Only listof valid length allowed!")
    def __iter__(self):
        return self.board.__iter__()
    def __len__(self):
        return self.board.__len__()
    def printMe(self, p_a, p_b, neutral):
        chars = ["-", "X", "O"]
        roles = [neutral, p_a, p_b]
        rowNo = 0
        colNo = 0
        for row in self:
            if colNo==0:
                print("   ", end="")
                for number in row:
                    print(str((colNo))+" ", end="")
                    colNo+=1
                print("\n", end="")
            print(str(rowNo)+" |", end="")
            rowNo+=1
            for number in row:
                field_type = roles.index(number)
                if field_type<0 or field_type>=len(chars):
                    field_type = 0
                print((chars[field_type])+" ", end="")
            print("\n", end="")
