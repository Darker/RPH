import player_abstract

class MyPlayer(player_abstract.MyPlayer):
    '''This is "border player". It always prefers to pick border and 
    especially corner stones. That's because once you've got corner stone
    it will never be reversed'''
    def find_position(self, board):
        coords, scores = board.get_positions_and_scores(self)
        if len(scores) > 0:
            # First try to find corner stones
            for pos in coords:
                if self.is_corner(board, pos):
                    return pos
                elif self.is_border(board, pos):
                    return pos
            
            best_score = scores.index(max(scores))
            return coords[best_score]
        else: 
            return None
    #returns true if tile is at board's corner
    def is_corner(self, board, pos):
        corners = [0, len(board)-1, len(board[0])-1]
        try:
            corners.index(pos[0])
            corners.index(pos[1])
        except ValueError as e:
            return False
        else:
            return True
    #returns true if tile is at board's border     
    # that is, if one of tile's coordinates
    # equals to board boundary coordinates
    def is_border(self, board, pos):
        corners = [[0, len(board)-1], [0, len(board[0])-1]]
        i = 0
        border = 0
        while i<2:
            if self.safe_index(corners[i], pos[i])!=-1:
                border+=1
            i+=1
        return border>0
    def safe_index(self, alist, val):
        try:
            return alist.index(val)
        except ValueError as e:
            return -1